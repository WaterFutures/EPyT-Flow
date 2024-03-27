.. _tut.events:

******
Events
******

EPyT-Flow comes with a comprehensive set of pre-defined WDN events such as
:ref:`leakages <leakages>`, :ref:`actuator events <actuators>`,
:ref:`sensor faults <sensors_faults>`, and :ref:`sensor reading attacks <sensors_attacks>`.
It is also possible to define and implement :ref:`custom events <custom_events>` while
keeping the effort to do so to a minimum.


.. _leakages:

Leakages
++++++++

EPyT-Flow comes with two pre-defined leakage types: 
an abrupt leakage implemented in :class:`~epyt_flow.simulation.events.leakages.AbruptLeakage`, 
and an incipient leakage implemented in :class:`~epyt_flow.simulation.events.leakages.IncipientLeakage`.

Custom leakages can be implemented by deriving a sub-class from :class:`~epyt_flow.simulation.events.leakages.Leakage`.

The created leakage can be added to the scenario by calling 
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_leakage`  
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance.

In both cases, the ID of the link/pipe, the leak diameter (i.e. size of the leak), 
and start and end time in seconds (after simulation start) are needed.
In the case of an incipient leakage, the peak time (in seconds) is also needed -- 
the leak size is increasing linearly from the start time until it reaches its maximum 
at the peak time where it stays until the leakage is over.

.. note::
    Which leak diameter refers to small or large leak depends mainly on the link/pipe diameter, 
    which might be different for different links/pipes and is also likely to differ between
    different water distribution networks.

Example for adding an abrupt and an incipient leakage:

.. code-block:: python

    # Load Hanoi network with a default sensor configuration
    network_config = load_hanoi(include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Place a large abrupt leakage at link/pipe "12"
        leak = AbruptLeakage(link_id="12", diameter=0.1,
                             start_time=to_seconds(hours=2),
                             end_time=to_seconds(hours=28))
        sim.add_leakage(leak)

        # Place a small incipient leakage at link/pipe "9"
        leak = IncipientLeakage(link_id="9", diameter=0.01,
                                start_time=to_seconds(hours=2),
                                end_time=to_seconds(hours=28),
                                peak_time=to_seconds(hours=15))
        sim.add_leakage(leak)
        
        # Run simulation
        scada_data = sim.run_simulation()


.. _actuators:

Actuator Events
+++++++++++++++

EPyT-Flow comes with implementations of many different actuator events -- i.e. events that affect
actuators such as pumps and valves:

+-------------------------------------------------------------------------+--------------------------+
| Implementation                                                          | Description              |
+=========================================================================+==========================+
| :class:`~epyt_flow.simulation.events.actuator_events.PumpStateEvent`    | Starts or stops a pump.  |
+-------------------------------------------------------------------------+--------------------------+
| :class:`~epyt_flow.simulation.events.actuator_events.PumpSpeedEvent`    | Changes the pump speed.  |
+-------------------------------------------------------------------------+--------------------------+
| :class:`~epyt_flow.simulation.events.actuator_events.ValveStateEvent`   | Opens or closes a valve. |
+-------------------------------------------------------------------------+--------------------------+

.. note::

    Note that actuator events are one-time events -- i.e. they are executed only
    once at a given point in time.

Such actuator events can be added to the scenario simulation by calling
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_actuator_event`  
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance.

Example of manually deactivating and re-activating a pump:

.. code-block:: python

    # Create new scenario based on Net1
    with ScenarioSimulator(scenario_config=load_net1()) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Remove existing control rules
        # ...

        # Deactivate pump "9" at 14h after simulation start
        sim.add_actuator_event(PumpStateEvent(pump_id="9",
                                              pump_state=ActuatorConstants.EN_CLOSED,
                                              time=to_seconds(hours=14)))

        # Re-activate pump "9" at 45h after simulation start
        sim.add_actuator_event(PumpStateEvent(pump_id="9",
                                              pump_state=ActuatorConstants.EN_OPEN,
                                              time=to_seconds(hours=45)))
        
        # Run simulation
        # ...


