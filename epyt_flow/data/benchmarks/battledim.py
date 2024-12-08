"""
The Battle of the Leakage Detection and Isolation Methods (*BattLeDIM*) 2020, organized by
S. G. Vrachimis, D. G. Eliades, R. Taormina, Z. Kapelan, A. Ostfeld, S. Liu, M. Kyriakou,
P. Pavlou, M. Qiu, and M. M. Polycarpou, as part of the 2nd International CCWI/WDSA Joint
Conference in Beijing, China, aims at objectively comparing the performance of methods for
the detection and localization of leakage events, relying on SCADA measurements of flow and
pressure sensors installed within water distribution networks.

See https://github.com/KIOS-Research/BattLeDIM for details.

This module provides functions for loading the original BattLeDIM data set
:func:`~epyt_flow.data.benchmarks.battledim.load_data`, as well as methods for loading the scenarios
:func:`~epyt_flow.data.benchmarks.battledim.load_scenario` and pre-generated SCADA data
:func:`~epyt_flow.data.benchmarks.battledim.load_scada_data`.
The official scoring/evaluation is implemented in
:func:`~epyt_flow.data.benchmarks.battledim.compute_evaluation_score` -- i.e. those results can be
directly compared to the official leaderboard results.
Besides this, the user can choose to evaluate predictions using any other metric from
:mod:`~epyt_flow.metrics`.
"""
from typing import Any, Union
import os
import math
from datetime import datetime
import functools
import scipy
import pandas as pd
import numpy as np
from scipy.sparse import bsr_array

from .battledim_data import START_TIME_TEST, START_TIME_TRAIN, LEAKS_CONFIG_TEST, \
    LEAKS_CONFIG_TRAIN
from ..networks import load_ltown
from ...simulation.events import AbruptLeakage, IncipientLeakage, Leakage
from ...simulation import ScenarioConfig
from ...topology import NetworkTopology
from ...simulation.scada import ScadaData
from ...utils import get_temp_folder, to_seconds, create_path_if_not_exist, download_if_necessary


def __parse_leak_config(start_time: str, leaks_config: str) -> list[Leakage]:
    leakages = []
    for leak in leaks_config.splitlines():
        # Parse entry
        items = [i.strip() for i in leak.split(",")]
        leaky_pipe_id = items[0]
        leak_start_time = int((datetime.strptime(items[1], "%Y-%m-%d %H:%M") - start_time)
                              .total_seconds())
        leak_end_time = int((datetime.strptime(items[2], "%Y-%m-%d %H:%M") - start_time)
                            .total_seconds())
        leak_diameter = float(items[3])
        leak_type = items[4]
        leak_peak_time = int((datetime.strptime(items[5], "%Y-%m-%d %H:%M") - start_time)
                             .total_seconds())

        # Create leak config
        if leak_type == "incipient":
            leak = IncipientLeakage(link_id=leaky_pipe_id, diameter=leak_diameter,
                                    start_time=leak_start_time, end_time=leak_end_time,
                                    peak_time=leak_peak_time)
        elif leak_type == "abrupt":
            leak = AbruptLeakage(link_id=leaky_pipe_id, diameter=leak_diameter,
                                 start_time=leak_start_time, end_time=leak_end_time)

        leakages.append(leak)

    return leakages


def __create_labels(n_time_steps: int, return_test_scenario: bool,
                    links: list[str]) -> tuple[np.ndarray, scipy.sparse.bsr_array]:
    y = np.zeros(n_time_steps)

    start_time = START_TIME_TEST if return_test_scenario is True else START_TIME_TRAIN
    leaks_config = LEAKS_CONFIG_TEST if return_test_scenario is True else LEAKS_CONFIG_TRAIN
    leakages = __parse_leak_config(start_time, leaks_config)

    def leak_time_to_idx(t: int, round_up: bool = False):
        if round_up is False:
            return math.floor(t / 300)
        else:
            return math.ceil(t / 300)

    leak_locations_row = []
    leak_locations_col = []
    for leak in leakages:
        t_idx_start = leak_time_to_idx(leak.start_time)
        t_idx_end = leak_time_to_idx(leak.end_time, round_up=True)
        y[t_idx_start:t_idx_end] = 1

        leak_link_idx = links.index(leak.link_id)
        for t in range(t_idx_end - t_idx_start):
            leak_locations_row.append(t_idx_start + t)
            leak_locations_col.append(leak_link_idx)

    y_leak_locations = bsr_array(
        (np.ones(len(leak_locations_row)), (leak_locations_row, leak_locations_col)),
        shape=(n_time_steps, len(links)))

    return y, y_leak_locations


