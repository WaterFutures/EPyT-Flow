.. _tut.control:

*******
Control
*******

Besides the :ref:`simple EPANET control rules <simple_controls>`, EPyT-Flow also supports
the implementation of :ref:`custom (advanced) control modules & algorithms <advanced_controls>`
in Python code.
Note that those advanced control modules can go beyond simple IF-THEN-ELSE controls as supported
by EPANET -- i.e. arbitrary control logic can be implemented by the user, incl. AI-based controls
where for instance a neural network is utlized to make control decisions.

.. _simple_controls:

Simple EPANET Control Rules
+++++++++++++++++++++++++++

EPANET natively supports
`simple control rules <https://epanet22.readthedocs.io/en/latest/back_matter.html#controls>`_
that can change valves and pumps at some points in time or if a lower or upper bound on some node's
pressure or tank level is observed.

.. note::
    Be aware that those rules are directly processed by EPANET and are therefore not affected
    by any sensor noise or sensor reading attacks.

EPyT-Flow implements those simple control rules in
:class:`~epyt_flow.simulation.scada.simple_control.SimpleControlModule`
and makes them accesible by the
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.simple_controls` property
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance.

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

TODO-Example

.. code-block:: python

    # TODO


.. _advanced_controls:

Advanced Control
++++++++++++++++

All advanced controls must be derived from
:class:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule` 
and implement the
:func:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule.step` method.
This function implements the control logic and is called in every simulation step.
It gets the current sensor readings as an :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
instance as an argument and is supposed to apply the control logic.

.. note::
    Be aware that the obtained sensor readings from the
    :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
    instance might be subject to sensor faults and noise.

Optionally, the :func:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule.init`
method can be overridden for running some initialization logic -- make sure to call the parent's
:func:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule.init` first.

Besides implementing the control strategy through EPANET and EPANET-MSX functions,
EPyT-Flow also provides some pre-defined helper functions:

+------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------+
| Function                                                                                                   | Description                                                                                             |
+============================================================================================================+=========================================================================================================+
| :func:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule.set_pump_status`                 | Sets the status (i.e. turn it on or off) of a pump.                                                     |
+------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------+
| :func:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule.set_pump_speed`                  | Sets the speed of a pump.                                                                               |
+------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------+
| :func:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule.set_valve_status`                | Sets the status (i.e. open or closed) of a valve.                                                       |
+------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------+
| :func:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule.set_node_quality_source_value`   | Sets the quality source (e.g. chemical injection amount) at a particular node to a specific value.      |
+------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------+

.. note::
    
    Note that EPANET control rules such as time-based rules specified in the .inp file
    will be prioritized. Other than that, EPyT-Flow first applies events and then controls --
    i.e. events are always prioritized over controls.

Example of implementing a simple pump control strategy where pump "9" is activated or deactivated
based on the water level in tank "2":

.. code-block:: python

    class MyControl(AdvancedControlModule):
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
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_advanced_control`
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
        sim.add_advanced_control(MyControl())

        # Run simulation
        # ....
