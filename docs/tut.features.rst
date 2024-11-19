.. _tut.features:

**********************
Features of EPyT-Flow
**********************

This page gives an overview of the features and functionalities of EPyT-Flow.

:ref:`Scenario simulation via EPANET and EPANET-MSX <tut.scenarios>`:
  - :ref:`Hydraulics <scenarios_basics>`
  - :ref:`Basic <basic_quality>` + :ref:`Advanced <advanced_quality>` water quality
  - :ref:`Sensor configurations and wide range of different units <tut.scada>`
  - :ref:`Custom control logic <tut.control>`
  - :ref:`Step-wise simulation <scenarios_basics>`
  - :ref:`Parallel simulation of several scenarions <scenarios_parallel_simulation>`
  - Included :ref:`benchmarks <benchmarks>` and :ref:`.inp files <networks>`

:ref:`Events <tut.events>`:
    - :ref:`Leakages <leakages>`:

      * Abrupt
      * Incipient
    - :ref:`Sensor faults <sensors_faults>`:

      * Constant shift
      * Drift
      * Gaussian noise
      * Percentage shift
      * Stuck-at-zero
    - :ref:`Senor reading attacks <sensors_attacks>`:

      * Replay attacks
      * Override attack
    - :ref:`Actuator events <actuators>`:

      * Pump states
      * Pump speed
      * Valve state
    - :ref:`Species Injection Events <msx_events>`
    - :ref:`Custom events <custom_events>`


:ref:`Uncertainties <tut.uncertainty>`:
  - :ref:`Pre-defined types of uncertainties<tut.uncertainty>`
  - :ref:`Model uncertainties (e.g. pipe length uncertainty) <model_uncertainty>`
  - :ref:`Sensor uncertainties <sensor_uncertainty>`

Data handling:
    - :ref:`Export to Excel, MATLAB, Numpy, etc. <scada_import_export>`
    - :ref:`Import + export in custom file format<tut.serialization>`

REST API:
    - :ref:`REST API server <tut.rest_api>`