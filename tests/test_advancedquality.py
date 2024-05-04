"""
Module provides tests to test the advanced quality analysis.
"""
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.utils import to_seconds


def test_msx_net2cl2():
    # Load net2-cl2 scenario
    with ScenarioSimulator(f_inp_in="net2-cl2.inp", f_msx_in="net2-cl2.msx") as sim:
        # Set simulation duration to ten days
        sim.set_general_parameters(simulation_duration=to_seconds(days=10))

        # Monitor "CL2" bulk species at every node
        sim.set_bulk_species_node_sensors(sensor_info={"CL2": sim.sensor_config.nodes})

        # Run entire simulation
        res = sim.run_simulation(verbose=True)

        # Show sensor readings over the entire simulation
        assert res.get_data_bulk_species_node_concentration() is not None


def test_msx_Net3NH2CL():
    # Load Net3-NH2CL scenario
    with ScenarioSimulator(f_inp_in="Net3-NH2CL.inp", f_msx_in="Net3-NH2CL.msx") as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Monitor "HOCL" bulk species at every node and pipe
        sim.set_bulk_species_node_sensors(sensor_info={"HOCL": sim.sensor_config.nodes})
        sim.set_bulk_species_link_sensors(sensor_info={"HOCL": sim.sensor_config.links})

        # Run entire simulation
        res = sim.run_simulation()

        # Show sensor readings over the entire simulation
        assert res.get_data_bulk_species_node_concentration() is not None
        assert res.get_data_bulk_species_link_concentration() is not None


def test_msx_example():
    # Load example scenario
    with ScenarioSimulator(f_inp_in="example.inp", f_msx_in="example.msx") as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Monitor "AS5s" surface species at every node
        sim.set_surface_species_sensors(sensor_info={"AS5s": sim.sensor_config.links})

        # Run entire simulation
        res = sim.run_simulation()

        # Show sensor readings over the entire simulation
        assert res.get_data_surface_species_concentration() is not None
