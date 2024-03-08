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
"""
from typing import Any
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


def load_data(return_test_scenario: bool, download_dir: str = None, return_X_y: bool = False,
              return_features_desc: bool = False, return_leak_locations: bool = False) -> Any:
    """
    Laods the original BattLeDIM benchmark data set.
    Note that the data set exists in two different version --
    a training version and an evaluation/test version.

    Parameters
    ----------
    return_test_scenario : `bool`
        If True, the evaluation/test data set is returned, otherwise the historical
        (i.e. training) data set is returned.
    download_dir : `str`, optional
        Path to the data files -- if None, the temp folder will be used.
        If the path does not exist, the data files will be downloaded to the give path.

        The default is None.
    return_X_y : `bool`, optional
        If True, the data is returned together with the labels (presence of a leakage) as
        two Numpy arrays, otherwise the data is returned as a
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.

        The default is False.
    return_features_desc : `bool`, optional
        If True and if `return_X_y` is True, the returned dictionary contains the
        features' describtions (i.e. names) under the key "features_desc".

        The default is False.
    return_leak_locations : `bool`
        If True, the leak locations are returned as well --
        as an instance of `scipy.sparse.bsr_array`.

        The default is False.

    Returns
    -------
    Either a `pandas.DataFrame` instance or a tuple of Numpy arrays.
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

    download_if_necessary(f_in, url_data)

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
                    return_X_y: bool = False, return_leak_locations: bool = False) -> list[Any]:
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
        If the path does not exist, the data files will be downloaded to the give path.

        The default is None.
    return_X_y : `bool`, optional
        If True, the data is returned together with the labels (presence of a leakage) as
        two Numpy arrays, otherwise the data is returned as a
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.

        The default is False.
    return_leak_locations : `bool`
        If True, the leak locations are returned as well --
        as an instance of `scipy.sparse.bsr_array`.

        The default is False.

    Returns
    -------
    :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` or `list[tuple[numpy.ndarray, numpy.ndarray]]`
        The simulated benchmark scenario as either a
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance or as a tuple of
        (X, y) Numpy arrays. If 'return_leak_locations' is True, the leak locations are included
        as an instance of `scipy.sparse.bsr_array` as well.
    """
    download_dir = download_dir if download_dir is not None else get_temp_folder()

    url_data = "https://filedn.com/lumBFq2P9S74PNoLPWtzxG4/EPyT-Flow/BattLeDIM/"

    f_in = f"{'battledim_test' if return_test_scenario else 'battledim_train'}.epytflow_scada_data"
    download_if_necessary(os.path.join(download_dir, f_in), url_data + f_in)

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


def load_scenario(return_test_scenario: bool, download_dir: str = None) -> ScenarioConfig:
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
        If the path does not exist, the .inp will be downloaded to the give path.

        The default is None.

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Complete scenario configuration of the BattLeDIM benchmark scenario.
    """

    # Load L-Town network including the sensor placement
    if download_dir is not None:
        ltown_config = load_ltown(download_dir=download_dir, use_realistic_demands=True,
                                  include_default_sensor_placement=True)
    else:
        ltown_config = load_ltown(use_realistic_demands=True, include_default_sensor_placement=True)

    # Set simulation duration
    general_params = {"simulation_duration": to_seconds(days=365),   # One year
                      "hydraulic_time_step": 300}   # 5min time steps

    # Add events
    start_time = START_TIME_TEST if return_test_scenario is True else START_TIME_TRAIN
    leaks_config = LEAKS_CONFIG_TEST if return_test_scenario is True else LEAKS_CONFIG_TRAIN
    leakages = __parse_leak_config(start_time, leaks_config)

    # Build final scenario
    return ScenarioConfig(f_inp_in=ltown_config.f_inp_in, general_params=general_params,
                          sensor_config=ltown_config.sensor_config, system_events=leakages)
