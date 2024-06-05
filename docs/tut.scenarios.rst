.. _tut.scenarios:

*********
Scenarios
*********

In EPyT-Flow, a *scenario* refers to a water distribution network (WDN) that is to be simulated -- 
i.e. performing a hydraulic and quality analysis.
Besides the network itself, a scenario usually contains a sensor configuration and 
might also contain some events such as leakages, sensor faults, actuator events, etc.
Furthermore, a scenario might also include some control modules.

Basics
++++++

There are two important classes for working with scenarios in EPyT-Flow.
The class :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig` for
describing the scenario, and the class
:class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`
for simulating the scenario.

For creating new instance of :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`,
either an `.inp file <http://wateranalytics.org/EPANET/_inp_file.html>`_
(together with an optional
`.msx file <https://raw.githubusercontent.com/USEPA/EPANETMSX/master/Doc/EPANETMSX.pdf>`_)
is needed, or an instance of  :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
describing and precisely specifying the scenario to be simulated.

.. note::
    When using the :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` class, 
    it is important to close it afterward so that EPANET is unloaded correctly.

Closing a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` 
instance can done automatically by using a ``with`` statement:

.. code-block:: python

    # Creates a new scenario based on the Hanoi network -- 
    # it will be closed automatically after the with block is left!
    with ScenarioSimulator(f_inp="Hanoi.inp") as sim:
        # Set any additional parameters and finalize the scenario configuration ....
        # Run simulation ...

Alternatively, you can close and unload everything manually by calling 
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.close`.
Beware of any potential exceptions that might occur during the process of setting up and running
the simulation.

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    sim = ScenarioSimulator(f_inp="Hanoi.inp")
        
    # Set any additional parameters and finalize the scenario configuration ....
    # Run simulation ...

    # Do not forget to close the scenario
    sim.close()

The simulation (i.e. hydraulics and quality analysis) itself is run by calling 
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.run_simulation`.
Alternatively, the simulation can also be run step-by-step by calling 
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.run_simulation_as_generator`.
In both cases, the result of the simulation is provided as a 
:class:`~epyt_flow.simulation.scada.scada_data.ScadaData` object.
In the latter case, the result is provided as a generator.

.. code-block:: python

    # Load Hanoi network
    with ScenarioSimulator(f_inp="Hanoi.inp") as sim:
        # Run simulation
        scada_data = sim.run_simulation()

More details on :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` are given
:ref:`here <tut.scada>`.


EPyT-Flow also supports the parallel simulation of scenarios. This becomes handy in cases where
many scenarios have to be simulated at once and multiple CPU cores are available.

.. note::

    EPANET (in contrast to EPANET-MSX) does not make use multiple CPU cores -- i.e.
    simualting the hydraulics of a single scenario will always use a single CPU core only.

For this, the function :func:`~epyt_flow.simulation.parallel_simulation.ParallelScenarioSimulation.run`
of the static class :class:`~epyt_flow.simulation.parallel_simulation.ParallelScenarioSimulation`
can be utilized.

.. code-block:: python

    # Load the first 10 LeakDB Net1 scenarios
    scenarios = load_leakdb_scenarios(range(10), use_net1=True)

    # Run simulations in parallel using as many CPU cores as possible
    # SCADA data of each scenario will be stored in "my_leakdb_results" folder
    ParallelScenarioSimulation.run(scenarios,
                                   callback=callback_save_to_file(folder_out="my_leakdb_results"))


Network Topology
++++++++++++++++

The topology (i.e. a graph) of the WDN is represented by a
:class:`~epyt_flow.topology.NetworkTopology` instance and can be obtained by calling
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.get_topology` of a
:class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance.

The topology :class:`~epyt_flow.topology.NetworkTopology` not only contains the WDN as a graph
but also includes node and link/pipe attributes such as elevation, diameter, length, etc.
Furthermore, :class:`~epyt_flow.topology.NetworkTopology` also comes with some helper functions
such as those for computing the adjacency matrix
(:func:`~epyt_flow.topology.NetworkTopology.get_adj_matrix`) or the shortest path between two nodes
(:func:`~epyt_flow.topology.NetworkTopology.get_shortest_path`).

Example of working with :class:`~epyt_flow.topology.NetworkTopology`:

.. code-block:: python

    # Create scenario based in Net1
    with ScenarioSimulator(scenario_config=load_net1()) as sim:
        # Get network topology
        topo = sim.get_topology()

        # Show all edges
        print(topo.edges)

        # Show all nodes
        print(topo.nodes)

        # Shortest path between node "2" and node "22"
        print(topo.get_shortest_path("2", "22"))

        # Adjacency matrix of the graph
        # A sparse matrix is returned, which we convert it to a dense matrix
        print(topo.get_adj_matrix().todense())


Low-level EPANET and EPANET-MSX Functions
+++++++++++++++++++++++++++++++++++++++++

Besides providing high-level functions for working with scenarios, EPyT-Flow also provides access
to lower-level functions as provided by EPyT, EPANET, and EPANET-MSX.
EPyT functions can be accessed through the attribute `epanet_api` of a
:class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance.
Note that EPyT also provides access to all EPANET and EPANET-MSX functions.

.. warning::

    Caution must be used when calling EPANET or EPANET-MSX functions as those might cause
    side-effects in EPyT-Flow.

    Whenever possible, EPyT-Flow functions should be used!

Example of manually setting the emitter coefficient of a node by calling an EPANET function:

.. code-block:: python

    # Create scenario based in Net1
    with ScenarioSimulator(scenario_config=load_net1()) as sim:
        # Calling an EPANET function for setting the emitter coefficient of the first node to zero
        sim.epanet_api.setNodeEmitterCoeff(1, 0.)

        # ....


Units of Measurements
+++++++++++++++++++++

The units if measurement are automatically derived from the .inp and .msx files.
However, it is also possible to change some of those before the simulation is run and all
measurement units can be changed afterwards by post-processing the SCADA data --
see :ref:`here <scada_change_units>` for more information.


Scenario Configurations
+++++++++++++++++++++++

An alternative to passing the path to an .inp file (and .msx file) to
:class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`, is to use a
:class:`~epyt_flow.simulation.scenario_config.ScenarioConfig` instance which completely
describes/specifies a scenario.

