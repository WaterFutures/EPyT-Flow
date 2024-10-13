"""
Minimalistic usage example of EPyt-Flow.
"""
from epyt_flow.simulation.scada.scada_data_export import ScadaDataXlsxExport
from epyt_flow.data.benchmarks import load_leakdb_scenarios
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.utils import to_seconds, plot_timeseries_data


if __name__ == "__main__":
    # Load first Hanoi scenario from LeakDB
    network_config, = load_leakdb_scenarios(scenarios_id=["1"], use_net1=False)

    # Create scenario
    with ScenarioSimulator(scenario_config=network_config) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Place pressure sensors at nodes "13", "16", "22", and "30"
        sim.set_pressure_sensors(sensor_locations=["13", "16", "22", "30"])

        # Place a flow sensor at link/pipe "1"
        sim.set_flow_sensors(sensor_locations=["1"])

        # Run entire simulation
        scada_data = sim.run_simulation()

        # Export data in excel
        ScadaDataXlsxExport(f_out="myHanoiResults.xlsx").export(scada_data)

        # Print & plot sensor readings over the entire simulation
        print(f"Pressure readings: {scada_data.get_data_pressures()}")
        print(f"Flow readings: {scada_data.get_data_flows()}")

        plot_timeseries_data(scada_data.get_data_pressures().T,
                             labels=[f"Node {n_id}" for n_id in
                                     scada_data.sensor_config.pressure_sensors],
                             x_axis_label="Time (30min steps)", y_axis_label="Pressure in $m$")
        plot_timeseries_data(scada_data.get_data_flows().T,
                             x_axis_label="Time (30min steps)", y_axis_label="Flow rate in $m^3/h$")
