import sys
sys.path.insert(0,'..')

from epyt_flow.data.networks import load_hanoi, load_net1
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator
from epyt_flow.simulation.sensor_config import SENSOR_TYPE_NODE_QUALITY

from utils import get_temp_folder


def test_water_age():
    network_config = load_hanoi(download_dir=get_temp_folder(),
                                include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        sim.set_sensors(SENSOR_TYPE_NODE_QUALITY, sensor_locations=sim.sensor_config.nodes)

        sim.enable_waterage_analysis()

        res = sim.run_simulation()
        res.get_data()


def test_source_tracing():
    network_config = load_hanoi(download_dir=get_temp_folder(),
                                include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        sim.set_sensors(SENSOR_TYPE_NODE_QUALITY, sensor_locations=sim.sensor_config.nodes)

        sim.enable_sourcetracing_analysis("2")

        res = sim.run_simulation()
        res.get_data()


def test_chlorine():
    network_config = load_net1(download_dir=get_temp_folder())
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        sim.set_sensors(SENSOR_TYPE_NODE_QUALITY, sensor_locations=sim.sensor_config.nodes)

        sim.enable_chemical_analysis()

        res = sim.run_simulation()
        res.get_data()
