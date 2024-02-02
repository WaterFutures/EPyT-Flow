import sys
sys.path.insert(0,'..')

from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import ScenarioConfig


def test_configparser():
    config_as_json = """{
            "general": {
                "file_inp": "/tmp/Hanoi.inp",
                "file_msx": "",
                "simulation_duration": 100,
                "demand_model": "pdd",
                "hydraulic_time_step": 0,
                "quality_time_step": 0
            },
            "uncertainties": {
                "pipe_length": {"type": "gaussian", "mean": 0, "scale": 1},
                "pipe_roughness": {"type": "uniform", "low": 0, "hight": 1},
                
                "sensor_noise": {"type": "gaussian", "mean": 0, "scale": 0.01}
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
    load_hanoi()
    config = ScenarioConfig.load_from_json(config_as_json)
    print(config)
