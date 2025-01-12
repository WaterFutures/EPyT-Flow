"""
Example of implementing a simple pump control strategy using complex control modules.
"""
from epyt.epanet import ToolkitConstants
from epyt_flow.data.networks import load_net1
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.simulation.scada import ComplexControlModule, RuleAction, RuleCondition, \
    EN_R_ACTION_STATUS_CLOSED, EN_R_ACTION_STATUS_OPEN, EN_R_LEVEL, EN_R_LEQ, EN_R_GEQ
from epyt_flow.utils import to_seconds


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
        # IF TANK 2 LEVEL <= 110 THEN PUMP 9 SETTING IS OPEN
        condition_1 = RuleCondition(object_type_id=ToolkitConstants.EN_R_NODE,
                                    object_id="2",
                                    attribute_id=EN_R_LEVEL,
                                    relation_type_id=EN_R_LEQ,
                                    value=110)
        action_1 = RuleAction(link_type_id=ToolkitConstants.EN_PUMP,
                              link_id="9",
                              action_type_id=EN_R_ACTION_STATUS_OPEN,
                              action_value=None)
        my_control_1 = ComplexControlModule(rule_id="PUMP-9_1",
                                            condition_1=condition_1,
                                            additional_conditions=[],
                                            actions=[action_1],
                                            else_actions=[],
                                            priority=1)

        # IF TANK 2 LEVEL >= 140 THEN PUMP 9 SETTING IS CLOSED
        condition_1 = RuleCondition(object_type_id=ToolkitConstants.EN_R_NODE,
                                    object_id="2",
                                    attribute_id=EN_R_LEVEL,
                                    relation_type_id=EN_R_GEQ,
                                    value=140)
        action_1 = RuleAction(link_type_id=ToolkitConstants.EN_PUMP,
                              link_id="9",
                              action_type_id=EN_R_ACTION_STATUS_CLOSED,
                              action_value=None)
        my_control_2 = ComplexControlModule(rule_id="PUMP-9_2",
                                            condition_1=condition_1,
                                            additional_conditions=[],
                                            actions=[action_1],
                                            else_actions=[],
                                            priority=1)

        # Add control rules
        sim.add_complex_control(my_control_1)
        sim.add_complex_control(my_control_2)

        # Run simulation and show sensor readings over time
        scada_data_res = sim.run_simulation()
        scada_data_res.plot_pumps_state()
        scada_data_res.plot_tanks_water_volume()
