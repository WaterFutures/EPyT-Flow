.. _tut.control:

*******
Control
*******

Besides the :ref:`simple <simple_controls>` and :ref:`complex <complex_controls>` EPANET
control rules, EPyT-Flow also supports the implementation of
:ref:`custom control modules & algorithms <custom_controls>` in Python code.
Note that those custom control modules can go beyond IF-THEN-ELSE controls as supported
by EPANET -- i.e. arbitrary control logic can be implemented by the user, incl. AI-based controls
where for instance a neural network is utlized to make control decisions.

.. note::

    We recommend checking out `EPyT-Control <https://github.com/WaterFutures/EPyT-Control>`_, if you
    are interested in developing and benchmarking (data-driven) control algorithms such as
    classic control or reinforcement learning.

    EPyT-Control is a Python package building on top of
    `EPyT-Flow <https://github.com/WaterFutures/EPyT-Flow>`_ for implementing and evaluating control
    algorithms & strategies in water distribution networks (WDN).
    Besides related control tasks such as state estimation and event diagnosis, a special focus of
    the EPyT-Control Python package is Reinforcement Learning for data-driven control in WDNs and
    therefore it provides full compatibility with the
    `Stable-Baselines3 <https://stable-baselines3.readthedocs.io/en/master/>`_ package.


.. _simple_controls:

Simple EPANET Control Rules
+++++++++++++++++++++++++++

EPANET natively supports
`simple control rules <https://epanet22.readthedocs.io/en/latest/back_matter.html#controls>`_
that can change valves and pumps at some points in time or if a lower or upper bound on some node's
pressure or tank level is observed.
Those control rules are stated in the `[CONTROLS]` section of the .inp file.

.. note::
    Be aware that those rules are directly processed by EPANET and are therefore not affected
    by any sensor noise or sensor reading attacks.

EPyT-Flow implements those simple control rules in
:class:`~epyt_flow.simulation.scada.simple_control.SimpleControlModule`
and makes them accesible by the
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.simple_controls` property
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance.
EPyT-Flow automatically parses all simple control rules from the given .inp file and creates
the corresponding :class:`~epyt_flow.simulation.scada.simple_control.SimpleControlModule`
instances in :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.simple_controls`.

Such simple EPANET control rules can be added to a scenario by calling the
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_simple_control` function
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance.

For the users' convinience, EPyT-Flow comes with wrappers for all possible types of EPANET control rules:

+-------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| Class                                                                               | Description                                                                                                    |
+=====================================================================================+================================================================================================================+
| :func:`~epyt_flow.simulation.scada.simple_control.SimplePumpSpeedTimeControl`       | Sets the pump speed at some points in time.                                                                    |
+-------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| :func:`~epyt_flow.simulation.scada.simple_control.SimplePumpSpeedConditionControl`  | Sets the pump speed if some pressure or water level condition is met at a given node.                          |
+-------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| :func:`~epyt_flow.simulation.scada.simple_control.SimpleValveTimeControl`           | Sets the valve status (i.e. open or closed) at some points in time.                                            |
+-------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| :func:`~epyt_flow.simulation.scada.simple_control.SimpleValveConditionControl`      | Sets the valve status (i.e. open or closed) if some pressure or water level condition is met at a given node.  |
+-------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+

Example of implementing a simple pump control strategy where pump "9" is activated or deactivated
based on the water level in tank "2":

.. code-block:: python

    # Create new scenario based on Net1
    with ScenarioSimulator(scenario_config=load_net1()) as sim:
        # Remove all controls that might exist
        # ...

        # Create two control rules for operating pump "9"
        # LINK 9 OPEN IF NODE 2 BELOW 110
        my_control_1 = SimpleControlModule(link_id="9",
                                           link_status=ActuatorConstants.EN_OPEN,
                                           cond_type=EpanetConstants.EN_LOWLEVEL,
                                           cond_var_value="2",
                                           cond_comp_value=110)

        # LINK 9 CLOSED IF NODE 2 ABOVE 140
        my_control_2 = SimpleControlModule(link_id="9",
                                           link_status=ActuatorConstants.EN_CLOSED,
                                           cond_type=EpanetConstants.EN_HILEVEL,
                                           cond_var_value="2",
                                           cond_comp_value=140)

        # Add control rules
        sim.add_simple_control(my_control_1)
        sim.add_simple_control(my_control_2)

        # Run simulation
        # ....


.. _complex_controls:

Complex EPANET Control Rules
++++++++++++++++++++++++++++

In addition to the :ref:`simple control rules <simple_controls>`, EPANET also supports more complex
`IF-THEN-ELSE control rules <https://epanet22.readthedocs.io/en/latest/back_matter.html#rules>`_
that can change valves and pumps at some points in time or if some (complex) condition on the
water tank level, node pressure/head, demand, etc.
Those control rules are stated in the `[RULES]` section of the .inp file.

.. note::
    Be aware that those rules are directly processed by EPANET and are therefore not affected
    by any sensor noise or sensor reading attacks.

