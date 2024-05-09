# EPyT-Flow -- EPANET Python Toolkit - Flow

EPyT-Flow is a Python package building on top of [EPyT](https://github.com/OpenWaterAnalytics/EPyT) 
for providing easy access to water distribution network simulations.
It aims to provide a high-level interface for the easy generation of hydraulic and water quality scenario data.
However, it also provides access to low-level functions by [EPANET](https://github.com/USEPA/EPANET2.2) 
and [EPANET-MSX](https://github.com/USEPA/EPANETMSX/).

EPyT-Flow provides easy access to popular benchmark data sets for event detection and localization.
Furthermore, it also provides an environment for developing and testing control algorithms.

![](https://github.com/WaterFutures/EPyT-Flow/blob/main/docs/_static/net1_plot.png?raw=true)

## Installation

EPyT-Flow supports Python 3.9 - 3.12

Note that [EPANET and EPANET-MSX sources](epyt_flow/EPANET/) are compiled and overrite the binaries
shipped by EPyT IF EPyT-Flow is installed on a Linux system. By this we not only aim to achieve
a better performance of the simulations but also avoid any compatibility problems of pre-compiled binaries.

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

        # Show sensor readings over the entire simulation
        print(f"Pressure readings: {scada_data.get_data_pressures()}")
        print(f"Flow readings: {scada_data.get_data_flows()}")
```

## Documentation

Documentation is available on readthedocs: [https://epytflow.readthedocs.io/en/latest/](https://epytflow.readthedocs.io/en/latest/)

## License

MIT license -- see [LICENSE](LICENSE)

## How to Cite?

If you use this software, please cite it as follows:

```
@misc{github:epytflow,
        author = {André Artelt, Marios S. Kyriakou, Stelios G. Vrachimis, Demetrios G. Eliades, Barbara Hammer, Marios M. Polycarpou},
        title = {EPyT-Flow -- EPANET Python Toolkit - Flow},
        year = {2024},
        publisher = {GitHub},
        journal = {GitHub repository},
        howpublished = {\url{https://github.com/WaterFutures/EPyT-Flow}}
    }
```

## How to Contribute?

Contributions (e.g. creating issues, pull-requests, etc.) are welcome -- please make sure to read the [code of conduct](CODE_OF_CONDUCT.md) and follow the [developers' guidelines](DEVELOPERS.md).
