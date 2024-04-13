"""
Example of leak detection in some LeakDB scenarios.
"""
from epyt_flow.data.benchmarks import load_leakdb_scada_data
from epyt_flow.models import SensorInterpolationDetector


if __name__ == "__main__":
    data = load_leakdb_scada_data(scenarios_id=[4, 1], use_net1=True)

    data_train = data[0]
    data_test = data[1]

    detector = SensorInterpolationDetector()
    detector.fit(data_train)

    suspicous_time_points = detector.apply(data_test)
    print(suspicous_time_points)
