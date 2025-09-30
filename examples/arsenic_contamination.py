"""
Example of adding a simple arsenic contamination event to a scenario.
"""
import numpy as np
from epyt_flow.data.benchmarks import load_leakdb_scenarios
from epyt_flow.simulation import ScenarioSimulator, EpanetConstants, ScenarioConfig
from epyt_flow.simulation.events import SpeciesInjectionEvent
from epyt_flow.utils import to_seconds


if __name__ == "__main__":
    # Create a new scenario based on the first Net1 LeakDB scenario --
    # we add an additional EPANET-MSX configuration file
    config, = load_leakdb_scenarios(scenarios_id=["1"], use_net1=True)
    config = ScenarioConfig(scenario_config=config,
                            f_msx_in="arsenic_contamination.msx")

    with ScenarioSimulator(scenario_config=config) as sim:
        # Set simulation duration to 21 days
        sim.set_general_parameters(simulation_duration=to_seconds(days=21))

        # Place some chlorine sensors and also keep track of the contaminant
        cl_sensor_locations = ["10", "11", "12", "13", "21", "22", "23", "31", "32"]
        all_nodes = sim.sensor_config.nodes
        sim.set_bulk_species_node_sensors({"Chlorine": cl_sensor_locations,
                                           # Also: Keep track of the contaminant
                                           "AsIII": all_nodes})   # Arsenite

        # Create a 1-day contamination event --
        # i.e. injection of Arsenite (100mg/L) at node "22"
        contamination_event = SpeciesInjectionEvent(species_id="AsIII", node_id="22",
                                                    profile=np.array([100]),
                                                    source_type=EpanetConstants.EN_MASS,
                                                    start_time=to_seconds(days=3),
                                                    end_time=to_seconds(days=4))
        sim.add_system_event(contamination_event)

        # Run simulation
        scada_data = sim.run_simulation()

        # Inspect simulation results -- i.e. sensor readings over time
        scada_data.plot_bulk_species_node_concentration({"Chlorine": cl_sensor_locations})
        scada_data.plot_bulk_species_node_concentration({"AsIII": all_nodes})
