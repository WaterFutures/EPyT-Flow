"""
Example of manually setting the state of a pump.
"""
from epyt_flow.data.networks import load_net1
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.utils import to_seconds
from epyt_flow.simulation.events import PumpStateEvent, ActuatorConstants


if __name__ == "__main__":
    # Create new scenario based on Net1
    with ScenarioSimulator(scenario_config=load_net1()) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Monitor states of tank "2" and pump "9"
        sim.set_tank_sensors(sensor_locations=["2"])
        sim.set_pump_sensors(sensor_locations=["9"])

        # Remove all controls that might exist
        sim.epanet_api.deleteControls()

        # Add custom controls
        # Deactivate pump "9" at 14h after simulation start
        sim.add_actuator_event(PumpStateEvent(pump_id="9",
                                              pump_state=ActuatorConstants.EN_CLOSED,
                                              time=to_seconds(hours=14)))

        # Activate pump "9" at 45h after simulation start
        sim.add_actuator_event(PumpStateEvent(pump_id="9",
                                              pump_state=ActuatorConstants.EN_OPEN,
                                              time=to_seconds(hours=45)))

        # Run simulation and show sensor readings over time
        res = sim.run_simulation()
        print(res.get_data())
