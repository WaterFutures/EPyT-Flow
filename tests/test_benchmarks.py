import sys
sys.path.insert(0,'..')

from epyt_flow.data.benchmarks import load_leakdb, load_battledim
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
