"""
Example of retrieving the network topology.
"""
from epyt_flow.data.networks import load_net1
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.topology import unitscategoryid_to_str, UNITS_SIMETRIC, UNITS_USCUSTOM


if __name__ == "__main__":
    # Load Net1 network
    network_config = load_net1()

    # Create scenario
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Get network topology
        topo = sim.get_topology()

        # Show edges/links
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

        # Get GeoDataFrame
        geo_data = topo.to_gis()
        print(geo_data["nodes"])

        # Which units are used in this NetworkTopology instance?
        print(unitscategoryid_to_str(topo.units))

        # Convert units to SI METRIC -- i.e. pipe diameter in *millimeter*,
        # pipe length in *meter*, node elevation in *meter*, ...
        new_topo = topo.convert_units(UNITS_SIMETRIC)

        print(new_topo.get_node_info("2"))
        print(new_topo.get_link_info("10"))

        # Convert units back to US CUSTOMARY
        new_topo = new_topo.convert_units(UNITS_USCUSTOM)

        print(new_topo.get_node_info("2"))
        print(new_topo.get_link_info("10"))
