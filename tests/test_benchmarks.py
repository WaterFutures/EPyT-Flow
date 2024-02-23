import sys
sys.path.insert(0,'..')
import numpy as np

from epyt_flow.data.benchmarks.leakdb import load_leakdb
from epyt_flow.data.benchmarks.battledim import load_battledim
from epyt_flow.data.benchmarks.gecco_water_quality import load_gecco2017_water_quality_data, \
    load_gecco2018_water_quality_data, load_gecco2019_water_quality_data, \
        evaluation_score as gecco_evaluation_score
from epyt_flow.data.benchmarks.water_usage import load_water_usage, \
    evaluation_score as water_usage_evaluation_score
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator

from utils import get_temp_folder


def test_leakdb():
    # Net1
    configs = load_leakdb(scenarios_id=range(1, 5), use_net1=True, download_dir=get_temp_folder())

    for c in configs:
        with WaterDistributionNetworkScenarioSimulator(scenario_config=c) as sim:
            res = sim.run_simulation()
            assert res is not None

    # Hanoi
    configs = load_leakdb(scenarios_id=range(1, 5), use_net1=False, download_dir=get_temp_folder())

    for c in configs:
        with WaterDistributionNetworkScenarioSimulator(scenario_config=c) as sim:
            res = sim.run_simulation()
            assert res is not None


def test_battledim():
    hist_scenario = load_battledim(evaluation=False, download_dir=get_temp_folder())
    assert hist_scenario is not None

    eval_scenario = load_battledim(evaluation=True, download_dir=get_temp_folder())
    assert eval_scenario is not None


def test_gecco_water_quality():
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
    df_data= data["train"]
    assert df_data is not None

    df_data= data["validation"]
    assert df_data is not None

    df_data = data["test"]
    assert df_data is not None


def test_water_usage():
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


    data = load_water_usage(return_X_y=False)
    df_data= data["train"]
    assert df_data is not None

    df_data= data["validation"]
    assert df_data is not None

    df_data = data["test"]
    assert df_data is not None
