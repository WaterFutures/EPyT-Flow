"""
This example demonstrates how to create an event detection problem --
i.e. a scenario with several different events to be detected.
"""
import numpy as np
import matplotlib.pyplot as plt
from epyt_flow.data.networks import load_ltown
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.simulation.events import AbruptLeakage, IncipientLeakage, SensorFaultDrift
from epyt_flow.simulation import SENSOR_TYPE_LINK_FLOW
from epyt_flow.utils import to_seconds, time_points_to_one_hot_encoding
from epyt_flow.models import SensorInterpolationDetector


if __name__ == "__main__":
    # Load the L-Town water distribution network with a default sensor placement
    # and realistic demand patterns
    config = load_ltown(use_realistic_demands=True,
                        include_default_sensor_placement=True)

    # Create new scenario
    with ScenarioSimulator(scenario_config=config) as scenario:
        # Set simulation duration to 2 weeks (i.e. 14 days)
        params = {"simulation_duration": to_seconds(days=14),
                  "hydraulic_time_step": to_seconds(minutes=5),
                  "reporting_time_step": to_seconds(minutes=5)}
        scenario.set_general_parameters(**params)

        # The first week is fault free but in the second week,
        # several events such as leakages and sensor faults are active
        leak1 = AbruptLeakage(link_id="p673", diameter=0.001,
                              start_time=to_seconds(days=7),
                              end_time=to_seconds(days=8))
        scenario.add_leakage(leak1)

        leak2 = IncipientLeakage(link_id="p31", diameter=0.02,
                                 start_time=to_seconds(days=11),
                                 end_time=to_seconds(days=13),
                                 peak_time=to_seconds(days=12))
        scenario.add_leakage(leak2)

        sensor_fault = SensorFaultDrift(coef=1.1, sensor_id="p227",
                                        sensor_type=SENSOR_TYPE_LINK_FLOW,
                                        start_time=to_seconds(days=9),
                                        end_time=to_seconds(days=10))
        scenario.add_sensor_fault(sensor_fault)

        # Run simulation
        scada_data = scenario.run_simulation(verbose=True)

        # Fit and apply classic residual-based sensor interpolation detector to sensor readings
        X = np.concatenate((scada_data.get_data_pressures(), scada_data.get_data_flows()), axis=1)

        events_times = [int(t / params["hydraulic_time_step"])
                        for t in scenario.get_events_active_time_points()]
        y = time_points_to_one_hot_encoding(events_times, total_length=X.shape[0])

        split_point = 2000
        X_train, y_train = X[:split_point, :], y[:split_point]
        X_test, y_test = X[split_point:, :], y[split_point:]

        detector = SensorInterpolationDetector()
        detector.fit(X_train)

        suspicious_time_points = detector.apply(X_test)
        y_test_pred = time_points_to_one_hot_encoding(suspicious_time_points, X_test.shape[0])

        # Show results
        plt.figure()
        plt.plot(list(range(len(y_test))), y_test, color="red", label="Ground truth event")
        plt.bar(list(range(len(y_test_pred))), y_test_pred, label="Raised alarm")
        plt.legend()
        plt.ylabel("Event indicator")
        plt.yticks([0, 1], ["Inactive", "Active"])
        plt.xlabel("Time (5min steps)")
        plt.show()
