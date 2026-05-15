"""
Example of retrieving the network topology.
"""
from epyt_flow.data.networks import load_net1
from epyt_flow.simulation import ScenarioSimulator, EpanetConstants
from epyt_flow.topology import flowunit_to_str


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

        # Which flow units are used in this NetworkTopology instance?
        print(flowunit_to_str(topo.flow_units))

        # Convert units to SI METRIC -- i.e. flow units to cubic meter per hours and pressure to meter.
        # This will results yield pipe diameter in *millimeter*, pipe length in *meter*,
        # node elevation in *meter*, ...
        new_topo = topo.convert_units(flow_units=EpanetConstants.EN_CMH,
                                      pressure_units=EpanetConstants.EN_METERS)

        print(new_topo.get_node_info("2"))
        print(new_topo.get_link_info("10"))

        # Convert units back to US CUSTOMARY -- i.e., flow units should be gallons per minute
        # and pressure in psi
        new_topo = new_topo.convert_units(flow_units=EpanetConstants.EN_GPM,
                                          pressure_units=EpanetConstants.EN_PSI)

        print(new_topo.get_node_info("2"))
        print(new_topo.get_link_info("10"))
