"""
Example of running an advanced quality analysis of Cl2 in Net2 using EPANET-MSX.
"""
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.utils import to_seconds, plot_timeseries_data


if __name__ == "__main__":
    # Load scenario for chlorine analysis in Net2
    with ScenarioSimulator(f_inp_in="net2-cl2.inp", f_msx_in="net2-cl2.msx") as sim:
        # Set simulation duration to 5 days
        sim.set_general_parameters(simulation_duration=to_seconds(days=5))

        # Monitor "CL2" bulk species at every node
        sim.set_bulk_species_node_sensors(sensor_info={"CL2": sim.sensor_config.nodes})

        # Run entire simulation
        scada_data = sim.run_simulation()

        # Show "CL2" concentration at the 11th node over the entire simulation
        conc = scada_data.get_data_bulk_species_node_concentration()
        plot_timeseries_data(conc[:, 10].reshape(1, -1),
                             x_axis_label="Time (60min steps)",
                             y_axis_label="Cl2 $mg/L$")