def compute_evaluation_score(y_leak_locations_pred: list[tuple[str, int]],
                             test_scenario: bool, verbose: bool = True) -> dict:
    """
    Evaluates the predictions (i.e. start time and location of leakages) as it was done in the
    BattLeDIM competition -- i.e. the output of this functions can be directly compared
    to the official leaderboard results.

    Parameters
    ----------
    y_leak_locations_pred : `list[tuple[str, int]]`
        Predictions of location (link/pipe ID) and start time
        (in seconds since simulation start) of leakages.
    test_scenario : `bool`
        True if the given predictions are made for the test scenario, False otherwise.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading files.

        The default is True.

    Returns
    -------
    `dict`
        Dictionary containing the true positive rate, true positives, false positives,
        false negatives, and total monetary (Euro) savings (only available if `test_scenario`
        is True).
    """
    # Original MATLAB implementation:
    # https://github.com/KIOS-Research/BattLeDIM/blob/master/Scoring%20Algorithm/Scoring_Algorithm.m

    # Scoring parameters
    dist_max = 300      # Max pipe distance for leakage detection (meters)
    cost_water = .8     # Cost of water per m3 (Euro)
    cost_crew = 500     # Max repair crew cost per assignment (Euro)

    hydraulic_time_step = to_seconds(minutes=5)

    # Get WDN topology and find minimum topological distance (using the pipe lengths)
    # between all nodes
    f_topology_in = os.path.join(get_temp_folder(), "BattLeDIM", "ltown.epytflow_topology")
    url_topology = "https://filedn.com/lumBFq2P9S74PNoLPWtzxG4/EPyT-Flow/BattLeDIM/" +\
        "ltown.epytflow_topology"

    download_if_necessary(f_topology_in, url_topology, verbose)
    topology = NetworkTopology.load_from_file(f_topology_in)

    all_pairs_shortest_path_length = topology.get_all_pairs_shortest_path_length()

    # Load ground truth
    sim_start_time = START_TIME_TEST if test_scenario is True else START_TIME_TRAIN
    leaks_config = LEAKS_CONFIG_TEST if test_scenario is True else LEAKS_CONFIG_TRAIN
    leakages = __parse_leak_config(sim_start_time, leaks_config)
    n_leakages = len(leakages)

    leak_demands = {}
    if test_scenario is True:
        # Download leak demands
        for leak in leakages:
            f_in = f"Leak_{leak.link_id}.xlsx"
            url = "https://raw.githubusercontent.com/KIOS-Research/BattLeDIM/master/" + \
                f"Scoring%20Algorithm/competition_leakages/{f_in}"

            f_local_in = os.path.join(get_temp_folder(), "BattLeDIM", f_in)
            download_if_necessary(f_local_in, url, verbose)

            df_leak_demand = pd.read_excel(f_local_in, sheet_name="Demand (m3_h)")
            leak_demand = df_leak_demand[leak.link_id].to_numpy()
            leak_demands[leak.link_id] = leak_demand

    # Evaluate given predictions/alarms
    total_savings = 0
    true_positives = 0
    false_positives = 0
    detected_leaks = []

    leak_data = []
    for leak in leakages:
        leak_data.append((leak.link_id, leak.start_time, leak.end_time))

    def __find_closest_leaky_pipe(link_id) -> tuple[str, float, int]:
        closest_leaky_pipe_id = None
        closest_dist = float("inf")
        closest_start_time = None
        closest_end_time = None

        node_a, node_b = topology.get_link_info(link_id)["nodes"]

        for leak_pipe_id, start_time_leak, end_time_leak in leak_data:
            link_info = topology.get_link_info(leak_pipe_id)
            end_node_a, end_node_b = link_info["nodes"]
            link_length = link_info["length"]

            dists = []
            dists.append(all_pairs_shortest_path_length[node_a][end_node_a] + .5 * link_length)
            dists.append(all_pairs_shortest_path_length[node_a][end_node_b] + .5 * link_length)
            dists.append(all_pairs_shortest_path_length[node_b][end_node_a] + .5 * link_length)
            dists.append(all_pairs_shortest_path_length[node_b][end_node_b] + .5 * link_length)
            if min(dists) < closest_dist:
                closest_dist = min(dists)
                closest_leaky_pipe_id = leak_pipe_id
                closest_start_time = start_time_leak
                closest_end_time = end_time_leak

        return closest_leaky_pipe_id, closest_dist, closest_start_time, closest_end_time

    for pipe_id, start_time in y_leak_locations_pred:
        # Check if leakages was found and if so, how far away it is from the ground truth
        leaky_pipe_dist = None
        leaky_pipe = None
        if any(pipe_id == leaky_pipe_id and start_time >= start_time_leak and
               start_time <= end_time_leak and
               pipe_id not in detected_leaks
               for leaky_pipe_id, start_time_leak, end_time_leak in leak_data):
            leaky_pipe_dist = 0
            leaky_pipe = pipe_id
        else:
            closest_leaky_pipe_id, dist, start_time_leak, end_time_leak = \
                __find_closest_leaky_pipe(pipe_id)
            if start_time >= start_time_leak and start_time <= end_time_leak:
                leaky_pipe_dist = dist
                leaky_pipe = closest_leaky_pipe_id

        # Compute score of current alarm
        if leaky_pipe is not None:
            detected_leaks.append(leaky_pipe)
            true_positives += 1

            water_saved = 0
            if leaky_pipe in leak_demands:
                leak_demand = leak_demands[leaky_pipe]
                start_time_idx = math.ceil(start_time / hydraulic_time_step)
                water_saved = np.sum(leak_demand[start_time_idx:])
            total_savings += water_saved * cost_water - (leaky_pipe_dist / dist_max) * cost_crew
        else:
            false_positives += 1
            total_savings += -1. * cost_crew

    # Compute final scores
    false_negatives = n_leakages - true_positives
    true_positive_rate = true_positives / (true_positives + false_negatives)

    return {"true_positive_rate": true_positive_rate, "true_positives": true_positives,
            "false_positives": false_positives, "false_negatives": false_negatives,
            "total_savings": total_savings if test_scenario is True else None}


