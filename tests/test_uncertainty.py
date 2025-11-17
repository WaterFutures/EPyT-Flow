"""
Module provides tests to test different types of uncertainties and noise.
"""
import numpy as np
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import ScenarioSimulator, EpanetConstants
from epyt_flow.uncertainty import AbsoluteGaussianUncertainty, RelativeGaussianUncertainty, \
    RelativeUniformUncertainty, AbsoluteUniformUncertainty, PercentageDeviationUncertainty, \
    AbsoluteDeepGaussianUncertainty, RelativeDeepGaussianUncertainty, \
    AbsoluteDeepUniformUncertainty, RelativeDeepUniformUncertainty, ModelUncertainty, SensorNoise
from epyt_flow.utils import to_seconds

from .utils import get_temp_folder


def test_model_uncertainty():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2),
                                   demand_model={"type": EpanetConstants.EN_PDA,
                                                 "pressure_min": 0,
                                                 "pressure_required": 0.1,
                                                 "pressure_exponent": 0.5})
        uncertainties = {"global_pipe_length_uncertainty": RelativeUniformUncertainty(low=0.9,
                                                                                      high=1.1),
                         "global_pipe_roughness_uncertainty": RelativeUniformUncertainty(low=0.75,
                                                                                         high=1.25),
                         "global_pipe_diameter_uncertainty": AbsoluteGaussianUncertainty(mean=0.,
                                                                                         scale=.05),
                         "global_base_demand_uncertainty": RelativeUniformUncertainty(low=0.75,
                                                                                      high=1.25),
                         "global_demand_pattern_uncertainty": RelativeUniformUncertainty(low=0.75,
                                                                                         high=1.25),
                         "global_elevation_uncertainty": AbsoluteGaussianUncertainty(mean=0.,
                                                                                     scale=0.1)}
        sim.set_model_uncertainty(ModelUncertainty(**uncertainties))

        res = sim.run_simulation()
        assert res.get_data() is not None


def test_model_uncertainty_reset():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                        include_default_sensor_placement=True)

    uncertainties = {"global_pipe_length_uncertainty": RelativeUniformUncertainty(low=0.9,
                                                                                  high=1.1),
                    "global_pipe_roughness_uncertainty": RelativeUniformUncertainty(low=0.75,
                                                                                    high=1.25),
                    "global_pipe_diameter_uncertainty": AbsoluteGaussianUncertainty(mean=0.,
                                                                                    scale=.05),
                    "global_base_demand_uncertainty": RelativeUniformUncertainty(low=0.75,
                                                                                 high=1.25),
                    "global_demand_pattern_uncertainty": RelativeUniformUncertainty(low=0.75,
                                                                                    high=1.25),
                    "global_elevation_uncertainty": AbsoluteGaussianUncertainty(mean=0.,
                                                                                scale=0.1)}

    # reapply_uncertainty=True
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.set_model_uncertainty(ModelUncertainty(**uncertainties))

        r1 = sim.run_simulation(reapply_uncertainties=True).get_data()
        r2 = sim.run_simulation(reapply_uncertainties=True).get_data()

        assert not np.all(r1 == r2)

    # reapply_uncertainty=False
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.set_model_uncertainty(ModelUncertainty(**uncertainties))

        r1 = sim.run_simulation().get_data()
        r2 = sim.run_simulation().get_data()

        assert np.all(r1 == r2)


def test_model_uncertainty_seed():
    def run_sim() -> np.ndarray:
        hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                          include_default_sensor_placement=True)
        with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
            sim.set_general_parameters(simulation_duration=to_seconds(days=2))
            uncertainties = {"global_pipe_length_uncertainty": RelativeUniformUncertainty(low=0.9,
                                                                                        high=1.1),
                            "global_pipe_roughness_uncertainty": RelativeUniformUncertainty(low=0.75,
                                                                                            high=1.25),
                            "global_pipe_diameter_uncertainty": AbsoluteGaussianUncertainty(mean=0.,
                                                                                            scale=.05),
                            "global_base_demand_uncertainty": RelativeUniformUncertainty(low=0.75,
                                                                                        high=1.25),
                            "global_demand_pattern_uncertainty": RelativeUniformUncertainty(low=0.75,
                                                                                            high=1.25),
                            "global_elevation_uncertainty": AbsoluteGaussianUncertainty(mean=0.,
                                                                                        scale=0.1)}
            sim.set_model_uncertainty(ModelUncertainty(**uncertainties, seed=42))

            return sim.run_simulation().get_data()

    data_1 = run_sim()
    data_2 = run_sim()

    assert np.all(data_1 == data_2)


def test_sensor_noise():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2),
                                   demand_model={"type": EpanetConstants.EN_PDA,
                                                 "pressure_min": 0,
                                                 "pressure_required": 0.1,
                                                 "pressure_exponent": 0.5})
        sim.set_sensor_noise(SensorNoise(global_uncertainty=RelativeGaussianUncertainty(scale=1.)))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2),
                                   demand_model={"type": EpanetConstants.EN_PDA,
                                                 "pressure_min": 0,
                                                 "pressure_required": 0.1,
                                                 "pressure_exponent": 0.5})
        sim.set_sensor_noise(SensorNoise(global_uncertainty=PercentageDeviationUncertainty(0.2)))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2),
                                   demand_model={"type": EpanetConstants.EN_PDA,
                                                 "pressure_min": 0,
                                                 "pressure_required": 0.1,
                                                 "pressure_exponent": 0.5})
        sim.set_sensor_noise(SensorNoise(global_uncertainty=AbsoluteUniformUncertainty(0, .5)))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2),
                                   demand_model={"type": EpanetConstants.EN_PDA,
                                                 "pressure_min": 0,
                                                 "pressure_required": 0.1,
                                                 "pressure_exponent": 0.5})
        sim.set_sensor_noise(SensorNoise(global_uncertainty=AbsoluteDeepUniformUncertainty()))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2),
                                   demand_model={"type": EpanetConstants.EN_PDA,
                                                 "pressure_min": 0,
                                                 "pressure_required": 0.1,
                                                 "pressure_exponent": 0.5})
        sim.set_sensor_noise(SensorNoise(global_uncertainty=RelativeDeepUniformUncertainty()))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2),
                                   demand_model={"type": EpanetConstants.EN_PDA,
                                                 "pressure_min": 0,
                                                 "pressure_required": 0.1,
                                                 "pressure_exponent": 0.5})
        sim.set_sensor_noise(SensorNoise(global_uncertainty=AbsoluteDeepUniformUncertainty()))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2),
                                   demand_model={"type": EpanetConstants.EN_PDA,
                                                 "pressure_min": 0,
                                                 "pressure_required": 0.1,
                                                 "pressure_exponent": 0.5})
        sim.set_sensor_noise(SensorNoise(global_uncertainty=AbsoluteDeepGaussianUncertainty()))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2),
                                   demand_model={"type": EpanetConstants.EN_PDA,
                                                 "pressure_min": 0,
                                                 "pressure_required": 0.1,
                                                 "pressure_exponent": 0.5})
        sim.set_sensor_noise(SensorNoise(global_uncertainty=RelativeDeepGaussianUncertainty()))

        res = sim.run_simulation()
        assert res.get_data() is not None
