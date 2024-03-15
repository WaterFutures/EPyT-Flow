"""
Module provides helper functions.
"""
import os
import tempfile
import zipfile
from pathlib import Path
import requests
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt


def plot_timeseries_data(data: np.ndarray, labels: list[str] = None, show: bool = True) -> None:
    """
    Plots a single or multiple time series.

    Parameters
    ----------
    data : `numpy.ndarray`
        Time series data -- each row in `data` corresponds to a complete time series.
    labels : `list[str]`, optional
        Labels for each time series in `data`.
        If None, no labels are shown.

        The default is None.
    show : `bool`, optional
        If True, the plot/figure is shown in a window.

        The default is True.
    """
    if not isinstance(data, np.ndarray):
        raise TypeError(f"'data' must be an instance of 'numpy.ndarray' but not of '{type(data)}'")
    if not len(data.shape) != 2:
        raise ValueError("'data' must be a 2d array where each row corresponds to a time series")
    if labels is not None:
        if not isinstance(labels, list) or not all(isinstance(label, str) for label in labels):
            raise TypeError("'labels' must be a instance of 'list[str]'")
    if not isinstance(show, bool):
        raise TypeError(f"'show' must be an instance of 'bool' but not of '{type(show)}'")

    plt.figure()

    labels = labels if labels is not None else [None] * data.shape[0]

    for i in range(data.shape[0]):
        plt.plot(data[i, :], ".-", label=labels[i])

    if not any(label is None for label in labels):
        plt.legend()

    if show is True:
        plt.show()


def plot_timeseries_prediction(y: np.ndarray, y_pred: np.ndarray,
                               confidence_interval: np.ndarray = None, show: bool = True) -> None:
    """
    Plots the prediction (e.g. forecast) of *single* time series together with the
    ground truth time series. In addition, confidence intervals can be plotted as well.

    Parameters
    ----------
    y : `numpy.ndarray`
        Ground truth values.
    y_pred : `numpy.ndarray`
        Predicted values.
    confidence_interval : `numpy.ndarray`, optional
        Confidence interval (upper and lower value) for each prediction in `y_pred`.
        If not None, the confidence interval is plotted as well.

        The default is None.
    show : `bool`, optional
        If True, the plot/figure is shown in a window.

        The default is True.
    """
    if not isinstance(y_pred, np.ndarray):
        raise TypeError("'y_pred' must be an instance of 'numpy.ndarray' " +
                        f"but not of '{type(y_pred)}'")
    if not isinstance(y, np.ndarray):
        raise TypeError("'y' must be an instance of 'numpy.ndarray' " +
                        f"but not of '{type(y)}'")
    if y_pred.shape != y.shape:
        raise ValueError(f"Shape mismatch: {y_pred.shape} vs. {y.shape}")
    if len(y_pred.shape) != 1:
        raise ValueError("'y_pred' must be a 1d array")
    if len(y.shape) != 1:
        raise ValueError("'y' must be a 1d array")
    if not isinstance(show, bool):
        raise TypeError(f"'show' must be an instance of 'bool' but not of '{type(show)}'")

    plt.figure()

    if confidence_interval is not None:
        plt.fill_between(range(len(y_pred)),
                         y_pred - confidence_interval[0],
                         y_pred + confidence_interval[1],
                         alpha=0.5)
    plt.plot(y_pred, ".-", label="Prediction")
    plt.plot(y, ".-", label="Ground truth")
    plt.legend()

    if show is True:
        plt.show()


def download_if_necessary(download_path: str, url: str) -> None:
    """
    Downloads a file from a given URL if it does not already exist in a given path.

    Parameters
    ----------
    download_path : `str`
        Local path to the file -- if this path does not exist, the file will be downloaded from
        the provided 'url' and stored in 'download_dir'.
    url : `str`
        Web-URL.
    """
    if not os.path.isfile(download_path):
        response = requests.get(url, stream=True, allow_redirects=True, timeout=1000)
        content_length = int(response.headers.get('content-length', 0))
        with open(download_path, "wb") as file, tqdm(desc=download_path,
                                                     total=content_length,
                                                     unit='B',
                                                     unit_scale=True,
                                                     unit_divisor=1024) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)


def create_path_if_not_exist(path_in: str) -> None:
    """
    Creates a directory and all its parent directories if they do not already exist.

    Parameters
    ----------
    path_in : `str`
        Path to be created.
    """
    Path(path_in).mkdir(parents=True, exist_ok=True)


def unpack_zip_archive(f_in: str, folder_out: str) -> None:
    """
    Unpacks a .zip archive.

    Parameters
    ----------
    f_in : `str`
        Path to the .zip file.
    folder_out : `str`
        Path to the folder where the unpacked files will be stored.
    """
    with zipfile.ZipFile(f_in, "r") as f:
        f.extractall(folder_out)


def get_temp_folder() -> str:
    """
    Gets a path to a temporary folder -- i.e. a folder for storing temporary files.

    Returns
    -------
    `str`
        Path to a temporary folder.
    """
    return tempfile.gettempdir()


def to_seconds(days: int = None, hours: int = None, minutes: int = None) -> int:
    """
    Converts a time stamp (i.e. days, hours, minutes) into seconds.

    Parameters
    ----------
    days : `int`, optional
        Days.
    hours : `int`, optional
        Hours.
    minutes : `int`, optional
        Minutes.

    Returns
    -------
    `int`
        Time stamp in seconds.
    """
    sec = 0

    if days is not None:
        if not isinstance(days, int):
            raise TypeError(f"'days' must be an instance of 'int' but not of {type(days)}")
        if days <= 0:
            raise ValueError("'days' must be positive")

        sec += 24*60*60 * days
    if hours is not None:
        if not isinstance(hours, int):
            raise TypeError(f"'hours' must be an instance of 'int' but not of {type(hours)}")
        if hours <= 0:
            raise ValueError("'hours' must be positive")

        sec += 60*60 * hours
    if minutes is not None:
        if not isinstance(minutes, int):
            raise TypeError(f"'minutes' must be an instance of 'int' but not of {type(minutes)}")
        if minutes <= 0:
            raise ValueError("'minutes' must be positive")

        sec += 60 * minutes

    return sec
