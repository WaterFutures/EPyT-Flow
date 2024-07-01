"""
Example of implementing a simple pump control strategy.
"""
from epyt_flow.data.networks import load_net1
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.simulation import AdvancedControlModule, ScadaData
from epyt_flow.utils import to_seconds, volume_to_level
from epyt_flow.simulation.events import ActuatorConstants


class MyControl(AdvancedControlModule):
    """
    Mimics the control rules stated in Net1.inp
    """
    def __init__(self, **kwds):
        # Tank and pump ID
        self.__tank_id = "2"
        self.__pump_id = "9"

        # Tank diameter could be also obtained by calling epanet.getNodeTankData
        self.__tank_diameter = 50.5

        # Lower and upper threshold on tank level
        self.__lower_level_threshold = 110
        self.__upper_level_threshold = 140

        super().__init__(**kwds)

    def step(self, scada_data: ScadaData) -> None:
        # Retrieve current water level in the tank
        tank_volume = scada_data.get_data_tanks_water_volume([self.__tank_id])[0, 0]
        tank_level = volume_to_level(float(tank_volume), self.__tank_diameter)

        # Decide if pump has to be deactivated or re-activated
        if tank_level <= self.__lower_level_threshold:
            self.set_pump_status(self.__pump_id, ActuatorConstants.EN_OPEN)
        elif tank_level >= self.__upper_level_threshold:
            self.set_pump_status(self.__pump_id, ActuatorConstants.EN_CLOSED)


if __name__ == "__main__":
    # Create new scenario based on Net1
    with ScenarioSimulator(scenario_config=load_net1()) as sim:
        # Set simulation duration to two days
        sim.set_general_parameters(simulation_duration=to_seconds(days=2))

        # Monitor states of tank "2" and pump "9"
        sim.set_tank_sensors(sensor_locations=["2"])
        sim.set_pump_state_sensors(sensor_locations=["9"])

        # Remove all existing controls
        sim.epanet_api.deleteControls()

        # Add custom controls
        sim.add_control(MyControl())

        # Run simulation and show sensor readings over time
        scada_data_res = sim.run_simulation()
        print(scada_data_res.get_data())
