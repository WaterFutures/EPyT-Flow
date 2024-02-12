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

System events are events that directly affect the simulation (e.g. leakages, actuator events, etc.).
System events must be derived from :class:`~epyt_flow.simulation.events.system_event.SystemEvent` 
and must implement the :func:`~epyt_flow.simulation.events.system_event.SystemEvent.apply` method. 
This function is called in every simulation step to apply the event's logic by making use of 
the EPANET and EPANET-MSX interface.

.. note::
    Note that the function gets the current simulation time 
    passed as an argument and must respect the start and end time of the event 
    as stored in its parent class :class:`~epyt_flow.simulation.events.event.Event`.

Optionally, the :func:`~epyt_flow.simulation.events.system_event.SystemEvent.init` method can also 
be override for running some initialization logic -- make sure to call the parent's 
:func:`~epyt_flow.simulation.events.system_event.SystemEvent.init` first.

Example of a system event that activates a pump:

.. code-block:: python

    class MySystemEvent(SystemEvent):
        def __init__(self, **kwds):
            self.pump_link_idx = None

            super().__init__(**kwds)
        
        def init(self, epanet_api:epyt.epanet) -> None:
            super().init(epanet_api)

            # Custom init logic if needed ...
            pump_idx = self._epanet_api.getLinkPumpNameID().index("9")
            pump_link_idx = self._epanet_api.getLinkPumpIndex()[pump_idx]

        def apply(self, cur_time:int) -> None:
            # Activate pump "9" while this event is active
            if self.start_time <= cur_time < self.end_time:
                pump_status = 2
                self._epanet_api.setLinkStatus(self.pump_link_idx, pump_status)


System events can be added to a scenario by calling 
:func:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator.add_system_event`  
of a :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator` 
instance BEFORE running the simulation:

.. code-block:: python

    # Open/Create a new scenario based on the Net1 network
    config = load_net1()
    with WaterDistributionNetworkScenarioSimulator(scenario_config=config) as sim:
        # Setup scenario settings
        # ...

        # Add the system event implemented in the "MySystemEvent" class
        sim.add_system_event(MySystemEvent(start_time=5000, end_time=100000))

        # Run simulation
        # ....


Sensor reading events
---------------------

Sensor reading events are events that affect sensor readings only (e.g. sensor faults, 
communication events, etc.). Those events must be derived from 
:class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent` 
and must implement the :func:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent.apply` 
method. This method gets the raw sensor readings as well as the time steps as input, applies the event's logic to it, and 
returns the processed sensor readings.

.. note::
    Note that :func:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent.apply` 
    is called at each simulation time steps -- the method must respect the start and end time of the event 
    as stored in its parent class :class:`~epyt_flow.simulation.events.event.Event`.

Example of a custom sensor reading event that adds Gaussian noise to the sensor readings:

.. code-block:: python

    class MySensorReadingEvent(SensorReadingEvent):
        def __init__(**kwds):
            super().__init__(**kwds)    # Sets start & end time, location, etc.

        def apply(self, sensor_readings:numpy.ndarray,
                    sensor_readings_time:numpy.ndarray) -> numpy.ndarray:
            for i in range(sensor_readings.shape[0]):
                if self.start_time <= sensor_readings_time[i] < self.end_time:
                    sensor_readings[i] += numpy.random.normal(loc=0, scale=1)
            
            return sensor_readings

System events can be added to a scenario by calling 
:func:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator.add_sensor_reading_event`  
of a :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator` 
instance BEFORE running the simulation:

.. note::

    Be aware that multiple sensor reading events can be active for the same sensor -- 
    i.e. chaining of events is possible. In this case, the input to the 
    :func:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent.apply` is the 
    output of the previous method. The ordering of the sensor reading events is determined by 
    the order they were added to the scenario.
