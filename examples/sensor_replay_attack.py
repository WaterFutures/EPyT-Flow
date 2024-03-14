"""
Example of implementing a sensor replay attack.
"""
from epyt_flow.data.benchmarks import load_leakdb_scenarios
from epyt_flow.simulation import ScenarioSimulator, SENSOR_TYPE_NODE_PRESSURE
from epyt_flow.simulation.events import SensorReplayAttack
from epyt_flow.utils import to_seconds


if __name__ == "__main__":
    # Load the first LeakDB Hanoi scenario
    config = load_leakdb_scenarios(scenarios_id=["1"], use_net1=False)[0]
    with ScenarioSimulator(scenario_config=config) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Add a sensor replay attack -- pressure readings at node "13" between 5hrs and 7hrs
        # after simulation start (time steps 10 - 15) are replaced by the historical readings
        # collected from the first 150min (i.e. first 5 time steps)
        sim.add_sensor_reading_event(SensorReplayAttack(replay_data_time_window_start=0,
                                                        replay_data_time_window_end=to_seconds(
                                                            minutes=150),
                                                        start_time=to_seconds(hours=5),
                                                        end_time=to_seconds(hours=7),
                                                        sensor_id="13",
                                                        sensor_type=SENSOR_TYPE_NODE_PRESSURE))

        # Run simulation and and retrieve pressure readings
        res = sim.run_simulation()

        pressure_readings = res.get_data_pressures(sensor_locations=["13"])
        print(pressure_readings[:5])
        print(pressure_readings[10:15])     # The same as the first 5 readings!
        print(pressure_readings[16:])
