.. _tut.scenarios:

*********
Scenarios
*********

Basics
++++++

There are two important classes for working with scenarios in EPyT-Flow.
The class :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig` for
describing the scenario, and the class
:class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`
for simulating the scenario.

For creating new instance of :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`
either an .inp file (together with an optional .msx file) are needed, or an instance of 
:class:`~epyt_flow.simulation.scenario_config.ScenarioConfig` describing and precisely specifying the scenario to be simulated.

.. note::
    When using the :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator` class, 
    it is important to close it so that EPANET is unloaded correctly.

Closing a :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator` 
instance can done in automatically by using a ``with`` statement:

.. code-block:: python

    # Creates a new scenario based on the Hanoi network -- 
    # it will be closed automatically after the with block is left!
    with WaterDistributionNetworkScenarioSimulator(f_inp="Hanoi.inp") as sim:
        # Set any additional parameters and finalize the scenario configuration ....
        # Run simulation ...

Alternatively, you can close and unload everything manually by calling 
:func:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator.close`.
Beware of any potential exceptions that might occur during the process of setting up and running
the simulation.

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    sim = WaterDistributionNetworkScenarioSimulator(f_inp="Hanoi.inp")
        
    # Set any additional parameters and finalize the scenario configuration ....
    # Run simulation ...

    # Do not forget to close the scenario
    sim.close()

The simulation (i.e. hydraulics and quality analysis) itself is run by calling 
:func:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator.run_simulation`.
Alternatively, the simulation can also be run step-by-step by calling 
:func:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator.run_simulation_as_generator`.
In both cases, the result of the simulation is provided as a 
:class:`~epyt_flow.simulation.scada.scada_data.ScadaData` object.
In the latter case, the result is provided as a generator.

.. code-block:: python

    # Load Hanoi network
    with WaterDistributionNetworkScenarioSimulator(f_inp="Hanoi.inp") as sim:
        # Run simulation
        scada_data = sim.run_simulation()

More details on :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` are given :ref:`here <tut.scada>`.

Scenario Configurations
+++++++++++++++++++++++

An alternative to passing the path to an .inp file (and .msx file) to :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`, 
is to use a :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig` instance which completly describes/specifies a scenario.

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
    with WaterDistributionNetworkScenarioSimulator(scenario_config=scenario_config) as sim:
        # Make some modifications to the scenario configuration ....
        # Run simulation ...

where `myScenarioConfig.json` contains a sensor placement (4 pressure and one flow sensor), 
two leakages (one abrupt and one incipient), one sensor fault, 
and uncertanties with respect to pipe length and roughtness, as well as sensor noise:

.. code-block:: json

    {
        "general": {
            "file_inp": "Hanoi.inp",
            "file_msx": "",
            "simulation_duration": 100,
            "demand_model": "pdd",
            "hydraulic_time_step": 1800,
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

Note that the individual entries in the JSON file correspond to the classes at implemented in EPyT-Flow.

At every time, a complete :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig` can be obtained by calling 
:func:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator.get_scenario_config`.
This scenario configuration could be than, for instance, be stored in a file so that it can be reloaded in the future 
without having to make all the manual specifications again.

Example of obtaining and storing the current scenario configuration:

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    with WaterDistributionNetworkScenarioSimulator(f_inp="Hanoi.inp") as sim:
        # Make some modifications to the scenario configuration ....
        
        # Get final scenario configuration
        scenario_config_final = sim.get_scenario_config()

        # Store scenario configuration in a file
        scenario_config_final.save_to_file("myHanoiConfig.epytflow_config")

    # ....

    # Load scenario configuration
    scenario_config = ScenarioConfig.load("myHanoiConfig.epytflow_config")
    with WaterDistributionNetworkScenarioSimulator(scenario_config) as sim:
        # ....


Predefined networks
-------------------

EPyT-Flow comes with set of popular benchmark water distribution networks already included.
These networks are, if necessary, downloaded and wrapped inside a :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig` 
instance, so that they can directly be passed to :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.

Also note that in some cases (i.e. Hanoi and L-TOWN) a predefined sensor placement can be included as well.

+------------+-------------------------------------------------+
| Network    | Function for loading                            |
+============+=================================================+
| Net1       | :func:`~epyt_flow.data.networks.load_net1`      |
+------------+-------------------------------------------------+
| Net2       | :func:`~epyt_flow.data.networks.load_net2`      |
+------------+-------------------------------------------------+
| Net3       | :func:`~epyt_flow.data.networks.load_net3`      |
+------------+-------------------------------------------------+
| Richmond   | :func:`~epyt_flow.data.networks.load_richmond`  |
+------------+-------------------------------------------------+
| Anytown    | :func:`~epyt_flow.data.networks.load_anytown`   |
+------------+-------------------------------------------------+
| Kentucky   | :func:`~epyt_flow.data.networks.load_kentucky`  |
+------------+-------------------------------------------------+
| Hanoi      | :func:`~epyt_flow.data.networks.load_hanoi`     |
+------------+-------------------------------------------------+
| L-TOWN     | :func:`~epyt_flow.data.networks.load_ltown`     |
+------------+-------------------------------------------------+


Example of loading the Hanoi network:

.. code-block:: python

    network_config = load_hanoi()   # Load Hanoi network
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        # Set any additional parameters and finalize the scenario configuration ....
        # Run simulation ...