"""
The BATtle of the Attack Detection ALgorithms (*BATADAL*) by Riccardo Taormina, Stefano Galelli,
Nils Ole Tippenhauer, Avi Ostfeld, Elad Salomons, Demetrios Eliades is a competition on planning
and management of water networks undertaken within the Water Distribution Systems Analysis
Symposium. The goal of the battle was to compare the performance of algorithms for the detection
of cyber-physical attacks, whose frequency has increased in the last few years along with the
adoption of smart water technologies. The design challenge was set for the C-Town network,
a real-world, medium-sized water distribution system operated through programmable logic
controllers and a supervisory control and data acquisition (SCADA) system. Participants were
provided with data sets containing (simulated) SCADA observations, and challenged to design
an attack detection algorithm. The effectiveness of all submitted algorithms was evaluated in
terms of time-to-detection and classification accuracy. Seven teams participated in the battle
and proposed a variety of successful approaches leveraging data analysis, model-based detection
mechanisms, and rule checking. Results were presented at the Water Distribution Systems Analysis
Symposium (World Environmental and Water Resources Congress) in Sacramento, California on
May 21-25, 2017.
The `paper <https://doi.org/10.1061/(ASCE)WR.1943-5452.0000969>`_ summarizes the BATADAL
problem, proposed algorithms, results, and future research directions.

See https://www.batadal.net/ for details.

This module provides functions for loading the original BATADAL data set
:func:`~epyt_flow.data.benchmarks.batadal.load_data`, as well as functions for loading the
scenarios :func:`~epyt_flow.data.benchmarks.batadal.load_scenario` and pre-generated
SCADA data :func:`~epyt_flow.data.benchmarks.batadal.load_scada_data`.
"""
import os
from typing import Any
from datetime import datetime
import pandas as pd
import numpy as np

from .batadal_data import TRAINING_DATA_2_ATTACKS_TIME, TRAINING_DATA_2_START_TIME, \
    TEST_DATA_ATTACKS_TIME, TEST_DATA_START_TIME
from ...utils import get_temp_folder, unpack_zip_archive, to_seconds, download_if_necessary
from ...simulation import ScenarioConfig


def __parse_attacks_time(start_time: str, attacks_time):
    events = []
    for event in attacks_time.splitlines():
        # Parse entry
        items = [i.strip() for i in event.split(",")]

        event_start_time = int((datetime.strptime(items[0], "%d/%m/%Y %H:%M") - start_time)
                               .total_seconds())
        event_end_time = int((datetime.strptime(items[1], "%d/%m/%Y %H:%M") - start_time)
                             .total_seconds())

        events.append((event_start_time, event_end_time))

    return events


