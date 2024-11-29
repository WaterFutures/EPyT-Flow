"""
Example of adding a chlorine injection to a scenario.
"""
import numpy
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import ScenarioSimulator, ToolkitConstants
from epyt_flow.utils import to_seconds


if __name__ == "__main__":
    # Load Hanoi network
    network_config = load_hanoi()

    # Create scenario
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Set simulation duration to 12 hours
        sim.set_general_parameters(simulation_duration=to_seconds(hours=12))

        # Enable chemical analysis
        sim.enable_chemical_analysis()

        # Sets the concentration at node "1" (reservoir) to 1.0 for all time steps.
        sim.add_quality_source(node_id="1",
                               pattern=numpy.array([1.]),
                               source_type=ToolkitConstants.EN_CONCEN)

        # Places quality sensors at all nodes --
        # i.e. measuring the chemical concentration at all nodes
        sim.set_node_quality_sensors(sensor_locations=sim.sensor_config.nodes)

        # Run simulation
        scada_data = sim.run_simulation()

        # Retrieve and show the simulated chemical concentrations at all nodes
        nodes_quality = scada_data.get_data_nodes_quality()
        print(nodes_quality)
        scada_data.plot_nodes_quality()
