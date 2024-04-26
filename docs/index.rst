Welcome to EPyT-Flow's documentation!
=====================================

EPANET Python Toolkit Flow -- EPyT-Flow
+++++++++++++++++++++++++++++++++++++++

EPyT-Flow is a Python package building on top of `EPyT <https://github.com/OpenWaterAnalytics/EPyT>`_ 
for providing easy access to water distribution network simulations.
It aims to provide a high-level interface for the easy generation of hydraulic and water quality scenario data.
However, it also provides access to low-level functions by `EPANET <https://github.com/USEPA/EPANET2.2>`_ 
and `EPANET-MSX <https://github.com/USEPA/EPANETMSX/>`_.

EPyT-Flow provides easy access to popular benchmark data sets for event detection and localization.
Furthermore, it also provides an environment for developing and testing control algorithms.

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
   examples/control_example
   examples/water_age
   examples/chlorine_injection
   examples/net2-cl2_example
   examples/event_detection


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
