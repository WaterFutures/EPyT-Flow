"""
Module provides helper functions.
"""
import os
import math
import tempfile
import zipfile
from pathlib import Path
import requests
from tqdm import tqdm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def time_points_to_one_hot_encoding(time_points: list[int], total_length: int) -> list[int]:
    """
    Converts a list of time points into a one-hot-encoding.

    Parameters
    ----------
    time_points : `list[int]`
        Time points to be one-hot-encoded.
    total_length : `int`
        Length of final one-hot-encoding.

    Returns
    -------
    `list[int]`
        One-hot-encoded time points.
    """
    results = [0] * total_length

    for t in time_points:
        results[t] = 1

    return results


def volume_to_level(tank_volume: float, tank_diameter: float) -> float:
    """
    Computes the water level in a tank containing a given volume of water.

    Parameters
    ----------
    tank_volume : `float`
        Water volume in the tank.
    tank_diameter : `float`
        Diameter of the tank.

    Returns
    -------
    `float`
        Water level in tank.
    """
    if not isinstance(tank_volume, float):
        raise TypeError("'tank_volume' must be an instace of 'float' " +
                        f"but not of '{type(tank_volume)}'")
    if tank_volume < 0:
        raise ValueError("'tank_volume' can not be negative")
    if not isinstance(tank_diameter, float):
        raise TypeError("'tank_diameter' must be an instace of 'float' " +
                        f"but not of '{type(tank_diameter)}'")
    if tank_diameter <= 0:
        raise ValueError("'tank_diameter' must be greater than zero")

    return (4. / (math.pow(tank_diameter, 2) * math.pi)) * tank_volume


def plot_timeseries_data(data: np.ndarray, labels: list[str] = None, x_axis_label: str = None,
                         y_axis_label: str = None, y_ticks: tuple[list[float], list[str]] = None,
                         show: bool = True, save_to_file: str = None,
                         ax: matplotlib.axes.Axes = None) -> matplotlib.axes.Axes:
    """
    Plots a single or multiple time series.

    Parameters
    ----------
    data : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        Time series data -- each row in `data` corresponds to a complete time series.
    labels : `list[str]`, optional
        Labels for each time series in `data`.
        If None, no labels are shown.

        The default is None.
    x_axis_label : `str`, optional
        X axis label.

        The default is None.
    y_axis_label : `str`, optional
        Y axis label.

        The default is None.
    y_ticks: `(list[float], list[str])`, optional
        Tuple of ticks (numbers) and labels (strings) for the y-axis.

        The default is None.
    show : `bool`, optional
        If True, the plot/figure is shown in a window.

        Only considered when 'ax' is None.

        The default is True.
    save_to_file : `str`, optional
        File to which the plot is saved.

        If specified, 'show' must be set to False --
        i.e. a plot can not be shown and saved to a file at the same time!

        The default is None.
    ax : `matplotlib.axes.Axes <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.html>`_, optional
        If not None, 'ax' is used for plotting.

        The default is None.

    Returns
    -------
    `matplotlib.axes.Axes <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.html>`_
        Plot.
    """
    if not isinstance(data, np.ndarray):
        raise TypeError(f"'data' must be an instance of 'numpy.ndarray' but not of '{type(data)}'")
    if len(data.shape) != 2:
        raise ValueError("'data' must be a 2d array where each row corresponds to a time series " +
                         "-- use '.reshape(1, -1)' in case of single time series")
    if labels is not None:
        if not isinstance(labels, list) or not all(isinstance(label, str) for label in labels):
            raise TypeError("'labels' must be a instance of 'list[str]'")
    if x_axis_label is not None:
        if not isinstance(x_axis_label, str):
            raise TypeError("'x_axis_label' must be an instance of 'str' " +
                            f"but not of '{type(x_axis_label)}'")
    if y_axis_label is not None:
        if not isinstance(y_axis_label, str):
            raise TypeError("'y_axis_label' must be an instance of 'str' " +
                            f"but not of '{type(y_axis_label)}'")
    if y_ticks is not None:
        if len(y_ticks) != 2:
            raise ValueError("'y_ticks' must be a tuple ticks (numbers) and labels (strings)")
    if not isinstance(show, bool):
        raise TypeError(f"'show' must be an instance of 'bool' but not of '{type(show)}'")
    if save_to_file is not None:
        if show is True:
            raise ValueError("'show' must be False if 'save_to_file' is set")

        if not isinstance(save_to_file, str):
            raise TypeError("'save_to_file' must be an instance of 'str' but not of " +
                            f"'{type(save_to_file)}'")
    if ax is not None:
        if not isinstance(ax, matplotlib.axes.Axes):
            raise TypeError("ax' must be an instance of 'matplotlib.axes.Axes'" +
                            f"but not of '{type(ax)}'")

    fig = None
    if ax is None:
        fig, ax = plt.subplots()

    labels = labels if labels is not None else [None] * data.shape[0]

    for i in range(data.shape[0]):
        ax.plot(data[i, :], ".-", label=labels[i])

    if not any(label is None for label in labels):
        ax.legend()

    if x_axis_label is not None:
        ax.set_xlabel(x_axis_label)
    if y_axis_label is not None:
        ax.set_ylabel(y_axis_label)
    if y_ticks is not None:
        yticks_pos, yticks_labels = y_ticks
        ax.set_yticks(yticks_pos, labels=yticks_labels)

    if show is True and fig is not None:
        plt.show()
    if save_to_file is not None:
        folder_path = str(Path(save_to_file).parent.absolute())
        create_path_if_not_exist(folder_path)

        if fig is None:
            plt.savefig(save_to_file, bbox_inches='tight')
        else:
            fig.savefig(save_to_file, bbox_inches='tight')

    return ax


