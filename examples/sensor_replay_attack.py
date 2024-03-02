"""
Example of implementing a sensor replay attack.
"""
from epyt_flow.data.benchmarks import load_leakdb
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator, \
    SENSOR_TYPE_NODE_PRESSURE
from epyt_flow.simulation.events import SensorReplayAttack


if __name__ == "__main__":
    # Load the first LeakDB Hanoi scenario
    config = load_leakdb(scenarios_id=["1"], use_net1=False)[0]
    with WaterDistributionNetworkScenarioSimulator(scenario_config=config) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=2)

        # Add a sensor replay attack -- pressure readings at node "13" between 18000s and 27000s
        # (time steps 10 - 15) are replaced by the historical readings collected from 0 to 9000s
        # (i.e. first 5 time steps)
        sim.add_sensor_reading_event(SensorReplayAttack(replay_data_time_window_start=0,
                                                        replay_data_time_window_end=9000,
                                                        start_time=18000, end_time=27000,
                                                        sensor_id="13",
                                                        sensor_type=SENSOR_TYPE_NODE_PRESSURE))

        # Run simulation and and retrieve pressure readings
        res = sim.run_simulation()

        pressure_readings = res.get_data_pressures(sensor_locations=["13"])
        print(pressure_readings[:5])
        print(pressure_readings[10:15])     # The same as the first 5 readings!
        print(pressure_readings[16:])
