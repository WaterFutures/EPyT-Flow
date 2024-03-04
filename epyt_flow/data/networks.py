"""
Module provides functions for loading different water distribution networks.
"""
import os
import requests
from tqdm import tqdm

from ..simulation import ScenarioConfig, WaterDistributionNetworkScenarioSimulator, SensorConfig
from ..utils import get_temp_folder


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


def create_empty_sensor_config(f_inp: str) -> SensorConfig:
    """
    Creates an empty sensor configuration for a given .inp file.

    Parameters
    ----------
    f_inp : `str`
        Path to the .inp file.

    Returns
    -------
    :class:`~epyt_flow.simulation.sensor_config.SensorConfig`
        Sensor configuration.
    """
    with WaterDistributionNetworkScenarioSimulator(f_inp_in=f_inp) as sim:
        return sim.sensor_config


def load_inp(f_in: str, include_empty_sensor_config: bool = True) -> ScenarioConfig:
    """
    Loads and .inp file and wraps it into a scenario configuration.

    Parameters
    ----------
    f_in : `str`
        Path to the .inp file.
    include_empty_sensor_config : `bool`, optional
        If True, an empty sensor configuration will be included in the returned
        scenario configuration.

        The default is True.

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Scenario configuration for the .inp file.
    """
    if not os.path.isfile(f_in):
        raise ValueError("Can not find 'f_in'")

    if include_empty_sensor_config is True:
        return ScenarioConfig(f_inp_in=f_in, sensor_config=create_empty_sensor_config(f_inp=f_in))
    else:
        return ScenarioConfig(f_inp_in=f_in)


def load_net1(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the Net1 network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Net1 network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "Net1.inp")
    url = "https://raw.githubusercontent.com/OpenWaterAnalytics/EPyT/main/epyt/networks/" + \
          "asce-tf-wdst/Net1.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_net2(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the Net2 network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Net2 network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "Net2.inp")
    url = "https://raw.githubusercontent.com/OpenWaterAnalytics/EPyT/main/epyt/networks/" + \
          "asce-tf-wdst/Net2.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_net3(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the Net3 network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Net3 network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "Net3.inp")
    url = "https://raw.githubusercontent.com/OpenWaterAnalytics/EPyT/main/epyt/networks/" + \
          "asce-tf-wdst/Net3.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_net6(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the Net6 network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Net6 network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "Net6.inp")
    url = "https://github.com/OpenWaterAnalytics/WNTR/raw/main/examples/networks/Net6.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_richmond(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the Richmond network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Richmond network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "Richmond_standard.inp")
    url = "https://raw.githubusercontent.com/OpenWaterAnalytics/EPyT/main/epyt/networks/" + \
          "exeter-benchmarks/Richmond_standard.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_micropolis(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the MICROPOLIS network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        MICROPOLIS network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "MICROPOLIS_v1.inp")
    url = "https://github.com/OpenWaterAnalytics/EPyT/raw/main/epyt/networks/asce-tf-wdst/" + \
          "MICROPOLIS_v1.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_balerma(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the Balerma network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Balerma network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "Balerma.inp")
    url = "https://github.com/OpenWaterAnalytics/EPyT/raw/main/epyt/networks/" + \
          "asce-tf-wdst/Balerma.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_rural(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the Rural network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Rural network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "RuralNetwork.inp")
    url = "https://github.com/OpenWaterAnalytics/EPyT/raw/main/epyt/networks/" + \
          "asce-tf-wdst/RuralNetwork.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_bwsn1(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the BWSN-1 network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        BWSN-1 network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "BWSN_Network_1.inp")
    url = "https://github.com/OpenWaterAnalytics/EPyT/raw/main/epyt/networks/" + \
          "asce-tf-wdst/BWSN_Network_1.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_bwsn2(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the BWSN-2 network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        BWSN-2 network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "BWSN_Network_2.inp")
    url = "https://github.com/OpenWaterAnalytics/EPyT/raw/main/epyt/networks/" + \
          "asce-tf-wdst/BWSN_Network_2.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_anytown(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the Anytown network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Anytown network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "Anytown.inp")
    url = "https://raw.githubusercontent.com/OpenWaterAnalytics/EPyT/main/epyt/networks/" + \
          "asce-tf-wdst/Anytown.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_dtown(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the D-Town network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        D-Town network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "d-town.inp")
    url = "https://www.exeter.ac.uk/media/universityofexeter/emps/research/cws/downloads/d-town.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_ctown(download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the C-Town network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        C-Town network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "CTOWN.INP")
    url = "https://github.com/scy-phy/www.batadal.net/raw/master/data/CTOWN.INP"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_kentucky(wdn_id: int = 1, download_dir: str = get_temp_folder()) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the specified Kentucky network.

    Parameters
    ----------
    wdn_id : `int`, optional
        The ID (1-15) of the particular network.

        The default is wdn_id=1
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Kentucky network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    if not isinstance(wdn_id, int):
        raise ValueError("'wdn_id' must be an integer in [1, 15]")
    if wdn_id < 1 or wdn_id > 15:
        raise ValueError(f"Unknown network 'ky{wdn_id}.inp'")

    f_in = os.path.join(download_dir, f"ky{wdn_id}.inp")
    url = "https://raw.githubusercontent.com/OpenWaterAnalytics/EPyT/main/epyt/networks/" + \
          f"asce-tf-wdst/ky{wdn_id}.inp"

    download_if_necessary(f_in, url)
    return load_inp(f_in)


