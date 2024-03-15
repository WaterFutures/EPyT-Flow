.. _tut.scada:

**********
SCADA Data
**********

Simulation results are stored in :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances.

Sensor Placements
+++++++++++++++++

A sensor placement is necessary for getting actual sensor readings from a 
:class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.
Such a sensor placement can be set before the simulation is run by calling 
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_sensors`
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance, 
or after when post-processing the results a :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances -- 
this becomes handy in cases where multiple sensor configurations have to be evaluated without 
having to re-run the simulation every time.

EPyT-Flow supports different types of sensors:

+---------------------------+--------------------------------------------------------------------------------+
| Identifier                | Description                                                                    |
+===========================+================================================================================+
| SENSOR_TYPE_NODE_PRESSURE | Pressure at a node.                                                            |
+---------------------------+--------------------------------------------------------------------------------+
| SENSOR_TYPE_NODE_QUALITY  | Water quality (e.g. chemical concentration, water age, etc.) at a node.        |
+---------------------------+--------------------------------------------------------------------------------+
| SENSOR_TYPE_NODE_DEMAND   | Demand (i.e. water consumption) at a node.                                     |
+---------------------------+--------------------------------------------------------------------------------+
| SENSOR_TYPE_LINK_FLOW     | Flow rate at a link/pipe.                                                      |
+---------------------------+--------------------------------------------------------------------------------+
| SENSOR_TYPE_LINK_QUALITY  | Water quality (e.g. chemical concentration, water age, etc.) at a link/pipe.   |
+---------------------------+--------------------------------------------------------------------------------+
| SENSOR_TYPE_VALVE_STATE   | State of a valve.                                                              |
+---------------------------+--------------------------------------------------------------------------------+
| SENSOR_TYPE_PUMP_STATE    | State of a pump.                                                               |
+---------------------------+--------------------------------------------------------------------------------+
| SENSOR_TYPE_TANK_LEVEL    | Water level in a tank.                                                         |
+---------------------------+--------------------------------------------------------------------------------+

Example for specifying a sensor placement BEFORE the simulation is run:

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    network_config = load_hanoi()
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Place pressure sensors at nodes "13", "16", "22", and "30"
        sim.set_sensors(SENSOR_TYPE_NODE_PRESSURE, sensor_locations=["13", "16", "22", "30"])

        # Place a flow sensor at link/pipe "1"
        sim.set_sensors(SENSOR_TYPE_LINK_FLOW, sensor_locations=["1"])

        # Run simulation
        # ....

Alternatively, one can use sensor type specific functions for specifying a sensor placement 
BEFORE the simulation is run:

+---------------------+--------------------------------------------------------------------------------------------------+
| Sensor type         | Function for specifying sensors                                                                  |
+=====================+==================================================================================================+
| Pressure            | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_pressure_sensors`          |
+---------------------+--------------------------------------------------------------------------------------------------+
| Flow                | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_flow_sensors`              |
+---------------------+--------------------------------------------------------------------------------------------------+
| Demand              | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_demand_sensors`            |
+---------------------+--------------------------------------------------------------------------------------------------+
| Link quality        | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_link_quality_sensors`      |
+---------------------+--------------------------------------------------------------------------------------------------+
| Node quality        | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_node_quality_sensors`      |
+---------------------+--------------------------------------------------------------------------------------------------+
| Valve state         | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_valve_sensors`             |
+---------------------+--------------------------------------------------------------------------------------------------+
| Pump state          | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_pump_sensors`              |
+---------------------+--------------------------------------------------------------------------------------------------+
| Tank water level    | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_tank_sensors`              |
+---------------------+--------------------------------------------------------------------------------------------------+

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    network_config = load_hanoi()
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Place pressure sensors at nodes "13", "16", "22", and "30"
        sim.set_pressure_sensors(sensor_locations=["13", "16", "22", "30"])

        # Place a flow sensor at link/pipe "1"
        sim.set_flow_sensors(sensor_locations=["1"])

        # Run simulation
        # ....


Example for specifying a sensor placement AFTER the simulation is run by calling 
:func:`~epyt_flow.simulation.scada.scada_data.ScadaData.change_sensor_config` 
of a :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance:

.. code-block:: python

    # Load scenario
    # ...

    # Run simulation
    scada_data = sim.run_simulation()

    # Set new sensor configuration
    sensor_config = scada_data.sensor_config    # Copy current sensor configuration

    sensor_config.pressure_sensors = ["13", "16", "22", "30"]   # Change/Set pressure sensors
    sensor_config.flow_sensors = ["1"]     # Change/Set flow sensors

    scada_data.change_sensor_config(cur_sensor_config)  # Set new sensor configuration


If a sensor placement have been specified, the final sensor readings of all sensor (as a `numpy.array`) 
can be obtained by calling :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data` 
of a given :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance:

