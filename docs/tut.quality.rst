.. _tut.quality:

*******
Quality
*******

EPyT-Flow supports basic and advanced quality analysis -- the former is realized
through `EPANET <https://github.com/OpenWaterAnalytics/epanet>`_ and the latter one
through the usage of `EPANET-MSX <https://github.com/OpenWaterAnalytics/epanet-msx>`_.

Basic Quality Analysis
++++++++++++++++++++++

The basic quality analysis supports water age analysis, simple chemical analysis, 
and source tracing analysis.

.. note::
    Note that only one of these analysis be performed at a time -- i.e. multiple simulation runs 
    are necessary if different quality analysis are requested.

The requested quality analysis must be set (i.e. activated) before the simulation is run:

+-------------------+----------------------------------------------------------------------------------------------------+
| Quality Analysis  | Function for enabling the analysis                                                                 |
+===================+====================================================================================================+
| Water age         | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.enable_waterage_analysis`        |
+-------------------+----------------------------------------------------------------------------------------------------+
| Chemical          | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.enable_chemical_analysis`        |
+-------------------+----------------------------------------------------------------------------------------------------+
| Source tracing    | :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.enable_sourcetracing_analysis`   |
+-------------------+----------------------------------------------------------------------------------------------------+

In order to access the quality results, quality sensors must be placed at the links and 
nodes of interest.

Example for performing a water age analysis at all nodes:

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    network_config = load_hanoi()
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Enable water age analysis
        sim.enable_waterage_analysis()

        # Places quality sensors at all nodes -- i.e. measuring the water age at each node
        sim.set_node_quality_sensors(sensor_locations=sim.sensor_config.nodes)

        # Run simulation
        scada_data = sim.run_simulation()

        # Retrieve simulated water age at all nodes
        nodes_quality = scada_data.get_data_nodes_quality()


Chemical Analysis
-----------------

In the case of a chemical analysis, it is also necessary to set at least one source of chemicals 
if not already set in the .inp file. This can be done by calling 
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_quality_source` 
of the :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance.
Besides the location (i.e. node ID), the source pattern together with is type and (name, optional)
must be specified as well.
Note that the pattern repeats automatically when the simulation duration is exceeding the
pattern length.

.. code-block:: python

    # ...
    
    # Adds a source pattern called "my-pattern" at node "1".
    # The pattern alternates the chemical concentration leaving this node between 1. and 0.
    sim.add_quality_source(node_id="1", pattern_id="my-pattern",
                            pattern=numpy.array([1., 0.]),
                            source_type=ToolkitConstants.EN_SETPOINT)

Different types of source patterns are supported:

+--------------+------------------------------------------------------------+
| Source type  | Description                                                |
+==============+============================================================+
| EN_CONCEN    | Sets the concentration of external inflow entering a node  |
+--------------+------------------------------------------------------------+
| EN_MASS      | Injects a given mass/minute into a node                    |
+--------------+------------------------------------------------------------+
| EN_SETPOINT  | Sets the concentration leaving a node to a given value     |
+--------------+------------------------------------------------------------+
| EN_FLOWPACED | Adds a given value to the concentration leaving a node     |
+--------------+------------------------------------------------------------+


Furthermore, reaction options such as bulk and wall coefficients might be set as well by 
either setting the options in the .inp file or by calling the corresponding EPANET functions.

Example for running a chemical analysis where the concentration at the reservoir
is fixed over time.

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    network_config = load_hanoi()
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Enable chemical analysis
        sim.enable_chemical_analysis()

        # Sets the concentration at node "1" (reservoir) to 1.0 for all time steps -- 
        # this constant concentration pattern is named "my-constant-pattern"
        sim.add_quality_source(node_id="1", pattern_id="my-constant-pattern",
                                pattern=numpy.array([1.]),
                                source_type=ToolkitConstants.EN_CONCEN)

        # Places quality sensors at all nodes -- 
        # i.e. measuring the chemical concentration at all nodes
        sim.set_node_quality_sensors(sensor_locations=sim.sensor_config.nodes)

        # Run simulation
        scada_data = sim.run_simulation()

        # Retrieve simulated chemical concentrations at all nodes
        nodes_quality = scada_data.get_data_nodes_quality()


Advanced Quality Analysis
+++++++++++++++++++++++++

TODO