def load_data(return_test_scenario: bool, download_dir: str = None, return_X_y: bool = False,
              return_features_desc: bool = False, return_leak_locations: bool = False,
              verbose: bool = True) -> Union[pd.DataFrame, Any]:
    """
    Loads the original BattLeDIM benchmark data set.
    Note that the data set exists in two different version --
    a training version and an evaluation/test version.

    Parameters
    ----------
    return_test_scenario : `bool`
        If True, the evaluation/test data set is returned, otherwise the historical
        (i.e. training) data set is returned.
    download_dir : `str`, optional
        Path to the data files -- if None, the temp folder will be used.
        If the path does not exist, the data files will be downloaded to the given path.

        The default is None.
    return_X_y : `bool`, optional
        If True, the data is returned together with the labels (presence of a leakage) as
        two Numpy arrays, otherwise, the data is returned as a
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.

        The default is False.
    return_features_desc : `bool`, optional
        If True and if `return_X_y` is True, the returned dictionary contains the
        features' descriptions (i.e. names) under the key "features_desc".

        The default is False.
    return_leak_locations : `bool`
        If True, the leak locations are returned as well --
        as an instance of `scipy.sparse.bsr_array`.

        The default is False.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading files.

        The default is True.

    Returns
    -------
    Either a `pandas.DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ instance or a tuple of `Numpy arrays <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_.
        Benchmark data set.
    """
    # Download data files if necessary
    if return_test_scenario is True:
        url_data = "https://zenodo.org/records/4017659/files/2018_SCADA.xlsx?download=1"
        f_in = "2018_SCADA.xlsx"
    else:
        url_data = "https://zenodo.org/records/4017659/files/2019_SCADA.xlsx?download=1"
        f_in = "2019_SCADA.xlsx"

    download_dir = download_dir if download_dir is not None else get_temp_folder()
    download_dir = os.path.join(download_dir, "BattLeDIM")
    create_path_if_not_exist(download_dir)
    f_in = os.path.join(download_dir, f_in)

    download_if_necessary(f_in, url_data, verbose)

    # Load and parse data files
    df_pressures = pd.read_excel(f_in, sheet_name="Pressures (m)")
    df_pressures.columns = ["Timestamp"] + [f"Pressure_{n_id}" for n_id in df_pressures.columns[1:]]

    df_demands = pd.read_excel(f_in, sheet_name="Demands (L_h)")
    df_demands.columns = ["Timestamp"] + [f"Demand_{n_id}" for n_id in df_demands.columns[1:]]

    df_flows = pd.read_excel(f_in, sheet_name="Flows (m3_h)")
    df_flows.columns = ["Timestamp"] + [f"Flow_{l_id}" for l_id in df_flows.columns[1:]]

    df_levels = pd.read_excel(f_in, sheet_name="Levels (m)")
    df_levels.columns = ["Timestamp"] + [f"Level_{t_id}" for t_id in df_levels.columns[1:]]

    df_final = functools.reduce(lambda left, right: pd.merge(left, right, on="Timestamp"),
                                [df_pressures, df_flows, df_levels, df_demands])

    # Prepare and return final data
    if return_X_y is True:
        features_desc = list(df_final.columns)
        features_desc.remove("Timestamp")

        network_config = load_ltown(download_dir)
        links = network_config.sensor_config.links

        X = df_final[features_desc].to_numpy()
        y, y_leak_locations = __create_labels(X.shape[0], return_test_scenario, links)

        if return_features_desc is True:
            if return_leak_locations is True:
                return X, y, features_desc, y_leak_locations
            else:
                return X, y, features_desc
        else:
            if return_leak_locations is True:
                return X, y, y_leak_locations
            else:
                return X, y
    else:
        return df_final