Because :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig` instances are immutable, 
there are usually not explicitly constructed by the user but loaded/parsed from a file 
(custom binary and JSON files are supported).

Example of loading a scenario from a JSON configuration file called `myScenarioConfig.json`:

.. code-block:: python

    # Load scenario configuration from JSON file
    scenario_config = None
    with open("myScenarioConfig.json", "r") as f:
        scenario_config = ScenarioConfig.load_from_json(f.read())

    # Create scenario based on scenario configuration
    with ScenarioSimulator(scenario_config=scenario_config) as sim:
        # Make some modifications to the scenario configuration ....
        # Run simulation ...

where `myScenarioConfig.json` contains a sensor placement (4 pressure and one flow sensor), 
two leakages (one abrupt and one incipient), one sensor fault, 
and uncertainties with respect to pipe length and roughness, as well as sensor noise:

.. code-block:: json

    {
        "general": {
            "file_inp": "Hanoi.inp",
            "simulation_duration": 100,
            "demand_model": {"type": "PDA", "pressure_min": 0, "pressure_required": 0.1,
                             "pressure_exponent": 0.5},
            "hydraulic_time_step": 1800,
            "reporting_time_step": 3600,
            "quality_time_step": 300
        },
        "uncertainties": {
            "pipe_length": {"type": "gaussian", "mean": 0, "scale": 1},
            "pipe_roughness": {"type": "uniform", "low": 0, "hight": 1},
            
            "sensor_noise": {"type": "gaussian", "mean": 0, "scale": 0.01}
        },
        "sensors": {
            "pressure_sensors": ["13", "16", "22", "30"],
            "flow_sensors": ["1"],
            "demand_sensors": [],
            "node_quality_sensors": [],
            "link_quality_sensors": []
        },
        "leakages": [
            {"type": "abrupt", "link_id": "12", "diameter": 0.1, 
                "start_time": 7200, "end_time": 100800},
            {"type": "incipient", "link_id": "10", "diameter": 0.01,
                "start_time": 7200, "end_time": 100800, "peak_time": 54000}
        ],
        "sensor_faults": [
            {"type": "constant", "constant_shift": 2.0, "sensor_id": "16",
                "sensor_type": 1, "start_time": 5000, "end_time": 100000}
        ]
    }

Note that the individual entries in the JSON file correspond to the classes as implemented
in EPyT-Flow.

At every time, a complete :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig` can be
obtained by calling
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.get_scenario_config`.
This scenario configuration could be then, for instance, stored in a file so that it can be
reloaded in the future  without having to make all the manual specifications again -- see
:ref:`Serialization <tut.serialization>` for details.

Example of obtaining and storing the current scenario configuration:

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    with ScenarioSimulator(f_inp="Hanoi.inp") as sim:
        # Make some modifications to the scenario configuration ....
        
        # Get final scenario configuration
        scenario_config_final = sim.get_scenario_config()

        # Store scenario configuration in a file
        scenario_config_final.save_to_file("myHanoiConfig.epytflow_config")

    # ....

    # Load scenario configuration
    scenario_config = ScenarioConfig.load("myHanoiConfig.epytflow_config")
    with ScenarioSimulator(scenario_config) as sim:
        # ....


Predefined networks
-------------------

EPyT-Flow comes with a set of popular benchmark water distribution networks already included.
These networks are, if necessary, downloaded and wrapped inside a
:class:`~epyt_flow.simulation.scenario_config.ScenarioConfig` instance, so that they can be
directly passed to :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`.

Also, note that in some cases (i.e. Hanoi and L-TOWN) a predefined sensor placement
can be included as well.

