#!/usr/bin/env python
# coding=utf-8

# -------------------------------------------------------------------------------
#    ____        _   _____ ____        _
#   |  _ \ _   _| | |_   _/ ___| _ __ (_) ___ ___
#   | |_) | | | | |   | | \___ \| '_ \| |/ __/ _ \
#   |  __/| |_| | |___| |  ___) | |_) | | (_|  __/
#   |_|    \__, |_____|_| |____/| .__/|_|\___\___|
#          |___/                |_|
#
# Name:        sim_runner.py
# Purpose:     Tool used to launch LTSpice simulation in batch mode.
#
# Author:      Nuno Brum (nuno.brum@gmail.com)
#
# Created:     23-12-2016
# Licence:     refer to the LICENSE file
# -------------------------------------------------------------------------------
"""
Allows launching LTSpice simulations from a Python Script, thus allowing to overcome the 3 dimensions STEP limitation on
LTSpice, update resistor values, or component models.

The code snipped below will simulate a circuit with two different diode models, set the simulation
temperature to 80 degrees, and update the values of R1 and R2 to 3.3k. ::

    LTC = SimCommander("my_circuit.asc")
    LTC.set_parameters(temp=80)  # Sets the simulation temperature to be 80 degrees
    LTC.set_component_value('R2', '3.3k')  #  Updates the resistor R2 value to be 3.3k
    for dmodel in ("BAT54", "BAT46WJ"):
        LTC.set_element_model("D1", model)  # Sets the Diode D1 model
        for res_value in sweep(2.2, 2,4, 0.2):  # Steps from 2.2 to 2.4 with 0.2 increments
            LTC.set_component_value('R1', res_value)  #  Updates the resistor R1 value to be 3.3k
            LTC.run()

    LTC.wait_completion()  # Waits for the LTSpice simulations to complete

    print("Total Simulations: {}".format(LTC.runno))
    print("Successful Simulations: {}".format(LTC.okSim))
    print("Failed Simulations: {}".format(LTC.failSim))

The first line will create a python class instance that represents the LTSpice file or netlist that is to be
simulated. This object implements methods that are used to manipulate the spice netlist. For example, the method
set_parameters() will set or update existing parameters defined in the netlist. The method set_component_value() is
used to update existing component values or models.

---------------
Multiprocessing
---------------

For making better use of today's computer capabilities, the SimCommander spawns several LTSpice instances
each executing in parallel a simulation.

By default, the number of parallel simulations is 4, however the user can override this in two ways. Either
using the class constructor argument ``parallel_sims`` or by forcing the allocation of more processes in the
run() call by setting ``wait_resource=False``. ::

    LTC.run(wait_resource=False)

The recommended way is to set the parameter ``parallel_sims`` in the class constructor. ::

    LTC=SimCommander("my_circuit.asc", parallel_sims=8)

The user then can launch a simulation with the updates done to the netlist by calling the run() method. Since the
processes are not executed right away, but rather just scheduled for simulation, the wait_completion() function is
needed if the user wants to execute code only after the completion of all scheduled simulations.

The usage of wait_completion() is optional. Just note that the script will only end when all the scheduled tasks are
executed.

---------
Callbacks
---------

As seen above, the `wait_completion()` can be used to wait for all the simulations to be finished. However, this is
not efficient from a multiprocessor point of view. Ideally, the post-processing should be also handled while other
simulations are still running. For this purpose, the user can use a function call back.

The callback function is called when the simulation has finished directly by the thread that has handling the
simulation. A function callback receives two arguments.
The RAW file and the LOG file names. Below is an example of a callback function::

    def processing_data(raw_filename, log_filename):
        '''This is a call back function that just prints the filenames'''
        print("Simulation Raw file is %s. The log is %s" % (raw_filename, log_filename)
        # Other code below either using LTSteps.py or raw_read.py
        log_info = LTSpiceLogReader(log_filename)
        log_info.read_measures()
        rise, measures = log_info.dataset["rise_time"]

The callback function is optional. If  no callback function is given, the thread is terminated just after the
simulation is finished.
"""
__author__ = "Nuno Canto Brum <nuno.brum@gmail.com>"
__copyright__ = "Copyright 2020, Fribourg Switzerland"

