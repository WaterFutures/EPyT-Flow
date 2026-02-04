.. _tut.scada:

**********
SCADA Data
**********

Simulation results are stored in :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances.

The topology of the simulated water distribution network can be accessed by the property
:func:`~epyt_flow.simulation.scada.scada_data.ScadaData.network_topo` of a given
:class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.
In addition to that, the function 
:func:`~epyt_flow.simulation.scada.scada_data.ScadaData.topo_adj_matrix` returns the
the adjacency matrix, and the function
:func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_topo_edge_indices` returns the
topology as edge indices.


Sensor Placements
+++++++++++++++++

A sensor placement is necessary for getting actual sensor readings from a 
:class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.
Such a sensor placement can be set before the simulation is run by calling 
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_sensors`
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance, 
or after when post-processing the results a
:class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances --  this becomes handy in cases
where multiple sensor configurations have to be evaluated without  having to re-run the
simulation every time.

.. note::

    The default, when loading an .inp file and specifying anything else, is an empty sensor config
    -- i.e. no sensors anywhere. However, note that some networks and scenarios included in
    EPyT-Flow do come with a default sensor placement -- please refer to the documentation for
    the specific network/scenario.

EPyT-Flow supports different types of sensors:

+------------------------------------+------------------------------------------------------------------------------+
| Identifier                         | Description                                                                  |
+====================================+==============================================================================+
| SENSOR_TYPE_NODE_PRESSURE          | Pressure at a node.                                                          |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_NODE_QUALITY           | Water quality (e.g. chemical concentration, water age, etc.) at a node.      |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_NODE_DEMAND            | Demand (i.e. water consumption) at a node.                                   |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_LINK_FLOW              | Flow rate at a link/pipe.                                                    |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_LINK_QUALITY           | Water quality (e.g. chemical concentration, water age, etc.) at a link/pipe. |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_VALVE_STATE            | State of a valve.                                                            |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_PUMP_STATE             | State of a pump.                                                             |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_PUMP_EFFICIENCY        | Efficiency of a pump.                                                        |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_PUMP_ENERGYCONSUMPTION | Energy consumption of a pump.                                                |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_TANK_VOLUME            | Water volume in a tank.                                                      |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_NODE_BULK_SPECIES      | Bulk species concentrations at a node.                                       |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_LINK_BULK_SPECIES      | Bulk species concentrations at a link/pipe.                                  |
+------------------------------------+------------------------------------------------------------------------------+
| SENSOR_TYPE_SURFACE_SPECIES        | Surface species concentrations at a link/pipe.                               |
+------------------------------------+------------------------------------------------------------------------------+

Before the simulation run
-------------------------

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

Alternatively, one can use sensor type-specific functions to specify a sensor placement 
BEFORE the simulation is run:

+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Sensor type                      | Function for specifying sensors                                                                        |
+==================================+========================================================================================================+
| Pressure                         | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_pressure_sensors`                |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Flow                             | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_flow_sensors`                    |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Demand                           | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_demand_sensors`                  |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Link quality                     | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_link_quality_sensors`            |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Node quality                     | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_node_quality_sensors`            |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Valve state                      | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_valve_sensors`                   |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Pump state                       | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_pump_state_sensors`              |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Pump efficiency                  | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_pump_efficiency_sensors`         |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Pump energy consumption          | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_pump_energyconsumption_sensors`  |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Tank water volume                | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_tank_sensors`                    |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Bulk species node concentrations | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_bulk_species_node_sensors`       |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Bulk species link concentrations | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_bulk_species_link_sensors`       |
+----------------------------------+--------------------------------------------------------------------------------------------------------+
| Surface species concentrations   | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_surface_species_sensors`         |
+----------------------------------+--------------------------------------------------------------------------------------------------------+

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


Besides specifying sensors manually, it is also possible to easily place sensors everywhere --
e.g. placing a pressure sensors at all nodes in the network.
This can be done by calling the following functions before BEFORE the simulation is run:

+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Sensor type                      | Function for specifying sensors                                                                                    |
+==================================+====================================================================================================================+
| Pressure                         | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_pressure_sensors_everywhere`               |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Flow                             | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_flow_sensors_everywhere`                   |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Demand                           | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_demand_sensors_everywhere`                 |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Link quality                     | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_link_quality_sensors_everywhere`           |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Node quality                     | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_node_quality_sensors_everywhere`           |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Valve state                      | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_valve_sensors_everywhere`                  |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Pump state                       | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_pump_state_sensors_everywhere`             |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Pump efficiency                  | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_pump_efficiency_sensors_everywhere`        |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Pump energy consumption          | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_pump_energyconsumption_sensors_everywhere` |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| All pump quantities              | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_pump_sensors_everywhere`                   |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Tank water volume                | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_tank_sensors_everywhere`                   |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Bulk species node concentrations | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_bulk_species_node_sensors_everywhere`      |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Bulk species link concentrations | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_bulk_species_link_sensors_everywhere`      |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| Surface species concentrations   | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_surface_species_sensors_everywhere`        |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+
| All quantities                   | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.place_sensors_everywhere`                        |
+----------------------------------+--------------------------------------------------------------------------------------------------------------------+


