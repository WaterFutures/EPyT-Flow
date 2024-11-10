---
title: 'EPyT-Flow: A Toolkit for Generating Water Distribution Network Data'
tags:
  - Python
  - EPANET
  - smart water networks
  - hydraulics
  - water quality
  - simulation
authors:
  - name: André Artelt
    equal-contrib: true
    orcid: 0000-0002-2426-3126
    affiliation: "1, 3"
    corresponding: true
  - name: Marios S. Kyriakou
    orcid: 0000-0002-2324-8661
    equal-contrib: true
    affiliation: 1
  - name: Stelios G. Vrachimis
    orcid: 0000-0001-8862-5205
    equal-contrib: true
    affiliation: "1, 2"
  - name: Demetrios G. Eliades
    orcid: 0000-0001-6184-6366
    equal-contrib: true
    affiliation: 1
  - name: Barbara Hammer
    equal-contrib: true
    orcid: 0000-0002-0935-5591
    affiliation: 3
  - name: Marios M. Polycarpou
    orcid: 0000-0001-6495-9171
    equal-contrib: true
    affiliation: "1, 2"
affiliations:
  - name: KIOS Research and Innovation Center of Excellence, University of Cyprus, Cyprus
    index: 1
  - name: Department of Electrical and Computer Engineering, University of Cyprus, Cyprus
    index: 2
  - name: Faculty of Technology, Bielefeld University, Germany
    index: 3
bibliography: paper.bib

---

# Summary

