"""
Module provides tests to test the `epty_flow.data.benchmarks` module.
"""
from datetime import datetime
import json
import numpy as np
from epyt_flow.data.benchmarks import load_batadal_data
from epyt_flow.data.benchmarks import load_leakdb_scenarios, load_leakdb_scada_data, \
    load_leakdb_data, compute_leakdb_evaluation_score
from epyt_flow.data.benchmarks.leakdb_data import NET1_LEAKAGES
from epyt_flow.data.benchmarks import load_battledim_scenario, compute_battledim_evaluation_score
from epyt_flow.data.benchmarks.battledim_data import LEAKS_CONFIG_TEST, START_TIME_TEST
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
                                              download_dir=get_temp_folder(),
                                              return_leak_locations=True)[0]
    assert X is not None
    assert y is not None
    assert y_leak_loc is not None

    data = load_leakdb_data(scenarios_id=range(1, 5), use_net1=True, download_dir=get_temp_folder())
    assert data is not None

    data = load_leakdb_data(scenarios_id=range(1, 5), use_net1=True, return_X_y=True,
                            download_dir=get_temp_folder(),
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
                                              download_dir=get_temp_folder(),
                                              return_leak_locations=True)[0]
    assert X is not None
    assert y is not None
    assert y_leak_loc is not None

    data = load_leakdb_data(scenarios_id=range(1, 5), use_net1=False, download_dir=get_temp_folder())
    assert data is not None

    data = load_leakdb_data(scenarios_id=range(1, 5), use_net1=False, return_X_y=True,
                            download_dir=get_temp_folder(),
                            return_features_desc=True, return_leak_locations=True)
    assert data is not None


def test_leakdb_evaluation_score():
    # Expected values as computed by the official scoring_algorithm.m.
    # Scenario 3 has two overlapping leaks (counted as one), scenario 9 has two leaks,
    # the second one lasting only 4 time steps.
    scenarios_id = [1, 2, 3, 5, 6, 9]
    n_time_steps = 17520
    leaks_info = json.loads(NET1_LEAKAGES)

    y_true = []
    y_burst = []
    for s_id in scenarios_id:
        y = np.zeros(n_time_steps)
        y_b = np.zeros(n_time_steps)
        for leak in leaks_info[str(s_id)]:
            t_start = int(leak["leak_start_time"])
            y[t_start:int(np.ceil(leak["leak_end_time"]))] = 1
            y_b[t_start:t_start + 10] = 1
        y_true.append(y)
        y_burst.append(y_b)

    # Perfect detector -- the 4 time steps long leak is not detected because only 4 of the
    # 14 time steps in its detection window are alarms
    score = compute_leakdb_evaluation_score(scenarios_id, True, y_true)
    assert score["f1_score"] == 1.
    assert score["true_positive_rate"] == 1.
    assert score["true_negative_rate"] == 1.
    assert abs(score["early_detection_score"] - 6. / 7.) < 1e-10

    # Detector that is delayed by 5 time steps
    y_delayed = [np.concatenate((np.zeros(5), y[:-5])) for y in y_true]
    score = compute_leakdb_evaluation_score(scenarios_id, True, y_delayed)
    assert abs(score["f1_score"] - 0.9985504774897682) < 1e-10
    assert abs(score["true_negative_rate"] - 0.9995836598746082) < 1e-10
    assert abs(score["early_detection_score"] - 0.8511361425430957) < 1e-10

    # Alarms only in the first 10 time steps of each leak
    score = compute_leakdb_evaluation_score(scenarios_id, True, y_burst)
    assert abs(score["f1_score"] - 0.00628823929299796) < 1e-10
    assert score["early_detection_score"] == 0.

    # Alarm in every time step
    score = compute_leakdb_evaluation_score(scenarios_id, True,
                                            [np.ones(n_time_steps) for _ in scenarios_id])
    assert score["true_positive_rate"] == 1.
    assert score["true_negative_rate"] == 0.
    assert score["early_detection_score"] == 1.


def test_battledim():
    hist_scenario = load_battledim_scenario(return_test_scenario=False,
                                            download_dir=get_temp_folder())
    assert hist_scenario is not None

    eval_scenario = load_battledim_scenario(return_test_scenario=True,
                                            download_dir=get_temp_folder())
    assert eval_scenario is not None


def test_battledim_evaluation_score():
    # One alarm on each leaky pipe at the start of its leak
    perfect_alarms = []
    for leak in LEAKS_CONFIG_TEST.splitlines():
        items = [i.strip() for i in leak.split(",")]
        start_time = (datetime.strptime(items[1], "%Y-%m-%d %H:%M") - START_TIME_TEST)
        perfect_alarms.append((items[0], int(start_time.total_seconds())))

    # As in the official PERFECT_TEAM_report.txt: EUR 523,153.82 with 23 true positives
    score = compute_battledim_evaluation_score(perfect_alarms, test_scenario=True)
    assert score["true_positives"] == 23 and score["false_positives"] == 0
    assert abs(score["total_savings"] - 523153.82) < .01

    # Repeated detections are ignored
    score = compute_battledim_evaluation_score(perfect_alarms + perfect_alarms,
                                               test_scenario=True)
    assert score["true_positives"] == 23 and score["false_positives"] == 0
    assert abs(score["total_savings"] - 523153.82) < .01

    # An alarm more than 300m away from all leaks is a false positive
    score = compute_battledim_evaluation_score([("p227", 3600)], test_scenario=True)
    assert score["true_positives"] == 0 and score["false_positives"] == 1
    assert score["total_savings"] == -500.


def test_gecco_water_quality():
    # 2017 version
    X, y = load_gecco2017_water_quality_data(download_dir=get_temp_folder(), return_X_y=True)
    assert X is not None
    assert y is not None
    assert gecco_evaluation_score(np.random.choice([0, 1], size=y.shape), y=y) is not None

    df_data = load_gecco2017_water_quality_data(download_dir=get_temp_folder(), return_X_y=False)
    assert df_data is not None

    # 2018 version
    X, y = load_gecco2018_water_quality_data(download_dir=get_temp_folder(), return_X_y=True)
    assert X is not None
    assert y is not None
    assert gecco_evaluation_score(np.random.choice([0, 1], size=y.shape), y=y) is not None

    df_data = load_gecco2018_water_quality_data(download_dir=get_temp_folder(), return_X_y=False)
    assert df_data is not None

    # 2019 version
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
    data = load_water_usage(return_X_y=True, download_dir=get_temp_folder())
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

    # Load as pandas.DataFrame instances
    data = load_water_usage(return_X_y=False, download_dir=get_temp_folder())
    df_data = data["train"]
    assert df_data is not None

    df_data = data["validation"]
    assert df_data is not None

    df_data = data["test"]
    assert df_data is not None
