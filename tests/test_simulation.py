"""
Module provides tests to test the 
:class:`~epyt_flow.simulation.WaterDistributionNetworkScenarioSimulator` class.
"""
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator

from .utils import get_temp_folder


def test_randomize_demands():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)
        sim.randomize_demands()

        res = sim.run_simulation()
        res.get_data()
