"""
Module provides tests to test the advanced quality analysis.
"""
import os
import random
from epyt_flow.simulation import ScenarioSimulator, SENSOR_TYPE_NODE_BULK_SPECIES, \
    SENSOR_TYPE_LINK_BULK_SPECIES
from epyt_flow.simulation.events import SensorFaultStuckZero
from epyt_flow.utils import to_seconds


def test_msx_net2cl2():
    # Load net2-cl2 scenario
    with ScenarioSimulator(f_inp_in=os.path.join("tests", "net2-cl2.inp"),
                           f_msx_in=os.path.join("tests", "net2-cl2.msx")) as sim:
        # Set simulation duration to ten days
        sim.set_general_parameters(simulation_duration=to_seconds(days=10))

        # Monitor "CL2" bulk species at every node
        sim.set_bulk_species_node_sensors(sensor_info={"CL2": sim.sensor_config.nodes})

        # Add sensor fault
        node_id = random.choice(sim.sensor_config.nodes)
        sim.add_sensor_fault(SensorFaultStuckZero(sensor_id=node_id,
                                                  sensor_type=SENSOR_TYPE_NODE_BULK_SPECIES,
                                                  start_time=to_seconds(days=1),
                                                  end_time=to_seconds(days=3)))

        # Run entire simulation
        res = sim.run_simulation(verbose=True)

        # Show sensor readings over the entire simulation
        assert res.get_data_bulk_species_node_concentration() is not None


def test_msx_net2cl2_place_sensors_everywhere():
    # Load net2-cl2 scenario
    with ScenarioSimulator(f_inp_in=os.path.join("tests", "net2-cl2.inp"),
                           f_msx_in=os.path.join("tests", "net2-cl2.msx")) as sim:
        # Set simulation duration to ten days
        sim.set_general_parameters(simulation_duration=to_seconds(days=10))

        # Monitor "CL2" bulk species at every node
        sim.place_bulk_species_node_sensors_everywhere()
        sim.place_bulk_species_link_sensors_everywhere()

        # Place sensor faults
        link_id = random.choice(sim.sensor_config.links)
        sim.add_sensor_fault(SensorFaultStuckZero(sensor_id=link_id,
                                                  sensor_type=SENSOR_TYPE_LINK_BULK_SPECIES,
                                                  start_time=to_seconds(days=4),
                                                  end_time=to_seconds(days=5)))

        # Run entire simulation
        res = sim.run_simulation(verbose=True)

        # Show sensor readings over the entire simulation
        assert res.get_data_bulk_species_node_concentration() is not None
        assert res.get_data_bulk_species_link_concentration() is not None


def test_msx_net2cl2_place_sensors_everywhere2():
    # Load net2-cl2 scenario
    with ScenarioSimulator(f_inp_in=os.path.join("tests", "net2-cl2.inp"),
                           f_msx_in=os.path.join("tests", "net2-cl2.msx")) as sim:
        # Set simulation duration to ten days
        sim.set_general_parameters(simulation_duration=to_seconds(days=10))

        # Monitor "CL2" bulk species at every node
        sim.place_bulk_species_node_sensors_everywhere(["CL2"])
        sim.place_bulk_species_link_sensors_everywhere(["CL2"])

        # Run entire simulation
        res = sim.run_simulation(verbose=True)

        # Show sensor readings over the entire simulation
        assert res.get_data_bulk_species_node_concentration() is not None
        assert res.get_data_bulk_species_link_concentration() is not None


def test_msx_Net3NH2CL():
    # Load Net3-NH2CL scenario
    with ScenarioSimulator(f_inp_in=os.path.join("tests", "Net3-NH2CL.inp"),
                           f_msx_in=os.path.join("tests", "Net3-NH2CL.msx")) as sim:
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
    with ScenarioSimulator(f_inp_in=os.path.join("tests", "example.inp"),
                           f_msx_in=os.path.join("tests", "example.msx")) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Monitor "AS5s" surface species at every node
        sim.set_surface_species_sensors(sensor_info={"AS5s": sim.sensor_config.links})

        # Run entire simulation
        res = sim.run_simulation()

        # Show sensor readings over the entire simulation
        assert res.get_data_surface_species_concentration() is not None
