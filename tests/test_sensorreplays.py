"""
Module provides tests to test sensor replay and override attacks.
"""
import numpy as np

from epyt_flow.data.benchmarks import load_leakdb_scenarios
from epyt_flow.simulation import ScenarioSimulator, SENSOR_TYPE_NODE_PRESSURE
from epyt_flow.simulation.events import SensorReplayAttack, SensorOverrideAttack
from epyt_flow.utils import to_seconds

from .utils import get_temp_folder


def test_replay_attack():
    config = load_leakdb_scenarios(download_dir=get_temp_folder(),
                                   scenarios_id=["1"], use_net1=False)[0]
    with ScenarioSimulator(scenario_config=config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        sim.add_sensor_reading_event(SensorReplayAttack(replay_data_time_window_start=0,
                                                        replay_data_time_window_end=9000,
                                                        start_time=18000, end_time=27000,
                                                        sensor_id="13",
                                                        sensor_type=SENSOR_TYPE_NODE_PRESSURE))

        res = sim.run_simulation()

        pressure_readings = res.get_data_pressures(sensor_locations=["13"])
        assert np.all(pressure_readings[:5] == pressure_readings[10:15])


def test_override_attack():
    config = load_leakdb_scenarios(download_dir=get_temp_folder(),
                                   scenarios_id=["1"], use_net1=False)[0]
    with ScenarioSimulator(scenario_config=config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        new_sensor_values = np.array([42]*5)
        sim.add_sensor_reading_event(SensorOverrideAttack(new_sensor_values, start_time=18000,
                                                          end_time=27000, sensor_id="13",
                                                          sensor_type=SENSOR_TYPE_NODE_PRESSURE))

        res = sim.run_simulation()

        pressure_readings = res.get_data_pressures(sensor_locations=["13"])
        assert np.all(pressure_readings[10:15] == new_sensor_values)