__all__ = ['SimRunner']

import shutil
from pathlib import Path
from time import sleep, thread_time as clock

from typing import Callable, Union, Any, Type, Protocol
import logging
_logger = logging.getLogger("PyLTSpice.SimRunner")

from .process_callback import ProcessCallback
from ..sim.run_task import RunTask, clock_function
from ..sim.simulator import Simulator
from ..editor.base_editor import BaseEditor

END_LINE_TERM = '\n'


class SimRunnerTimeoutError(TimeoutError):
    """Timeout Error class"""
    ...


class AnyRunner(Protocol):
    def run(self, netlist: Union[str, Path, BaseEditor], **kwargs) -> None:
        ...


class SimRunner(object):
    """
    The SimCommander class implements all the methods required for launching batches of LTSpice simulations.
    It takes a parameter the path to the LTSpice .asc file to be simulated, or directly the .net file.
    If an .asc file is given, the class will try to generate the respective .net file by calling LTspice with
    the --netlist option
    :raises FileNotFoundError: When the file is not found  /!\\ This will be changed

    :param parallel_sims: Defines the number of parallel simulations that can be executed at the same time. Ideally this
                          number should be aligned to the number of CPUs (processor cores) available on the machine.
    :type parallel_sims: int, optional
    :param timeout: Timeout parameter as specified on the os subprocess.run() function. Default is 600 seconds, i.e.
        10 minutes. For no timeout, set to None.
    :type timeout: float, optional
    :param verbose: If True, it enables a richer printout of the program execution.
    :type verbose: bool, optional
    :param output_folder: specifying which directory shall be used for simulation files (raw and log files).
    :param output_folder: str
    :param simulator: Forcing a given simulator executable.
    :type simulator: str or Simulator, optional

    """

    def __init__(self, *, simulator=None, parallel_sims: int = 4, timeout: float = 600.0, verbose=True,
                 output_folder: str = None):
        # The '*' in the parameter list forces the user to use named parameters for the rest of the parameters.
        # This is a good practice to avoid confusion.
        self.verbose = verbose
        self.timeout = timeout
        self.cmdline_switches = []

        if output_folder:
            self.output_folder = Path(output_folder)  # If not None converts to Path() object
            if not self.output_folder.exists():
                self.output_folder.mkdir()
        else:
            self.output_folder = None

        self.parallel_sims = parallel_sims
        self.active_tasks = []
        self.completed_tasks = []
        self._iterator_counter = 0  # Note: Nested iterators are not supported

        # master_log_filename = self.circuit_radic + '.masterlog' TODO: create the JSON or YAML file
        _logger.info("SimRunner started")

        self.runno = 0  # number of total runs
        self.failSim = 0  # number of failed simulations
        self.okSim = 0  # number of successful completed simulations
        # self.failParam = []  # collects for later user investigation of failed parameter sets

        # Gets a simulator.
        if simulator is None:
            from ..sim.ltspice_simulator import LTspice  # Used for defaults
            self.simulator = LTspice
        elif isinstance(simulator, (str, Path)):
            self.simulator = Simulator.create_from(simulator)
        elif issubclass(simulator, Simulator):
            self.simulator = simulator
        else:
            raise TypeError("Invalid simulator type.")

    def __del__(self):
        """Class Destructor : Closes Everything"""
        _logger.debug("Waiting for all spawned sim_tasks to finish.")
        self.wait_completion(abort_all_on_timeout=True)  # Kill all pending simulations
        _logger.debug("Exiting SimCommander")

    def set_run_command(self, spice_tool: Union[str, Type[Simulator]]) -> None:
        """
        Manually setting the LTSpice run command

        :param spice_tool: String containing the path to the spice tool to be used, or alternatively the Simulator
            object.
        :type spice_tool: str or Simulator
        :return: Nothing
        :rtype: None
        """
        if isinstance(spice_tool, str):
            self.simulator = Simulator.create_from(spice_tool)
        elif issubclass(spice_tool, Simulator):
            self.simulator = spice_tool
        else:
            raise TypeError("Expecting str or Simulator objects")

    def SetRunCommand(self, spice_tool: Union[str, Type[Simulator]]) -> None:
        """
        *(Deprecated)*
        Use set_run_command() method.
        """
        self.set_run_command(spice_tool)

    def clear_command_line_switches(self):
        """Clear all the command line switches added previously"""
        self.cmdline_switches.clear()

    def add_command_line_switch(self, switch, path=''):
        """
        Used to add an extra command line argument such as -I<path> to add symbol search path or -FastAccess
        to convert the raw file into Fast Access.
        The argument is a string as is defined in the LTSpice command line documentation.

        :param switch: switch to be added.
        :type switch: str:  A command line switch such as "-ascii" for generating a raw file in text format or
            "-alt" for setting the solver to alternate. See Command Line Switches information on LTSpice help file.
        :param path: path to the file related to the switch being given.
        :type path: str, optional
        :returns: Nothing
        """
        self.cmdline_switches.append(switch)
        if path is not None:
            self.cmdline_switches.append(path)

    def _on_output_folder(self, afile):
        if self.output_folder:
            return self.output_folder / afile
        else:
            return Path(afile)

    def _to_output_folder(self, afile: Path, *, copy: bool, new_name: str = ''):
        if self.output_folder:
            if new_name:
                ddst = self.output_folder / new_name
            else:
                ddst = self.output_folder

            if copy:
                dest = shutil.copy(afile, ddst)
            else:
                dest = shutil.move(afile, ddst)
            return Path(dest)
        else:
            if new_name:
                dest = shutil.copy(afile, afile.parent / new_name)
                return Path(dest)
            else:
                return afile

    def _run_file_name(self, netlist):
        if not isinstance(netlist, Path):
            netlist = Path(netlist)
        return "%s_%i%s" % (netlist.stem, self.runno, netlist.suffix)

    def create_netlist(self, asc_file: Union[str, Path]):
        """Creates a .net from an .asc using the LTSpice -netlist command line"""
        if not isinstance(asc_file, Path):
            asc_file = Path(asc_file)
        if asc_file.suffix == '.asc':
            if self.verbose:
                _logger.info("Creating Netlist")
            return self.simulator.create_netlist(asc_file)
        else:
            _logger.warning("Unable to create the Netlist from %s" % asc_file)
            return None

    def _prepare_sim(self, netlist: Union[str, Path, BaseEditor], run_filename: str):
        """Internal function"""
        # update number of simulation
        self.runno += 1  # Incrementing internal simulation number
        # Harmonize the netlist into a Path object pointing to a netlist file on the right output folder
        if isinstance(netlist, BaseEditor):
            if run_filename is None:
                run_filename = self._run_file_name(netlist.circuit_file)

            # Calculates the path where to store the new netlist.
            run_netlist_file = self._on_output_folder(run_filename)
            netlist.write_netlist(run_netlist_file)

        elif isinstance(netlist, (Path, str)):
            if run_filename is None:
                run_filename = self._run_file_name(netlist)
            if isinstance(netlist, str):
                netlist = Path(netlist)
            run_netlist_file = self._to_output_folder(netlist, copy=True, new_name=run_filename)
        else:
            raise TypeError("'netlist' parameter shall be a SpiceEditor, pathlib.Path or a plain str")

        return run_netlist_file

    def run(self, netlist: Union[str, Path, BaseEditor], *, wait_resource: bool = True,
            callback: Union[Type[ProcessCallback], Callable[[Path, Path], Any]] = None, switches=None,
            timeout: float = None, run_filename: str = None) -> Union[RunTask, None]:
        """
        Executes a simulation run with the conditions set by the user.
        Conditions are set by the set_parameter, set_component_value or add_instruction functions.

        :param netlist:
            The name of the netlist can be optionally overridden if the user wants to have a better control of how the
            simulations files are generated.
        :type netlist: SpiceEditor or a path to the file
        :param wait_resource:
            Setting this parameter to False will force the simulation to start immediately, irrespective of the number
            of simulations already active.
            By default, the SimCommander class uses only four processors. This number can be overridden by setting
            the parameter ´parallel_sims´ to a different number.
            If there are more than ´parallel_sims´ simulations being done, the new one will be placed on hold till one
            of the other simulations are finished.
        :type wait_resource: bool, optional
        :param callback:
            The user can optionally give a callback function for when the simulation finishes so that processing can
            be done immediately. The callback function must receive two input parameters that correspond the raw and
            log files created by the simulation. The argument type is of the type pathlib.Path
        :type: callback: function(raw_file: Path, log_file: Path), optional
        :param switches: Command line switches override
        :type switches: list
        :param timeout: Timeout to be used in waiting for resources. Default time is value defined in this class
            constructor.
        :type timeout: float, optional
        :param run_filename: Name to be used for the log and raw file.
        :type run_filename: str or Path
        :returns: The task object of type RunTask
        """
        if switches is None:
            switches = []
        run_netlist_file = self._prepare_sim(netlist, run_filename)

        if timeout is None:
            timeout = self.timeout

        t0 = clock()  # Store the time for timeout calculation
        while clock() - t0 < timeout + 1:  # Give one second slack in relation to the task timeout
            cmdline_switches = switches or self.cmdline_switches  # If switches are passed, they override the ones
            # inside the class.

            if (wait_resource is False) or (self.active_threads() < self.parallel_sims):
                t = RunTask(self.simulator, self.runno, run_netlist_file, callback, cmdline_switches,
                            timeout=self.timeout, verbose=self.verbose)
                self.active_tasks.append(t)
                t.start()
                sleep(0.01)  # Give slack for the thread to start
                return t  # Returns the task object
            sleep(0.1)  # Give Time for other simulations to end
        else:
            _logger.error("Timeout waiting for resources for simulation %d" % self.runno)
            if self.verbose:
                _logger.warning("Timeout on launching simulation %d." % self.runno)
            return None

    def run_now(self, netlist: Union[str, Path, BaseEditor], *, switches=None, run_filename: str = None,
                timeout: float = None) -> (str, str):
        """
        Executes a simulation run with the conditions set by the user.
        Conditions are set by the set_parameter, set_component_value or add_instruction functions.

        :param netlist:
            The name of the netlist can be optionally overridden if the user wants to have a better control of how the
            simulations files are generated.
        :type netlist: SpiceEditor or a path to the file
        :param switches: Command line switches override
        :type switches: list
        :param run_filename: Name to be used for the log and raw file.
        :type run_filename: str or Path
        :param timeout: Timeout to be used in waiting for resources. Default time is value defined in this class
            constructor.
        :type timeout: float, optional
        :returns: the raw and log filenames
        """
        if switches is None:
            switches = []
        run_netlist_file = self._prepare_sim(netlist, run_filename)

        cmdline_switches = switches or self.cmdline_switches  # If switches are passed, they override the ones inside
        # the class.

        if timeout is None:
            timeout = self.timeout

        def dummy_callback(raw, log):
            """Dummy call back that does nothing"""
            return None

        t = RunTask(self.simulator, self.runno, run_netlist_file, dummy_callback, cmdline_switches,
                    timeout=timeout, verbose=self.verbose)
        t.join(timeout + 1)  # Give one second slack in relation to the task timeout

        return t.raw_file, t.log_file  # Returns the raw and log file

    def active_threads(self):
        """Returns the number of active sim_tasks"""
        self.update_completed()
        return len(self.active_tasks)

    def update_completed(self):
        """
        This function updates the active_tasks and completed_tasks lists. It moves the finished task from the
        active_tasks list to the completed_tasks list.
        It should be called periodically to update the status of the simulations.

        :returns: Nothing
        """
        i = 0
        while i < len(self.active_tasks):
            if self.active_tasks[i].is_alive():
                i += 1
            else:
                if self.active_tasks[i].retcode == 0:
                    self.okSim += 1
                else:
                    # simulation failed
                    self.failSim += 1
                task = self.active_tasks.pop(i)
                self.completed_tasks.append(task)

    def kill_all_ltspice(self):
        """Function to terminate LTSpice in windows"""
        simulator = Simulator
        process_name = simulator.process_name
        import psutil
        for proc in psutil.process_iter():
            # check whether the process name matches

            if proc.name() == process_name:
                _logger.info("killing ngspice", proc.pid)
                proc.kill()

    def _maximum_stop_time(self):
        """
        This function will return the maximum timeout time of all active tasks.
        :return: Maximum timeout time or None, if there is no timeout defined.
        :rtype: float or None
        """
        alarm = None
        for task in self.active_tasks:
            tout = task.timeout if task.timeout is not None else self.timeout
            if tout is not None:
                stop = task.start_time + tout
                if alarm is None:
                    alarm = stop
                elif stop > alarm:
                    alarm = stop
        return alarm

    def wait_completion(self, timeout=None, abort_all_on_timeout=False) -> bool:
        """
        This function will wait for the execution of all scheduled simulations to complete.

        :param timeout: Cancels the wait after the number of seconds specified by the timeout.
            This timeout is reset everytime that a simulation is completed. The difference between this timeout and the
            one defined in the SimRunner instance, is that the latter is implemented by the subprocess class, and
            this one just cancels the wait.
        :type timeout: int
        :param abort_all_on_timeout: attempts to stop all LTSpice processes if timeout is expired.
        :type abort_all_on_timeout: bool
        :returns: True if all simulations were executed successfully
        :rtype: bool
        """
        self.update_completed()
        if timeout is not None:
            stop_time = clock_function() + timeout
        while len(self.active_tasks) > 0:
            sleep(1)
            self.update_completed()
            if timeout is None:
                stop_time = self._maximum_stop_time()
            if stop_time is not None:  # This can happen if timeout was set as none everywhere
                if clock_function() > stop_time:
                    if abort_all_on_timeout:
                        self.kill_all_ltspice()
                    return False

        return self.failSim == 0

    @staticmethod
    def _del_file_if_exists(workfile: Path):
        """
        Deletes a file if it exists.
        :param workfile: File to be deleted
        :type workfile: Path
        :return: Nothing
        """
        if workfile.exists():
            _logger.info("Deleting..." + workfile.name)
            workfile.unlink()

    @staticmethod
    def _del_file_ext_if_exists(workfile: Path, ext: str):
        """
        Deletes a file extension if it exists.
        :param workfile: File to be deleted
        :type workfile: Path
        :param ext: Extension to be deleted
        :type ext: str
        :return: Nothing
        """
        sim_file = workfile.with_suffix(ext)
        SimRunner._del_file_if_exists(sim_file)

    def cleanup_files(self):
        """
        Will delete all log and raw files that were created by the script. This should only be executed at the end
        of data processing.
        """
        self.update_completed()  # Updates the active_tasks and completed_tasks lists

        for task in self.completed_tasks:
            netlistfile = task.netlist_file
            self._del_file_if_exists(netlistfile)  # Delete the netlist file if still exists
            self._del_file_if_exists(task.log_file)  # Delete the log file if was created
            self._del_file_if_exists(task.raw_file)  # Delete the raw file if was created

            if netlistfile.suffix == '.net' or netlistfile.suffix == '.asc':
                # Delete the files that have been potentially created by LTSpice
                for ext in ('.log.raw', '.op.raw'):
                    self._del_file_ext_if_exists(netlistfile, ext)

                if netlistfile.suffix == '.asc':  # If simulated from an asc file, delete the .net file
                    # Then needs to delete the .net as well
                    self._del_file_ext_if_exists(netlistfile, '.net')

    def file_cleanup(self):
        """(Deprecated) Use cleanup_files() instead"""
        self.cleanup_files()  # Alias for backward compatibility, this will be deleted in the future

    def __iter__(self):
        self._iterator_counter = 0  # Reset the iterator counter. Note: nested iterators are not supported
        return self

    def __next__(self):
        while True:
            self.update_completed()  # Updates the active_tasks and completed_tasks lists
            # First go through the completed tasks
            if self._iterator_counter < len(self.completed_tasks):
                ret = self.completed_tasks[self._iterator_counter]
                self._iterator_counter += 1
                return ret.get_results()

            # Then check if there are any active tasks
            if len(self.active_tasks) == 0:
                raise StopIteration

            # Then go through the active tasks to get the maximum timeout
            stop_time = self._maximum_stop_time()

            if stop_time is not None and clock_function() > stop_time:  # All tasks are on timeout condition
                raise SimRunnerTimeoutError(f"Exceeded {self.timeout} seconds waiting for tasks to finish")

            # Wait for the active tasks to finish with a timeout
            sleep(0.2)  # Go asleep for a while

