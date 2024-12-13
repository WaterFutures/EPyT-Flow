"""
Example of adding uncertainty with respect to WDN parameters (e.g. demand pattern).
"""
import numpy as np
from epyt_flow.data.networks import load_ltown
from epyt_flow.simulation import ScenarioSimulator, ModelUncertainty, RelativeUniformUncertainty
from epyt_flow.utils import to_seconds, plot_timeseries_data


if __name__ == "__main__":
    # Load L-Town network with realistic demands
    network_config = load_ltown(include_default_sensor_placement=True, use_realistic_demands=True)

    # Create scenario
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Set simulation duration to three hours
        sim.set_general_parameters(simulation_duration=to_seconds(hours=3))

        # Add uncertainty (i.e. randomness) with respect to the demand pattern --
        # i.e. demand pattern values can deviate up to 25% from their original value.
        # Consequently, the simulation is no longer deterministic and the results vary
        # from run to run.
        uc = RelativeUniformUncertainty(low=0.75, high=1.25)
        sim.set_model_uncertainty(ModelUncertainty(global_demand_pattern_uncertainty=uc))

        # Run simulation three times and retrieve sensor readings at node "n105"
        measurements = []
        for _ in range(3):
            scada_data = sim.run_simulation()
            measurements.append(scada_data.get_data_pressures(sensor_locations=["n105"]).
                                flatten().tolist())
        print(np.mean(measurements, axis=0), np.var(measurements, axis=0))
        plot_timeseries_data(np.array(measurements),
                             labels=[f"Scenario {s_id}" for s_id in range(len(measurements))],
                             x_axis_label="Time (5min steps)", y_axis_label="Pressure in $m$")
