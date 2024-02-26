"""
Module provides tests to test different :class:`~epyt_flow.simulation.scada.ScadaData` exports.
"""
import os
import numpy as np
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator
from epyt_flow.simulation.scada import ScadaDataNumpyExport, ScadaDataXlsxExport, \
    ScadaDataMatlabExport

from .utils import get_temp_folder


def test_numpyexport():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)

        res = sim.run_simulation()
        data = res.get_data()
        time = res.sensor_readings_time

        f_out = os.path.join(get_temp_folder(), "numpy_export.npz")
        ScadaDataNumpyExport(f_out=f_out).export(res)

        data_restored = np.load(f_out)

        assert np.all(data == data_restored["sensor_readings"]) and \
            np.all(time == data_restored["sensor_readings_time"])


def test_xlsx_export():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)

        res = sim.run_simulation()

        f_out = os.path.join(get_temp_folder(), "excel_export.xlsx")
        ScadaDataXlsxExport(f_out=f_out).export(res)


def test_mat_export():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)

        res = sim.run_simulation()

        f_out = os.path.join(get_temp_folder(), "matlab_export.mat")
        ScadaDataMatlabExport(f_out=f_out).export(res)
