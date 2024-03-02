"""
Example of implementing a sensor override attack.
"""
import numpy as np
from epyt_flow.data.benchmarks import load_leakdb
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator, \
    SENSOR_TYPE_LINK_FLOW
from epyt_flow.simulation.events import SensorOverrideAttack


if __name__ == "__main__":
    # Load the first LeakDB Hanoi scenario
    config = load_leakdb(scenarios_id=["1"], use_net1=False)[0]
    with WaterDistributionNetworkScenarioSimulator(scenario_config=config) as sim:
        # Set simulaton duration to two days
        sim.set_general_parameters(simulation_duration=2)

        # Override the sensor readings of the flow sensor at link "1" with the value "42" for
        # the time 18000s to 27000s (i.e. time steps 10 - 15)
        new_sensor_values = np.array([42]*5)
        sim.add_sensor_reading_event(SensorOverrideAttack(new_sensor_values, start_time=18000,
                                                          end_time=27000, sensor_id="1",
                                                          sensor_type=SENSOR_TYPE_LINK_FLOW))

        # Run simulation and and retrieve flow readings
        res = sim.run_simulation()

        flow_readings = res.get_data_flows(sensor_locations=["1"])
        print(flow_readings)
