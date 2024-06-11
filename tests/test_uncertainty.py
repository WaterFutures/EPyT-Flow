"""
Module provides tests to test different types of uncertainties and noise.
"""
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import ScenarioSimulator
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
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.set_model_uncertainty(
            ModelUncertainty(pipe_length_uncertainty=RelativeUniformUncertainty(low=0.9,
                                                                                high=1.1),
                             pipe_roughness_uncertainty=RelativeUniformUncertainty(low=0.75,
                                                                                   high=1.25),
                             pipe_diameter_uncertainty=AbsoluteGaussianUncertainty(mean=0.,
                                                                                   scale=.05),
                             base_demand_uncertainty=RelativeUniformUncertainty(low=0.75,
                                                                                high=1.25),
                             demand_pattern_uncertainty=RelativeUniformUncertainty(low=0.75,
                                                                                   high=1.25),
                             elevation_uncertainty=AbsoluteGaussianUncertainty(mean=0.,
                                                                               scale=0.1)))

        res = sim.run_simulation()
        assert res.get_data() is not None


def test_sensor_noise():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.set_sensor_noise(SensorNoise(RelativeGaussianUncertainty(scale=1.)))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.set_sensor_noise(SensorNoise(PercentageDeviationUncertainty(0.2)))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.set_sensor_noise(SensorNoise(AbsoluteUniformUncertainty(0, .5)))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.set_sensor_noise(SensorNoise(AbsoluteDeepUniformUncertainty()))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.set_sensor_noise(SensorNoise(RelativeDeepUniformUncertainty()))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.set_sensor_noise(SensorNoise(AbsoluteDeepUniformUncertainty()))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.set_sensor_noise(SensorNoise(AbsoluteDeepGaussianUncertainty()))

        res = sim.run_simulation()
        assert res.get_data() is not None

    with ScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))
        sim.set_sensor_noise(SensorNoise(RelativeDeepGaussianUncertainty()))

        res = sim.run_simulation()
        assert res.get_data() is not None