EPyT-Flow implements those complex control rules in
:class:`~epyt_flow.simulation.scada.complex_control.ComplexControlModule`
and makes them accesible by the
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.complex_controls` property
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance.
EPyT-Flow automatically parses all complex control rules from the given .inp file and creates
the corresponding :class:`~epyt_flow.simulation.scada.complex_control.ComplexControlModule`
instances in :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.complex_controls`.

Such complex EPANET control rules can be added to a scenario by calling the
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_complex_control` function
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance.


Example of implementing a simple pump control strategy where pump "9" is activated or deactivated
based on the water level in tank "2":

.. code-block:: python

    # Create new scenario based on Net1
    with ScenarioSimulator(scenario_config=load_net1()) as sim:
        # Remove all controls that might exist
        # ...

        # Create two control rules for operating pump "9"
        # IF TANK 2 LEVEL <= 110 THEN PUMP 9 SETTING IS OPEN
        condition_1 = RuleCondition(object_type_id=EpanetConstants.EN_R_NODE,
                                    object_id="2",
                                    attribute_id=EN_R_LEVEL,
                                    relation_type_id=EN_R_LEQ,
                                    value=110)
        action_1 = RuleAction(link_type_id=EpanetConstants.EN_PUMP,
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
        condition_1 = RuleCondition(object_type_id=EpanetConstants.EN_R_NODE,
                                    object_id="2",
                                    attribute_id=EN_R_LEVEL,
                                    relation_type_id=EN_R_GEQ,
                                    value=140)
        action_1 = RuleAction(link_type_id=EpanetConstants.EN_PUMP,
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

        # Run simulation
        # ....



.. _custom_controls:

Custom Control
++++++++++++++

EPyT-Flow allows the user to implement completly custom control modules.

All custom controls must be derived from
:class:`~epyt_flow.simulation.scada.custom_control.CustomControlModule` 
and implement the
:func:`~epyt_flow.simulation.scada.custom_control.CustomControlModule.step` method.
This function implements the control logic and is called in every simulation step.
It gets the current sensor readings as an :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
instance as an argument and is supposed to apply the control logic.

.. note::
    Be aware that the obtained sensor readings from the
    :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
    instance might be subject to sensor faults and noise.

Optionally, the :func:`~epyt_flow.simulation.scada.custom_control.CustomControlModule.init`
method can be overridden for running some initialization logic -- make sure to call the parent's
:func:`~epyt_flow.simulation.scada.custom_control.CustomControlModule.init` first.

Besides implementing the control strategy through EPANET and EPANET-MSX functions,
EPyT-Flow also provides some pre-defined helper functions:

+--------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------+
| Function                                                                                               | Description                                                                                             |
+========================================================================================================+=========================================================================================================+
| :func:`~epyt_flow.simulation.scada.custom_control.CustomControlModule.set_pump_status`                 | Sets the status (i.e. turn it on or off) of a pump.                                                     |
+--------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------+
| :func:`~epyt_flow.simulation.scada.custom_control.CustomControlModule.set_pump_speed`                  | Sets the speed of a pump.                                                                               |
+--------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------+
| :func:`~epyt_flow.simulation.scada.custom_control.CustomControlModule.set_valve_status`                | Sets the status (i.e. open or closed) of a valve.                                                       |
+--------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------+
| :func:`~epyt_flow.simulation.scada.custom_control.CustomControlModule.set_node_quality_source_value`   | Sets the quality source (e.g. chemical injection amount) at a particular node to a specific value.      |
+--------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------+

.. note::
    
    Note that EPANET control rules specified in the .inp file
    will be prioritized. Other than that, EPyT-Flow first applies events and then custom controls --
    i.e. events are always prioritized over custom controls.

Example of implementing a simple pump control strategy where pump "9" is activated or deactivated
based on the water level in tank "2":

.. code-block:: python

    class MyControl(CustomControlModule):
        def __init__(self, **kwds):
            # Tank and pump ID
            self.__tank_id = "2"
            self.__pump_id = "9"

            # Tank diameter could be also obtained by calling epanet.getNodeTankData
            self.__tank_diameter = 50.5

            # Lower and upper threshold on tank level
            self.__lower_level_threshold = 110
            self.__upper_level_threshold = 140

            super().__init__(**kwds)

        def step(self, scada_data: ScadaData) -> None:
            # Retrieve current water level in the tank
            tank_volume = scada_data.get_data_tanks_water_volume([self.__tank_id]).flatten()[0]
            tank_level = volume_to_level(float(tank_volume), self.__tank_diameter)

            # Decide if pump has to be deactivated or re-activated
            if tank_level <= self.__lower_level_threshold:
                self.set_pump_status(self.__pump_id, ActuatorConstants.EN_OPEN)
            elif tank_level >= self.__upper_level_threshold:
                self.set_pump_status(self.__pump_id, ActuatorConstants.EN_CLOSED)



Custom control modules & algorithms can be added to a scenario by calling
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_custom_control`
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`
instance BEFORE running the simulation:

.. code-block:: python

    # Create new scenario based on Net1
    with ScenarioSimulator(scenario_config=load_net1()) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Monitor water volume in tank "2"
        sim.set_tank_sensors(sensor_locations=["2"])

        # Remove all controls that might exist
        # ...

        # Add custom controls
        sim.add_custom_control(MyControl())

        # Run simulation
        # ....
