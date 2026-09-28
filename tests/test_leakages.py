"""
Module provides test to test different types of leakages.
"""
import math
import numpy as np

from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import ScenarioSimulator, IncipientLeakage, AbruptLeakage, Leakage, \
    EpanetConstants
from epyt_flow.utils import to_seconds

from .utils import get_temp_folder


def test_abrupt_leakage():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True,
                                      flow_units_id=EpanetConstants.EN_CMH)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        leak = AbruptLeakage(link_id="12", diameter=0.1, start_time=7200, end_time=100800)
        sim.add_leakage(leak)

        res = sim.run_simulation()
        res.get_data()


def test_abrupt_leakage_area():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True,
                                      flow_units_id=EpanetConstants.EN_CMH)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        leak = AbruptLeakage(link_id="12", area=0.79, start_time=7200, end_time=100800)
        sim.add_leakage(leak)

        res = sim.run_simulation()
        res.get_data()


def test_incipient_leakage():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True,
                                      flow_units_id=EpanetConstants.EN_CMH)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        leak = IncipientLeakage(link_id="12", diameter=0.01,
                                start_time=7200, end_time=100800, peak_time=54000)
        sim.add_leakage(leak)

        res = sim.run_simulation()
        res.get_data()


def test_incipient_leakage_area():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True,
                                      flow_units_id=EpanetConstants.EN_CMH)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        leak = IncipientLeakage(link_id="12", area=0.79,
                                start_time=7200, end_time=100800, peak_time=54000)
        sim.add_leakage(leak)

        res = sim.run_simulation()
        res.get_data()


def test_custom_leakage_profile():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True,
                                      flow_units_id=EpanetConstants.EN_CMH)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        hyd_time_step = sim.epanet_api.get_hydraulic_time_step()
        n_leaky_time_steps = math.ceil((100800 - 7200) / hyd_time_step)

        profile = np.array([.1, .2, .5, .7, .9] + [1.] * (n_leaky_time_steps - 5))
        leak = Leakage(link_id="12", area=0.79, profile=profile, start_time=7200, end_time=100800)
        sim.add_leakage(leak)

        res = sim.run_simulation()
        res.get_data()


def test_leakage_emitter_coefficient():
    for flow_units, expected_coefficient in [(EpanetConstants.EN_CMH, 93.9297458066044),
                                             (EpanetConstants.EN_CFS, 0.04725187090647694)]:
        hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                          flow_units_id=flow_units)
        with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
            leak_kwargs = {"link_id": None, "node_id": "13", "start_time": 0,
                           "end_time": 7200}
            leaks = [
                (Leakage(diameter=0.1, profile=np.ones(2), **leak_kwargs),
                 expected_coefficient),
                (Leakage(area=0.007853981633974483, profile=np.ones(2), **leak_kwargs),
                 expected_coefficient),
                (AbruptLeakage(diameter=0.1, **leak_kwargs), expected_coefficient),
                (IncipientLeakage(diameter=0.1, peak_time=3600, **leak_kwargs),
                 expected_coefficient),
                (Leakage(diameter=0.2, profile=np.ones(2), **leak_kwargs),
                 4. * expected_coefficient),
            ]

            node_idx = sim.epanet_api.get_node_idx("13")
            for leak, expected in leaks:
                sim.add_leakage(leak)
                leak.apply(0)
                coefficient = sim.epanet_api.getnodevalue(node_idx,
                                                          EpanetConstants.EN_EMITTER)
                assert np.isclose(coefficient, expected)