After the simulation run
------------------------

Besides specifying a sensor placement before the simulation is run, it is also possible to change
the sensor configuration of a :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances
if the simulation was run with `frozen_sensor_config=False` (default).

Example of specifying a sensor placement AFTER the simulation is run by calling 
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


Accessing Sensor Readings
+++++++++++++++++++++++++

If a sensor placement has been specified, the final sensor readings of all sensors (as a `numpy.array`) 
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


Alternatively, one can use sensor type-specific function for retrieving the readings of all 
or some sensors of that type - note that the ordering of the columns (i.e. sensors) in the
returned array depends on the ordering of the specified sensors:

+---------------------------------+---------------------------------------------------------------------------------------------------+
| Sensor type                     | Function for getting sensor readings                                                              |
+=================================+===================================================================================================+
| Pressure                        | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_pressures`                       |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Flow                            | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_flows`                           |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Demand                          | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_demands`                         |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Node quality                    | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_nodes_quality`                   |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Link quality                    | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_links_quality`                   |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Valve state                     | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_valves_state`                    |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Pump state                      | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_pumps_state`                     |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Pump efficiency                 | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_pumps_efficiency`                |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Pump energy consumption         | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_pumps_energyconsumption`         |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Tank water volume               | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_tanks_water_volume`              |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Bulk species node concentration | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_bulk_species_node_concentration` |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Bulk species link concentration | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_bulk_species_link_concentration` |
+---------------------------------+---------------------------------------------------------------------------------------------------+
| Surface species concentration   | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_surface_species_concentration`   |
+---------------------------------+---------------------------------------------------------------------------------------------------+

Example for getting the pressure readings at node "5":

.. code-block:: python

    # Load scenario
    # ...

    # Run simulation
    scada_data = sim.run_simulation()

    # Access pressure readings at node "5"
    pressure_at_node_5 = scada_data.get_data_pressures(sensor_locations=["5"])


Connecting sensor readings to the topology of the network
---------------------------------------------------------

Sensor readings can also be directly connected to the topology of the network,
which for instance is useful when working with Graph Neural Networks (GNNs) -- also refer
to :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_topo_edge_indices` for getting
the topology of the network as edge indices (compatible with
`PyTorch Geometric <https://github.com/pyg-team/pytorch_geometric>`_).

For this purpose, :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances have
dedicated functions for returning the sensor readings in topology consistent feature matrices
and masks indicating the presence of a sensor:

+---------------------------------+-------------------------------------------------------------------------------------------------------------------+
| Sensor type                     | Function for getting a topology consistent feature matrix                                                         |
+=================================+===================================================================================================================+
| Pressure                        | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_pressures_as_node_features`                      |
+---------------------------------+-------------------------------------------------------------------------------------------------------------------+
| Flow                            | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_flows_as_edge_features`                          |
+---------------------------------+-------------------------------------------------------------------------------------------------------------------+
| Node quality                    | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_nodes_quality_as_node_features`                  |
+---------------------------------+-------------------------------------------------------------------------------------------------------------------+
| Link quality                    | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_links_quality_as_edge_features`                  |
+---------------------------------+-------------------------------------------------------------------------------------------------------------------+
| Surface species concentration   | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_surface_species_concentrations_as_edge_features` |
+---------------------------------+-------------------------------------------------------------------------------------------------------------------+
| Bulk species node concentration | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_bulk_species_concentrations_as_node_features`    |
+---------------------------------+-------------------------------------------------------------------------------------------------------------------+
| Bulk species link concentration | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_bulk_species_concentrations_as_edge_features`    |
+---------------------------------+-------------------------------------------------------------------------------------------------------------------+

For convience, :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances also have
functions for retrieving all node features 
:func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_node_features`,
and all edges features
:func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data_edge_features`.


Plotting of sensor readings
---------------------------

Similar to the functions for retrieving the final sensor reading, there also exist
dedicated functions for plotting the final sensor readings:

+---------------------------------+-----------------------------------------------------------------------------------------------+
| Sensor type                     | Plot function                                                                                 |
+=================================+===============================================================================================+
| Pressure                        | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_pressures`                       |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Flow                            | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_flows`                           |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Demand                          | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_demands`                         |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Node quality                    | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_nodes_quality`                   |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Link quality                    | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_links_quality`                   |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Valve state                     | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_valves_state`                    |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Pump state                      | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_pumps_state`                     |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Pump efficiency                 | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_pumps_efficiency`                |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Pump energy consumption         | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_pumps_energyconsumption`         |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Tank water volume               | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_tanks_water_volume`              |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Bulk species node concentration | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_bulk_species_node_concentration` |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Bulk species link concentration | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_bulk_species_link_concentration` |
+---------------------------------+-----------------------------------------------------------------------------------------------+
| Surface species concentration   | :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.plot_surface_species_concentration`   |
+---------------------------------+-----------------------------------------------------------------------------------------------+

