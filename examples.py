from epyt_flow.simulation import *
from epyt_flow.data.networks import load_hanoi, load_ltown
from epyt_flow.data.benchmarks import load_leakdb
from epyt_flow.uncertainty import *


def run_sim_from_config():
    sim = ScenarioConfigParser.parse("my_scenario_config.xml")
    res = sim.run_simulation()
    ExcelDataExport("results.xlsx").export(sim.get_scenario_config(), res)
    sim.close()


def run_sim_hanoi():
    sim = WaterDistributionNetworkSimulator(load_hanoi())
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))
    res = sim.run_simulation()
    ExcelDataExport("results.xlsx").export(sim.get_scenario_config(), res)
    sim.close()

def run_sim_ltown():
    sim = WaterDistributionNetworkSimulator(load_town(demand_profile="real"))
    sim.set_sensor_config(SensorConfig(pressure_sensors=["n54", "n105", "n114"]))
    res = sim.run_simulation()
    ExcelDataExport("results.xlsx").export(sim.get_scenario_config(), res)
    sim.close()


def run_sim_leakdb():
    sim = WaterDistributionNetworkSimulator(load_leakdb(scenario_id=42))
    res = sim.run_simulation()
    ExcelDataExport("results.xlsx").export(sim.get_scenario_config(), res)
    sim.close()


def run_sim():
    sim = WaterDistributionNetworkScenarioSimulator("Hanoi_CMH_Scenario-1.inp")
    sim.set_general_parameters(simulation_duration=30)  # Simulation for 30 days
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))

    ExcelDataExport("results.xlsx").export(sim.get_scenario_config(), res)
    sim.close()



def run_sim2():
    sim = WaterDistributionNetworkScenarioSimulator("Hanoi_CMH_Scenario-1.inp")
    sim.set_general_parameters(simulation_duration=30)  # Simulation for 30 days
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))

    sim.set_model_uncertainty(ModelUncertainty(demand_base_uncertainty=GaussianUncertainty(mean=0, std=2)))

    ExcelDataExport("results.xlsx").export(sim.get_scenario_config(), res)
    sim.close()
    
    
def run_sensorfaults_sim():
    sim = WaterDistributionNetworkScenarioSimulator("Hanoi_CMH_Scenario-1.inp")
    sim.set_general_parameters(simulation_duration=30)  # Simulation for 30 days
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))

    sim.add_sensor_fault(sensor_faults.StuckAtZero(start_time=1000, end_time=1500, sensor_id="13", sensor_type=NODE_PRESSURE)
    sim.set_sensor_noise(SensorNoise(UniformUncertainty(-5, 5)), sensor_type=NODE_PRESSURE)  # All pressure sensor are affected by a (absolute) uniform uncertainty

    ExcelDataExport("results.xlsx").export(sim.get_scenario_config(), res)
    sim.close()



def run_leaky_sim():
    sim = WaterDistributionNetworkScenarioSimulator("Hanoi_CMH_Scenario-1.inp")
    sim.set_general_parameters(simulation_duration=30)
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))
    
    sim.add_leakage(AbruptLeakage(node_id="10", leak_diameter=0.1, start_time=0, end_time=10000))
    sim.add_leakage(IncipientLeakage(node_id="2", leak_diameter=0.05, start_time=5000, peak_time=8000, end_time=14000))

    NumpyDataExport("results.npz").export(sim.get_scenario_config(), res)
    sim.close()



def run_chlorine_injection():
    sim = WaterDistributionNetworkScenarioSimulator("Hanoi_CMH_Scenario-1.inp")
    sim.set_general_parameters(simulation_duration=30, quality_model={"type": "Chlorine", "units": "mg/L"})
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))
    
    ch_injection_pattern = np.ones(sim.get_max_pattern_length())
    sim.add_chlorine_injection(sim.epanet.getNodeReservoirIndex()[0], ch_injection_pattern, source_type=NODE_QUALITY_SOURCE_TYPE_SETPOINT)


    NumpyDataExport("results.npz").export(sim.get_scenario_config(), res)
    sim.close()