.. code-block:: python

    # Load scenario
    # ...

    # Run simulation
    scada_data = sim.run_simulation()

    # Compute final sensor readings that are observed
    observed_sensor_readings = scada_data.get_data()


.. note::
    The function :func:`~epyt_flow.simulation.sensor_config.SensorConfig.get_index_of_reading` of 
    the sensor configuration can be used to get the index of a particular sensor in the final 
    sensor reading numpy array.

    Example for getting the pressure readings at node "5":

    .. code-block:: python

        # Load and run scenario simulation ...

        # Compute final sensor readings that are observed
        observed_sensor_readings = scada_data.get_data()

        # Access pressure readings at node "5"
        pressure_sensor_5_idx = scada_data.sensor_config.get_index_of_reading(
            pressure_sensor="5")
        pressures_at_node_5 = observed_sensor_readings[:, pressure_sensor_5_idx]


Alternatively, one can use sensor type specific function for retrieving the readings of all 
or some sensors of that type:

+-------------------+----------------------------------------------------------------------------------------------------------------------------+
| Sensor type       | Function for getting sensors readings                                                                                      |
+===================+============================================================================================================================+
| Pressure          | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_pressures`                                                |
+-------------------+----------------------------------------------------------------------------------------------------------------------------+
| Flow              | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_flows`                                                    |
+-------------------+----------------------------------------------------------------------------------------------------------------------------+
| Demand            | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_demands`                                                  |
+-------------------+----------------------------------------------------------------------------------------------------------------------------+
| Node quality      | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_nodes_quality`                                            |
+-------------------+----------------------------------------------------------------------------------------------------------------------------+
| Link quality      | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_links_quality`                                            |
+-------------------+----------------------------------------------------------------------------------------------------------------------------+
| Valve state       | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_valves_state`                                             |
+-------------------+----------------------------------------------------------------------------------------------------------------------------+
| Pump state        | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_pumps_state`                                              |
+-------------------+----------------------------------------------------------------------------------------------------------------------------+
| Tank water level  | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_tanks_water_level`                                        |
+-------------------+----------------------------------------------------------------------------------------------------------------------------+

Example for getting the pressure readings at node "5":

.. code-block:: python

    # Load scenario
    # ...

    # Run simulation
    scada_data = sim.run_simulation()

    # Access pressure readings at node "5"
    pressure_at_node_5 = scada_data.get_data_pressures(sensor_locations=["5"])


Importing and Exporting
+++++++++++++++++++++++

SCADA data can be exported and also imported if stored in a custom binary file -- 
see :ref:`Serialization <tut.serialization>` for details.

Example for exporting and important :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances:

.. code-block:: python

    # Load Hanoi network with a default sensor configuration
    network_config = load_hanoi(include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Run simulation
        scada_data = sim.run_simulation()

        # Store simulation results in a file
        scada_data.save_to_file("myHanoiResuls.epytflow_scada_data")

    # ...

    # Load SCADA results from file
    scada_data = ScadaData.load_from_file("myHanoiResuls.epytflow_scada_data")


.. note::

    Note that the use of the ".epytflow_scada_data" file extension is **mandatory** and will be
    appended automatically if not already present.


Export to other file formats
----------------------------

EPyT-Flow also supports the export of SCADA data to Numpy, .xlsx, MatLab files -- 
see :ref:`here <epyt_flow.simulation.scada.scada_data_export>`.

.. note::
    In these cases, the exported SCADA data CANNOT be imported again!

Example for exporting a :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance to numpy:

.. code-block:: python

    # Load Hanoi network with a default sensor configuration
    network_config = load_hanoi(include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Run simulation
        scada_data = sim.run_simulation()

        # Export results (i.e. SCADA for the current sensor configuration) to numpy
        ScadaDataNumpyExport(f_out="myHanoiResults.npz").export(scada_data)