.. _sensors_faults:

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
calling :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_sensor_fault`  
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance BEFORE running the simulation.

.. code-block:: python

    # Load Hanoi network with a default sensor configuration
    network_config = load_hanoi(include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Add a sensor fault that adds a constant to the original pressure reading
        # at node "16"
        sim.add_sensor_fault(SensorFaultConstant(constant_shift=2.,
                                                sensor_id="16",
                                                sensor_type=SENSOR_TYPE_NODE_PRESSURE,
                                                start_time=to_seconds(minutes=80),
                                                end_time=to_seconds(minutes=180)))
        
        # Run simulation
        scada_data = sim.run_simulation()

        # ...


Alternatively, sensor faults can also be added and changed AFTER the simulation by calling 
:func:`~epyt_flow.simulation.scada.scada_data.ScadaData.change_sensor_faults` 
of a given :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance:

.. code-block:: python

    # Load Hanoi network with a default sensor configuration
    network_config = load_hanoi(include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=network_config) as sim:        
        # Run simulation
        scada_data = sim.run_simulation()

        # Sets a single sensor fault: Gaussian noise to the pressure reading at node "16"
        # Note that this overrides all existing sensor faults!
        sensor_fault = SensorFaultGaussian(std=1., sensor_id="16",
                                           sensor_type=SENSOR_TYPE_NODE_PRESSURE,
                                           start_time=to_seconds(minutes=80),
                                           end_time=to_seconds(minutes=180))
        scada_data.change_sensor_faults([sensor_fault])
        
        # ...


.. _sensors_attacks:

Sensor Reading Attacks
++++++++++++++++++++++

To support the simulation of cyber-(physical) attacks on water distribution networks, 
EPyT-Flow comes with a set of pre-defined sensor reading attacks:

+---------------------------------------------------------------------------------+--------------------------------------------------------------+
| Implementation                                                                  | Attack description                                           |
+=================================================================================+==============================================================+
| :class:`~epyt_flow.simulation.events.sensor_reading_attack.SensorReplayAttack`  | Sensor readings are replaced by historical readings.         |
+---------------------------------------------------------------------------------+--------------------------------------------------------------+
| :class:`~epyt_flow.simulation.events.sensor_reading_attack.SensorOverrideAttack`| Sensor readings are overriden with some pre-defined values.  |
+---------------------------------------------------------------------------------+--------------------------------------------------------------+

Sensor reading attack can be added BEFORE running the simulation by calling 
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_sensor_reading_attack`
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance, 
or AFTERWARDS by calling :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.change_sensor_reading_attacks`  
of a :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.

Example of a sensor replay attack on a pressure sensor:

.. code-block:: python

    # Load the first LeakDB Hanoi scenario
    config = load_leakdb(scenarios_id=["1"], use_net1=False)[0]
    with ScenarioSimulator(scenario_config=config) as sim:
        # Set simulaton duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Add a sensor replay attack -- pressure readings at node "13" between 5hrs and 7hrs
        # after simulation start (time steps 10 - 15) are replaced by the historical readings
        # collected from the first 150min (i.e. first 5 time steps)
        sensor_replay_attack = SensorReplayAttack(replay_data_time_window_start=0,
                                                  replay_data_time_window_end=to_seconds(
                                                    minutes=150),
                                                  start_time=to_seconds(hours=5),
                                                  end_time=to_seconds(hours=7),
                                                  sensor_id="13",
                                                  sensor_type=SENSOR_TYPE_NODE_PRESSURE)
        sim.add_sensor_reading_event(sensor_replay_attack)

        # Run simulation and and retrieve pressure readings
        res = sim.run_simulation()

        pressure_readings = res.get_data_pressures(sensor_locations=["13"])
        print(pressure_readings)


Example of a sensor override attack on a flow sensor -- the flow readings are set to 42:

.. code-block:: python

    # Load the first LeakDB Hanoi scenario
    config = load_leakdb(scenarios_id=["1"], use_net1=False)[0]
    with ScenarioSimulator(scenario_config=config) as sim:
        # Set simulaton duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Override the sensor readings of the flow sensor at link "1" with the value "42" for
        # 2hrs -- i.e. time steps 10 - 15.
        new_sensor_values = np.array([42]*5)
        sim.add_sensor_reading_event(SensorOverrideAttack(new_sensor_values,
                                                          start_time=to_seconds(hours=5),
                                                          end_time=to_seconds(hours=7),
                                                          sensor_id="1",
                                                          sensor_type=SENSOR_TYPE_LINK_FLOW))

        # Run simulation and and retrieve flow readings
        res = sim.run_simulation()

        flow_readings = res.get_data_flows(sensor_locations=["1"])
        print(flow_readings)


.. _custom_events:

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
This function is called at every simulation step, when the event is active, and is supposed to
apply the event's logic by making use of the EPANET and EPANET-MSX interface.

Optionally, the :func:`~epyt_flow.simulation.events.system_event.SystemEvent.init` method can also 
be override for running some initialization logic -- make sure to call the parent's 
:func:`~epyt_flow.simulation.events.system_event.SystemEvent.init` first.
Also, if some "clean-up" logic is needed (i.e. some code that must run after the end of the event),
the method :func:`~epyt_flow.simulation.events.system_event.SystemEvent.exit` can be overriden --
this method is called ONCE after the end of the event.
In order to support multiple simulation runs of the same scenario, the method
:func:`~epyt_flow.simulation.events.system_event.SystemEvent.reset` can be overriden to reset the
event (e.g. resetting time index of a leak profile).

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
            pump_status = 2
            self._epanet_api.setLinkStatus(self.pump_link_idx, pump_status)


System events can be added to a scenario by calling 
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_system_event`  
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` 
instance BEFORE running the simulation:

.. code-block:: python

    # Open/Create a new scenario based on the Net1 network
    config = load_net1()
    with ScenarioSimulator(scenario_config=config) as sim:
        # Setup scenario settings
        # ...

        # Add the system event implemented in the "MySystemEvent" class
        sim.add_system_event(MySystemEvent(start_time=to_seconds(hours=5),
                                           end_time=to_seconds(hours=7)))

        # Run simulation
        # ....


Sensor reading events
---------------------

Sensor reading events are events that affect sensor readings only (e.g. sensor faults, 
sensor reading attacks, etc.). Those events must be derived from 
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
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_sensor_reading_event`  
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` 
instance BEFORE running the simulation:

.. note::

    Be aware that multiple sensor reading events can be active for the same sensor -- 
    i.e. chaining of events is possible. In this case, the input to the 
    :func:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent.apply` is the 
    output of the previous method. The ordering of the sensor reading events is determined by 
    the order they were added to the scenario.
