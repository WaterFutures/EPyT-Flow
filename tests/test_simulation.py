"""
Module provides tests to test the
:class:`~epyt_flow.simulation.ScenarioSimulator` class.
"""
import os
from epyt_flow.data.networks import load_hanoi
from epyt_flow.data.benchmarks import load_leakdb_scenarios
from epyt_flow.simulation import ScenarioSimulator, ParallelScenarioSimulation, \
    callback_save_to_file
from epyt_flow.utils import to_seconds, create_path_if_not_exist

from .utils import get_temp_folder


def test_randomize_demands():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.randomize_demands()

        sim.estimate_memory_consumption()
        res = sim.run_simulation()

        res.get_data()


def test_parallel_simulation():
    scenarios = load_leakdb_scenarios(range(5), use_net1=True)

    folder_out = os.path.join(get_temp_folder(), "my_leakdb_results")
    create_path_if_not_exist(folder_out)
    ParallelScenarioSimulation.run(scenarios,
                                   callback=callback_save_to_file(folder_out=folder_out))