def plot_timeseries_prediction(y: np.ndarray, y_pred: np.ndarray,
                               confidence_interval: np.ndarray = None,
                               x_axis_label: str = None, y_axis_label: str = None,
                               y_ticks: tuple[list[float], list[str]] = None,
                               show: bool = True, save_to_file: str = None,
                               ax: matplotlib.axes.Axes = None
                               ) -> matplotlib.axes.Axes:
    """
    Plots the prediction (e.g. forecast) of *single* time series together with the
    ground truth time series. In addition, confidence intervals can be plotted as well.

    Parameters
    ----------
    y : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        Ground truth values.
    y_pred : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        Predicted values.
    confidence_interval : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_, optional
        Confidence interval (upper and lower value) for each prediction in `y_pred`.
        If not None, the confidence interval is plotted as well.

        The default is None.
    x_axis_label : `str`, optional
        X axis label.

        The default is None.
    y_axis_label : `str`, optional
        Y axis label.

        The default is None.
    y_ticks: `(list[float], list[str])`, optional
        Tuple of ticks (numbers) and labels (strings) for the y-axis.

        The default is None.
    show : `bool`, optional
        If True, the plot/figure is shown in a window.

        Only considered when 'ax' is None.

        The default is True.
    save_to_file : `str`, optional
        File to which the plot is saved.

        If specified, 'show' must be set to False --
        i.e. a plot can not be shown and saved to a file at the same time!

        The default is None.
    ax : `matplotlib.axes.Axes <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.html>`_, optional
        If not None, 'axes' is used for plotting.

        The default is None.

    Returns
    -------
    `matplotlib.axes.Axes <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.html>`_
        Plot.
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
    if x_axis_label is not None:
        if not isinstance(x_axis_label, str):
            raise TypeError("'x_axis_label' must be an instance of 'str' " +
                            f"but not of '{type(x_axis_label)}'")
    if y_axis_label is not None:
        if not isinstance(y_axis_label, str):
            raise TypeError("'y_axis_label' must be an instance of 'str' " +
                            f"but not of '{type(y_axis_label)}'")
    if y_ticks is not None:
        if len(y_ticks) != 2:
            raise ValueError("'y_ticks' must be a tuple ticks (numbers) and labels (strings)")
    if not isinstance(show, bool):
        raise TypeError(f"'show' must be an instance of 'bool' but not of '{type(show)}'")
    if save_to_file is not None:
        if show is True:
            raise ValueError("'show' must be False if 'save_to_file' is set")

        if not isinstance(save_to_file, str):
            raise TypeError("'save_to_file' must be an instance of 'str' but not of " +
                            f"'{type(save_to_file)}'")
    if ax is not None:
        if not isinstance(ax, matplotlib.axes.Axes):
            raise TypeError("ax' must be an instance of 'matplotlib.axes.Axes'" +
                            f"but not of '{type(ax)}'")

    fig = None
    if ax is None:
        fig, ax = plt.subplots()

    if confidence_interval is not None:
        ax.fill_between(range(len(y_pred)),
                        y_pred - confidence_interval[0],
                        y_pred + confidence_interval[1],
                        alpha=0.5)
    ax.plot(y, ".-", label="Ground truth")
    ax.plot(y_pred, ".-", label="Prediction")
    ax.legend()

    if x_axis_label is not None:
        ax.set_xlabel(x_axis_label)
    if y_axis_label is not None:
        ax.set_ylabel(y_axis_label)
    if y_ticks is not None:
        yticks_pos, yticks_labels = y_ticks
        ax.set_yticks(yticks_pos, labels=yticks_labels)

    if show is True and fig is not None:
        plt.show()
    if save_to_file is not None:
        folder_path = str(Path(save_to_file).parent.absolute())
        create_path_if_not_exist(folder_path)

        if fig is None:
            plt.savefig(save_to_file, bbox_inches='tight')
        else:
            fig.savefig(save_to_file, bbox_inches='tight')

    return ax


def download_if_necessary(download_path: str, url: str, verbose: bool = True) -> None:
    """
    Downloads a file from a given URL if it does not already exist in a given path.

    Note that if the path (folder) does not already exist, it will be created.

    Parameters
    ----------
    download_path : `str`
        Local path to the file -- if this path does not exist, the file will be downloaded from
        the provided 'url' and stored in 'download_dir'.
    url : `str`
        Web-URL.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading the file.

        The default is True.
    """
    folder_path = str(Path(download_path).parent.absolute())
    create_path_if_not_exist(folder_path)

    if not os.path.isfile(download_path):
        response = requests.get(url, stream=verbose, allow_redirects=True, timeout=1000)

        if verbose is True:
            content_length = int(response.headers.get('content-length', 0))
            with open(download_path, "wb") as file, tqdm(desc=download_path,
                                                         total=content_length,
                                                         ascii=True,
                                                         unit='B',
                                                         unit_scale=True,
                                                         unit_divisor=1024) as progress_bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    progress_bar.update(size)
        else:
            with open(download_path, "wb") as f_out:
                f_out.write(response.content)


def create_path_if_not_exist(path_in: str) -> None:
    """
    Creates a directory and all its parent directories if they do not already exist.

    Parameters
    ----------
    path_in : `str`
        Path to be created.
    """
    Path(path_in).mkdir(parents=True, exist_ok=True)


def pack_zip_archive(f_in: list[str], f_out: str) -> None:
    """
    Compresses a given list of files into a .zip archive.

    Parameters
    ----------
    f_in : `list[str]`
        List of files to be compressed into the .zip archive.
    f_out : `str`
        Path to the final .zip file.
    """
    with zipfile.ZipFile(f_out, "w") as f_zip_out:
        for f_cur_in in f_in:
            f_zip_out.write(f_cur_in, compress_type=zipfile.ZIP_DEFLATED)


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
    Converts a timestamp (i.e. days, hours, minutes) into seconds.

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
        Timestamp in seconds.
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
