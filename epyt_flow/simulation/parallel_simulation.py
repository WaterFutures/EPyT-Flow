"""
Module provides functions for simulating several scenarios in parallel.
"""
from typing import Callable, Any
import os
import warnings
import shutil
from multiprocess import Pool, cpu_count
import psutil

from .scenario_config import ScenarioConfig
from .scada import ScadaData
from .scenario_simulator import ScenarioSimulator


def callback_save_to_file(folder_out: str = "") -> Callable[[ScadaData, ScenarioConfig, int], None]:
    """
    Creates a callback for storing the simulation results in a .epytflow_scada_data file.
    The returned callback can be directly passed to
    :func:`~epyt_flow.simulation.parallel_simulation.ParallelScenarioSimulation.run`.

    Parameters
    ----------
    folder_out : `str`, optional
        Path to the folder where the simulation results will be stored.

        The default is the current working directory.

    Returns
    -------
    `Callable[[ScadaData, ScenarioConfig, int], None]`
        Callback storing the simulation results.
    """
    def callback(scada_data: ScadaData, _, scenario_idx: int) -> None:
        scada_data.save_to_file(os.path.join(folder_out, f"{scenario_idx}"))

    return callback


def _run_scenario_simulation(scenario_config: ScenarioConfig, scenario_idx: int,
                             callback: Callable[[ScadaData, ScenarioConfig, int], Any]) -> Any:
    with ScenarioSimulator(scenario_config=scenario_config) as sim:
        return callback(sim.run_simulation(), scenario_config, scenario_idx)


class ParallelScenarioSimulation():
    """
    Class providing functions to run scenario simulations in parallel.
    """
    @staticmethod
    def run(scenarios: list[ScenarioConfig], n_jobs: int = -1,
            max_working_memory_consumption: int = None,
            callback: Callable[[ScadaData, ScenarioConfig, int], Any] = callback_save_to_file()
            ) -> Any:
        """
        Simulates multiple scenarios in parallel.

        Parameters
        ----------
        scenarios : list[:class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`]
            List of scenarios to be simulated.
        n_jobs : `int`, optional
            Number of CPUs that can be used by the simulations -- usually, this translates to
            the number of scenarios that are simulated in parallel.

            If -1, all CPUs are used.

            The default is -1
        max_working_memory_consumption : `int`, optional
            Maximum amount of working memory in MB that can be used by the simulations.
            Note that this might limit the number of scenarios that can be simulated in parallel.

            The default is None.
        callback: `Callable[[ScadaData, ScenarioConfig, int], None]`, optional
            Callback that is called after the simulation of a scenario finished.

            The callback gets the simulation results as a
            :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance, the scenario
            configuration as a :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
            instance, and the index of the scenario in 'scenarios' as arguments.

            The default is :func:`~epyt_flow.simulation.parallel_simulation.callback_save_to_file`.
        """
        if not isinstance(scenarios, list):
            raise TypeError("'scenarios' must be an instance of 'list[ScenarioConfig]' " +
                            f"but not of '{type(scenarios)}'")
        if any(not isinstance(item, ScenarioConfig) for item in scenarios):
            raise TypeError("Each item in 'scenarios' must be an instance of 'ScenarioConfig'")

        if not isinstance(n_jobs, int):
            raise TypeError(f"'n_jobs' must be an instance of 'int' but not of '{type(n_jobs)}'")
        if not (n_jobs == -1 or n_jobs > 0):
            raise ValueError("'n_jobs' must be either -1 or a positive integer")

        if max_working_memory_consumption is not None:
            if not isinstance(max_working_memory_consumption, int) or \
                    max_working_memory_consumption <= 0:
                raise ValueError("'max_working_memory_consumption' must be a positive integer")

        if not callable(callback):
            raise TypeError("'callback' mut be a callable " +
                            "'Callable[[ScadaData, ScenarioConfig, int], None]'")

        # Get free memory in MB
        ram_free_memory = psutil.virtual_memory().free * .000001
        if max_working_memory_consumption is not None:
            ram_free_memory = max(ram_free_memory, max_working_memory_consumption)

        harddisk_free_memory = shutil.disk_usage(".").free * .000001

        # Check memory requirements of each scenario
        max_memory_required = max(s_config.memory_consumption_estimate
                                  if s_config.memory_consumption_estimate is not None else 0
                                  for s_config in scenarios)
        if max_memory_required > ram_free_memory:
            raise RuntimeError("Not enough working memory avaialble! " +
                               f"Requested {max_memory_required} MB but only " +
                               f"{ram_free_memory} MB are available")

        if sum(s_config.memory_consumption_estimate
               if s_config.memory_consumption_estimate is not None else 0
               for s_config in scenarios) >= harddisk_free_memory:
            warnings.warn("There might not be enough free space on the hard disk " +
                          "to store all scenario results")

        # Compute number of processes that can run in parallel
        n_available_cpus = cpu_count()
        if n_jobs != -1:
            n_available_cpus = min(n_available_cpus, n_jobs)

        required_memory_bound = min(ram_free_memory, harddisk_free_memory)
        n_max_parallel_scenarios = n_available_cpus
        if max_memory_required != 0:
            n_max_parallel_scenarios = int(required_memory_bound / max_memory_required)

        n_parallel_scenarios = min(n_available_cpus, n_max_parallel_scenarios)

        if any(s_config.f_msx_in is not None for s_config in scenarios):
            n_parallel_scenarios = 1

        # Run scenario simulations
        scenarios_task = []
        for scenario_idx, scenario in enumerate(scenarios):
            scenarios_task.append((scenario, scenario_idx, callback))

        with Pool(processes=n_parallel_scenarios, maxtasksperchild=1) as pool:
            return pool.starmap(_run_scenario_simulation, scenarios_task)
