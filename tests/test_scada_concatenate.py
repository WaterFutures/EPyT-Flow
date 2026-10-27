"""Regression tests for time windows after concatenating SCADA data."""
import numpy as np
import pytest

from epyt_flow.simulation import SensorConfig
from epyt_flow.simulation.scada import ScadaData
from epyt_flow.topology import NetworkTopology


def _make_scada(times: list[int]) -> ScadaData:
    """Build deterministic readings without running a hydraulic simulation."""
    topology = NetworkTopology(
        f_inp="synthetic.inp", nodes=[("1", {"type": 0, "elevation": 0.}),
                                      ("2", {"type": 0, "elevation": 0.})],
        links=[("1", ("1", "2"), {"type": 1, "diameter": 100., "length": 10.})],
        pumps={}, valves={}, curves={}, patterns={},
        flow_units=5, pressure_units=0)
    config = SensorConfig(
        nodes=["1", "2"], links=["1"], valves=[], pumps=[], tanks=[],
        bulk_species=[], surface_species=[], flow_unit=5, pressure_unit=0,
        pressure_sensors=["1"], demand_sensors=["1"])
    timestamps = np.array(times)
    return ScadaData(
        sensor_config=config, network_topo=topology,
        sensor_readings_time=timestamps,
        pressure_data_raw=np.column_stack((timestamps + 100., timestamps + 110.)),
        demand_data_raw=np.column_stack((timestamps + 200., timestamps + 210.)),
        warnings_code=timestamps // 10)


@pytest.mark.parametrize("start,end,expected", [
    (20, 30, [20, 30]),
    (10, 20, [10, 20]),
    (20, None, [20, 30]),
    (0, 10, [0, 10]),
])
def test_time_window_after_concatenate(start: int, end: int,
                                       expected: list[int]) -> None:
    data = _make_scada([0, 10])
    data.concatenate(_make_scada([20, 30]))
    window = data.extract_time_window(start, end)
    times = np.array(expected)
    np.testing.assert_array_equal(window.sensor_readings_time, times)
    np.testing.assert_array_equal(window.get_data_pressures(),
                                  (times + 100.).reshape(-1, 1))
    np.testing.assert_array_equal(window.get_data_demands(),
                                  (times + 200.).reshape(-1, 1))
    np.testing.assert_array_equal(window.warnings_code, times // 10)


def test_time_window_after_repeated_concatenation() -> None:
    data = _make_scada([0, 10])
    data.concatenate(_make_scada([20, 30]))
    data.concatenate(_make_scada([40, 50]))
    window = data.extract_time_window(30)
    times = np.array([30, 40, 50])
    np.testing.assert_array_equal(window.sensor_readings_time, times)
    np.testing.assert_array_equal(window.get_data_pressures(),
                                  (times + 100.).reshape(-1, 1))
    np.testing.assert_array_equal(window.get_data_demands(),
                                  (times + 200.).reshape(-1, 1))
    np.testing.assert_array_equal(window.warnings_code, times // 10)
