.. _tut.quality:

*************
Water Quality
*************

EPyT-Flow supports :ref:`basic <basic_quality>` and :ref:`advanced <advanced_quality>` water quality analysis -- the former is realized
through `EPANET <https://github.com/USEPA/EPANET2.2>`__ and the latter one
through the usage of `EPANET-MSX <https://github.com/USEPA/EPANETMSX/>`__.


.. _basic_quality:

Basic Water Quality Analysis
++++++++++++++++++++++++++++

The basic water quality analysis supports water age analysis, simple chemical analysis, 
and source tracing analysis.

.. note::
    Note that only one of these analyses can be performed at a time -- i.e. multiple simulation runs 
    are necessary if different quality analyses are requested.
    
If the hydraulic analysis of the WDN has already been computed and stored as an .hyd file,
those can be utilized when running the quality analysis without having to re-compute the hydraulics.
The functions :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.run_basic_quality_simulation`
and :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.run_basic_quality_simulation_as_generator`
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance run the quality
analysis without re-computing the hydraulics.

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
Besides the location (i.e. node ID), the source pattern together with its type and (name, optional)
must be specified as well.
Note that the pattern repeats automatically when the simulation duration exceeds the
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


Furthermore, initial node concentrations, and reaction options such as bulk and wall coefficients
can be set as well by either setting the options in the .inp file or by calling
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_quality_parameters`.

Example of running a chemical analysis where the concentration at the reservoir
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


.. _advanced_quality:

Advanced Water Quality Analysis
+++++++++++++++++++++++++++++++

EPyT-Flow provides advanced water quality analysis through
`EPANET-MSX <https://github.com/OpenWaterAnalytics/epanet-msx>`_.

The central concept in advanced quality analysis is the concept of a *species*.
A species can be living matter such as bacteria or chemicals such as chlorine, arsenite, etc.
In EPANET-MSX, we distinguish between two types of species:
*bulk species*, which are species "living" in the water,
and *surface/wall species*, which are species "living" on link/pipe walls.
The interaction of different species is modeled by *reaction equations*.

More details about species and their reaction equations can be found in the
`EPANET-MSX user manual <https://cfpub.epa.gov/si/si_public_file_download.cfm?p_download_id=547058&Lab=CESER>`_.

The adavanced quality analysis requires an additional .msx file (`f_msx_in`) when creating a new
:class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance:

.. code-block:: python

    scenario = ScenarioSimulator(f_inp_in="net2-cl2.inp", f_msx_in="net2-cl2.msx") 

The .msx file contains the specifications of different species as well as their reaction dynamics.
By passing an .msx file to `f_msx_in`, EPANET-MSX is loaded and initialized automatically.

Specifying an injection of an existing species can be done by calling the function
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.add_species_injection_source`.
In addition, note that :ref:`injection events <msx_events>` are also implemented.

Specifying the initial concentration of bulk and surface species can be done by calling the functions 
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_bulk_species_node_initial_concentrations` and
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_species_link_initial_concentrations`

When running the simulation by calling
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.run_simulation`, first the
hydraulics for the entire duration are simulated, and then the quality dynamics
for the entire duration.

Similar to the case of :ref:`basic quality analysis <basic_quality>`, if the hydraulic analysis of
the WDN has already been computed and stored as an .hyd file, those can be utilized when running
the advanced quality analysis without having to re-compute the hydraulics. The functions
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.run_advanced_quality_simulation`
and :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.run_advanced_quality_simulation_as_generator`
of a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance run the advanced quality
analysis without re-computing the hydraulics.

.. note::

    EPANET and EPANET-MSX do NOT support the simultaneous step-wise simulation of
    hydraulics and advanced quality.


Similar to all other quantities, species sensors must be specified in order to
retrieve the concentrations of those species.

Example of a scenario where we want to monitor chlorine in Net2:

.. code-block:: python

    # Load EPANET-MSX scenario "net2-cl2" -- note that an .inp file as well
    # as an .msx file is required
    with ScenarioSimulator(f_inp_in="net2-cl2.inp", f_msx_in="net2-cl2.msx") as sim:
        # Set simulation duration to 5 days
        sim.set_general_parameters(simulation_duration=to_seconds(days=5))

        # Monitor bulk species "CL2" at every node
        sim.set_bulk_species_node_sensors(sensor_info={"CL2": sim.sensor_config.nodes})

        # Run entire simulation
        res = sim.run_simulation(verbose=True)

        # Show concentration of chlorine species at every node
        print(res.get_data_bulk_species_node_concentration())
