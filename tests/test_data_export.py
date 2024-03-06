"""
Module provides tests to test different :class:`~epyt_flow.simulation.scada.ScadaData` exports.
"""
import os
import numpy as np
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import ScenarioSimulator, ScadaData
from epyt_flow.simulation.scada import ScadaDataNumpyExport, ScadaDataXlsxExport, \
    ScadaDataMatlabExport
from epyt_flow.utils import to_seconds

from .utils import get_temp_folder


def test_customformat():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        res = sim.run_simulation()

        f_out = os.path.join(get_temp_folder(), "data_export.epytflow_scada_data")
        res.save_to_file(f_out)

        res_restored = ScadaData.load_from_file(f_out)
        assert res == res_restored


def test_numpyexport():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        res = sim.run_simulation()
        data = res.get_data()
        time = res.sensor_readings_time

        f_out = os.path.join(get_temp_folder(), "numpy_export_raw.npz")
        ScadaDataNumpyExport(f_out=f_out, export_raw_data=True).export(res)

        f_out = os.path.join(get_temp_folder(), "numpy_export.npz")
        ScadaDataNumpyExport(f_out=f_out).export(res)

        data_restored = np.load(f_out)

        assert np.all(data == data_restored["sensor_readings"]) and \
            np.all(time == data_restored["sensor_readings_time"])


def test_xlsx_export():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        res = sim.run_simulation()

        f_out = os.path.join(get_temp_folder(), "excel_export_raw.xlsx")
        ScadaDataXlsxExport(f_out=f_out, export_raw_data=True).export(res)

        f_out = os.path.join(get_temp_folder(), "excel_export.xlsx")
        ScadaDataXlsxExport(f_out=f_out).export(res)


def test_mat_export():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        res = sim.run_simulation()

        f_out = os.path.join(get_temp_folder(), "matlab_export_raw.mat")
        ScadaDataMatlabExport(f_out=f_out, export_raw_data=True).export(res)

        f_out = os.path.join(get_temp_folder(), "matlab_export.mat")
        ScadaDataMatlabExport(f_out=f_out).export(res)
