.. _tut.events:

******
Events
******

Leakages
++++++++

EPyT-Flow comes with two pre-defined leakage types: 
an abrupt leakage implemented in :class:`~epyt_flow.simulation.events.leakages.AbruptLeakage`, 
and an incipient leakage implemented in :class:`~epyt_flow.simulation.events.leakages.IncipientLeakage`.

Custom leakages can be implemented by deriving a sub-class from :class:`~epyt_flow.simulation.events.leakages.Leakage`.

The created leakage can be added to the scenario by calling 
:func:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator.add_leakage`  
of a :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator` instance.

In both cases, the ID of the link/pipe, the leak diameter (i.e. size of the leak), 
and start and end time in seconds (after simulation start) are needed.
In the case of an incipient leakage, the peak time (in seconds) is also needed -- 
the leak size is increasing linearly from the start time until it reaches its maximum 
at the peak time where it stays until the leakage is over.

.. note::
    What leak diameter refers to small or large leak depends mainly on the link/pipe diameter, 
    which might be different for different links/pipes and is also likely to differ between different water distribution networks.

Example for adding an abrupt and an incipient leakage:

.. code-block:: python

    # Load Hanoi network with a default sensor configuration
    network_config = load_hanoi(include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        # Place a large abrupt leakage at link/pipe "12"
        leak = AbruptLeakage(link_id="12", diameter=0.1, start_time=7200, end_time=100800)
        sim.add_leakage(leak)

        # Place a small incipient leakage at link/pipe "9"
        leak = IncipientLeakage(link_id="9", diameter=0.01,\
                                start_time=7200, end_time=100800, peak_time=54000)
        sim.add_leakage(leak)
        
        # Run simulation
        scada_data = sim.run_simulation()


Sensor Faults
+++++++++++++

EPyT-Flow comes with a set of pre-defined sensor faults:

+-------------------------------------------------------------------------------+--------------------------------------------------------+
| Implementation                                                                | Sensor fault description                               |
+===============================================================================+========================================================+
| :class:`~epyt_flow.simulation.events.sensor_faults.SensorFaultConstant`       | Adds a constant to the sensor reading.                 |
+-------------------------------------------------------------------------------+--------------------------------------------------------+
| :class:`~epyt_flow.simulation.events.sensor_faults.SensorFaultDrift`          | The sensor reading is linearly increasing over time.   |
+-------------------------------------------------------------------------------+--------------------------------------------------------+
| :class:`~epyt_flow.simulation.events.sensor_faults.SensorFaultGaussian`       | Adds Gaussian noise to the sensor reading.             |
+-------------------------------------------------------------------------------+--------------------------------------------------------+
| :class:`~epyt_flow.simulation.events.sensor_faults.SensorFaultPercentage`     | Adds a pecentage of the original sensor reading to it. |
+-------------------------------------------------------------------------------+--------------------------------------------------------+
| :class:`~epyt_flow.simulation.events.sensor_faults.SensorFaultStuckZero`      | Sets the sensor reading to zero.                       |
+-------------------------------------------------------------------------------+--------------------------------------------------------+

All sensor faults are derived from :class:`~epyt_flow.simulation.events.sensor_faults.SensorFault` and 
need a starting and end time, as well as the location (i.e. type and location of the sensor that is affected by the fault). 
Furthermore, most sensor faults also need a parameter describing the strength of the fault (e.g. variance of the Gaussian noise).

Sensor faults (i.e. instances of :class:`~epyt_flow.simulation.events.sensor_faults.SensorFault`) can be directly added to the simulation by 
calling :func:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator.add_sensor_fault`  
of a :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator` instance BEFORE running the simulation.

.. code-block:: python

    # Load Hanoi network with a default sensor configuration
    network_config = load_hanoi(include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        # Add a sensor fault that adds a constant to the original pressure reading at node "16"
        sim.add_sensor_fault(SensorFaultConstant(constant_shift=2.,
                                                sensor_id="16",
                                                sensor_type=SENSOR_TYPE_NODE_PRESSURE,
                                                start_time=5000, end_time=100000))
        
        # Run simulation
        scada_data = sim.run_simulation()

        # ...


Alternatively, sensor faults can also be added and changed AFTER the simulation by calling 
:func:`~epyt_flow.simulation.scada.scada_data.ScadaData.change_sensor_faults` 
of a given :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance:

.. code-block:: python

    # Load Hanoi network with a default sensor configuration
    network_config = load_hanoi(include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:        
        # Run simulation
        scada_data = sim.run_simulation()

        # Sets a single sensor fault: Gaussian noise to the pressure reading at node "16"
        sensor_fault = SensorFaultGaussian(std=1., sensor_id="16",
                                            sensor_type=SENSOR_TYPE_NODE_PRESSURE,
                                            start_time=5000, end_time=100000)
        scada_data.change_sensor_faults([sensor_fault])  # Overrides all existing sensor faults!
        
        # ...


Custom Events
+++++++++++++

Besides deriving sub-classes for leakages (see :class:`~epyt_flow.simulation.events.leakages.Leakage`) and 
sensor faults (see :class:`~epyt_flow.simulation.events.sensor_faults.SensorFault`), 
users can also implement completly custom events by either implementing a `system event` or a `sensor reading event`.


System events
-------------

TODO


Sensor reading events
---------------------

TODO