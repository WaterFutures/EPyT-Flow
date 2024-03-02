"""
Example on the implementation of an abrupt leakage.
"""
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator, AbruptLeakage


if __name__ == "__main__":
    # Load Hanoi network with default sensor placement
    hanoi_network_config = load_hanoi(include_default_sensor_placement=True)

    # Create scenario
    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        # Set simulation duration to 7 days
        sim.set_general_parameters(simulation_duration=7)

        # Add an abrupt leakage at link/pipe "14" -- the leakage is active for 26hrs and
        # starts at 2hrs after simulation begin -- recall that the time arguments are seconds!
        leak = AbruptLeakage(link_id="14", diameter=0.01, start_time=7200, end_time=100800)
        sim.add_leakage(leak)

        # Run entire simulation
        res = sim.run_simulation()

        # Retrieve and show pressure at node "13" over time
        print(f"Pressure at node '13': {res.get_data_pressures(sensor_locations=['13'])}")
