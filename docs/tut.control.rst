.. _tut.control:

*******
Control
*******

EPyT-Flow supports the implementation of custom control modules & algorithms in Python code.
Note that those controls can go beyond simple IF-THEN-ELSE controls as supported by EPANET --
i.e. arbitrary control logic can be implemented by the user, incl. AI-based controls where
for instance a neural network is utlized to make control decisions.

All controls must be derived from
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
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_control`
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
        sim.add_control(MyControl())

        # Run simulation
        # ....