def load_hanoi(download_dir: str = get_temp_folder(),
               include_default_sensor_placement: bool = False) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the Hanoi network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)
    include_default_sensor_placement : `bool`, optional
        If True, a default sensor placement will be included in the returned scenario configuration.

        The default is False

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Hanoi network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_in = os.path.join(download_dir, "Hanoi.inp")
    url = "https://raw.githubusercontent.com/OpenWaterAnalytics/EPyT/main/epyt/networks/" + \
          "asce-tf-wdst/Hanoi.inp"

    download_if_necessary(f_in, url)
    config = load_inp(f_in)

    if include_default_sensor_placement is True:
        sensor_config = config.sensor_config
        sensor_config.pressure_sensors = ["13", "16", "22", "30"]
        sensor_config.flow_sensors = ["1"]

        config = ScenarioConfig(f_inp_in=config.f_inp_in, sensor_config=sensor_config)

    return config


def load_ltown(download_dir: str = get_temp_folder(), use_realistic_demands: bool = False,
               include_default_sensor_placement: bool = False) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the L-TOWN_v2 network.

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)
    use_realistic_demands : `bool`, optional
        If True, realistic demands from the BattLeDIM challenge will be included,
        toy demands will be included otherwise.

        The default is False
    include_default_sensor_placement : `bool`, optional
        If True, the L-TOWN default sensor placement will be included
        in the returned scenario configuration.

        The default is False

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        L-TOWN_v2 network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_inp = "L-TOWN_v2_Model.inp" if use_realistic_demands is False else "L-TOWN_v2_Real.inp"

    f_in = os.path.join(download_dir, f_inp)
    if use_realistic_demands:
        url = "https://zenodo.org/records/4017659/files/L-TOWN.inp?download=1"
    else:
        url = "https://zenodo.org/records/4017659/files/L-TOWN_Real.inp?download=1"

    download_if_necessary(f_in, url)
    config = load_inp(f_in)

    if include_default_sensor_placement is True:
        sensor_config = config.sensor_config
        sensor_config.pressure_sensors = ["n54", "n105", "n114", "n163", "n188", "n229", "n288",
                                          "n296", "n332", "n342", "n410", "n415", "n429", "n458",
                                          "n469", "n495", "n506", "n516", "n519", "n549", "n613",
                                          "n636", "n644", "n679", "n722", "n726", "n740", "n752",
                                          "n769"]
        sensor_config.flow_sensors = ["p227", "p235"]

        config = ScenarioConfig(f_inp_in=config.f_inp_in, sensor_config=sensor_config)

    return config


def load_ltown_a(download_dir: str = get_temp_folder(), use_realistic_demands: bool = False,
                 include_default_sensor_placement: bool = False) -> ScenarioConfig:
    """
    Loads (and downloads if necessary) the L-TOWN-A network (area "A" of the L-TOWN network).

    Parameters
    ----------
    download_dir : `str`, optional
        Path to the directory where the .inp file is stored.

        The default is the OS specific temporary directory (e.g. "C:\\\\temp", "/tmp/", etc.)
    use_realistic_demands : `bool`, optional
        If True, realistic demands from the BattLeDIM challenge will be included,
        toy demands will be included otherwise.

        The default is False
    include_default_sensor_placement : `bool`, optional
        If True, the L-TOWN default sensor placement will be included
        in the returned scenario configuration.

        The default is False

    Returns
    -------
    :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        L-TOWN-A network loaded into a scenario configuration that can be passed on to
        :class:`~epyt_flow.simulation.scenario_simulator.WaterDistributionNetworkScenarioSimulator`.
    """
    f_inp = "L-TOWN_v2-A_Model.inp" if use_realistic_demands is False else "L-TOWN_v2-A_Real.inp"

    f_in = os.path.join(download_dir, f_inp)
    url = f"https://filedn.com/lumBFq2P9S74PNoLPWtzxG4/EPyT-Flow/Networks/{f_inp}"

    download_if_necessary(f_in, url)
    config = load_inp(f_in)

    if include_default_sensor_placement is True:
        sensor_config = config.sensor_config
        sensor_config.pressure_sensors = ["n54", "n105", "n114", "n163", "n188", "n229", "n288",
                                          "n296", "n332", "n342", "n410", "n415", "n429", "n458",
                                          "n469", "n495", "n506", "n516", "n519", "n549", "n613",
                                          "n636", "n644", "n679", "n722", "n726", "n740", "n752",
                                          "n769"]
        sensor_config.flow_sensors = ["p227", "p235"]

        config = ScenarioConfig(f_inp_in=config.f_inp_in, sensor_config=sensor_config)

    return config