+------------+-------------------------------------------------+
| Network    | Function for loading                            |
+============+=================================================+
| Net1       | :func:`~epyt_flow.data.networks.load_net1`      |
+------------+-------------------------------------------------+
| Net2       | :func:`~epyt_flow.data.networks.load_net2`      |
+------------+-------------------------------------------------+
| Net3       | :func:`~epyt_flow.data.networks.load_net3`      |
+------------+-------------------------------------------------+
| Net6       | :func:`~epyt_flow.data.networks.load_net6`      |
+------------+-------------------------------------------------+
| Richmond   | :func:`~epyt_flow.data.networks.load_richmond`  |
+------------+-------------------------------------------------+
| MICROPOLIS | :func:`~epyt_flow.data.networks.load_micropolis`|
+------------+-------------------------------------------------+
| Balerma    | :func:`~epyt_flow.data.networks.load_balerma`   |
+------------+-------------------------------------------------+
| Rural      | :func:`~epyt_flow.data.networks.load_rural`     |
+------------+-------------------------------------------------+
| BSWN-1     | :func:`~epyt_flow.data.networks.load_bwsn1`     |
+------------+-------------------------------------------------+
| BWSN-2     | :func:`~epyt_flow.data.networks.load_bwsn2`     |
+------------+-------------------------------------------------+
| Anytown    | :func:`~epyt_flow.data.networks.load_anytown`   |
+------------+-------------------------------------------------+
| D-Town     | :func:`~epyt_flow.data.networks.load_dtown`     |
+------------+-------------------------------------------------+
| C-Town     | :func:`~epyt_flow.data.networks.load_ctown`     |
+------------+-------------------------------------------------+
| Kentucky   | :func:`~epyt_flow.data.networks.load_kentucky`  |
+------------+-------------------------------------------------+
| Hanoi      | :func:`~epyt_flow.data.networks.load_hanoi`     |
+------------+-------------------------------------------------+
| L-TOWN     | :func:`~epyt_flow.data.networks.load_ltown`     |
+------------+-------------------------------------------------+
| L-TOWN-A   | :func:`~epyt_flow.data.networks.load_ltown_a`   |
+------------+-------------------------------------------------+


Example of loading the Hanoi network:

.. code-block:: python

    network_config = load_hanoi()   # Load Hanoi network
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Set any additional parameters and finalize the scenario configuration ....
        # Run simulation ...


Benchmarks scenarios
--------------------

EPyT-Flow comes with a set of benchmark scenarios. Usually, those are pre-defined scenarios for 
different tasks such as leakage detection and localization.

+----------------+----------------------------------------------+
| Benchmark      | Module                                       |
+================+==============================================+
| LeakDB [1]_    | :mod:`~epyt_flow.data.benchmarks.leakdb`     |
+----------------+----------------------------------------------+
| BattLeDIM [2]_ | :mod:`~epyt_flow.data.benchmarks.battledim`  |
+----------------+----------------------------------------------+
| BATADAL [3]_   | :mod:`~epyt_flow.data.benchmarks.batadal`    |
+----------------+----------------------------------------------+


Benchmark data sets
+++++++++++++++++++

In addition to benchmark scenarios (see previous section), EPyT-Flow also includes
several (WDN related) benchmark data sets from the literature:

+--------------------------------+---------------------------------------------------------------------------------------------+
| Benchmark                      | Function for loading                                                                        |
+================================+=============================================================================================+
| GECCO Water Quality 2017 [4]_  | :func:`~epyt_flow.data.benchmarks.gecco_water_quality.load_gecco2017_water_quality_data`    |
+--------------------------------+---------------------------------------------------------------------------------------------+
| GECCO Water Quality 2018 [5]_  | :func:`~epyt_flow.data.benchmarks.gecco_water_quality.load_gecco2018_water_quality_data`    |
+--------------------------------+---------------------------------------------------------------------------------------------+
| GECCO Water Quality 2019 [6]_  | :func:`~epyt_flow.data.benchmarks.gecco_water_quality.load_gecco2019_water_quality_data`    |
+--------------------------------+---------------------------------------------------------------------------------------------+
| Water Usage [7]_               | :func:`~epyt_flow.data.benchmarks.water_usage.load_water_usage`                             |
+--------------------------------+---------------------------------------------------------------------------------------------+


.. [1] Vrachimis et al. (2018) -- see https://github.com/KIOS-Research/LeakDB/
.. [2] Vrachmimis et al. (2020) -- see https://github.com/KIOS-Research/BattLeDIM
.. [3] Taormina et al. (2017) -- see https://www.batadal.net/
.. [4] Friese et al. (2017) -- see http://www.spotseven.de/gecco-challenge/gecco-challenge-2017/
.. [5] Rehbach et al. (2018) -- see http://www.spotseven.de/gecco/gecco-challenge/gecco-challenge-2018/
.. [6] Rehbach et al. (2019) -- see https://www.th-koeln.de/informatik-und-ingenieurwissenschaften/gecco-challenge-2019_63244.php
.. [7] Pavlou et al. (2018) -- see https://github.com/KIOS-Research/Water-Usage-Dataset/
