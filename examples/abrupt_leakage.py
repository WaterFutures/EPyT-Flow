"""
Example on the implementation of an abrupt leakage.
"""
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import ScenarioSimulator, AbruptLeakage
from epyt_flow.utils import to_seconds


if __name__ == "__main__":
    # Load Hanoi network with default sensor placement
    hanoi_network_config = load_hanoi(include_default_sensor_placement=True)

    # Create scenario
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        # Set simulation duration to 7 days
        sim.set_general_parameters(simulation_duration=to_seconds(days=7))

        # Note that leakages are only modeled for two flow units.
        # We therefore change the flow units to cubic meter per hour --
        # could also be done when loading the network!
        sim.epanet_api.setFlowUnitsCMH()

        # Add an abrupt leakage at link/pipe "14" -- the leakage is active for 18 hours and
        # starts at 10 hours after simulation begin -- recall that the time arguments are seconds!
        leak = AbruptLeakage(link_id="14", diameter=0.001,
                             start_time=to_seconds(hours=10),
                             end_time=to_seconds(hours=28))
        sim.add_leakage(leak)

        # Run entire simulation
        scada_data = sim.run_simulation()

        # Retrieve and show pressure at node "13" over time
        print(f"Pressure at node '13': {scada_data.get_data_pressures(sensor_locations=['13'])}")
