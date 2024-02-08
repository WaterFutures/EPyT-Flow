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
:func:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator.set_sensors`
of a :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator` instance, 
or after when post-processing the results a :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances -- 
this becomes handy in cases where multiple sensor configurations have to be evaluated without 
having to re-run the simulation every time.

Example for specifying a sensor placement BEFORE the simulation is run:

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    network_config = load_hanoi()
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        # Place pressure sensors at nodes "13", "16", "22", and "30"
        sim.set_sensors(SENSOR_TYPE_NODE_PRESSURE, sensor_locations=["13", "16", "22", "30"])

        # Place a flow sensor at link/pipe "1"
        sim.set_sensors(SENSOR_TYPE_LINK_FLOW, sensor_locations=["1"])

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


If a sensor placement have been specified, the final sensor readings (as a `numpy.array`) 
can be obtained by calling :func:`~epyt_flow.simulation.scada.scada_data.ScadaData.get_data` 
of a given :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance:

.. code-block:: python

    # Load scenario
    # ...

    # Run simulation
    scada_data = sim.run_simulation()

    # Compute final sensor readings that are observed
    observed_sensor_readings = scada_data.get_data()


Importing and Exporting
+++++++++++++++++++++++

SCADA data can be exported and also imported if stored in a custom binary file -- 
see :ref:`Serialization <tut.serialization>` for details.

Example for exporting and important :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances:

.. code-block:: python

    # Load Hanoi network with a default sensor configuration
    network_config = load_hanoi(include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        # Run simulation
        scada_data = sim.run_simulation()

        # Store simulation results in a file
        scada_data.save_to_file("myHanoiResuls.epytflow_scada")

    # ...

    # Load SCADA results from file
    scada_data = ScadaData.load_from_file("myHanoiResuls.epytflow_scada")


EPyT-Flow also supports the export of SCADA data to Numpy, .xlsx, MatLab files -- 
see :ref:`here <epyt_flow.simulation.scada.scada_data_export>`.

.. note::
    In these cases, the exported SCADA data CANNOT be imported again!

Example for exporting a :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance to numpy:

.. code-block:: python

    # Load Hanoi network with a default sensor configuration
    network_config = load_hanoi(include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        # Run simulation
        scada_data = sim.run_simulation()

        # Export results (i.e. SCADA for the current sensor configuration) to numpy
        ScadaDataNumpyExport(f_out="myHanoiResults.npz").export(scada_data)
