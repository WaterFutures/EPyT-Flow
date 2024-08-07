"""
Module provides tests to test parsing a :class:`~epty_flow.simulation.ScenarioConfig`
instance from text data.
"""
import os
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import ScenarioConfig, ScenarioSimulator

from .utils import get_temp_folder


def test_configparser():
    config_as_json = """{
            "general": {
                "file_inp": "/tmp/Hanoi.inp",
                "simulation_duration": 864000,
                "demand_model": {"type": "PDA", "pressure_min": 0, "pressure_required": 0.1, "pressure_exponent": 0.5},
                "hydraulic_time_step": 1800,
                "quality_time_step": 300,
                "reporting_time_step": 1800,
                "flow_units_id": 8
            },
            "uncertainties": {
                "pipe_length": {"type": "absolute_gaussian", "mean": 0, "scale": 1},
                "pipe_roughness": {"type": "absolute_uniform", "low": 0, "high": 1},
                "sensor_noise": {"type": "relative_gaussian", "scale": 0.01}
            },
            "sensors": {
                "pressure_sensors": ["13", "16", "22", "30"],
                "flow_sensors": ["1"],
                "demand_sensors": [],
                "node_quality_sensors": [],
                "link_quality_sensors": []
            },
            "leakages": [
                {"type": "abrupt", "link_id": "12", "diameter": 0.1, "start_time": 7200, "end_time": 100800},
                {"type": "incipient", "link_id": "10", "diameter": 0.01, "start_time": 7200, "end_time": 100800, "peak_time": 54000}
            ],
            "sensor_faults": [
                {"type": "constant", "constant_shift": 2.0, "sensor_id": "16", "sensor_type": 1, "start_time": 5000, "end_time": 100000}
            ]
        }"""
    # Use OS dependend path
    config_as_json = config_as_json.replace("/tmp/Hanoi.inp", f"{os.path.join(get_temp_folder(), 'Hanoi.inp')}").\
        replace("\\", "\\\\")

    # Make sure Hanoi network is available
    load_hanoi(download_dir=get_temp_folder())

    # Load config from JSON and run the simulation
    config = ScenarioConfig.load_from_json(config_as_json)
    with ScenarioSimulator(scenario_config=config) as sim:
        sim.run_simulation()
