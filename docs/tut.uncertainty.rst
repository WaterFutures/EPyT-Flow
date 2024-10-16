.. _tut.uncertainty:

*************
Uncertainties
*************

Because WDNs are subject to many different types of uncertainties, EPyT-Flow comes with a set
of pre-defined and implemented uncertainties that allow the user to introduce uncertainties and
noise in the scenario generation.

Most types of uncertainty exist in two versions: *absolute* and *relative*.
While absolute uncertainties usually refer to the addition of noise that follows some distribution,
relative uncertainties usually refer to some kind of multiplication.
A complete list of pre-defined and implemented uncertainties is given in the following table:

+------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| Implementation                                                                     |  Description                                                         |
+====================================================================================+======================================================================+
| :class:`~epyt_flow.uncertainty.uncertainties.AbsoluteGaussianUncertainty`          | Gaussian noise is added.                                             |
+------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~epyt_flow.uncertainty.uncertainties.RelativeGaussianUncertainty`          | Gaussian noise centered at zero is added.                            |
+------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~epyt_flow.uncertainty.uncertainties.AbsoluteUniformUncertainty`           | Uniform noise is added.                                              |
+------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~epyt_flow.uncertainty.uncertainties.RelativeUniformUncertainty`           | Data is multiplied by uniform noise.                                 |
+------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~epyt_flow.uncertainty.uncertainties.PercentageDeviationUncertainty`       | Data can deviate up to some percentage from its original value.      |
+------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~epyt_flow.uncertainty.uncertainties.AbsoluteDeepUniformUncertainty`       | Uniform noise (changing over time) is added.                         |
+------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~epyt_flow.uncertainty.uncertainties.RelativeDeepUniformUncertainty`       | Data is multiplied by uniform noise that is changing over time.      |
+------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~epyt_flow.uncertainty.uncertainties.AbsoluteDeepGaussianUncertainty`      | Gaussian noise (changing over time) is added.                        |
+------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~epyt_flow.uncertainty.uncertainties.RelativeDeepGaussianUncertainty`      | Gaussian noise (changing over time) centered add zero is added.      |
+------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~epyt_flow.uncertainty.uncertainties.AbsoluteDeepUncertainty`              | Random pattern/noise (chaning over time) is added.                   |
+------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~epyt_flow.uncertainty.uncertainties.RelativeDeepUncertainty`              | Data is multiplied by random pattern/noise (chaning over time).      |
+------------------------------------------------------------------------------------+----------------------------------------------------------------------+

.. note::

    A custom type of uncertainty can be implemented by deriving a sub-class from
    :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`.


.. _model_uncertainty:

Model Uncertainty
+++++++++++++++++

Model uncertainty refers to uncertainty in the WDN model -- i.e. uncertainty in pipe lengths,
pipe diameters, base demands, demand patterns, etc.

EPyT-Flow allows the user to specify model uncertainties by instantiating
:class:`~epyt_flow.uncertainty.model_uncertainty.ModelUncertainty`. This instance can then be passed
to the scenario simulator
(instance of :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`) by calling
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_model_uncertainty` BEFORE
the simulation is run.

Example of setting pipe length, and demand pattern uncertainty -- in both cases the uncertainty
corresponds to a uniform deviation of up to 10%:

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    network_config = load_hanoi()
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Specify pipe length and demand pattern uncertainty
        uncertainty = PercentageDeviationUncertainty(deviation_percentage=.1)
        model_uncertainty = ModelUncertainty(pipe_length_uncertainty=uncertainty,
                                             demand_pattern_uncertainty=uncertainty)
        sim.set_model_uncertainty(model_uncertainty)

        # Run the simulation
        # ...


.. _sensor_uncertainty:

Sensor Uncertainty
++++++++++++++++++

Sensor uncertainty (also referred to as sensor noise) refers to uncertainty that affects **ALL**
sensor readings -- i.e. all sensor readings are perturbed by the given uncertainty.
In EPyT-Flow, sensor uncertainties have to be
:class:`~epyt_flow.uncertainty.uncertainties.Uncertainty` instances wrapped inside a
:class:`~epyt_flow.uncertainty.sensor_noise.SensorNoise` instance.

Sensor uncertainty/noise can be added BEFORE the simulation is run by calling
:func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.set_sensor_noise` of a
:class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` instance.

Example setting Gaussian uncertainty BEFORE the simulation is run:

.. code-block:: python

    # Open/Create a new scenario based on the Hanoi network
    network_config = load_hanoi()
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Sensor readings are affected by relative Gaussian uncertainty with scale=1
        uncertainty = RelativeGaussianUncertainty(scale=1.)
        sim.set_sensor_noise(SensorNoise(uncertainty))

        # Run simulation
        # ....

AFTERWARDS, the sensor uncertainty/noise can be set or changed by calling
:func:`~epyt_flow.simulation.scada.scada_data.ScadaData.change_sensor_noise` of a
:class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.

Example of setting/changing the sensor uniform deviation uncertainty AFTER the
simulation was run:

.. code-block:: python

    # Load scenario
    # ...

    # Run simulation
    scada_data = sim.run_simulation()

    # Sensor readings deviate (uniformly) up to 10% from their original value
    uncertainty = PercentageDeviationUncertainty(deviation_percentage=.1)
    scada_data.change_sensor_noise(SensorNoise(uncertainty))