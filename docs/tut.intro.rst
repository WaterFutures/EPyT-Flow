.. _tut.intro:

***************************************
Modeling of Water Distribution Networks
***************************************

This page is supposed to give a very brief overview of the modeling and terminology of 
water distribution networks (WDNs).

Topology
++++++++

The structure/topology of a WDN is modeled as a graph, where edges model links/pipes 
and nodes model junctions -- see the following Figure for an illustration.

.. image:: _static/net1_plot.png

Edges
-----

Edges (e.g. links/pipes) have certain parameters such as length, diameter,
roughness coefficient, etc. There exist different types of links:

+-----------+--------------------------------------------------------------------------------------------------+
| Type      | Description                                                                                      |
+===========+==================================================================================================+
| Link/Pipe | Transporting water                                                                               | 
+-----------+--------------------------------------------------------------------------------------------------+
| Pump      | Moving water from one segment to another                                                         |
+-----------+--------------------------------------------------------------------------------------------------+
| Valve     | Blocking or letting water pass through -- can also control (i.e. reduce) pressure in the network |
+-----------+--------------------------------------------------------------------------------------------------+


Nodes
-----

The nodes in the graph do not only model junctions but also consumers -- i.e. locations where
water is taken (i.e. consumed) from the WDN.  Consequently, different nodes might have different
elevations which makes the use of pumps necessary. Water consumption is modeled by demand patterns
that describe how much water is consumed over time -- each node in the graph can have its
own demand pattern. Furthermore, there exist different types of nodes:

+-------------+-------------------------------------------------------------------------------------------+
| Type        | Description                                                                               |
+=============+===========================================================================================+
| Reservoirs  | "Infinite" source of water (e.g. a lake or river)                                         |
+-------------+-------------------------------------------------------------------------------------------+
| Tank        | Storing water                                                                             |
+-------------+-------------------------------------------------------------------------------------------+
| Junction    | Intersection of links/pipes and consumption point (i.e. water is taken from the network)  |
+-------------+-------------------------------------------------------------------------------------------+


Simulation
++++++++++

There are two types of dynamics that are relevant in a WDN: 1) hydraulics and 2) quality.

Hydraulics refers to quantities such as flow rates, pressures, etc., while quality refers to
chemical concentrations. Hydraulics depend not only on the topology of the WDN but also on demands
(i.e. water consumption) as well as pump and valve operations. Building on the hydraulics,
quality dynamics depend not only on the hydraulics (in particular flow rates)  but also on
chemical reactions (e.g. pipe wall reactions) and injections
(e.g. chlorine injection or contamination events).

Also, there exist two different types of demand models that can be used for simulating
the hydraulics: Demand-driven analysis (DDA) and a pressure-driven analysis (PDA) --
note that pressure-driven analysis (PDA) is more robust in extreme situations but requires
specifying additiona parameters such as the minimum pressure and the pressure exponent.

The units of measurement are set globally and are either in *US customary* or *SI metric*.
The units are set by settings the flow units -- more details can be found in the
`EPANET documents on units <https://epanet22.readthedocs.io/en/latest/back_matter.html#units-of-measurement>`_.

EPyT-Flow is based on EPANET and therefore uses a steady-state simulation of the hydraulics,
on which the quality dynamics are computed. Details can be found in the
`EPANET documentation <https://epanet22.readthedocs.io/en/latest/12_analysis_algorithms.html>`_.