"""
Example of retrieving the network topology.
"""
from epyt_flow.data.networks import load_net1
from epyt_flow.simulation import ScenarioSimulator


if __name__ == "__main__":
    # Load Net1 network
    network_config = load_net1()

    # Create scenario
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Get network topology
        topo = sim.get_topology()

        # Show edges
        print(topo.edges)

        # Show nodes
        print(topo.nodes)

        # Shortest path between node "2" and node "22"
        print(topo.get_shortest_path("2", "22"))

        # Adjacency matrix of the graph
        print(topo.get_adj_matrix().todense())

        # Show information associated with node "2"
        print(topo.get_node_info("2"))

        # Show information associated with link "10"
        print(topo.get_link_info("10"))
