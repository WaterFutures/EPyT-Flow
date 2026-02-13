"""
Module provides helper functions.
"""
import os
import math
import tempfile
import zipfile
from pathlib import Path
import re
import requests
import time
import multiprocessing as mp
from deprecated import deprecated
from tqdm import tqdm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from epanet_plus import EpanetConstants


def _get_flow_convert_factor(new_unit_id: int, old_unit: int) -> float:
    if new_unit_id == EpanetConstants.EN_CFS:
        if old_unit == EpanetConstants.EN_GPM:
            return .0022280093
        elif old_unit == EpanetConstants.EN_MGD:
            return 1.5472286523
        elif old_unit == EpanetConstants.EN_IMGD:
            return 1.8581441347
        elif old_unit == EpanetConstants.EN_AFD:
            return .5041666667
        elif old_unit == EpanetConstants.EN_LPS:
            return .0353146667
        elif old_unit == EpanetConstants.EN_LPM:
            return .0005885778
        elif old_unit == EpanetConstants.EN_MLD:
            return .40873456853575
        elif old_unit == EpanetConstants.EN_CMH:
            return .0098096296
        elif old_unit == EpanetConstants.EN_CMD:
            return .0004087346
    elif new_unit_id == EpanetConstants.EN_GPM:
        if old_unit == EpanetConstants.EN_CFS:
            return 448.8325660485
        elif old_unit == EpanetConstants.EN_MGD:
            return 694.44444444
        elif old_unit == EpanetConstants.EN_IMGD:
            return 833.99300382
        elif old_unit == EpanetConstants.EN_AFD:
            return 226.28571429
        elif old_unit == EpanetConstants.EN_LPS:
            return 15.850323141
        elif old_unit == EpanetConstants.EN_LPM:
            return .2641720524
        elif old_unit == EpanetConstants.EN_MLD:
            return 183.4528141376
        elif old_unit == EpanetConstants.EN_CMH:
            return 4.4028675393
        elif old_unit == EpanetConstants.EN_CMD:
            return .1834528141
    elif new_unit_id == EpanetConstants.EN_MGD:
        if old_unit == EpanetConstants.EN_CFS:
            return .6463168831
        elif old_unit == EpanetConstants.EN_GPM:
            return .00144
        elif old_unit == EpanetConstants.EN_IMGD:
            return 1.2009499255
        elif old_unit == EpanetConstants.EN_AFD:
            return 0.3258514286
        elif old_unit == EpanetConstants.EN_LPS:
            return .0228244653
        elif old_unit == EpanetConstants.EN_LPM:
            return .0003804078
        elif old_unit == EpanetConstants.EN_MLD:
            return .26417205124156
        elif old_unit == EpanetConstants.EN_CMH:
            return .0063401293
        elif old_unit == EpanetConstants.EN_CMD:
            return .0002641721
    elif new_unit_id == EpanetConstants.EN_IMGD:
        if old_unit == EpanetConstants.EN_CFS:
            return .5381713837
        elif old_unit == EpanetConstants.EN_MGD:
            return .8326741846
        elif old_unit == EpanetConstants.EN_GPM:
            return .0011990508
        elif old_unit == EpanetConstants.EN_AFD:
            return .2713280726
        elif old_unit == EpanetConstants.EN_LPS:
            return .0190053431
        elif old_unit == EpanetConstants.EN_LPM:
            return .0003167557
        elif old_unit == EpanetConstants.EN_MLD:
            return .21996924829908776
        elif old_unit == EpanetConstants.EN_CMH:
            return .005279262
        elif old_unit == EpanetConstants.EN_CMD:
            return .0002199692
    elif new_unit_id == EpanetConstants.EN_AFD:
        if old_unit == EpanetConstants.EN_CFS:
            return 1.9834710744
        elif old_unit == EpanetConstants.EN_MGD:
            return 3.0688832772
        elif old_unit == EpanetConstants.EN_GPM:
            return .0044191919
        elif old_unit == EpanetConstants.EN_IMGD:
            return 3.6855751432
        elif old_unit == EpanetConstants.EN_LPS:
            return .0700456199
        elif old_unit == EpanetConstants.EN_LPM:
            return .001167427
        elif old_unit == EpanetConstants.EN_MLD:
            return .81070995093708
        elif old_unit == EpanetConstants.EN_CMH:
            return .0194571167
        elif old_unit == EpanetConstants.EN_CMD:
            return .0008107132
    elif new_unit_id == EpanetConstants.EN_LPS:
        if old_unit == EpanetConstants.EN_CFS:
            return 28.316846592
        elif old_unit == EpanetConstants.EN_MGD:
            return 43.812636389
        elif old_unit == EpanetConstants.EN_IMGD:
            return 52.616782407
        elif old_unit == EpanetConstants.EN_GPM:
            return .0630901964
        elif old_unit == EpanetConstants.EN_AFD:
            return 14.276410157
        elif old_unit == EpanetConstants.EN_LPM:
            return .0166666667
        elif old_unit == EpanetConstants.EN_MLD:
            return 11.574074074074
        elif old_unit == EpanetConstants.EN_CMH:
            return .2777777778
        elif old_unit == EpanetConstants.EN_CMD:
            return .0115740741
    elif new_unit_id == EpanetConstants.EN_LPM:
        if old_unit == EpanetConstants.EN_CFS:
            return 1699.0107955
        elif old_unit == EpanetConstants.EN_MGD:
            return 2628.7581833
        elif old_unit == EpanetConstants.EN_IMGD:
            return 3157.0069444
        elif old_unit == EpanetConstants.EN_AFD:
            return 856.58460941
        elif old_unit == EpanetConstants.EN_LPS:
            return 60
        elif old_unit == EpanetConstants.EN_GPM:
            return 3.785411784
        elif old_unit == EpanetConstants.EN_MLD:
            return 694.44444444443
        elif old_unit == EpanetConstants.EN_CMH:
            return 16.666666667
        elif old_unit == EpanetConstants.EN_CMD:
            return 0.6944444444
    elif new_unit_id == EpanetConstants.EN_MLD:
        if old_unit == EpanetConstants.EN_CFS:
            return 2.4465755456688
        elif old_unit == EpanetConstants.EN_MGD:
            return 3.7854117999999777
        elif old_unit == EpanetConstants.EN_IMGD:
            return 4.54609
        elif old_unit == EpanetConstants.EN_AFD:
            return 1.2334867714947
        elif old_unit == EpanetConstants.EN_LPS:
            return .0864
        elif old_unit == EpanetConstants.EN_LPM:
            return .00144
        elif old_unit == EpanetConstants.EN_GPM:
            return .00545099296896
        elif old_unit == EpanetConstants.EN_CMH:
            return .024
        elif old_unit == EpanetConstants.EN_CMD:
            return .00099999999999999
    elif new_unit_id == EpanetConstants.EN_CMH:
        if old_unit == EpanetConstants.EN_CFS:
            return 101.94064773
        elif old_unit == EpanetConstants.EN_MGD:
            return 157.725491
        elif old_unit == EpanetConstants.EN_IMGD:
            return 189.42041667
        elif old_unit == EpanetConstants.EN_AFD:
            return 51.395076564
        elif old_unit == EpanetConstants.EN_LPS:
            return 3.6
        elif old_unit == EpanetConstants.EN_LPM:
            return .06
        elif old_unit == EpanetConstants.EN_MLD:
            return 41.666666666666
        elif old_unit == EpanetConstants.EN_GPM:
            return .227124707
        elif old_unit == EpanetConstants.EN_CMD:
            return 0.0416666667
    elif new_unit_id == EpanetConstants.EN_CMD:
        if old_unit == EpanetConstants.EN_CFS:
            return 2446.5755455
        elif old_unit == EpanetConstants.EN_MGD:
            return 3785.411784
        elif old_unit == EpanetConstants.EN_IMGD:
            return 4546.09
        elif old_unit == EpanetConstants.EN_AFD:
            return 1233.4818375
        elif old_unit == EpanetConstants.EN_LPS:
            return 86.4
        elif old_unit == EpanetConstants.EN_LPM:
            return 1.44
        elif old_unit == EpanetConstants.EN_MLD:
            return 1000.
        elif old_unit == EpanetConstants.EN_CMH:
            return 24
        elif old_unit == EpanetConstants.EN_GPM:
            return 5.450992969


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


