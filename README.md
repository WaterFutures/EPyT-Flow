# EPyT-Flow -- EPANET Python Toolkit - Flow

EPyT-Flow is a Python package building on top of [EPyT](https://github.com/OpenWaterAnalytics/EPyT) for providing easy access to water distribution network simulations.

## Installation

EPyT-Flow supports Python 3.9 - 3.12

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

```python
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator
from epyt_flow.simulation.sensor_config import SENSOR_TYPE_NODE_PRESSURE,\
    SENSOR_TYPE_LINK_FLOW


if __name__ == "__main__":
    # Load Hanoi network
    network_config = load_hanoi()

    # Create scenario
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=2)

        # Place pressure sensors at nodes "13", "16", "22", and "30"
        sim.set_sensors(SENSOR_TYPE_NODE_PRESSURE, sensor_locations=["13", "16", "22", "30"])

        # Place a flow sensor at link/pipe ""
        sim.set_sensors(SENSOR_TYPE_LINK_FLOW, sensor_locations=["1"])

        # Run entire simulation
        res = sim.run_simulation()

        # Show sensor readings over the entire simulation
        print(res.get_data())
```

## Documentation

Documentation is available on readthedocs: [https://epytflow.readthedocs.io/en/latest/](https://epytflow.readthedocs.io/en/latest/)

## License

MIT license -- see [LICENSE](LICENSE)

## How to Cite?

If you use this software, please cite it as follows:

```
@misc{github:epytflow,
        author = {André Artelt, Marios S. Kyriakou, Stelios G. Vrachimis},
        title = {EPyT-Flow -- EPANET Python Toolkit - Flow},
        year = {2024},
        publisher = {GitHub},
        journal = {GitHub repository},
        howpublished = {\url{https://github.com/WaterFutures/EPyT-Flow}}
    }
```

## How to Contribute?

Contributions (e.g. creating issues, pull-requests, etc.) are welcome -- please make sure to read the [code of conduct](CODE_OF_CONDUCT.md) and follow the [developers' guidelines](DEVELOPERS.md).