"""
Module provides test to test different types of leakages.
"""
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator, IncipientLeakage, \
    AbruptLeakage

from .utils import get_temp_folder


def test_abrupt_leakage():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)

        leak = AbruptLeakage(link_id="12", diameter=0.1, start_time=7200, end_time=100800)
        sim.add_leakage(leak)

        res = sim.run_simulation()
        res.get_data()


def test_incipient_leakage():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)

        leak = IncipientLeakage(link_id="12", diameter=0.01,
                                start_time=7200, end_time=100800, peak_time=54000)
        sim.add_leakage(leak)

        res = sim.run_simulation()
        res.get_data()
