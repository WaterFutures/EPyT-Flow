"""
Example of setting the state of a pump in an acutator event.
"""
from epyt_flow.data.networks import load_net1
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.utils import to_seconds, plot_timeseries_data
from epyt_flow.simulation.events import PumpStateEvent, ActuatorConstants


if __name__ == "__main__":
    # Create new scenario based on Net1
    with ScenarioSimulator(scenario_config=load_net1()) as sim:
        # Set simulation duration to 40 hours
        sim.set_general_parameters(simulation_duration=to_seconds(hours=40))

        # Monitor states of tank "2" and pump "9"
        sim.set_tank_sensors(sensor_locations=["2"])
        sim.set_pump_state_sensors(sensor_locations=["9"])

        # Remove all existing controls
        sim.epanet_api.deleteControls()

        # Add actuator (i.e. pump state) events
        # Deactivate pump "9" at 14h after simulation start
        sim.add_actuator_event(PumpStateEvent(pump_id="9",
                                              pump_state=ActuatorConstants.EN_CLOSED,
                                              time=to_seconds(hours=14)))

        # Re-activate pump "9" at 25h after simulation start
        sim.add_actuator_event(PumpStateEvent(pump_id="9",
                                              pump_state=ActuatorConstants.EN_OPEN,
                                              time=to_seconds(hours=25)))

        # Run simulation and show sensor readings over time
        scada_data = sim.run_simulation()
        print(scada_data.get_data())

        plot_timeseries_data(scada_data.get_data_pumps_state().T,
                             x_axis_label="Time (30min steps)", y_axis_label="Pump state")
        plot_timeseries_data(scada_data.get_data_tanks_water_volume().T,
                             x_axis_label="Time (30min steps)",
                             y_axis_label="Water volume in $m^3$")
