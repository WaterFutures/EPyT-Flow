.. _tut.serialization:

*************
Serialization
*************

Basics
++++++

EPyT-Flow comes with a custom binary serialization method that allows the user to load and save 
almost any EPyT-Flow class to/from a file or byte array.
This allows an easy and fast storing/loading & sharing of configurations and results.

The implemented serialization mechanism is based on `MessagePack <https://msgpack.org/>`_ 
and enriched with zip compression.

Every serializable EPyT-Flow class supports the following functions:

+--------------------------------------------------------------+------------------------------------------------------------+
| Function                                                     | Description                                                |
+==============================================================+============================================================+
| :func:`~epyt_flow.serialization.Serializable.dump`           | Exports object to byte array                               |
+--------------------------------------------------------------+------------------------------------------------------------+
| :func:`~epyt_flow.serialization.Serializable.load`           | Imports/Creates object from byte array                     |
+--------------------------------------------------------------+------------------------------------------------------------+
| :func:`~epyt_flow.serialization.Serializable.save_to_file`   | Exports object into a file                                 |
+--------------------------------------------------------------+------------------------------------------------------------+
| :func:`~epyt_flow.serialization.Serializable.load_from_file` | Imports/Creates object from file                           |
+--------------------------------------------------------------+------------------------------------------------------------+

Example for exporting and importing a sensor configuration to/from a byte array:

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    network_config = load_hanoi()
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        # Create sensor placement ...

        # Export sensor config to byte array
        sensor_config_data = sim.sensor_config.dump()

        # ...

        # Load sensor config from byte array
        my_sensor_config = SensorConfig.load(sensor_config_data)
        print(my_sensor_config == sim.sensor_config)    # True


Example for storing and loading a scenario configuration to/from a file:

.. code-block:: python

    # Create scenario configuration
    config = load_hanoi()

    # Store in a file
    config.save_to_file("myHanoiConfig.epytflow_config")

    # ...

    # Load scenario configuration from file
    my_config = ScenarioConfig.load_from_file("myHanoiConfig.epytflow_config")


Advanced
++++++++

TODO