import sys
sys.path.insert(0,'..')

from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator
from epyt_flow.uncertainty import GaussianUncertainty, UniformUncertainty, ModelUncertainty, SensorNoise

from utils import get_temp_folder


def test_model_uncertainty():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)
        sim.set_model_uncertainty(
            ModelUncertainty(pipe_length_uncertainty=GaussianUncertainty(mean=0., scale=1.),
                             pipe_roughness_uncertainty=UniformUncertainty(low=0.0, high=0.1),
                             pipe_diameter_uncertainty=GaussianUncertainty(mean=0., scale=.5),
                             demand_base_uncertainty=UniformUncertainty(low=0, high=.1),
                             demand_pattern_uncertainty=UniformUncertainty(low=0, high=1),
                             elevation_uncertainty=GaussianUncertainty()))

        res = sim.run_simulation()
        res.get_data()


def test_sensor_noise():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)
    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)
        sim.set_sensor_noise(SensorNoise(GaussianUncertainty(mean=0, scale=1.)))

        res = sim.run_simulation()
        res.get_data()
