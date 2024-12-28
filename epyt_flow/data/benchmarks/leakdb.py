"""
LeakDB (Leakage Diagnosis Benchmark) by Vrachimis, S. G., Kyriakou, M. S., Eliades, D. G.,
and Polycarpou, M. M. (2018), is a realistic leakage dataset for water distribution networks.
The dataset is comprised of 1000 artificially created but realistic leakage
scenarios, on different water distribution networks, under varying conditions.

See https://github.com/KIOS-Research/LeakDB/ for details.

This module provides functions for loading the original LeakDB data set
:func:`~epyt_flow.data.benchmarks.leakdb.load_data`, as well as methods for loading the scenarios
:func:`~epyt_flow.data.benchmarks.leakdb.load_scenarios` and pre-generated SCADA data
:func:`~epyt_flow.data.benchmarks.leakdb.load_scada_data`.
The official scoring/evaluation is implemented in
:func:`~epyt_flow.data.benchmarks.leakdb.compute_evaluation_score` -- i.e. those results can be
directly compared to the official paper.
Besides this, the user can choose to evaluate predictions using any other metric from
:mod:`~epyt_flow.metrics`.
"""
import os
from typing import Union
import math
import json
import scipy
import numpy as np
import pandas as pd
from scipy.sparse import bsr_array

from ..networks import load_net1, load_hanoi
from .leakdb_data import NET1_LEAKAGES, HANOI_LEAKAGES
from ...utils import get_temp_folder, to_seconds, unpack_zip_archive, create_path_if_not_exist, \
    download_if_necessary
from ...metrics import f1_score, true_positive_rate, true_negative_rate
from ...simulation import ScenarioSimulator, ToolkitConstants
from ...simulation.events import AbruptLeakage, IncipientLeakage
from ...simulation import ScenarioConfig
from ...simulation.scada import ScadaData
from ...uncertainty import ModelUncertainty, UniformUncertainty


def __leak_time_to_idx(t: int, round_up: bool = False, hydraulic_time_step: int = 1800):
    if round_up is False:
        return math.floor(t / hydraulic_time_step)
    else:
        return math.ceil(t / hydraulic_time_step)


def __get_leak_time_windows(s_id: int, leaks_info: dict,
                            hydraulic_time_step: int = 1800) -> list[tuple[int, int]]:
    time_windows = []
    if str(s_id) in leaks_info:
        for leak in leaks_info[str(s_id)]:
            t_idx_start = __leak_time_to_idx(leak["leak_start_time"] * hydraulic_time_step)
            t_idx_end = __leak_time_to_idx(leak["leak_end_time"] * hydraulic_time_step,
                                           round_up=True)

            time_windows.append((t_idx_start, t_idx_end))

    return time_windows


def __create_labels(s_id: int, n_time_steps: int, nodes: list[str],
                    leaks_info: dict,
                    hydraulic_time_step: int = 1800) -> tuple[np.ndarray, scipy.sparse.bsr_array]:
    y = np.zeros(n_time_steps)

    leak_locations_row = []
    leak_locations_col = []
    if str(s_id) in leaks_info:
        for leak in leaks_info[str(s_id)]:
            t_idx_start = __leak_time_to_idx(leak["leak_start_time"] * hydraulic_time_step)
            t_idx_end = __leak_time_to_idx(leak["leak_end_time"] * hydraulic_time_step,
                                           round_up=True)

            leak_node_idx = nodes.index(leak["node_id"])

            for t in range(t_idx_end - t_idx_start):
                leak_locations_row.append(t_idx_start + t)
                leak_locations_col.append(leak_node_idx)

            y[t_idx_start:t_idx_end] = 1

    y_leak_locations = bsr_array(
        (np.ones(len(leak_locations_row)), (leak_locations_row, leak_locations_col)),
        shape=(n_time_steps, len(nodes)))

    return y, y_leak_locations


