"""
Example of adding uncertainty with respect to WDN parameters (e.g. demand pattern).
"""
from epyt_flow.data.networks import load_ltown
from epyt_flow.simulation import ScenarioSimulator, ModelUncertainty, RelativeUniformUncertainty
from epyt_flow.utils import to_seconds


if __name__ == "__main__":
    # Load L-Town network
    network_config = load_ltown(include_default_sensor_placement=True)

    # Create scenario
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Set simulation duration to five hours
        sim.set_general_parameters(simulation_duration=to_seconds(hours=5))

        # Add uncertainty (i.e. randomness) with respect to the demand pattern --
        # i.e. demand pattern values can be deviate up to 25% from their original value.
        uc = RelativeUniformUncertainty(low=0.75, high=1.25)
        sim.set_model_uncertainty(ModelUncertainty(demand_pattern_uncertainty=uc))

        # Run simulation and retrieve sensor readings
        res = sim.run_simulation()
        print(res.get_data())
