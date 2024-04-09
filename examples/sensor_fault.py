"""
Example of implementing a sensor fault.
"""
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import ScenarioSimulator, SENSOR_TYPE_NODE_PRESSURE
from epyt_flow.simulation.events import SensorFaultStuckZero
from epyt_flow.utils import to_seconds


if __name__ == "__main__":
    # Load the Hanoi network with default sensor configuration
    hanoi_network_config = load_hanoi(include_default_sensor_placement=True)

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        # Set simulaton duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Add a pressure sensor fault (i.e. power failure, sensor readings are set to zero) at
        # node "16" that is active for 90min (i.e. starts at 150min after simulation begin and ends
        # at 240min after simulation start).
        sim.add_sensor_fault(
            SensorFaultStuckZero(sensor_id="16",
                                 sensor_type=SENSOR_TYPE_NODE_PRESSURE,
                                 start_time=to_seconds(minutes=150),
                                 end_time=to_seconds(minutes=240)))

        # Run entire simulation
        scada_data = sim.run_simulation()

        # Retrieve pressure readings at node "16"
        print(scada_data.get_data_pressures(sensor_locations=["16"]))
