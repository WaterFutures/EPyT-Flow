"""
Module provides tests to test the `epty_flow.data.benchmarks` module.
"""
import numpy as np
from epyt_flow.data.benchmarks import load_batadal_data
from epyt_flow.data.benchmarks import load_leakdb_scenarios, load_leakdb_scada_data, \
    load_leakdb_data
from epyt_flow.data.benchmarks import load_battledim_scenario
from epyt_flow.data.benchmarks.gecco_water_quality import load_gecco2017_water_quality_data, \
    load_gecco2018_water_quality_data, load_gecco2019_water_quality_data, \
    compute_evaluation_score as gecco_evaluation_score
from epyt_flow.data.benchmarks.water_usage import load_water_usage, \
    compute_evaluation_score as water_usage_evaluation_score
from epyt_flow.simulation import ScenarioSimulator

from .utils import get_temp_folder


def test_batadal():
    data = load_batadal_data(download_dir=get_temp_folder())
    assert data is not None

    data = load_batadal_data(download_dir=get_temp_folder(), return_X_y=True)
    assert data is not None

    data = load_batadal_data(download_dir=get_temp_folder(), return_X_y=True,
                             return_ground_truth=True)
    assert data is not None

    data = load_batadal_data(download_dir=get_temp_folder(), return_X_y=True,
                             return_ground_truth=True, return_features_desc=True)
    assert data is not None


def test_leakdb():
    # Net1
    configs = load_leakdb_scenarios(scenarios_id=range(1, 5), use_net1=True,
                                    download_dir=get_temp_folder())
    for c in configs:
        with ScenarioSimulator(scenario_config=c) as sim:
            res = sim.run_simulation()
            assert res is not None

    X, y, y_leak_loc = load_leakdb_scada_data(scenarios_id=[3], use_net1=True, return_X_y=True,
                                              return_leak_locations=True)[0]
    assert X is not None
    assert y is not None
    assert y_leak_loc is not None

    data = load_leakdb_data(scenarios_id=range(1, 5), use_net1=True)
    assert data is not None

    data = load_leakdb_data(scenarios_id=range(1, 5), use_net1=True, return_X_y=True,
                            return_features_desc=True, return_leak_locations=True)
    assert data is not None

    # Hanoi
    configs = load_leakdb_scenarios(scenarios_id=range(1, 5), use_net1=False,
                                    download_dir=get_temp_folder())
    for c in configs:
        with ScenarioSimulator(scenario_config=c) as sim:
            res = sim.run_simulation()
            assert res is not None

    X, y, y_leak_loc = load_leakdb_scada_data(scenarios_id=[3], use_net1=False, return_X_y=True,
                                              return_leak_locations=True)[0]
    assert X is not None
    assert y is not None
    assert y_leak_loc is not None

    data = load_leakdb_data(scenarios_id=range(1, 5), use_net1=False)
    assert data is not None

    data = load_leakdb_data(scenarios_id=range(1, 5), use_net1=False, return_X_y=True,
                            return_features_desc=True, return_leak_locations=True)
    assert data is not None


def test_battledim():
    hist_scenario = load_battledim_scenario(return_test_scenario=False,
                                            download_dir=get_temp_folder())
    assert hist_scenario is not None

    eval_scenario = load_battledim_scenario(return_test_scenario=True,
                                            download_dir=get_temp_folder())
    assert eval_scenario is not None


def test_gecco_water_quality():
    # Load as Numpy arrays
    X, y = load_gecco2017_water_quality_data(download_dir=get_temp_folder(), return_X_y=True)
    assert X is not None
    assert y is not None
    assert gecco_evaluation_score(np.random.choice([0, 1], size=y.shape), y=y) is not None

    df_data = load_gecco2017_water_quality_data(download_dir=get_temp_folder(), return_X_y=False)
    assert df_data is not None

    X, y = load_gecco2018_water_quality_data(download_dir=get_temp_folder(), return_X_y=True)
    assert X is not None
    assert y is not None
    assert gecco_evaluation_score(np.random.choice([0, 1], size=y.shape), y=y) is not None

    df_data = load_gecco2018_water_quality_data(download_dir=get_temp_folder(), return_X_y=False)
    assert df_data is not None

    # Load as ScadaData instance
    data = load_gecco2019_water_quality_data(download_dir=get_temp_folder(), return_X_y=True)
    X, y = data["train"]
    assert X is not None
    assert y is not None

    X, y = data["validation"]
    assert X is not None
    assert y is not None

    X, y = data["test"]
    assert X is not None
    assert y is not None
    assert gecco_evaluation_score(np.random.choice([0, 1], size=y.shape), y=y) is not None

    data = load_gecco2019_water_quality_data(download_dir=get_temp_folder(), return_X_y=False)
    df_data = data["train"]
    assert df_data is not None

    df_data = data["validation"]
    assert df_data is not None

    df_data = data["test"]
    assert df_data is not None


def test_water_usage():
    # Load as Numpy arrays
    data = load_water_usage(return_X_y=True)
    X, y = data["train"]
    assert X is not None
    assert y is not None

    X, y = data["validation"]
    assert X is not None
    assert y is not None

    X, y = data["test"]
    assert X is not None
    assert y is not None
    assert water_usage_evaluation_score(np.random.choice([0, 1], size=y.shape), y) is not None

    # Load as ScadaData instance
    data = load_water_usage(return_X_y=False)
    df_data = data["train"]
    assert df_data is not None

    df_data = data["validation"]
    assert df_data is not None

    df_data = data["test"]
    assert df_data is not None