def level_to_volume(tank_level: float, tank_diameter: float) -> float:
    """
    Computes the volume of water in a tank given the water level in the tank.

    Parameters
    ----------
    tank_level : `float`
        Water level in the tank.
    tank_diameter : `float`
        Diameter of the tank.

    Returns
    -------
    `float`
        Water volume in tank.
    """
    if not isinstance(tank_level, float):
        raise TypeError("'tank_level' must be an instace of 'float' " +
                        f"but not of '{type(tank_level)}'")
    if tank_level < 0:
        raise ValueError("'tank_level' can not be negative")
    if not isinstance(tank_diameter, float):
        raise TypeError("'tank_diameter' must be an instace of 'float' " +
                        f"but not of '{type(tank_diameter)}'")
    if tank_diameter <= 0:
        raise ValueError("'tank_diameter' must be greater than zero")

    return tank_level * math.pow(0.5 * tank_diameter, 2) * math.pi


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


def robust_download(download_path: str, urls: str or list,
                    verbose: bool = True, timeout: int = 30) -> None:
    """
    Downloads a file from the given urls if it does not already exist in the
    given path. The urls are tried in order. If a download stops or stalls,
    the next url is tried until one succeeds or all urls have failed.

    Parameters
    ----------
    download_path : `str`
        Local path to the file -- if this path does not exist, the file will be
        downloaded from the provided 'urls' and stored there.
    urls : `list` or `str`
        One url or a list of urls (where additional urls function as backup) to
        download the file from.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading the file.

        The default is True.
    timeout : `int`
        If this time passed without progress while downloading, the download is
        considered failed.

        The default is 30 seconds.
    """
    if isinstance(urls, str):
        urls = [urls]

    for url in urls:
        try:
            download_if_necessary(download_path, url, verbose, timeout)
            return
        except Exception as e:
            print(f"Failed url: {url} with {e}")
            continue

    raise SystemError("All download attempts failed")


