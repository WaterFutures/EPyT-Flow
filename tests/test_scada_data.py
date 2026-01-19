"""
Module provides tests to test the :class:`epyt_flow.simulation.scada.ScadaData` class.
"""
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import ScenarioSimulator, EpanetConstants
from epyt_flow.utils import to_seconds

from .utils import get_temp_folder


def test_sensor_readings():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.randomize_demands()

        res = sim.run_simulation()

        assert len(res.get_data_pressures()) != 0
        assert len(res.get_data_flows()) != 0

        assert len(res.get_data_pressures(
            sensor_locations=[res.sensor_config.pressure_sensors[0]])) != 0
        assert len(res.get_data_flows(
            sensor_locations=[res.sensor_config.flow_sensors[0]])) != 0

def test_sensor_ordering():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        scada_data = sim.run_simulation()
        data_array = scada_data.get_data()
        assert data_array.shape[1] == 5
        sensor_config = scada_data.sensor_config
        assert sensor_config.get_index_of_reading(pressure_sensor='13') == 0
        assert sensor_config.get_index_of_reading(pressure_sensor='16') == 1
        assert sensor_config.get_index_of_reading(pressure_sensor='22') == 2
        assert sensor_config.get_index_of_reading(pressure_sensor='30') == 3
        assert sensor_config.get_index_of_reading(flow_sensor='1') == 4

def test_convert_unit():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        res = sim.run_simulation()

        res2 = res.convert_units()
        assert res == res2

        res2 = res.convert_units(flow_unit=EpanetConstants.EN_CFS)
        assert res != res2

