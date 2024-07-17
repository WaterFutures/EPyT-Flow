"""
Module provides tests to test the
:class:`~epyt_flow.simulation.ScenarioSimulator` class.
"""
import os
from epyt_flow.data.networks import load_hanoi, load_ctown
from epyt_flow.data.benchmarks import load_leakdb_scenarios
from epyt_flow.simulation import ScenarioSimulator, ParallelScenarioSimulation, \
    callback_save_to_file
from epyt_flow.utils import to_seconds, create_path_if_not_exist

from .utils import get_temp_folder


def test_randomize_demands():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.randomize_demands()

        assert sim.sensor_config.get_as_dict() is not None
        assert sim.sensor_config.is_empty() is False

        sim.estimate_memory_consumption()
        res = sim.run_simulation()

        res.get_data()


def test_sensor_config():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder())
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.place_sensors_everywhere()

        assert sim.sensor_config.is_empty() is False

        sim.estimate_memory_consumption()
        res = sim.run_simulation()

        res.get_data()


def test_parallel_simulation():
    scenarios = load_leakdb_scenarios(range(5), use_net1=True, download_dir=get_temp_folder())

    folder_out = os.path.join(get_temp_folder(), "my_leakdb_results")
    create_path_if_not_exist(folder_out)
    ParallelScenarioSimulation.run(scenarios,
                                   callback=callback_save_to_file(folder_out=folder_out))


def test_export_to_epanet_files_1():
    f_inp_out = os.path.join(get_temp_folder(), "ctown_water-age.inp")

    network_config = load_ctown(download_dir=get_temp_folder())
    with ScenarioSimulator(scenario_config=network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.enable_waterage_analysis()

        sim.set_node_quality_sensors(sensor_locations=sim.sensor_config.nodes)

        sim.save_to_epanet_file(inp_file_path=f_inp_out)

    with ScenarioSimulator(f_inp_in=f_inp_out) as sim:
        pass


def test_export_to_epanet_files_2():
    f_msx_out = os.path.join(get_temp_folder(), "my_Net3-NH2CL.msx")

    with ScenarioSimulator(f_inp_in="Net3-NH2CL.inp", f_msx_in="Net3-NH2CL.msx") as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=3))
        sim.set_bulk_species_node_sensors(sensor_info={"HOCL": sim.sensor_config.nodes})
        sim.set_bulk_species_link_sensors(sensor_info={"HOCL": sim.sensor_config.links})

        sim.save_to_epanet_file(None, msx_file_path=f_msx_out)

    with ScenarioSimulator(f_inp_in="Net3-NH2CL.inp", f_msx_in=f_msx_out) as sim:
        pass
