import sys
sys.path.insert(0,'..')
import os

from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator, SensorConfig,\
    ScenarioConfig, ScadaData

from utils import get_temp_folder


def test_sensorconfig():
    sensor_config = SensorConfig(nodes=["0", "1", "2"], links=["0", "1"], pressure_sensors=["2"])
    sensor_config_restored = SensorConfig.load(sensor_config.dump())

    assert sensor_config == sensor_config_restored


def test_scenarioconfig():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)

        assert ScenarioConfig.load(sim.get_scenario_config().dump()) == sim.get_scenario_config()


def test_scadadata():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)

        res = sim.run_simulation()

        f = os.path.join(get_temp_folder(), "my_hanoi.scada_data")
        res.save_to_file(f)
        res_loaded = ScadaData.load_from_file(f)

        assert res == res_loaded