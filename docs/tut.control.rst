.. _tut.control:

*******
Control
*******

EPyT-Flow supports the implementation of custom control modules & algorithms in Python code.

All controls must be derived from :class:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule` 
and implement the :func:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule.step` method. 
This functions implements the control logic and is called in every simulation steps. 
It gets the current sensor readings as an :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` 
instance as an argument and is supposed to apply the control logic.

.. note::
    Be aware that the obtained sensor readings from the 
    :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` 
    instance might be subject to sensor faults and noise.

Optionally, the :func:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule.init` method 
can be overriden for running some initialization logic -- make sure to call the parent's 
:func:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule.init` first.

Besides implementing the control strategy by means of EPANET and EPANET-MSX functions, 
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

Example of implementing a custom control module:

.. code-block:: python

    class MyControl(AdvancedControlModule):
        def __init__(self, **kwds):
            super().__init__(**kwds)
        
        def init(self, epanet_api:epyt.epanet) -> None:
            super().init(epanet_api)

            # Any custom initialization logic if needed ...
        
        def step(self, scada_data:ScadaData) -> None:
            # Simple rule for pump "9": Operate pump based on the water level in tank "2"
            sensor_idx = scada_data.sensor_config.get_index_of_reading(tank_level_sensor="2")
            if scada_data.get_data()[sensor_idx] <= 240000:
                self.set_pump_status("9", "3")  # Activate pump
            elif scada_data.get_data()[sensor_idx] >= 280000:
                self.set_pump_status("9", "2")  # Deactivate pump


Custom control modules & algorithms can be added to a scenario by calling 
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_control`  
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` 
instance BEFORE running the simulation:

.. code-block:: python

    # Open/Create a new scenario based on the Net1 network
    config = load_net1()
    with ScenarioSimulator(scenario_config=config) as sim:
        # Setup scenario settings
        # ...

        # Add custom control implemented in the "MyControl" class
        sim.add_control(MyControl())

        # Run simulation
        # ...