For more advanced plotting, the function :func:`~epyt_flow.utils.plot_timeseries_data` might be used.


.. _scada_change_units:

Units of Measurement
++++++++++++++++++++

The units of measurements are stored in the sensor configuration:

+----------------------------+--------------------------------------------------------------------------------------+
| Units of Measurements      | Attribute in the sensor configuration                                                |
+============================+======================================================================================+
| Hydraulics units           | :func:`~epyt_flow.simulation.sensor_config.SensorConfig.flow_unit`                   |
+----------------------------+--------------------------------------------------------------------------------------+
| Water quality unit         | :func:`~epyt_flow.simulation.sensor_config.SensorConfig.quality_unit`                |
+----------------------------+--------------------------------------------------------------------------------------+
| Bulk species mass unit     | :func:`~epyt_flow.simulation.sensor_config.SensorConfig.bulk_species_mass_unit`      |
+----------------------------+--------------------------------------------------------------------------------------+
| Surface species mass unit  | :func:`~epyt_flow.simulation.sensor_config.SensorConfig.surface_species_mass_unit`   |
+----------------------------+--------------------------------------------------------------------------------------+
| Surface species area unit  | :func:`~epyt_flow.simulation.sensor_config.SensorConfig.surface_species_area_unit`   |
+----------------------------+--------------------------------------------------------------------------------------+

For a full list of supported measurement units and how they releate to each other
can be found in the
`EPANET documentation <http://wateranalytics.org/EPANET/_units.html>`_.

The units can be changed (i.e. measurements are converted) by calling the function
:func:`~epyt_flow.simulation.scada.scada_data.ScadaData.convert_units` of a
:class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
instances.

Example of getting and changing the measurement units:

.. code-block:: python

    # Running a simulation of loading a ScadaData instance
    # ...

    # Show current hydraulic (i.e. flow) unit in a human-readable format
    print(flowunit_to_str(scada_data.sensor_config.flow_unit))

    # Change flow units to gal/min -- note that this changes the hydraulic units to US CUSTOM
    scada_data_new = scada_data.convert_units(EpanetConstants.EN_GPM)
    print(flowunit_to_str(scada_data_new.sensor_config.flow_unit))


.. _scada_import_export:

Importing and Exporting
+++++++++++++++++++++++

SCADA data can be exported and also imported if stored in a custom binary file -- 
see :ref:`Serialization <tut.serialization>` for details.

Example for exporting and important :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
instances:

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

Example for exporting a :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
instance to numpy:

.. code-block:: python

    # Load Hanoi network with a default sensor configuration
    network_config = load_hanoi(include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Run simulation
        scada_data = sim.run_simulation()

        # Export results (i.e. SCADA for the current sensor configuration) to numpy
        ScadaDataNumpyExport(f_out="myHanoiResults.npz").export(scada_data)


Importing external data
-----------------------

Some use cases might require loading external (real-world) SCADA data into EPyT-Flow for further
analysis/processing such as calibration and state estimation tasks where the user wants to use
information from both the hydraulic simulation results and sparse SCADA data to
correct parameters (like pipe roughnesses) or estimate real-time system-wide pressures and flows.

External SCADA data can be loaded into EPyT-Flow by manually creating a
:class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.

A hypothetical example of how to simulate a given .inp file and
loading external (real-world) sensor readings into EPyT-Flow:

.. code-block:: python

    # Load C-Town network
    with ScenarioSimulator(scenario_config=load_ctown()) as sim:
        # Place a pressure sensor at the tank "T1"
        sim.set_pressure_sensors(sensor_locations=["T1"])
        my_sensor_config = sim.sensor_config

        # Run simulation
        scada_data = sim.run_simulation()

        # Import external sensor measurements for the pressure at "T1" into a ScadaData instance
        my_measurement_time_points = np.arange(0, 3600*24, 3600)
        real_world_pressure_data = np.array([3, 2.82, 2.7, 2.62, 2.7, 2.89, 3.14, 3.26,
                                             3.4, 3.66, 3.73, 3.66, 3.73, 3.88, 4.07,
                                             4.23, 4.41, 4.44, 4.03, 4.03, 4.03, 4.03,
                                             4.03, 4.03])

        # We only have pressure data at the tank --
        # everything else is set to zero and will be ignored by ScadaData
        pressure_measurements = np.zeros((len(my_measurement_time_points),
                                          len(my_sensor_config.nodes)))
        tank_data_idx = my_sensor_config.map_node_id_to_idx("T1")
        pressure_measurements[:, tank_data_idx] = real_world_pressure_data

        # IMPORTANT: frozen_sensor_config=True because we only provide data for some specific sensors!
        my_scada_data = ScadaData(sensor_config=my_sensor_config,
                                  frozen_sensor_config=True,
                                  sensor_readings_time=my_measurement_time_points,
                                  pressure_data_raw=pressure_measurements)

        # Show/Analyze external sensor data in EPyT-Flow
        print(my_scada_data.get_data_pressures())

        # ....