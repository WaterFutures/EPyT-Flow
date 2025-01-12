"""
Example of implementing a simple pump control strategy using simple control modules.
"""
from epyt.epanet import ToolkitConstants
from epyt_flow.data.networks import load_net1
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.simulation.scada import SimpleControlModule
from epyt_flow.utils import to_seconds
from epyt_flow.simulation.events import ActuatorConstants


if __name__ == "__main__":
    # Create new scenario based on Net1
    with ScenarioSimulator(scenario_config=load_net1()) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Monitor states of tank "2" and pump "9"
        sim.set_tank_sensors(sensor_locations=["2"])
        sim.set_pump_state_sensors(sensor_locations=["9"])

        # Remove all existing controls
        # Note that Net1.inp contains some simple controls
        sim.remove_all_simple_controls()

        # Create two control rules for operating pump "9"
        # LINK 9 OPEN IF NODE 2 BELOW 110
        my_control_1 = SimpleControlModule(link_id="9",
                                           link_status=ActuatorConstants.EN_OPEN,
                                           cond_type=ToolkitConstants.EN_LOWLEVEL,
                                           cond_var_value="2",
                                           cond_comp_value=110.)

        # LINK 9 CLOSED IF NODE 2 ABOVE 140
        my_control_2 = SimpleControlModule(link_id="9",
                                           link_status=ActuatorConstants.EN_CLOSED,
                                           cond_type=ToolkitConstants.EN_HILEVEL,
                                           cond_var_value="2",
                                           cond_comp_value=140.)

        # Add control rules
        sim.add_simple_control(my_control_1)
        sim.add_simple_control(my_control_2)

        # Run simulation and show sensor readings over time
        scada_data_res = sim.run_simulation()
        scada_data_res.plot_pumps_state()
        scada_data_res.plot_tanks_water_volume()
