"""
Module provides helper functions.
"""
import os
import tempfile
import zipfile
from pathlib import Path
import requests
from tqdm import tqdm


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