def load_scada_data(return_test_scenario: bool, download_dir: str = None,
                    return_X_y: bool = False, return_leak_locations: bool = False,
                    verbose: bool = True) -> list[Union[ScadaData, Any]]:
    """
    Loads the SCADA data of the simulated BattLeDIM benchmark scenario -- note that due to
    randomness, these differ from the original data set which can be loaded by calling
    :func:`~epyt_flow.data.benchmarks.battledim.load_data`.

    .. warning::

        A large file (approx. 4GB) will be downloaded and loaded into memory --
        this might take some time.

    Parameters
    ----------
    return_test_scenario : `bool`
        If True, the evaluation/test scenario is returned, otherwise the historical
        (i.e. training) scenario is returned.
    download_dir : `str`, optional
        Path to the data files -- if None, the temp folder will be used.
        If the path does not exist, the data files will be downloaded to the given path.

        The default is None.
    return_X_y : `bool`, optional
        If True, the data is returned together with the labels (presence of a leakage) as
        two Numpy arrays, otherwise, the data is returned as a
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.

        The default is False.
    return_leak_locations : `bool`
        If True, the leak locations are returned as well --
        as an instance of `scipy.sparse.bsr_array`.

        The default is False.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading files.

        The default is True.

    Returns
    -------
    :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` or `list[tuple[numpy.ndarray, numpy.ndarray]]`
        The simulated benchmark scenario as either a
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance or as a tuple of
        (X, y) `Numpy arrays <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_.
        If 'return_leak_locations' is True, the leak locations are included
        as an instance of `scipy.sparse.bsr_array <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.bsr_array.html>`_ as well.
    """
    download_dir = download_dir if download_dir is not None else get_temp_folder()

    url_data = "https://filedn.com/lumBFq2P9S74PNoLPWtzxG4/EPyT-Flow/BattLeDIM/"

    f_in = f"{'battledim_test' if return_test_scenario else 'battledim_train'}.epytflow_scada_data"
    download_if_necessary(os.path.join(download_dir, f_in), url_data + f_in, verbose)

    data = ScadaData.load_from_file(os.path.join(download_dir, f_in))

    X = data.get_data()
    y, y_leak_locations = __create_labels(X.shape[0], return_test_scenario,
                                          data.sensor_config.links)

    if return_X_y is True:
        if return_leak_locations is True:
            return X, y, y_leak_locations
        else:
            return X, y
    else:
        if return_leak_locations is True:
            return data, y_leak_locations
        else:
            return data


def load_scenario(return_test_scenario: bool, download_dir: str = None,
                  verbose: bool = True) -> ScenarioConfig:
    """
    Creates and returns the BattLeDIM scenario -- it can be either modified or
    passed directly to the simulator
    :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`.

    .. note::

        Note that due to randomness, the simulation results differ from the original data set which
        can be loaded by calling :func:`~epyt_flow.data.benchmarks.battledim.load_data`.

    Parameters
    ----------
    return_test_scenario : `bool`
        If True, the evaluation/test scenario is returned, otherwise the historical
        (i.e. training) scenario is returned.
    download_dir : `str`, optional
        Path to the L-TOWN.inp file -- if None, the temp folder will be used.
        If the path does not exist, the .inp will be downloaded to the given path.

        The default is None.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading files.

        The default is True.

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Complete scenario configuration of the BattLeDIM benchmark scenario.
    """

    # Load L-Town network including the sensor placement
    if download_dir is not None:
        ltown_config = load_ltown(download_dir=download_dir, use_realistic_demands=True,
                                  include_default_sensor_placement=True, verbose=verbose)
    else:
        ltown_config = load_ltown(use_realistic_demands=True, include_default_sensor_placement=True,
                                  verbose=verbose)

    # Set simulation duration and other general parameters such as the demand model
    general_params = {"simulation_duration": to_seconds(days=365),    # One year
                      "hydraulic_time_step": to_seconds(minutes=5),   # 5min time steps
                      "reporting_time_step": to_seconds(minutes=5),
                      "demand_model": {"type": "PDA", "pressure_min": 0,
                                       "pressure_required": 0.1,
                                       "pressure_exponent": 0.5}
                      } | ltown_config.general_params

    # Add events
    start_time = START_TIME_TEST if return_test_scenario is True else START_TIME_TRAIN
    leaks_config = LEAKS_CONFIG_TEST if return_test_scenario is True else LEAKS_CONFIG_TRAIN
    leakages = __parse_leak_config(start_time, leaks_config)

    # Build final scenario
    return ScenarioConfig(f_inp_in=ltown_config.f_inp_in, general_params=general_params,
                          sensor_config=ltown_config.sensor_config, system_events=leakages)
