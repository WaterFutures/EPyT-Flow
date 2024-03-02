"""
Example of retrieving the network topology.
"""
from epyt_flow.data.networks import load_net1
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator


if __name__ == "__main__":
    # Load Net1 network
    network_config = load_net1()

    # Create scenario
    with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
        # Get network topology
        graph = sim.get_topology()

        # Show edges
        print(graph.edges)