def _download_process(download_path: str, url: str, backup_urls: list[str],
                     last_update: mp.Value, stop_flag: mp.Value,
                     finish_flag: mp.Value, verbose: bool) -> None:
    """
    Process that handles the actual download. It updates the last download
    update variable and cleans up the corrupted file if the download fails from
    within.

    This function is only to be called from `download_if_necessary`.

    Parameters
    ----------
    download_path : `str`
        Local path to the file -- if this path does not exist, the file will be
        downloaded from the provided 'urls' and stored there.
    url : `str`
        Web-URL pointing to the source the file should be downloaded from. Can
        also point to a google drive file.
    backup_urls : `list[str]`
        List of alternative URLs that are being tried in the case that
        downloading from 'url' fails. This is deprecated, but left in for
        downward compatibility with `download_if_necessary` calls with
        backup_urls. Not necessary when using `robust_download`.
    last_update : `mp.Value`
        Shared variable to keep track of the last successful download update.
    stop_flag : `mp.Value`
        Shared variable. Set to 1 when this process stopped by finishing or
        error.
    finish_flag : `mp.Value`
        Shared variable. Set to 1 when download finished successfully.
    verbose : `bool`
        If True, a progress bar is shown while downloading the file.
    """
    try:
        progress_bar = None
        response = None

        if "drive.google.com" in url:
            session = requests.Session()
            response = session.get(url)
            html = response.text

            def extract(pattern):
                match = re.search(pattern, html)
                return match.group(1) if match else None

            file_id = extract(r'name="id" value="([^"]+)"')
            file_confirm = extract(r'name="confirm" value="([^"]+)"')
            file_uuid = extract(r'name="uuid" value="([^"]+)"')

            if not all([file_id, file_confirm, file_uuid]):
                raise SystemError("Failed to extract download parameters")

            download_url = (
                f"https://drive.usercontent.google.com/download"
                f"?id={file_id}&export=download&confirm={file_confirm}&uuid={file_uuid}"
            )

            response = session.get(download_url, stream=True)

        else:
            response = requests.get(url, stream=True, allow_redirects=True,
                                    timeout=1000)

        # Deprecated, left in for backward compatibility
        if response.status_code != 200:
            for backup_url in backup_urls:
                response = requests.get(backup_url, stream=verbose,
                                        allow_redirects=True, timeout=1000)
                if response.status_code == 200:
                    break
        if response.status_code != 200:
            raise SystemError(f"Failed to download -- {response.status_code}")

        content_length = int(response.headers.get("content-length", 0))
        with open(download_path, "wb") as file:
            progress_bar = False
            if verbose:
                progress_bar = tqdm(desc=download_path, total=content_length,
                                    ascii=True, unit='B', unit_scale=True,
                                    unit_divisor=1024)
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                if progress_bar:
                    progress_bar.update(size)
                with last_update.get_lock():
                    last_update.value = time.time()
            with finish_flag.get_lock():
                finish_flag.value = 1
        with stop_flag.get_lock():
            stop_flag.value = 1
    finally:
        if progress_bar:
            progress_bar.close()
        if response:
            response.close()
        with finish_flag.get_lock():
            if os.path.exists(download_path) and finish_flag.value == 0:
                os.remove(download_path)
        with stop_flag.get_lock():
            stop_flag.value = 1


