from epyt_flow import *
from epyt_flow.data.networks import load_hanoi, load_ltown
from epyt_flow.data.scenarios import load_leakdb


def run_sim_hanoi():
    sim = load_hanoi()
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))
    sim.run_simulation(ExcelDataExport("results.xlsx"))
    sim.close()

def run_sim_ltown():
    sim = load_town(demand_profile="real")
    sim.run_simulation(SensorConfig(pressure_sensors=["n54", "n105", "n114"]), ExcelDataExport("results.xlsx"))
    sim.close()


def run_sim_leakdb():
    sim = load_leakdb(scenario_id=42)
    sim.run_simulation(ExcelDataExport("results.xlsx"))
    sim.close()


def run_sim():
    sim = WaterDistributionNetworkScenarioSimulator("Hanoi_CMH_Scenario-1.inp")
    sim.set_general_parameters(simulation_duration=30)  # Simulation for 30 days
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))

    sim.run_simulation(ExcelDataExport("results.xlsx"))
    sim.close()



def run_sim2():
    sim = WaterDistributionNetworkScenarioSimulator("Hanoi_CMH_Scenario-1.inp")
    sim.set_general_parameters(simulation_duration=30)  # Simulation for 30 days
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))

    sim.add_demand_uncertainty(GaussianUncertainty(mean=0, std=2)

    sim.run_simulation(ExcelDataExport("results.xlsx"))
    sim.close()
    
    
def run_sensorfaults_sim():
    sim = WaterDistributionNetworkScenarioSimulator("Hanoi_CMH_Scenario-1.inp")
    sim.set_general_parameters(simulation_duration=30)  # Simulation for 30 days
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))

    sim.add_sensor_fault(sensor_faults.StuckAtZero(start_time=1000, end_time=1500, sensor_id="13", sensor_type=NODE_PRESSURE)
    sim.add_sensor_uncertainty(SensorUncertainty(UniformUncertainty(-5, 5)), sensor_type=NODE_PRESSURE)  # All pressure sensor are affected by a (absolute) uniform uncertainty

    sim.run_simulation(ExcelDataExport("results.xlsx"))
    sim.close()



def run_leaky_sim():
    sim = WaterDistributionNetworkScenarioSimulator("Hanoi_CMH_Scenario-1.inp")
    sim.set_general_parameters(simulation_duration=30)
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))
    
    sim.add_leakage(AbruptLeakage(node_id="10", leak_diameter=0.1, start_time=0, end_time=10000))
    sim.add_leakage(IncipientLeakage(node_id="2", leak_diameter=0.05, start_time=5000, peak_time=8000, end_time=14000))

    sim.run_simulation(NumpyDataExport("results.npz"))
    sim.close()



def run_chlorine_injection():
    sim = WaterDistributionNetworkScenarioSimulator("Hanoi_CMH_Scenario-1.inp")
    sim.set_general_parameters(simulation_duration=30, quality_model={"type": "Chlorine", "units": "mg/L"})
    sim.set_sensor_config(SensorConfig(pressure_sensors=["13", "16", "22", "30"]))
    
    ch_injection_pattern = np.ones(sim.get_max_pattern_length())
    sim.add_chlorine_injection(sim.epanet.getNodeReservoirIndex()[0], ch_injection_pattern, source_type=NODE_QUALITY_SOURCE_TYPE_SETPOINT)


    sim.run_simulation(NumpyDataExport("results.npz"))
    sim.close()
