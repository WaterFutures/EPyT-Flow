[![pypi](https://img.shields.io/pypi/v/epyt-flow.svg)](https://pypi.org/project/epyt-flow/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/epyt-flow)
[![build](https://github.com/WaterFutures/EPyT-Flow/actions/workflows/build_tests.yml/badge.svg)](https://github.com/WaterFutures/EPyT-Flow/actions/workflows/build_tests.yml)
[![Documentation Status](https://readthedocs.org/projects/epyt-flow/badge/?version=stable)](https://epyt-flow.readthedocs.io/en/stable/?badge=stable)
[![Downloads](https://static.pepy.tech/badge/epyt-flow)](https://pepy.tech/project/epyt-flow)
[![Downloads](https://static.pepy.tech/badge/epyt-flow/month)](https://pepy.tech/project/epyt-flow)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.07104/status.svg)](https://doi.org/10.21105/joss.07104)

# EPyT-Flow -- EPANET Python Toolkit - Flow

<img src="https://github.com/WaterFutures/EPyT-Flow/blob/main/docs/_static/net1_plot.png?raw=true" align="right" height="230px"/>

EPyT-Flow is a Python package building on top of [EPyT](https://github.com/OpenWaterAnalytics/EPyT) 
for providing easy access to water distribution network simulations.
It aims to provide a high-level interface for the easy generation of hydraulic and water quality scenario data.
However, it also provides access to low-level functions by [EPANET](https://github.com/USEPA/EPANET2.2) 
and [EPANET-MSX](https://github.com/USEPA/EPANETMSX/).

EPyT-Flow provides easy access to popular benchmark data sets for event detection and localization.
Furthermore, it also provides an environment for developing and testing control algorithms.


## Unique Features

Unique features of EPyT-Flow that make it superior to other (Python) toolboxes are the following:

- High-performance hydraulic and (advanced) water quality simulation
- High- and low-level interface
- Object-orientated design that is easy to extend and customize
- Sensor configurations
- Wide variety of pre-defined events (e.g. leakages, sensor faults, actuator events, cyber-attacks, etc.)
- Wide variety of pre-defined types of uncertainties (e.g. model uncertainties)
- Step-wise simulation and environment for training and evaluating control strategies
- Serialization module for easy exchange of data and (scenario) configurations
- REST API to make EPyT-Flow accessible in other applications
- Access to many WDNs and popular benchmarks (incl. their evaluation)


## Installation

EPyT-Flow supports Python 3.9 - 3.12

Note that [EPANET and EPANET-MSX sources](epyt_flow/EPANET/) are compiled and overwrite the binaries
shipped by EPyT **IF** EPyT-Flow is installed on a Unix system and the *gcc* compiler is available.
By this, we not only aim to achieve a better performance of the simulations but also avoid any
compatibility issues of pre-compiled binaries.

#### Prerequisites for macOS users
The "true" *gcc* compiler (version 12) is needed which is not the
*clang* compiler that is shipped with Xcode and is linked to gcc!

The correct version of the "true" *gcc* can be installed via [brew](https://brew.sh/):
```
brew install gcc@12
```

### PyPI

```
pip install epyt-flow
```

### Git
Download or clone the repository:
```
git clone https://github.com/WaterFutures/EPyT-Flow.git
cd EPyT-Flow
```

Install all requirements as listed in [REQUIREMENTS.txt](REQUIREMENTS.txt):
```
pip install -r REQUIREMENTS.txt
```

Install the toolbox:
```
pip install .
```

## Quick Example

<a target="_blank" href="https://colab.research.google.com/github/WaterFutures/EPyT-Flow/blob/main/docs/examples/basic_usage.ipynb">
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

```python
from epyt_flow.data.benchmarks import load_leakdb_scenarios
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.utils import to_seconds


if __name__ == "__main__":
    # Load first Hanoi scenario from LeakDB
    network_config, = load_leakdb_scenarios(scenarios_id=["1"], use_net1=False)

    # Create scenario
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Place pressure sensors at nodes "13", "16", "22", and "30"
        sim.set_pressure_sensors(sensor_locations=["13", "16", "22", "30"])

        # Place a flow sensor at link/pipe "1"
        sim.set_flow_sensors(sensor_locations=["1"])

        # Run entire simulation
        scada_data = sim.run_simulation()

        # Print & plot sensor readings over the entire simulation
        print(f"Pressure readings: {scada_data.get_data_pressures()}")
        scada_data.plot_pressures()

        print(f"Flow readings: {scada_data.get_data_flows()}")
        scada_data.plot_flows()
```
### Generated plots

<div>
    <img src="https://github.com/WaterFutures/EPyT-Flow/blob/dev/docs/_static/examples_basic_usage_pressure.png?raw=true" width="49%"/>
    <img src="https://github.com/WaterFutures/EPyT-Flow/blob/dev/docs/_static/examples_basic_usage_flow.png?raw=true" width="49%"/>
</div>

## Documentation

Documentation is available on readthedocs: [https://epyt-flow.readthedocs.io/en/latest/](https://epyt-flow.readthedocs.io/en/stable)

## How to Get Started?

EPyT-Flow is accompanied by an extensive documentation
[https://epyt-flow.readthedocs.io/en/latest/](https://epyt-flow.readthedocs.io/en/stable)
(including many [examples](https://epyt-flow.readthedocs.io/en/stable/#examples)).

If you are new to water distribution networks, we recommend first to read the chapter on
[Modeling of Water Distribution Networks](https://epyt-flow.readthedocs.io/en/stable/tut.intro.html).
You might also want to check out some lecture notes on
[Smart Water Systems](https://github.com/KIOS-Research/ece808-smart-water-systems).

If you are already familiar with WDNs (and software such as EPANET), we recommend checking out
our [WDSA CCWI 2024 tutorial](https://github.com/WaterFutures/EPyT-and-EPyT-Flow-Tutorial) which
not only teaches you how to use EPyT and EPyT-Flow but also contains some examples of applying
Machine Learning in WDNs.
Besides that, you can read in-depth about the different functionalities of EPyT-Flow in the
[In-depth Tutorial](https://epyt-flow.readthedocs.io/en/stable/tutorial.html) of the documentation --
we recommend reading the chapters in the order in which they are presented;
you might decide to skip some of the last chapters if their content is not relevant to you.

## License

MIT license -- see [LICENSE](LICENSE)

## How to Cite?

If you use this software, please cite it as follows:

```bibtex
@article{Artelt2024,
    doi = {10.21105/joss.07104},
    url = {https://doi.org/10.21105/joss.07104},
    year = {2024},
    publisher = {The Open Journal},
    volume = {9},
    number = {103},
    pages = {7104},
    author = {André Artelt and Marios S. Kyriakou and Stelios G. Vrachimis and Demetrios G. Eliades and Barbara Hammer and Marios M. Polycarpou},
    title = {EPyT-Flow: A Toolkit for Generating Water Distribution Network Data},
    journal = {Journal of Open Source Software}
}
```

## How to get Support?

If you come across any bug or need assistance please feel free to open a new
[issue](https://github.com/WaterFutures/EPyT-Flow/issues/)
if non of the existing issues answers your questions.

## How to Contribute?

Contributions (e.g. creating issues, pull-requests, etc.) are welcome --
please make sure to read the [code of conduct](CODE_OF_CONDUCT.md) and
follow the [developers' guidelines](DEVELOPERS.md).