def compute_evaluation_score(scenarios_id: list[int], use_net1: bool,
                             y_pred_labels_per_scenario: list[np.ndarray]) -> dict:
    """
    Evaluates the predictions (leakage detection) for a list of given scenarios.

    Parameters
    ----------
    scenarios_id : `list[int]`
        List of scenarios ID that are to be evaluated -- there is a total number of 1000 scenarios.
    use_net1 : `bool`
        If True, Net1 LeakDB will be used for evaluation, otherwise the Hanoi LeakDB will be used.
    y_pred_labels_per_scenario : `list[numpy.ndarray] <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        Predicted binary labels (over time) for each scenario in `scenarios_id`.

    Returns
    -------
    `dict`
        Dictionary containing the f1-score, true positive rate, true negative rate,
        and early detection score.
    """
    # Original MATLAB implementation: https://github.com/KIOS-Research/LeakDB/blob/master/CCWI-WDSA2018/Scoring%20Function/scoring_algorithm.m
    if len(scenarios_id) != len(y_pred_labels_per_scenario):
        raise ValueError("Number of scenarios does not match number of predictions -- " +
                         f"expected {len(scenarios_id)} but got {len(y_pred_labels_per_scenario)}")

    # Load ground truth
    if use_net1 is True:
        leaks_info = json.loads(NET1_LEAKAGES)
    else:
        leaks_info = json.loads(HANOI_LEAKAGES)

    network_config = load_net1() if use_net1 is True \
        else load_hanoi()
    nodes = network_config.sensor_config.nodes

    y_true = []
    for i, s_id in enumerate(scenarios_id):
        y, _ = __create_labels(s_id, len(y_pred_labels_per_scenario[i]), nodes, leaks_info)
        if len(y) != len(y_pred_labels_per_scenario[i]):
            raise ValueError("A prediction must be provided for each time step -- " +
                             f"mismatch for scenario {i}, expected {len(y)} but got " +
                             f"{y_pred_labels_per_scenario[i]}")
        y_true.append(y)

    y_true = np.stack(y_true, axis=0)
    y_pred = np.stack(y_pred_labels_per_scenario, axis=0)

    # Evaluate predictions
    f1 = f1_score(y_pred, y_true)
    tpr = true_positive_rate(y_pred, y_true)
    tnr = true_negative_rate(y_pred, y_true)

    early_detection_score = 0
    normalizing = []
    n_time_steps_tolerance = 10
    detection_threshold = .75
    for i, s_id in enumerate(scenarios_id):
        y_pred_i = y_pred_labels_per_scenario[i]
        leaks_time_window = __get_leak_time_windows(s_id, leaks_info)

        scores = []
        for t0, _ in leaks_time_window:
            normalizing.append(1.)

            y_pred_window = y_pred_i[t0:t0+n_time_steps_tolerance]
            if 1 in y_pred_window and \
                    np.sum(y_pred_window) / len(y_pred_window) > detection_threshold:
                t_idx = np.argwhere(y_pred_window)[0] + 1
                scores.append(2. / (1 + np.exp((5. / n_time_steps_tolerance) * t_idx)))
            else:
                scores.append(0.)

        early_detection_score += np.sum(scores)

    early_detection_score = early_detection_score / np.sum(normalizing)

    return {"f1_score": f1, "true_positive_rate": tpr,
            "true_negative_rate": tnr, "early_detection_score": early_detection_score}


