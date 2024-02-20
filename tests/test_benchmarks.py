import sys
sys.path.insert(0,'..')

from epyt_flow.data.benchmarks import load_leakdb, load_battledim
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator


def test_leakdb():
    # Net1
    configs = load_leakdb(scenarios_id=range(1, 5), use_net1=True)

    for c in configs:
        with WaterDistributionNetworkScenarioSimulator(scenario_config=c) as sim:
            res = sim.run_simulation()
            assert res is not None

    # Hanoi
    configs = load_leakdb(scenarios_id=range(1, 5), use_net1=False)

    for c in configs:
        with WaterDistributionNetworkScenarioSimulator(scenario_config=c) as sim:
            res = sim.run_simulation()
            assert res is not None


def test_battledim():
    hist_scenario = load_battledim(evaluation=False)
    assert hist_scenario is not None

    eval_scenario = load_battledim(evaluation=True)
    assert eval_scenario is not None
