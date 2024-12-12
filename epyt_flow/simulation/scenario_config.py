"""
Module provides a class for specifying scenario configurations.
"""
from typing import Any
from copy import deepcopy
import os
import json
from pathlib import Path
import numpy as np

from ..uncertainty import AbsoluteGaussianUncertainty, RelativeGaussianUncertainty, \
    AbsoluteUniformUncertainty, RelativeUniformUncertainty, ModelUncertainty, \
    SensorNoise, Uncertainty
from .sensor_config import SensorConfig
from .scada import AdvancedControlModule
from .events import SystemEvent, SensorReadingEvent
from .events.sensor_faults import SensorFaultConstant, SensorFaultDrift, SensorFaultGaussian, \
    SensorFaultPercentage, SensorFaultStuckZero
from .events.leakages import AbruptLeakage, IncipientLeakage
from ..serialization import serializable, Serializable, SCENARIO_CONFIG_ID


@serializable(SCENARIO_CONFIG_ID, ".epytflow_scenario_config")
class ScenarioConfig(Serializable):
    """
    Configuration of a scenario.

    Parameters
    ----------
    scenario_config : :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`, optional
        Uses the given scenario configuration to create this instance --
        other attributes passed to this constructor override the attributes in 'scenario_config'.

        Note that if 'scenario_config' is None then 'f_inp_in' can not be None --
        i.e. either 'scenario_config' or 'f_inp_in' must be given.

        The default is None.
    f_inp_in : `str`, optional
        Path to the .inp file.

        Note that if 'f_inp_in' is None then 'scenario_config' can not be None --
        i.e. either 'scenario_config' or 'f_inp_in' must be given.

        The default is None.
    f_msx_in : `str`, optional
        Path to the .msx file -- optional, only necessary if EPANET-MSX is used.

        The default is None
    general_params : `dict`, optional
        General parameters such as the demand model, hydraulic time steps, etc.

        The default is None
    sensor_config : :class:`~epyt_flow.simulation.sensor_config.SensorConfig`, optional
        Specification of all sensors.

        The default is None
    memory_consumption_estimate : float, optional
        Estimated memory consumption of this scenario in MB -- i.e. the amount of memory that is
        needed on the hard disk as well as in RAM.

        The default is None.
    sensor_noise : :class:`~epyt_flow.uncertainty.sensor_noise.SensorNoise`, optional
        Speciation of sensor noise -- i.e. noise/uncertainty affecting the sensor readings.

        The default is None
    controls : list[:class:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule`], optional
        List of control modules that are active during the simulation.

        The default is an empty list.
    model_uncertainty : :class:`~epyt_flow.uncertainty.model_uncertainty.ModelUncertainty`, optional
        Specification of model uncertainty.
    system_events : list[:class:`~epyt_flow.simulation.events.system_event.SystemEvent`], optional
        List of system events -- i.e. events that directly affect the simulation (e.g. leakages).

        The default is an empty list.
    sensor_reading_events : list[:class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent`], optional
        List of sensor reading events -- i.e. events that affect the readings of sensors.

        The default is an empty list.
    """

    def __init__(self, scenario_config: Any = None, f_inp_in: str = None, f_msx_in: str = None,
                 general_params: dict = None, sensor_config: SensorConfig = None,
                 memory_consumption_estimate: float = None,
                 controls: list[AdvancedControlModule] = [],
                 sensor_noise: SensorNoise = None,
                 model_uncertainty: ModelUncertainty = None,
                 system_events: list[SystemEvent] = [],
                 sensor_reading_events: list[SensorReadingEvent] = [], **kwds):
        if f_inp_in is None and scenario_config is None:
            raise ValueError("Either 'f_inp_in' or 'scenario_config' must be given")
        if scenario_config is not None:
            if not isinstance(scenario_config, ScenarioConfig):
                raise TypeError("'scenario_config' must be an instance of " +
                                "'epyt_flow.simulation.ScenarioConfig' but not of " +
                                f"'{type(scenario_config)}'")
        if f_inp_in is not None:
            if not isinstance(f_inp_in, str):
                raise TypeError("'f_inp_in' must be an instance of 'str' " +
                                f"but no of '{type(f_inp_in)}'")
        if f_msx_in is not None:
            if not isinstance(f_msx_in, str):
                raise TypeError("'f_msx_in' must be an instance of 'str' " +
                                f"but no of '{type(f_msx_in)}'")
        if general_params is not None:
            if not isinstance(general_params, dict):
                raise TypeError("'general_params' must be an instance of 'dict' " +
                                f"but not of '{type(general_params)}'")
        if sensor_config is not None:
            if not isinstance(sensor_config, SensorConfig):
                raise TypeError("'sensor_config' must be an instance of " +
                                "'epyt_flow.simulation.SensorConfig' but not of " +
                                f"'{type(sensor_config)}'")
        if memory_consumption_estimate is not None:
            if not isinstance(memory_consumption_estimate, float) or \
                    memory_consumption_estimate <= 0:
                raise ValueError("'memory_consumption_estimate' must be a positive integer")
        if not isinstance(controls, list):
            raise TypeError("'controls' must be an instance of " +
                            "'list[epyt_flow.simulation.scada.AdvancedControlModule]' but no of " +
                            f"'{type(controls)}'")
        if len(controls) != 0:
            if any(not isinstance(c, AdvancedControlModule) for c in controls):
                raise TypeError("Each item in 'controls' must be an instance of " +
                                "'epyt_flow.simulation.scada.AdvancedControlModule'")
        if sensor_noise is not None:
            if not isinstance(sensor_noise, SensorNoise):
                raise TypeError("'sensor_noise' must be an instance of " +
                                "'epyt_flow.uncertainty.SensorNoise' but not of " +
                                f"'{type(sensor_noise)}'")
        if model_uncertainty is not None:
            if not isinstance(model_uncertainty, ModelUncertainty):
                raise TypeError("'model_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.ModelUncertainty' but not of " +
                                f"'{type(model_uncertainty)}'")
        if not isinstance(system_events, list):
            raise TypeError("'system_events' must be an instance of " +
                            "'list[epyt_flow.simulation.events.SystemEvent]' but no of " +
                            f"'{type(system_events)}'")
        if len(system_events) != 0:
            if any(not isinstance(c, SystemEvent) for c in system_events):
                raise TypeError("Each item in 'system_events' must be an instance of " +
                                "'epyt_flow.simulation.events.SystemEvent'")
        if not isinstance(sensor_reading_events, list):
            raise TypeError("'sensor_reading_events' must be an instance of " +
                            "'list[epyt_flow.simulation.events.SensorReadingEvent]' but not of " +
                            f"'{type(sensor_reading_events)}'")
        if len(sensor_reading_events) != 0:
            if any(not isinstance(c, SensorReadingEvent) for c in sensor_reading_events):
                raise TypeError("Each item in 'sensor_reading_events' must be an instance of " +
                                "'epyt_flow.simulation.events.SensorReadingEvent'")

        if scenario_config is not None:
            self.__f_inp_in = scenario_config.f_inp_in
            self.__f_msx_in = scenario_config.f_msx_in if f_msx_in is None else f_msx_in

            if general_params is None:
                self.__general_params = scenario_config.general_params
            else:
                self.__general_params = general_params

            if sensor_config is None:
                self.__sensor_config = scenario_config.sensor_config
            else:
                self.__sensor_config = sensor_config

            if memory_consumption_estimate is None:
                self.__memory_consumption_estimate = scenario_config.memory_consumption_estimate
            else:
                self.__memory_consumption_estimate = memory_consumption_estimate

            if len(controls) == 0:
                self.__controls = scenario_config.controls
            else:
                self.__controls = controls

            if sensor_noise is None:
                self.__sensor_noise = scenario_config.sensor_noise
            else:
                self.__sensor_noise = sensor_noise

            if model_uncertainty is None:
                self.__model_uncertainty = scenario_config.model_uncertainty
            else:
                self.__model_uncertainty = model_uncertainty

            if len(system_events) == 0:
                self.__system_events = scenario_config.system_events
            else:
                self.__system_events = system_events

            if len(sensor_reading_events) == 0:
                self.__sensor_reading_events = scenario_config.sensor_reading_events
            else:
                self.__sensor_reading_events = sensor_reading_events
        else:
            self.__f_inp_in = f_inp_in
            self.__f_msx_in = f_msx_in
            self.__general_params = general_params
            self.__sensor_config = sensor_config
            self.__memory_consumption_estimate = memory_consumption_estimate
            self.__controls = controls
            self.__sensor_noise = sensor_noise
            self.__system_events = system_events
            self.__sensor_reading_events = sensor_reading_events

            if model_uncertainty is not None:
                self.__model_uncertainty = model_uncertainty
            else:
                self.__model_uncertainty = ModelUncertainty()

        super().__init__(**kwds)

    @property
    def f_inp_in(self) -> str:
        """
        Gets the path to the .inp file.

        Returns
        -------
        `str`
            Path to the .inp file.
        """
        if Path(self.__f_inp_in).is_absolute():
            return self.__f_inp_in
        elif Path(self.__f_inp_in).name == self.__f_inp_in:
            return os.path.join(self._parent_path, self.__f_inp_in)
        else:
            return self.__f_inp_in

    @property
    def f_msx_in(self) -> str:
        """
        Gets the path to the .msx file.

        Returns
        -------
        `str`
            Path to the .msx file.
        """
        if self.__f_msx_in is None:
            return None
        else:
            if Path(self.__f_msx_in).is_absolute():
                return self.__f_msx_in
            elif Path(self.__f_msx_in).name == self.__f_msx_in:
                return os.path.join(self._parent_path, self.__f_msx_in)
            else:
                return self.__f_msx_in

    @property
    def general_params(self) -> dict:
        """
        Gets general parameters such as hydraulic time step, etc.

        Returns
        -------
        `dict`
            All general parameters as dictionary -- the parameter name serves as a key.
        """
        return deepcopy(self.__general_params)

    @property
    def sensor_config(self) -> SensorConfig:
        """
        Gets the sensor configuration.

        Returns
        -------
        :class:`~epyt_flow.simulation.sensor_config.SensorConfig`
            Sensor configuration.
        """
        return deepcopy(self.__sensor_config)

    @property
    def memory_consumption_estimate(self) -> float:
        """
        Gets the estimated memory consumption of this scenario -- i.e. the amount of memory that is
        needed on the hard disk as well as in RAM.

        Returns
        -------
        `float`
            Estimated memory consumption in MB.
        """
        return self.__memory_consumption_estimate

    @property
    def controls(self) -> list[AdvancedControlModule]:
        """
        Gets the list of all control modules that are active during the simulation.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule`]
            List of all control modules that are active during the simulation.
        """
        return deepcopy(self.__controls)

    @property
    def sensor_noise(self) -> SensorNoise:
        """
        Gets the sensor noise/uncertainty specification.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.sensor_noise.SensorNoise`
            Sensor noise/uncertainty.
        """
        return deepcopy(self.__sensor_noise)

    @property
    def model_uncertainty(self) -> ModelUncertainty:
        """
        Gets the model uncertainty specification.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.model_uncertainty.ModelUncertainty`
            Model uncertainty specification.
        """
        return deepcopy(self.__model_uncertainty)

    @property
    def system_events(self) -> list[SystemEvent]:
        """
        Gets all system events.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.events.system_event.SystemEvent`]
            All system events.
        """
        return deepcopy(self.__system_events)

    @property
    def sensor_reading_events(self) -> list[SensorReadingEvent]:
        """
        Gets all sensor reading events.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent`]
            All sensor reading events.
        """
        return deepcopy(self.__sensor_reading_events)

    def get_attributes(self) -> dict:
        my_attributes = {"f_inp_in": self.__f_inp_in, "f_msx_in": self.__f_msx_in,
                         "general_params": self.__general_params,
                         "sensor_config": self.__sensor_config,
                         "memory_consumption_estimate": self.__memory_consumption_estimate,
                         "controls": self.__controls,
                         "sensor_noise": self.__sensor_noise,
                         "model_uncertainty": self.__model_uncertainty,
                         "system_events": self.__system_events,
                         "sensor_reading_events": self.__sensor_reading_events}

        return super().get_attributes() | my_attributes

    def __eq__(self, other) -> bool:
        if not isinstance(other, ScenarioConfig):
            raise TypeError("Can not compare 'ScenarioConfig' instance " +
                            f"with '{type(other)}' instance")

        return self.__f_inp_in == other.f_inp_in and self.__f_msx_in == other.f_msx_in \
            and self.__general_params == other.general_params \
            and self.__memory_consumption_estimate == other.memory_consumption_estimate \
            and self.__sensor_config == other.sensor_config \
            and np.all(self.__controls == other.controls) \
            and self.__model_uncertainty == other.model_uncertainty \
            and np.all(self.__system_events == other.system_events) \
            and np.all(self.__sensor_reading_events == other.sensor_reading_events)

    def __str__(self) -> str:
        return f"f_inp_in: {self.f_inp_in} f_msx_in: {self.f_msx_in} " + \
            f"general_params: {self.general_params} sensor_config: {self.sensor_config} " + \
            f"memory_consumption_estimate: {self.memory_consumption_estimate} " + \
            f"controls: {self.controls} sensor_noise: {self.sensor_noise} " + \
            f"model_uncertainty: {self.model_uncertainty} " + \
            f"system_events: {','.join(map(str, self.system_events))} " + \
            f"sensor_reading_events: {','.join(map(str, self.sensor_reading_events))}"

    @staticmethod
    def load_from_json_file(f_json_in: str) -> Any:
        """
        Loads a scenario configuration from a given JSON file.

        Parameters
        ----------
        f_json_in : `str`
            Path to JSON configuration file.

        Returns
        -------
        :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
            Loaded scenario configuration.
        """
        with open(f_json_in, "r", encoding="utf-8") as f:
            return ScenarioConfig.load_from_json(f.read())

    @staticmethod
    def load_from_json(config_data: str) -> Any:
        """
        Loads a scenario configuration from a given JSON string.

        Parameters
        ----------
        config_data : `str`
            JSON data.

        Returns
        -------
        :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
            Loaded scenario configuration.
        """
        data = json.loads(config_data)

        # General parameters and sensor configuration
        general_settings = data["general"]
        f_inp_in = general_settings["file_inp"]
        f_msx_in = general_settings["file_msx"] if "file_msx" in general_settings.keys() else None

        general_params = {"simulation_duration": general_settings["simulation_duration"],
                          "hydraulic_time_step": general_settings["hydraulic_time_step"],
                          "quality_time_step": general_settings["quality_time_step"]}
        if "reporting_time_step" in general_settings.keys():
            general_params["reporting_time_step"] = general_settings["reporting_time_step"]
        if "reporting_time_start" in general_settings.keys():
            general_params["reporting_time_start"] = general_settings["reporting_time_start"]
        if "demand_model" in general_settings.keys():
            general_params["demand_model"] = general_settings["demand_model"]
        if "quality_model" in general_settings.keys():
            general_params["quality_model"] = general_settings["quality_model"]
        if "flow_units_id" in general_settings.keys():
            general_params["flow_units_id"] = general_settings["flow_units_id"]

        sensor_config = data["sensors"]

        if "pressure_sensors" in sensor_config.keys():
            pressure_sensors = sensor_config["pressure_sensors"]
        else:
            pressure_sensors = []

        if "flow_sensors" in sensor_config.keys():
            flow_sensors = sensor_config["flow_sensors"]
        else:
            flow_sensors = []

        if "demand_sensors" in sensor_config.keys():
            demand_sensors = sensor_config["demand_sensors"]
        else:
            demand_sensors = []

        if "node_quality_sensors" in sensor_config.keys():
            node_quality_sensors = sensor_config["node_quality_sensors"]
        else:
            node_quality_sensors = []

        if "link_quality_sensors" in sensor_config.keys():
            link_quality_sensors = sensor_config["link_quality_sensors"]
        else:
            link_quality_sensors = []

        if "tank_volume_sensors" in sensor_config.keys():
            tank_volume_sensors = sensor_config["tank_volume_sensors"]
        else:
            tank_volume_sensors = []

        if "valve_state_sensors" in sensor_config.keys():
            valve_state_sensors = sensor_config["valve_state_sensors"]
        else:
            valve_state_sensors = []

        if "pump_state_sensors" in sensor_config.keys():
            pump_state_sensors = sensor_config["pump_state_sensors"]
        else:
            pump_state_sensors = []

        if "bulk_species_node_sensors" in sensor_config.keys():
            bulk_species_node_sensors = sensor_config["bulk_species_node_sensors"]
        else:
            bulk_species_node_sensors = {}

        if "bulk_species_link_sensors" in sensor_config.keys():
            bulk_species_link_sensors = sensor_config["bulk_species_link_sensors"]
        else:
            bulk_species_link_sensors = {}

        if "surface_species_sensors" in sensor_config.keys():
            surface_species_sensors = sensor_config["surface_species_sensors"]
        else:
            surface_species_sensors = {}

        # Uncertainties
        if "uncertainties" in data.keys():
            def parse_uncertantiy(uncertainty_desc: dict) -> Uncertainty:
                uncertainty_type = uncertainty_desc["type"]
                del uncertainty_desc["type"]

                if uncertainty_type == "absolute_gaussian":
                    return AbsoluteGaussianUncertainty(**uncertainty_desc)
                elif uncertainty_type == "relative_gaussian":
                    return RelativeGaussianUncertainty(**uncertainty_desc)
                elif uncertainty_type == "absolute_uniform":
                    return AbsoluteUniformUncertainty(**uncertainty_desc)
                elif uncertainty_type == "relative_uniform":
                    return RelativeUniformUncertainty(**uncertainty_desc)
                else:
                    raise ValueError(f"Unknown uncertainty '{uncertainty_type}'")

            uncertanties = data["uncertainties"]
            if "pipe_length_uncertainty" in uncertanties.keys():
                pipe_length_uncertainty = parse_uncertantiy(uncertanties["pipe_length_uncertainty"])
            else:
                pipe_length_uncertainty = None
            if "pipe_roughness_uncertainty" in uncertanties.keys():
                pipe_roughness_uncertainty = parse_uncertantiy(
                    uncertanties["pipe_roughness_uncertainty"])
            else:
                pipe_roughness_uncertainty = None
            if "pipe_diameter_uncertainty" in uncertanties.keys():
                pipe_diameter_uncertainty = parse_uncertantiy(
                    uncertanties["pipe_diameter_uncertainty"])
            else:
                pipe_diameter_uncertainty = None
            if "demand_base_uncertainty" in uncertanties.keys():
                demand_base_uncertainty = parse_uncertantiy(uncertanties["demand_base_uncertainty"])
            else:
                demand_base_uncertainty = None
            if "demand_pattern_uncertainty" in uncertanties.keys():
                demand_pattern_uncertainty = parse_uncertantiy(
                    uncertanties["demand_pattern_uncertainty"])
            else:
                demand_pattern_uncertainty = None
            if "elevation_uncertainty" in uncertanties.keys():
                elevation_uncertainty = parse_uncertantiy(uncertanties["elevation_uncertainty"])
            else:
                elevation_uncertainty = None
            if "constants_uncertainty" in uncertanties.keys():
                constants_uncertainty = parse_uncertantiy(uncertanties["constants_uncertainty"])
            else:
                constants_uncertainty = None
            if "parameters_uncertainty" in uncertanties.keys():
                parameters_uncertainty = parse_uncertantiy(uncertanties["parameters_uncertainty"])
            else:
                parameters_uncertainty = None

            model_uncertainty = ModelUncertainty(pipe_length_uncertainty,
                                                 pipe_roughness_uncertainty,
                                                 pipe_diameter_uncertainty, demand_base_uncertainty,
                                                 demand_pattern_uncertainty, elevation_uncertainty,
                                                 constants_uncertainty, parameters_uncertainty)

            if "sensor_noise" in uncertanties.keys():
                sensor_noise = SensorNoise(parse_uncertantiy(uncertanties["sensor_noise"]))
            else:
                sensor_noise = None

        # Events
        leakages = []
        if "leakages" in data.keys():
            def parse_leak(leak_desc):
                leak_type = leak_desc["type"]
                del leak_desc["type"]

                if leak_type == "abrupt":
                    return AbruptLeakage(**leak_desc)
                elif leak_type == "incipient":
                    return IncipientLeakage(**leak_desc)
                else:
                    raise ValueError(f"Unknown leakage type '{leak_type}'")

            leakages = [parse_leak(leak) for leak in data["leakages"]]

        sensor_faults = []
        if "sensor_faults" in data.keys():
            def parse_sensor_fault(sensor_fault_desc):
                fault_type = sensor_fault_desc["type"]
                del sensor_fault_desc["type"]

                if fault_type == "constant":
                    return SensorFaultConstant(**sensor_fault_desc)
                elif fault_type == "drift":
                    return SensorFaultDrift(**sensor_fault_desc)
                elif fault_type == "gaussian":
                    return SensorFaultGaussian(**sensor_fault_desc)
                elif fault_type == "percentage":
                    return SensorFaultPercentage(**sensor_fault_desc)
                elif fault_type == "stuckatzero":
                    return SensorFaultStuckZero(**sensor_fault_desc)
                else:
                    raise ValueError(f"Unknown sensor fault '{fault_type}'")

            sensor_faults = [parse_sensor_fault(sensor_fault)
                             for sensor_fault in data["sensor_faults"]]

        #  Load .inp file to get a list of all nodes and links/pipes
        sensor_config = None
        from .scenario_simulator import ScenarioSimulator
        with ScenarioSimulator(f_inp_in) as scenario:
            sensor_config = SensorConfig.create_empty_sensor_config(scenario.sensor_config)
            sensor_config.pressure_sensors = pressure_sensors
            sensor_config.flow_sensors = flow_sensors
            sensor_config.demand_sensors = demand_sensors
            sensor_config.quality_node_sensors = node_quality_sensors
            sensor_config.quality_link_sensors = link_quality_sensors
            sensor_config.valve_state_sensors = valve_state_sensors
            sensor_config.pump_state_sensors = pump_state_sensors
            sensor_config.tank_volume_sensors = tank_volume_sensors
            sensor_config.bulk_species_node_sensors = bulk_species_node_sensors
            sensor_config.bulk_species_link_sensors = bulk_species_link_sensors
            sensor_config.surface_species_sensors = surface_species_sensors

        # Create final scenario configuration
        return ScenarioConfig(f_inp_in=f_inp_in, f_msx_in=f_msx_in, general_params=general_params,
                              sensor_config=sensor_config, controls=[], sensor_noise=sensor_noise,
                              model_uncertainty=model_uncertainty, system_events=leakages,
                              sensor_reading_events=sensor_faults)
