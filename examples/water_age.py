"""
Example on water age analysis.
"""
from epyt_flow.data.networks import load_ctown
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.utils import to_seconds


if __name__ == "__main__":
    # Create a new scenario simulation based on the C-Town network
    network_config = load_ctown()
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Enable water age analysis
        sim.enable_waterage_analysis()

        # Place quality sensors at all nodes -- i.e. measuring the water age at each node
        sim.set_node_quality_sensors(sensor_locations=sim.sensor_config.nodes)

        # Run simulation
        scada_data = sim.run_simulation()

        # Retrieve and show simulated water age at the first two nodes
        print(f"Water age: {scada_data.get_data_nodes_quality()}")
        scada_data.plot_nodes_quality(sensor_locations=sim.sensor_config.nodes[:2])