def load_data(scenarios_id: list[int], use_net1: bool, download_dir: str = None,
              return_X_y: bool = False, return_features_desc: bool = False,
              return_leak_locations: bool = False, verbose: bool = True) -> dict:
    """
    Loads the original LeakDB benchmark data set.

    .. warning::

        All scenarios together are a huge data set -- approx. 8GB for Net1 and 25GB for Hanoi.
        Downloading and loading might take some time! Also, a sufficient amount of hard disk
        memory is required.

    Parameters
    ----------
    scenarios_id : `list[int]`
        List of scenarios ID that are to be loaded -- there are a total number of 1000 scenarios.
    use_net1 : `bool`
        If True, Net1 LeakDB will be loaded, otherwise the Hanoi LeakDB will be loaded.
    download_dir : `str`, optional
        Path to the data files -- if None, the temp folder will be used.
        If the path does not exist, the data files will be downloaded to the given path.

        The default is None.
    return_X_y : `bool`, optional
        If True, the data is returned together with the labels (presence of a leakage) as
        two Numpy arrays, otherwise, the data is returned as Pandas data frames.

        The default is False.
    return_features_desc : `bool`, optional
        If True and if `return_X_y` is True, the returned dictionary contains the
        features' descriptions (i.e. names) under the key "features_desc".

        The default is False.
    return_leak_locations : `bool`
        If True and if `return_X_y` is True, the leak locations are returned as well --
        as an instance of `scipy.sparse.bsr_array <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.bsr_array.html>`_.

        The default is False.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading files.

        The default is True.

    Returns
    -------
    `dict`
        Dictionary containing the scenario data sets. Data of each requested scenario
        can be accessed by using the scenario ID as a key.
    """
    url_data = "https://filedn.com/lumBFq2P9S74PNoLPWtzxG4/EPyT-Flow/LeakDB-Original/" +\
        f"{'Net1_CMH/' if use_net1 is True else 'Hanoi_CMH/'}"

    if use_net1 is True:
        network_desc = "Net1"
        leaks_info = json.loads(NET1_LEAKAGES)
    else:
        network_desc = "Hanoi"
        leaks_info = json.loads(HANOI_LEAKAGES)

    download_dir = download_dir if download_dir is not None else get_temp_folder()
    download_dir = os.path.join(download_dir, network_desc)
    create_path_if_not_exist(download_dir)

    results = {}
    for s_id in scenarios_id:
        scenario_data = f"Scenario-{s_id}.zip"
        scenario_data_url = url_data + scenario_data
        scenario_data_file_in = os.path.join(download_dir, scenario_data)
        scenario_data_folder_in = os.path.join(download_dir, f"Scenario-{s_id}")

        download_if_necessary(scenario_data_file_in, scenario_data_url, verbose)
        create_path_if_not_exist(scenario_data_folder_in)
        unpack_zip_archive(scenario_data_file_in, scenario_data_folder_in)

        # Load and parse data
        pressure_files = list(filter(lambda d: d.endswith(".csv"),
                                     os.listdir(os.path.join(scenario_data_folder_in,
                                                             "Pressures"))))
        pressure_readings = {}
        all_nodes = []
        for f_in in pressure_files:
            df = pd.read_csv(os.path.join(scenario_data_folder_in, "Pressures", f_in))
            node_id = f_in.replace(".csv", "")
            all_nodes.append(node_id)
            pressure_readings[f"Pressure-{node_id}"] = df["Value"]

        flow_files = list(filter(lambda d: d.endswith(".csv"),
                                 os.listdir(os.path.join(scenario_data_folder_in, "Flows"))))
        flow_readings = {}
        for f_in in flow_files:
            df = pd.read_csv(os.path.join(scenario_data_folder_in, "Flows", f_in))
            flow_readings[f"Flow-{f_in.replace('.csv', '')}"] = df["Value"]

        df_labels = pd.read_csv(os.path.join(scenario_data_folder_in, "Labels.csv"))
        labels = df_labels["Label"]

        df_timestamps = pd.read_csv(os.path.join(scenario_data_folder_in, "Timestamps.csv"))
        sensor_reading_times = df_timestamps["Timestamp"]

        df_final = pd.DataFrame(pressure_readings | flow_readings |
                                {"labels": labels, "timestamps": sensor_reading_times})

        # Prepare final data
        if return_X_y is True:
            X = df_final[list(pressure_readings.keys()) + list(flow_readings.keys())].to_numpy()
            y = labels.to_numpy()

            network_config = load_net1(download_dir) if use_net1 is True \
                else load_hanoi(download_dir)
            nodes = network_config.sensor_config.nodes
            _, y_leak_locations = __create_labels(s_id, X.shape[0], nodes, leaks_info)

            if return_features_desc is True and "features_desc" not in results:
                results["features_desc"] = list(pressure_readings.keys()) + \
                    list(flow_readings.keys())

            if return_leak_locations is True:
                results[s_id] = (X, y, y_leak_locations)
            else:
                results[s_id] = (X, y)
        else:
            results[s_id] = df_final

    return results


