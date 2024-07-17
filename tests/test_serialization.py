"""
Module provides tests to test the serialization module.
"""
import os
import scipy
import numpy as np
from epyt_flow.data.networks import load_hanoi, load_net1
from epyt_flow.simulation import ScenarioSimulator, SensorConfig, ScenarioConfig, ScadaData, \
    ToolkitConstants
from epyt_flow.utils import to_seconds
from epyt_flow.serialization import load, dump

from .utils import get_temp_folder


def test_sensorconfig():
    sensor_config = SensorConfig(nodes=["0", "1", "2"], links=["0", "1"],
                                 flow_unit=ToolkitConstants.EN_GPM,
                                 valves=[], pumps=[], tanks=[], pressure_sensors=["2"],
                                 bulk_species=[], surface_species=[])
    sensor_config_restored = SensorConfig.load(sensor_config.dump())

    assert sensor_config == sensor_config_restored


def test_scenarioconfig():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        assert ScenarioConfig.load(sim.get_scenario_config().dump()) == sim.get_scenario_config()


def test_scadadata():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)

        res = sim.run_simulation()

        f = os.path.join(get_temp_folder(), "my_hanoi.epytflow_scada_data")
        res.save_to_file(f)
        res_loaded = ScadaData.load_from_file(f)

        assert res == res_loaded

        f = os.path.join(get_temp_folder(), "my_hanoi_2.epytflow_scada_data")
        with open(f, "wb") as f_out:
            res.dump(f_out)

        with open(f, "rb") as f_in:
            res_loaded = ScadaData.load(f_in)
            assert res == res_loaded


def test_topology():
    # Load Net1 network
    network_config = load_net1(download_dir=get_temp_folder())

    # Create scenario
    with ScenarioSimulator(scenario_config=network_config) as sim:
        graph = sim.get_topology()

        g = load(dump(graph))

        assert list(graph.nodes(data=True)) == list(g.nodes(data=True))


def test_sparse_matrix():
    m = scipy.sparse.bsr_array(scipy.sparse.random(100, 20, density=0.1, format="bsr"))

    m_rec = load(dump(m))

    assert np.all(m.todense() == m_rec.todense())
