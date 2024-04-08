"""
Module provides tests to test the `epty_flow.models` module
"""
from epyt_flow.data.benchmarks import load_leakdb_scada_data
from epyt_flow.models import SensorInterpolationDetector

from .utils import get_temp_folder


def test_sensor_interpolation_detector():
    data = load_leakdb_scada_data(scenarios_id=[4, 1], use_net1=True,
                                  download_dir=get_temp_folder())

    data_train = data[0]
    data_test = data[1]

    detector = SensorInterpolationDetector()
    detector.fit(data_train)

    assert detector.apply(data_test) is not None
