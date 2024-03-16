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
and enriched with gzip compression.

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
    with ScenarioSimulator(scenario_config=network_config) as sim:
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

To  make any new class (e.g. custom events) serializable, the class must be derived from 
:class:`~epyt_flow.serialization.Serializable` and be marked by the 
:func:`~epyt_flow.serialization.serializable` decorator.

Any class derived from :class:`~epyt_flow.serialization.Serializable`  must implement the 
:func:`~epyt_flow.serialization.Serializable.get_attributes` method. 
This method is supposed to return a dictionary of the attributes completely describing the instance -- 
those will be passed to the constructor when deserializing an instance of this class.

The decorator requires a **unique ID** of the class that is made serializeable -- 
i.e. every class (more general every data type) is assigned a unique ID to make it 
recognizable by the parser. All reserved IDs (you cannot use those!) are listed in 
:mod:`epyt_flow.serialization.py` -- right now any number greater than 25 is free for use.
Furthermore, a file extension is required which should allow the user to infer the type of content 
-- this file extension is appended to the path automatically, if not already present.

Example of making a new class `MyClass` serializable -- this class is assigned the ID `42`:

.. code-block:: python

    @serializable(42, ".my_file_ext")
    class MyNewClass(Serializable):
        def __init__(self, my_var_1, my_var_2, **kwds):
            self.my_var_1 = my_var_1
            self.my_var_2 = my_var_2

            # Other initialization logic ...

            super().__init__(**kwds)
        
        def get_attributes(self) -> dict:
            return super().get_attributes() | \
                {"my_var_1": self.my_var_1, "my_var_2": self.my_var_2}

        # Other class methods ...