def load_data(download_dir: str = None, return_X_y: bool = False,
              return_ground_truth: bool = False, return_features_desc: bool = False,
              verbose: bool = True) -> dict:
    """
    Loads the original BATADAL competition data.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the data files -- if None, the temp folder will be used.
        If the path does not exist, the data files will be downloaded to the given path.

        The default is None.
    return_X_y : `bool`, optional
        If True, the data together with the labels is returned as pairs of Numpy arrays.
        Otherwise, the data is returned as Pandas data frames.

        The default is False.
    return_ground_truth : `bool`
        If True and if `return_X_y` is True, the ground truth labels are included in the
        returned dictionary -- note that the labels provided in the benchmark constitute
        a partial labeling only.

        The default is False.
    return_features_desc : `bool`
        If True and if `return_X_y` is True, feature names (i.e. descriptions) are included
        in the returned dictionary.

        The default is False.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading files.

        The default is True.

    Returns
    -------
    `dict`
        Dictionary of the loaded benchmark data. The dictionary contains the two training
        data sets ("train_1" and "train_2"), as well as the test data set ("test").
        If `return_X_y` is False, each dictionary entry is a `Pandas dataframe <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_.
        Otherwise, it is a tuple of sensor readings and labels (except for the test set) --
        if `return_ground_truth` is True or `return_features_desc` is True, the corresponding
        data is appended to the tuple.
    """
    download_dir = download_dir if download_dir is not None else get_temp_folder()

    # Download data
    training_data_1_url = "https://www.batadal.net/data/BATADAL_dataset03.csv"
    training_data_2_url = "https://www.batadal.net/data/BATADAL_dataset04.csv"
    test_data_url = "https://www.batadal.net/data/BATADAL_test_dataset.zip"

    training_data_1_path = os.path.join(download_dir, "BATADAL_dataset03.csv")
    training_data_2_path = os.path.join(download_dir, "BATADAL_dataset04.csv")

    download_if_necessary(training_data_1_path, training_data_1_url, verbose)
    download_if_necessary(training_data_2_path, training_data_2_url, verbose)

    download_if_necessary(os.path.join(download_dir, "BATADAL_test_dataset.zip"),
                          test_data_url, verbose)
    unpack_zip_archive(os.path.join(download_dir, "BATADAL_test_dataset.zip"), download_dir)

    # Load and return data
    df_train_1 = pd.read_csv(training_data_1_path)
    df_train_2 = pd.read_csv(training_data_2_path)
    df_test = pd.read_csv(os.path.join(download_dir, "BATADAL_test_dataset.csv"))

    if return_X_y is True:
        # Convert data to numpy
        y_train_1 = df_train_1["ATT_FLAG"].to_numpy().astype(np.int8)
        del df_train_1["ATT_FLAG"]
        del df_train_1["DATETIME"]
        X_train_1 = df_train_1.to_numpy()

        y_train_2 = df_train_2[" ATT_FLAG"].to_numpy()
        idx = np.argwhere(y_train_2 == -999)
        y_train_2[idx] = 0
        y_train_2 = y_train_2.astype(np.int8)
        del df_train_2[" ATT_FLAG"]
        del df_train_2["DATETIME"]
        X_train_2 = df_train_2.to_numpy()

        del df_test["DATETIME"]
        X_test = df_test.to_numpy()

        # Create ground truth labels
        hydraulic_time_step = to_seconds(minutes=15)
        training_data_2_events_time = __parse_attacks_time(TRAINING_DATA_2_START_TIME,
                                                           TRAINING_DATA_2_ATTACKS_TIME)
        test_data_events_time = __parse_attacks_time(TEST_DATA_START_TIME, TEST_DATA_ATTACKS_TIME)

        y_train_2_truth = np.zeros(X_train_2.shape[0])
        for event_start, event_end in training_data_2_events_time:
            t0 = int(event_start / hydraulic_time_step)
            t1 = int(event_end / hydraulic_time_step)
            y_train_2_truth[t0:t1] = 1

        y_test_truth = np.zeros(X_test.shape[0])
        for event_start, event_end in test_data_events_time:
            t0 = int(event_start / hydraulic_time_step)
            t1 = int(event_end / hydraulic_time_step)
            y_test_truth[t0:t1] = 1

        # Create features' descriptions
        features_desc = list(df_train_1.columns)
        desc_mapping = {"PU": "Pump", "V": "Valve", "T": "Tank", "L": "Level", "S": "State",
                        "P": "Pressure", "F": "Flow"}
        for i, f_desc in enumerate(features_desc):
            pump = False
            for k, value in desc_mapping.items():
                if k in f_desc:
                    if k == "P" and pump is True:
                        continue
                    f_desc = f_desc.replace(k, value)
                    if k == "PU":
                        pump = True
            features_desc[i] = f_desc

        # Create final results
        r = {"train_1": (X_train_1, y_train_1), "train_2": (X_train_2, y_train_2),
             "test": X_test}

        if return_ground_truth is True:
            r["train_1"] = (r["train_1"][0], r["train_1"][1], y_train_1)
            r["train_2"] = (r["train_2"][0], r["train_2"][1], y_train_2_truth)
            r["test"] = (r["test"][0], y_test_truth)

        if return_features_desc is True:
            r["features_desc"] = features_desc

        return r
    else:
        return {"train_1": df_train_1, "train_2": df_train_2, "test": df_test}


def load_scada_data(download_dir: str = None, return_X_y: bool = False,
                    return_ground_truth: bool = False, return_features_desc: bool = False,
                    verbose: bool = True) -> Any:
    """
    Loads the SCADA data of the simulated BATADAL benchmark scenario -- note that due to
    randomness and undocumented aspects of the original BATADAL data set, these differ from
    the original data set which can be loaded by calling
    :func:`~epyt_flow.data.benchmarks.batadal.load_data`.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the data files -- if None, the temp folder will be used.
        If the path does not exist, the data files will be downloaded to the given path.

        The default is None.
    return_X_y : `bool`, optional
        If True, the data together with the labels is returned as pairs of Numpy arrays.
        Otherwisen the data is returned as Pandas data frames.

        The default is False.
    return_ground_truth : `bool`
        If True and if `return_X_y` is True, the ground truth labels are included in the
        returned dictionary -- note that the labels provided in the benchmark constitute
        a partial labeling only.

        The default is False.
    return_features_desc : `bool`
        If True and if `return_X_y` is True, feature names (i.e. descriptions) are included
        in the returned dictionary.

        The default is False.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading files.

        The default is True.
    """
    raise NotImplementedError()


def load_scenario(download_dir: str = None, verbose: bool = True) -> ScenarioConfig:
    """
    Creates and returns the BATADAL scenario -- it can be either modified or directly passed
    to the simulator :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`.

    .. note::

        Note that due to randomness and undocumented aspects of the original BATADAL benchmark,
        the scenario simulation results differ from the original data set which can be loaded by
        calling :func:`~epyt_flow.data.benchmarks.batadal.load_data`.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the data files -- if None, the temp folder will be used.
        If the path does not exist, the data files will be downloaded to the given path.

        The default is None.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading files.

        The default is True.

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        The BATADAL scenario.
    """
    raise NotImplementedError()
