import sys
sys.path.insert(0,'..')

import epyt_flow
from epyt_flow.data.networks import load_hanoi
from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator
from epyt_flow.simulation.events import SensorFaultConstant, SensorFaultDrift,\
    SensorFaultPercentage, SensorFaultStuckZero, SensorFaultGaussian

from utils import get_temp_folder


def test_sensor_fault():
    hanoi_network_config = load_hanoi(download_dir=get_temp_folder(),
                                      include_default_sensor_placement=True)

    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)
        sim.add_sensor_fault(
            SensorFaultConstant(constant_shift=2., sensor_id="16",
                                sensor_type=epyt_flow.simulation.SENSOR_TYPE_NODE_PRESSURE,
                                start_time=5000, end_time=100000))

        res = sim.run_simulation()
        res.get_data()


    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)
        sim.add_sensor_fault(
            SensorFaultDrift(coef=1.1, sensor_id="16",
                             sensor_type=epyt_flow.simulation.SENSOR_TYPE_NODE_PRESSURE,
                             start_time=5000, end_time=100000))

        res = sim.run_simulation()
        res.get_data()

    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)
        sim.add_sensor_fault(
            SensorFaultStuckZero(sensor_id="16",
                                 sensor_type=epyt_flow.simulation.SENSOR_TYPE_NODE_PRESSURE,
                                 start_time=5000, end_time=100000))

        res = sim.run_simulation()
        res.get_data()

    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)
        sim.add_sensor_fault(
            SensorFaultGaussian(std=1., sensor_id="16",
                                sensor_type=epyt_flow.simulation.SENSOR_TYPE_NODE_PRESSURE,
                                start_time=5000, end_time=100000))

        res = sim.run_simulation()
        res.get_data()

    with WaterDistributionNetworkScenarioSimulator(scenario_config=hanoi_network_config) as sim:
        sim.set_general_parameters(simulation_duration=2)
        sim.add_sensor_fault(
            SensorFaultPercentage(coef=1.2, sensor_id="16",
                                  sensor_type=epyt_flow.simulation.SENSOR_TYPE_NODE_PRESSURE,
                                  start_time=5000, end_time=100000))

        res = sim.run_simulation()
        res.get_data()
