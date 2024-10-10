"""
Example of implementing a sensor override attack.
"""
import numpy as np
from epyt_flow.data.benchmarks import load_leakdb_scenarios
from epyt_flow.simulation import ScenarioSimulator, SENSOR_TYPE_LINK_FLOW
from epyt_flow.simulation.events import SensorOverrideAttack
from epyt_flow.utils import to_seconds, plot_timeseries_data


if __name__ == "__main__":
    # Create a new scenario simulation based on the first LeakDB Hanoi scenario
    config = load_leakdb_scenarios(scenarios_id=["1"], use_net1=False)[0]
    with ScenarioSimulator(scenario_config=config) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Override the sensor readings of the flow sensor at link "1" with the value "42" for
        # 2hrs -- i.e. time steps 10 - 15.
        new_sensor_values = np.array([42]*5)
        sim.add_sensor_reading_event(SensorOverrideAttack(new_sensor_values,
                                                          start_time=to_seconds(hours=5),
                                                          end_time=to_seconds(hours=7),
                                                          sensor_id="1",
                                                          sensor_type=SENSOR_TYPE_LINK_FLOW))

        # Run simulation and and retrieve flow readings
        scada_data = sim.run_simulation()

        flow_readings = scada_data.get_data_flows(sensor_locations=["1"])
        print(flow_readings)
        plot_timeseries_data(flow_readings.T,
                             x_axis_label="Time (30min steps)",
                             y_axis_label="Flow rate in $m^3/h$")

        # Remove attack and recompute and show final sensor readings
        scada_data.sensor_reading_events = []

        flow_readings = scada_data.get_data_flows(sensor_locations=["1"])
        plot_timeseries_data(flow_readings.T,
                             x_axis_label="Time (30min steps)",
                             y_axis_label="Flow rate in $m^3/h$")