def load_scada_data(scenarios_id: list[int], use_net1: bool = True, download_dir: str = None,
                    return_X_y: bool = False, return_leak_locations: bool = False,
                    verbose: bool = True
                    ) -> Union[list[ScadaData], list[tuple[np.ndarray, np.ndarray]]]:
    """
    Loads the SCADA data of the simulated LeakDB benchmark scenarios -- see
    :func:`~epyt_flow.data.benchmarks.leakdb.load_scenarios`.

    .. note::
        Note that due to the randomness in the demand creation as well as in the model
        uncertainties, the SCADA data differs from the original data set
        which can be loaded by calling :func:`~epyt_flow.data.benchmarks.leakdb.load_data`.
        However, the leakages (i.e. location and profile) are consistent with the original data set.

    Parameters
    ----------
    scenarios_id : `list[int]`
        List of scenarios ID that are to be loaded -- there are a total number of 1000 scenarios.
    use_net1 : `bool`, optional
        If True, Net1 LeakDB will be loaded, otherwise the Hanoi LeakDB will be loaded.

        The default is True.
    download_dir : `str`, optional
        Path to the data files -- if None, the temp folder will be used.
        If the path does not exist, the data files will be downloaded to the given path.

        The default is None.
    return_X_y : `bool`, optional
        If True, the data is returned together with the labels (presence of a leakage) as
        two Numpy arrays, otherwise, the data is returned as
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances.

        The default is False.
    return_leak_locations : `bool`
        If True, the leak locations are returned as well --
        as an instance of `scipy.sparse.bsr_array <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.bsr_array.html>`_.

        The default is False.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading files.

        The default is True.

    Returns
    -------
    list[`:class:`~epyt_flow.simulation.scada.scada_data.ScadaData`] or `list[tuple[numpy.ndarray, numpy.ndarray]]`
        The simulated benchmark scenarios as either a list of
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances or as a list of
        (X, y) Numpy arrays. If 'return_leak_locations' is True, the leak locations are included
        as an instance of `scipy.sparse.bsr_array <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.bsr_array.html>`_ as well.
    """
    download_dir = download_dir if download_dir is not None else get_temp_folder()

    url_data = "https://filedn.com/lumBFq2P9S74PNoLPWtzxG4/EPyT-Flow/LeakDB/" +\
        f"{'Net1/' if use_net1 is True else 'Hanoi/'}"

    if use_net1 is True:
        leaks_info = json.loads(NET1_LEAKAGES)
    else:
        leaks_info = json.loads(HANOI_LEAKAGES)

    r = []

    for s_id in scenarios_id:
        f_in = f"{'Net1_ID' if use_net1 is True else 'Hanoi_ID'}={s_id}.epytflow_scada_data"
        download_if_necessary(os.path.join(download_dir, f_in), url_data + f_in, verbose)

        data = ScadaData.load_from_file(os.path.join(download_dir, f_in))

        X = data.get_data()
        y, y_leak_locations = __create_labels(s_id, X.shape[0], data.sensor_config.nodes,
                                              leaks_info)

        if return_X_y is True:
            if return_leak_locations is True:
                r.append((X, y, y_leak_locations))
            else:
                r.append((X, y))
        else:
            if return_leak_locations is True:
                r.append((data, y_leak_locations))
            else:
                r.append(data)

    return r


