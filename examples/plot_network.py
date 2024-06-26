"""
Example of plotting the network topology.
"""
from epyt_flow.data.networks import load_anytown
from epyt_flow.simulation import ScenarioSimulator, ScenarioVisualizer


if __name__ == "__main__":
    # Load Anytown network
    network_config = load_anytown()

    # Create scenario
    with ScenarioSimulator(scenario_config=network_config) as wdn:
        # Plot network topology
        ScenarioVisualizer(wdn).plot_topology()
