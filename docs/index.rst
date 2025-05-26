Welcome to EPyT-Flow's documentation!
=====================================

EPANET Python Toolkit Flow -- EPyT-Flow
+++++++++++++++++++++++++++++++++++++++

EPyT-Flow is a Python package building on top of `EPyT <https://github.com/OpenWaterAnalytics/EPyT>`_ 
for providing easy access to water distribution network simulations.
It aims to provide a high-level interface for the easy generation of hydraulic and water quality scenario data.
However, it also provides access to low-level functions by `EPANET <https://github.com/USEPA/EPANET2.2>`_ 
and `EPANET-MSX <https://github.com/USEPA/EPANETMSX/>`_.

We recommend checking out `EPyT-Control <https://github.com/WaterFutures/EPyT-Control>`_
if you are intersted in (data-driven) control and relates tasks such as state estimation
and event diagnosis in Water Distribution Networks.

Statement of need 
-----------------

Water Distribution Networks (WDNs) are designed to ensure a reliable supply of drinking water.
These systems are operated and monitored by humans, supported by software tools,
including basic control algorithms and event detectors that rely on a limited number of sensors
within the WDN. These sensors measure hydraulic (e.g., pressure, flow) and water quality
(e.g., chemical concentrations) states. However, given the rapid population growth of urban areas,
WDNs are becoming more complex to manage due to the resulting time-varying system uncertainty.
Consequently, key tasks such as event detection (e.g., leakage) and isolation, pump scheduling,
and control are becoming more challenging. Moreover, modeling and predicting water quality in the
distribution network is becoming more difficult due to changing environmental conditions.
This is why water utilities are now driven to install even more sensors to gather data on their
changing systems. Traditionally, model-based methods were used for planning and managing WDNs;
however, due to rapid changes, these methods may no longer be sufficient. New AI and data-driven
methods can now take advantage of big data and are promising tools for tackling challenges in
water management.

Currently, non-water experts such as AI researchers face several challenges when devising
practical solutions for water system applications, such as the unavailability of tools for
easy scenario/data generation and easy access to benchmarks, which hinder the progress of
applying AI to this domain. 
Easy-to-use toolboxes and access to benchmark data sets are extremely important for boosting and
accelerating research, as well as for supporting reproducible research, as it was, for instance,
the case in deep learning and machine learning where toolboxes such as TensorFlow and
scikit-learn had a significant impact on boosting research.

EPyT-Flow provides easy access to popular benchmark data sets for event detection and localization.
Furthermore, it also provides an environment for developing and testing control algorithms.

Unique Features
---------------

Unique features of EPyT-Flow that make it superior to other (Python) toolboxes are the following:

- High-performance hydraulic and (advanced) water quality simulation
- High- and low-level interface
- Object-orientated design that is easy to extend and customize
- Sensor configurations
- Wide variety of pre-defined events (e.g. leakages, sensor faults, actuator events, contamination, cyber-attacks, etc.)
- Wide variety of pre-defined types of global & local uncertainties (e.g. model uncertainties)
- Step-wise simulation and environment for training and evaluating control strategies
- Serialization module for easy exchange of data and (scenario) configurations
- REST API to make EPyT-Flow accessible in other applications
- Access to many WDNs and popular benchmarks (incl. their evaluation)



.. toctree::
    :maxdepth: 2
    :caption: User Guide

    installation
    basicusage

    tutorial

.. _tut.examples:

Examples
========
.. toctree::
   :maxdepth: 2
   :caption: Jupyter notebooks

   examples/basic_usage
   examples/plot_network
   examples/network_topology
   examples/uncertainties
   examples/abrupt_leakage
   examples/sensor_fault
   examples/sensor_override_attack
   examples/sensor_replay_attack
   examples/pump_states
   examples/simple_control_example
   examples/complex_control_example
   examples/custom_control_example
   examples/water_age
   examples/chlorine_injection
   examples/net2-cl2_example
   examples/arsenic_contamination
   examples/visualization


API Reference
=============
.. toctree::
    :maxdepth: 2
    :caption: API Reference

    epyt_flow


Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