This work introduces [`EPyT-Flow`](https://github.com/WaterFutures/EPyT-Flow), an open-source Python package building on top of [EPyT](https://github.com/OpenWaterAnalytics/EPyT) for facilitating water distribution network (WDN) simulations.
`EPyT-Flow` provides a high-level interface for the easy generation of hydraulic and water quality scenario data.
Additionally, it provides access to low-level functions of [EPANET](https://github.com/USEPA/EPANET2.2) and [EPANET-MSX](https://github.com/USEPA/EPANETMSX/) for hydraulic and water quality modeling respectively.
To accelerate research in WDN management, `EPyT-Flow` provides easy access to popular benchmark data sets for event detection and localization, and an environment for developing and testing feedback control algorithms.

# Statement of need 

Water Distribution Networks (WDNs) are designed to ensure a reliable supply of drinking water. These systems are operated and monitored by humans, supported by software tools, including basic control algorithms and event detectors that rely on a limited number of sensors within the WDN. These sensors measure hydraulic (e.g., pressure, flow) and water quality (e.g., chemical concentrations) states. However, given the rapid population growth of urban areas, WDNs are becoming more complex to manage due to the resulting time-varying system uncertainty. Consequently, key tasks such as event detection (e.g., leakage) and isolation, pump scheduling, and control are becoming more challenging. Moreover, modeling and predicting water quality in the distribution network is becoming more difficult due to changing environmental conditions. This is why water utilities are now driven to install even more sensors to gather data on their changing systems. Traditionally, model-based methods were used for planning and managing WDNs; however, due to rapid changes, these methods may no longer be sufficient. New AI and data-driven methods can now take advantage of big data and are promising tools for tackling challenges in water management.

Currently, non-water experts such as AI researchers face several challenges when devising practical solutions for water system applications, such as the unavailability of tools for easy scenario/data generation and easy access to benchmarks, which hinder the progress of applying AI to this domain. 
Easy-to-use toolboxes and access to benchmark data sets are extremely important for boosting and accelerating research, as well as for supporting reproducible research. This was, for instance, the case in deep learning and machine learning with toolboxes such as [TensorFlow](https://www.tensorflow.org/) and [scikit-learn](https://scikit-learn.org/stable/).


## State of the field

The modeling and simulation of hydraulic and water quality dynamics in water distribution networks have
progressively advanced with the introduction of simulation software. Notably, `EPANET` [@rossman2000] and
its extension `EPANET-MSX` [@shang2008modeling] are foundational tools in this area. These are complemented
by tools that make use of high-level programming languages, such as the `EPANET-MATLAB Toolkit (EMT)` [@eliades2016],
the `Object-Oriented Pipe Network Analyzer (OOPNET)` [@Steffelbauer2015], and the
`EPANET-Python Toolkit (EPyT)` [@kyriakou2023epyt]. Moreover, `viswaternet` provides visualizations
of static and time-varying attributes of EPANET-based WDNs [@Thomas2023]. These tools are instrumental in facilitating research
in WDN resilience and response to various operational challenges. 

These tools, however, do not support the creation of realistic (benchmark) scenarios with
essential aspects such as realistic fault models (of leakages and sensor faults), various sensor configurations,
custom control modules, and other events such as changes in water quality caused by external factors.
However, such data creation mechanisms are important for supporting and enabling research on the application of
Machine Learning (ML) and Artifical Intelligence (AI) in WDNs.
A first step towards such software for scenario creation is the `Water Network Tool for Resilience (WNTR)` [@klise2017software],
which facilitates the performing hydraulic simulations under various scenarios such as
pipe breaks, disasters such as earthquakes, power outages, and fires. However, it currently does not fully integrate
(advanced) quality dynamics with scenarios such as pipe leaks and also misses other crucial modules such as
sensor configurations, and considerations of industrial controls
(i.e. controls that go beyond simple IF-THEN-ELSE controls as supported by EPANET).

The transition to PYTHON-based open-source software [@kyriakou2023epyt; @klise2017software], underscores a broader trend
towards open-source, community-driven development in the water industry, aligning with the need for transparency,
reproducibility, and innovation in the sector.

# Functionality

Our PYTHON toolbox `EPyT-Flow` provides a high-level interface for easy generation of WDN scenario data,
but also provides access to low-level functions for maximum flexibility as needed by domain experts.
By this we aim to satisfy different needs and make it a toolbox for "everybody".
A special focus of EPyT-Flow is on data generation to enable and support research on the application of
ML and AI in WDNs.
In addition, its design and object-orientated implementation makes it easy to customize existing
functionalities and implement new ones.
`EPyT-Flow` builds upon `EPyT` which itself provides a PYTHON interface to `EPANET` 
and `EPANET-MSX` -- see Figure \ref{fig:toolbox:structure} for an illustration.

![Illustration of the functionality of the proposed toolbox *`EPyT-Flow`*.\label{fig:toolbox:structure}](figures/structure.drawio.png){ width=50% heigth=50%}

The toolbox currently includes $16$ Water Distribution Networks (WDNs) that can be used for scenario generation.
It goes beyond pure scenario generation by providing access to $7$ popular and widely adopted
benchmarks on event detection and localization (including their evaluation metrics) -- ready to be
utilized for building and evaluating algorithms.
Furthermore, it provides an environment, inspired by the modular and extensible design of [OpenAI Gym](https://gymnasium.farama.org/index.html)
for developing and implementing (AI-based) algorithms for tasks such as energy efficient pump scheduling.

To support modeling of a wide variety of scenarios, the toolbox comes with $4$ different event types
and a total number of $13$ pre-defined and implemented events ready to be utilized in custom scenarios:
$3$ different leakage types, $3$ actuator events, $5$ sensor fault types, and $2$ communication events.
All the events can be easily customized by the user.

Since the measured quantities in the real world are always subject to uncertainty, the toolbox comes with
$11$ pre-defined types of uncertainties ranging from classic Gaussian noise to different types of
(very) deep uncertainties that can be applied to hydraulic parameters such as pipe length, diameter,
and roughness, and water quality parameters, such as reaction coefficients, and sensor noise.

More information can be found in the comprehensive ($200$+ pages) [EPyT-Flow Documentation](https://epyt-flow.readthedocs.io/en/latest/)
and $14$ fully working examples that demonstrate how `EPyT-Flow` can be utilized in different tasks.

# Conclusions

In this work, we introduced a PYTHON toolbox called `EPyT-Flow` for realistic scenario data generation and
access to benchmarks of WDNs, that researchers can utilize to develop methods to support human WDN operators
in various real-world challenges.

Our long-term vision for this toolbox is to split it into three parts to further facilitate the progress of research in this area:

1) A core part for data generation (i.e., scenario simulation).
2) A `BenchmarkHub` as a platform for accessing and sharing WDN benchmarks.
3) A `ModelHub` as a platform for accessing and sharing AI, classic models and algorithms for different tasks in WDNs.

# Acknowledgments

This work was supported by the Ministry of Culture and Science NRW (Germany) as part of the Lamarr Fellow Network,
and by the European Research Council (ERC) under the ERC Synergy Grant Water-Futures (Grant agreement No. 951424).
This publication reflects the views of the authors only.

# References