def load_scenarios(scenarios_id: list[int], use_net1: bool = True,
                   download_dir: str = None, verbose: bool = True) -> list[ScenarioConfig]:
    """
    Creates and returns the LeakDB scenarios -- they can be either modified or
    passed directly to the simulator
    :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`.

    .. note::
        Note that due to the randomness in the demand creation as well as in the model
        uncertainties, the simulation results will differ between different runs, and
        will also differ from the original data set
        (see :func:`~epyt_flow.data.benchmarks.leakdb.load_data`).
        However, the leakages (i.e. location and profile) will be always the same and be
        consistent with the original data set.

    Parameters
    ----------
    scenarios_id : `list[int]`
        List of scenarios ID that are to be loaded -- there is a total number of 1000 scenarios.
    use_net1 : `bool`, optional
        If True, Net1 network will be used, otherwise the Hanoi network will be used.

        The default is True.
    download_dir : `str`, optional
        Path to the Net1.inp or Hanoi.inp file -- if None, the temp folder will be used.
        If the path does not exist, the .inp will be downloaded to the give path.

        The default is None.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading files.

        The default is True.

    Returns
    -------
    list[:class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`]
        LeakDB scenarios.
    """
    scenarios_inp = []

    # Load the network
    load_network = load_net1 if use_net1 is True else load_hanoi
    download_dir = download_dir if download_dir is not None else get_temp_folder()
    network_config = load_network(download_dir)

    # Set simulation duration and other general parameters such as the demand model and flow units
    hydraulic_time_step = to_seconds(minutes=30)    # 30min time steps
    general_params = {"simulation_duration": to_seconds(days=365),   # One year
                      "hydraulic_time_step": hydraulic_time_step,
                      "reporting_time_step": hydraulic_time_step,
                      "flow_units_id": ToolkitConstants.EN_CMH,
                      "demand_model": {"type": "PDA", "pressure_min": 0,
                                       "pressure_required": 0.1,
                                       "pressure_exponent": 0.5}
                      } | network_config.general_params

    # Add demand patterns
    def gen_dem(download_dir):
        # Taken from https://github.com/KIOS-Research/LeakDB/blob/master/CCWI-WDSA2018/Dataset_Generator_Py3/demandGenerator.py
        week_pat = scipy.io.loadmat(os.path.join(download_dir, "weekPat_30min.mat"))
        a_w = week_pat['Aw']
        nw = week_pat['nw']
        year_offset = scipy.io.loadmat(os.path.join(download_dir, "yearOffset_30min.mat"))
        a_y = year_offset['Ay']
        ny = year_offset['ny']

        # Create yearly component
        days = 365

        t = (288/6)*days    # one year period in five minute intervals
        w = 2*np.pi/t
        k = np.arange(1, days*288/6+1, 1)   # number of time steps in time series
        n = ny[0][0]    # number of fourier coefficients
        h_y = [1]*len(k)

        for i in range(1, n+1):
            h_y = np.column_stack((h_y, np.sin(i*w*k), np.cos(i*w*k)))

        unc_y = 0.1
        a_y_r = a_y*(1-unc_y + 2*unc_y*np.random.rand(int(a_y.shape[0]), int(a_y.shape[1])))
        year_offset = np.dot(h_y, a_y_r)

        # Create weekly component
        t = (288/6)*7   # one week period in five minute intervals
        w = 2*np.pi/t
        k = np.arange(1, days*288/6+1, 1)   # number of time steps in time series
        n = nw[0][0]    # number of fourier coefficients
        h_w = [1]*len(k)
        for i in range(1, n+1):
            h_w = np.column_stack((h_w, np.sin(i*w*k), np.cos(i*w*k)))

        unc_w = 0.1
        a_w_r = a_w*(1-unc_w + 2*unc_w*np.random.rand(int(a_w.shape[0]), int(a_w.shape[1])))
        week_year_pat = np.dot(h_w, a_w_r)

        # Create random component
        unc_r = 0.05
        random = np.random.normal(0, (-unc_r+2*unc_r),
                                  (int(week_year_pat.shape[0]), int(week_year_pat.shape[1])))

        # Create demand
        base = 1
        variation = 0.75 + np.random.normal(0, 0.07)  # from 0 to 1
        dem = base * (year_offset+1) * (week_year_pat*variation+1) * (random+1)

        dem = dem.tolist()
        dem_final = []
        for d in dem:
            dem_final.append(d[0])

        return dem_final

    week_pattern_url = "https://filedn.com/lumBFq2P9S74PNoLPWtzxG4/EPyT-Flow/Networks/CCWI-WDSA2018/" +\
        "Dataset_Generator_Py3/weekPat_30min.mat"
    year_offset_url = "https://filedn.com/lumBFq2P9S74PNoLPWtzxG4/EPyT-Flow/Networks/CCWI-WDSA2018/" +\
        "Dataset_Generator_Py3/yearOffset_30min.mat"

    download_if_necessary(os.path.join(download_dir, "weekPat_30min.mat"),
                          week_pattern_url, verbose)
    download_if_necessary(os.path.join(download_dir, "yearOffset_30min.mat"),
                          year_offset_url, verbose)

    for s_id in scenarios_id:   # Create new .inp files with demands if necessary
        f_inp_in = os.path.join(download_dir,
                                f"{'Net1' if use_net1 is True else 'Hanoi'}_LeakDB_ID={s_id}.inp")
        scenarios_inp.append(f_inp_in)

        if not os.path.exists(f_inp_in):
            with ScenarioSimulator(f_inp_in=network_config.f_inp_in) as wdn:
                wdn.set_general_parameters(**general_params)
                wdn.epanet_api.setTimePatternStep(hydraulic_time_step)

                wdn.epanet_api.deletePatternsAll()

                reservoir_nodes_id = wdn.epanet_api.getNodeReservoirNameID()
                for node_id in network_config.sensor_config.nodes:
                    if node_id in network_config.sensor_config.tanks or\
                            node_id in reservoir_nodes_id:
                        continue

                    node_idx = wdn.epanet_api.getNodeIndex(node_id)
                    base_demand = wdn.epanet_api.getNodeBaseDemands(node_idx)[1][0]

                    my_demand_pattern = np.array(gen_dem(download_dir))

                    wdn.set_node_demand_pattern(node_id=node_id, base_demand=base_demand,
                                                demand_pattern_id=f"demand_{node_id}",
                                                demand_pattern=my_demand_pattern)

                wdn.epanet_api.saveInputFile(f_inp_in)

    # Create uncertainties
    class MyUniformUncertainty(UniformUncertainty):
        """
        Custom uniform uncertainty for LeakDB scenarios.
        """
        def __init__(self, **kwds):
            super().__init__(**kwds)

        def apply(self, data: float) -> float:
            z = data * np.random.uniform(low=self.low, high=self.high)
            lower = data - z
            upper = data + z
            return lower + np.random.uniform() * (upper - lower)

    my_uncertainties = {"global_pipe_length_uncertainty": MyUniformUncertainty(low=0, high=0.25),
                        "global_pipe_roughness_uncertainty": MyUniformUncertainty(low=0, high=0.25),
                        "global_base_demand_uncertainty": MyUniformUncertainty(low=0, high=0.25)}
    model_uncertainty = ModelUncertainty(**my_uncertainties)

    # Create sensor config (place pressure and flow sensors everywhere)
    sensor_config = network_config.sensor_config
    sensor_config.pressure_sensors = sensor_config.nodes
    sensor_config.flow_sensors = sensor_config.links

    # Add leakages
    leaks_all = []

    if use_net1 is True:
        leaks_info = json.loads(NET1_LEAKAGES)
    else:
        leaks_info = json.loads(HANOI_LEAKAGES)

    for s_id in scenarios_id:
        leaks_data = []

        if str(s_id) in leaks_info:
            for leak in leaks_info[str(s_id)]:
                if leak["leak_type"] == "incipient":
                    leaks_data.append(
                        IncipientLeakage(node_id=leak["node_id"], link_id=None,
                                         diameter=leak["leak_diameter"],
                                         start_time=leak["leak_start_time"] * hydraulic_time_step,
                                         end_time=leak["leak_end_time"] * hydraulic_time_step,
                                         peak_time=leak["leak_peak_time"] * hydraulic_time_step))
                else:
                    leaks_data.append(
                        AbruptLeakage(node_id=leak["node_id"], link_id=None,
                                      diameter=leak["leak_diameter"],
                                      start_time=leak["leak_start_time"] * hydraulic_time_step,
                                      end_time=leak["leak_end_time"] * hydraulic_time_step))

        leaks_all.append(leaks_data)

    # Build final scenarios
    return [ScenarioConfig(f_inp_in=f_inp_in, general_params=general_params,
                           sensor_config=sensor_config, model_uncertainty=model_uncertainty,
                           system_events=leaks)
            for f_inp_in, leaks in zip(scenarios_inp, leaks_all)]