@deprecated(reason="Please use new function `robust_download` instead.")
def download_from_gdrive_if_necessary(download_path: str, url: str, verbose: bool = True) -> None:
    """
    Downloads a file from a google drive repository if it does not already exist
    in a given path.

    Note that if the path (folder) does not already exist, it will be created.

    Parameters
    ----------
    download_path : `str`
        Local path to the file -- if this path does not exist, the file will be downloaded from
        the provided 'url' and stored in 'download_dir'.
    url : `str`
        Web-URL of the google drive repository.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading the file.

        The default is True.
    """
    folder_path = str(Path(download_path).parent.absolute())
    create_path_if_not_exist(folder_path)

    if not os.path.isfile(download_path):
        session = requests.Session()

        response = session.get(url)
        html = response.text

        def extract(pattern):
            match = re.search(pattern, html)
            return match.group(1) if match else None

        file_id = extract(r'name="id" value="([^"]+)"')
        file_confirm = extract(r'name="confirm" value="([^"]+)"')
        file_uuid = extract(r'name="uuid" value="([^"]+)"')

        if not all([file_id, file_confirm, file_uuid]):
            raise SystemError("Failed to extract download parameters")

        download_url = (
            f"https://drive.usercontent.google.com/download"
            f"?id={file_id}&export=download&confirm={file_confirm}&uuid={file_uuid}"
        )

        response = session.get(download_url, stream=True)

        if response.status_code != 200:
            raise SystemError(f"Failed to download -- {response.status_code}")

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


# TODO: documentation
def download_if_necessary(download_path: str, url: str, verbose: bool = True,
                          backup_urls: list[str] = [], timeout: int = 30) -> None:
    """
    Downloads a file from a given URL if it does not already exist in a given
    path. This function is deprecated, please use `robust_download` instead.

    Note that if the path (folder) does not already exist, it will be created.

    Parameters
    ----------
    download_path : `str`
        Local path to the file -- if this path does not exist, the file will be
        downloaded from the provided 'url' and stored in 'download_dir'.
    url : `str`
        Web-URL.
    verbose : `bool`, optional
        If True, a progress bar is shown while downloading the file.

        The default is True.
    backup_urls : `list[str]`, optional
        List of alternative URLs that are being tried in the case that downloading from 'url' fails.

        The default is an empty list.
    timeout : `int`, optional
        Allowed download inactivity in seconds. After this time passed without
        an update, the donwload is considered failed.

        The default is 30 seconds.
    """
    folder_path = str(Path(download_path).parent.absolute())
    create_path_if_not_exist(folder_path)

    if os.path.isfile(download_path):
        return

    last_update = mp.Value('d', time.time())
    stop_flag = mp.Value('i', 0)
    finish_flag = mp.Value('i', 0)

    t = mp.Process(target=_download_process, args=(download_path, url, backup_urls, last_update, stop_flag, finish_flag, verbose))
    t.start()

    while True:
        time.sleep(1)
        with last_update.get_lock():
            idle = time.time() - last_update.value
        with stop_flag.get_lock():
            if stop_flag.value == 1:
                with finish_flag.get_lock():
                    if finish_flag.value == 1:
                        break
                    else:
                        if os.path.exists(download_path) and finish_flag.value == 0:
                            os.remove(download_path)
                        raise SystemError(f"failed downloading from {url}")
        if idle > timeout:
            with finish_flag.get_lock():
                t.terminate()
                t.join()
                if os.path.exists(download_path) and finish_flag.value == 0:
                    os.remove(download_path)
                raise SystemError(f"no progress in {timeout} seconds, aborting download")
    t.join()


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
