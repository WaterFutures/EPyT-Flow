"""
Module provides a class for scenario simulations.
"""
import os
from typing import Generator
from copy import deepcopy
import warnings
import random
import math
import numpy as np
from epyt import epanet
from epyt.epanet import ToolkitConstants
from tqdm import tqdm

from .scenario_config import ScenarioConfig
from .sensor_config import SensorConfig, SENSOR_TYPE_LINK_FLOW, SENSOR_TYPE_LINK_QUALITY, \
    SENSOR_TYPE_NODE_DEMAND, SENSOR_TYPE_NODE_PRESSURE, SENSOR_TYPE_NODE_QUALITY, \
    SENSOR_TYPE_PUMP_STATE, SENSOR_TYPE_TANK_VOLUME, SENSOR_TYPE_VALVE_STATE
from ..uncertainty import ModelUncertainty, SensorNoise
from .events import SystemEvent, Leakage, ActuatorEvent, SensorFault, SensorReadingAttack, \
    SensorReadingEvent
from .scada import ScadaData, AdvancedControlModule
from ..topology import NetworkTopology


class ScenarioSimulator():
    """
    Class for running a simulation of a water distribution network scenario.

    Parameters
    ----------
    f_inp_in : `str`
        Path to the .inp file.

        If this is None, then 'scenario_config' must be set with a valid configuration.
    f_msx_in : `str`, option
        Path to the .msx file -- optional, only necessary if EPANET-MSX is used.

        The default is None.
    scenario_config : :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Configuration of the scenario -- i.e. a description of the scenario to be simulated.

        If this is None, then 'f_inp_in' must be set with a valid path to the .inp file
        that is to be simulated.

    Attributes
    ----------
    epanet_api : `epyt.epanet`
        API to EPANET and EPANET-MSX.
    """

    def __init__(self, f_inp_in: str = None, f_msx_in: str = None,
                 scenario_config: ScenarioConfig = None):
        if f_msx_in is not None and f_inp_in is None:
            raise ValueError("'f_inp_in' must be set if 'f_msx_in' is set.")
        if f_inp_in is None and scenario_config is None:
            raise ValueError("Either 'f_inp_in' or 'scenario_config' must be set.")
        if f_inp_in is not None:
            if not isinstance(f_inp_in, str):
                raise TypeError("'f_inp_in' must be an instance of 'str' but not of " +
                                f"'{type(f_inp_in)}'")
        if f_msx_in is not None:
            if not isinstance(f_msx_in, str):
                raise TypeError("'f_msx_in' must be an instance of 'str' but not of " +
                                f"'{type(f_msx_in)}'")
        if scenario_config is not None:
            if not isinstance(scenario_config, ScenarioConfig):
                raise TypeError("'scenario_config' must be an instance of " +
                                "'epyt_flow.simulation.ScenarioConfig' but not of " +
                                f"'{type(scenario_config)}'")

        self.__f_inp_in = f_inp_in if scenario_config is None else scenario_config.f_inp_in
        self.__f_msx_in = f_msx_in if scenario_config is None else scenario_config.f_msx_in
        self.__model_uncertainty = ModelUncertainty()
        self.__sensor_noise = None
        self.__sensor_config = None
        self.__controls = []
        self.__system_events = []
        self.__sensor_reading_events = []

        self.epanet_api = epanet(self.__f_inp_in, msx=self.__f_msx_in is not None)
        if self.__f_msx_in is not None:
            self.epanet_api.loadMSXfile(self.__f_msx_in)

        self.__sensor_config = SensorConfig(nodes=self.epanet_api.getNodeNameID(),
                                            links=self.epanet_api.getLinkNameID(),
                                            valves=self.epanet_api.getLinkValveNameID(),
                                            pumps=self.epanet_api.getLinkPumpNameID(),
                                            tanks=self.epanet_api.getNodeTankNameID(),
                                            bulk_species=[],
                                            surface_species=[])
        if scenario_config is not None:
            if scenario_config.general_params is not None:
                self.set_general_parameters(**scenario_config.general_params)

            self.__model_uncertainty = scenario_config.model_uncertainty
            self.__sensor_noise = scenario_config.sensor_noise
            self.__sensor_config = scenario_config.sensor_config

            for control in scenario_config.controls:
                self.add_control(control)
            for event in scenario_config.system_events:
                self.add_system_event(event)
            for event in scenario_config.sensor_reading_events:
                self.add_sensor_reading_event(event)

    @property
    def f_inp_in(self) -> str:
        """
        Gets the path to the .inp file.

        Returns
        -------
        `str`
            Path to the .inp file.
        """
        self.__adapt_to_network_changes()

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
        self.__adapt_to_network_changes()

        return self.__f_msx_in

    @property
    def model_uncertainty(self) -> ModelUncertainty:
        """
        Gets the model uncertainty specification.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.model_uncertainty.ModelUncertainty`
            Model uncertainty.
        """
        self.__adapt_to_network_changes()

        return deepcopy(self.__model_uncertainty)

    @model_uncertainty.setter
    def model_uncertainty(self, model_uncertainty: ModelUncertainty) -> None:
        self.__adapt_to_network_changes()

        self.set_model_uncertainty(model_uncertainty)

    @property
    def sensor_noise(self) -> SensorNoise:
        """
        Gets the sensor noise/uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.sensor_noise.SensorNoise`
            Sensor noise.
        """
        self.__adapt_to_network_changes()

        return deepcopy(self.__sensor_noise)

    @sensor_noise.setter
    def sensor_noise(self, sensor_noise: SensorNoise) -> None:
        self.__adapt_to_network_changes()

        self.set_sensor_noise(sensor_noise)

    @property
    def sensor_config(self) -> SensorConfig:
        """
        Gets the sensor configuration.

        Returns
        -------
        :class:`~epyt_flow.simulation.sensor_config.SensorConfig`
            Sensor configuration.
        """
        self.__adapt_to_network_changes()

        return deepcopy(self.__sensor_config)

    @sensor_config.setter
    def sensor_config(self, sensor_config: SensorConfig) -> None:
        if not isinstance(sensor_config, SensorConfig):
            raise TypeError("'sensor_config' must be an instance of " +
                            "'epyt_flow.simulation.SensorConfig' but not of " +
                            f"'{type(sensor_config)}'")

        sensor_config.validate(self.epanet_api)

        self.__sensor_config = sensor_config

    @property
    def controls(self) -> list[AdvancedControlModule]:
        """
        Gets all control modules.

        Returns
        -------
        `list[`:class:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule` `]`
            All control modules.
        """
        self.__adapt_to_network_changes()

        return deepcopy(self.__controls)

    @property
    def leakages(self) -> list[Leakage]:
        """
        Gets all leakages.

        Returns
        -------
        `list[`:class:`~epyt_flow.simulation.events.leakages.Leakage` `]`
            All leakages.
        """
        self.__adapt_to_network_changes()

        return deepcopy(list(filter(lambda e: isinstance(e, Leakage), self.__system_events)))

    def actuator_events(self) -> list[ActuatorEvent]:
        """
        Gets all actuator events.

        Returns
        -------
        `list[`:class:`~epyt_flow.simulation.events.actuator_event.ActuatorEvent` `]`
            All actuator events.
        """
        self.__adapt_to_network_changes()

        return deepcopy(list(filter(lambda e: isinstance(e, ActuatorEvent), self.__system_events)))

    @property
    def system_events(self) -> list[SystemEvent]:
        """
        Gets all system events (e.g. leakages, etc.).

        Returns
        -------
        `list[`:class:`~epyt_flow.simulation.events.system_event.SystemEvent` `]`
            All system events.
        """
        self.__adapt_to_network_changes()

        return deepcopy(self.__system_events)

    @property
    def sensor_faults(self) -> list[SensorFault]:
        """
        Gets all sensor faults.

        Returns
        -------
        `list[`:class:`~epyt_flow.simulation.events.sensor_faults.SensorFault` `]`
            All sensor faults.
        """
        self.__adapt_to_network_changes()

        return deepcopy(list(filter(lambda e: isinstance(e, SensorFault),
                                    self.__sensor_reading_events)))

    @property
    def sensor_reading_events(self) -> list[SensorReadingEvent]:
        """
        Gets all sensor reading events (e.g. sensor faults, etc.).

        Returns
        -------
        `list[`:class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent` `]`
            All sensor reading events.
        """
        self.__adapt_to_network_changes()

        return deepcopy(self.__sensor_reading_events)

    def __adapt_to_network_changes(self):
        nodes = self.epanet_api.getNodeNameID()
        links = self.epanet_api.getLinkNameID()
        valves = self.epanet_api.getLinkValveNameID()
        pumps = self.epanet_api.getLinkPumpNameID()
        tanks = self.epanet_api.getNodeTankNameID()
        bulk_species = []
        surface_species = []

        node_id_to_idx = {node_id: self.epanet_api.getNodeIndex(node_id) - 1 for node_id in nodes}
        link_id_to_idx = {link_id: self.epanet_api.getLinkIndex(link_id) - 1 for link_id in links}
        valve_id_to_idx = None  # {valve_id: self.epanet_api.getLinkValveIndex(valve_id) for valve_id in valves}
        pump_id_to_idx = None # {pump_id: self.epanet_api.getLinkPumpIndex(pump_id) - 1 for pump_id in pumps}
        tank_id_to_idx = None #{tank_id: self.epanet_api.getNodeTankIndex(tank_id) - 1 for tank_id in tanks}
        bulkspecies_id_to_idx = None
        surfacespecies_id_to_idx = None

        if nodes != self.__sensor_config.nodes or links != self.__sensor_config.links or \
            valves != self.__sensor_config.valves or pumps != self.__sensor_config.pumps or \
            tanks != self.__sensor_config.tanks or \
            bulk_species != self.__sensor_config.bulk_species or \
                surface_species != self.__sensor_config.surface_species:
            # Adapt sensor configuration if anything in the network topology changed
            new_sensor_config = SensorConfig(nodes=nodes, links=links, valves=valves, pumps=pumps,
                                             tanks=tanks, bulk_species=bulk_species,
                                             surface_species=surface_species,
                                             node_id_to_idx=node_id_to_idx,
                                             link_id_to_idx=link_id_to_idx,
                                             valve_id_to_idx=valve_id_to_idx,
                                             pump_id_to_idx=pump_id_to_idx,
                                             tank_id_to_idx=tank_id_to_idx,
                                             bulkspecies_id_to_idx=bulkspecies_id_to_idx,
                                             surfacespecies_id_to_idx=surfacespecies_id_to_idx)
            new_sensor_config.pressure_sensors = self.__sensor_config.pressure_sensors
            new_sensor_config.flow_sensors = self.__sensor_config.flow_sensors
            new_sensor_config.demand_sensors = self.__sensor_config.demand_sensors
            new_sensor_config.quality_node_sensors = self.__sensor_config.quality_node_sensors
            new_sensor_config.quality_link_sensors = self.__sensor_config.quality_link_sensors
            new_sensor_config.pump_state_sensors = self.__sensor_config.pump_state_sensors
            new_sensor_config.valve_state_sensors = self.__sensor_config.valve_state_sensors
            new_sensor_config.tank_volume_sensors = self.__sensor_config.tank_volume_sensors
            new_sensor_config.bulk_species_sensors = self.__sensor_config.bulk_species_sensors
            new_sensor_config.surface_species_sensors = self.__sensor_config.surface_species_sensors

            self.__sensor_config = new_sensor_config

    def __find_temporary_file(self) -> str:
        # Sort files by time to find the temporary file created by EPANET
        files = list(filter(lambda f: os.path.isfile(f) and "." not in f, os.listdir()))
        files.sort(key=os.path.getmtime)

        if len(files) == 0:
            return None
        else:
            return files[::-1][0]

    def close(self):
        """
        Closes & unloads all resources and libraries.

        Call this function after the simulation is done -- do not call this function before!
        """
        if self.__f_msx_in is not None:
            self.epanet_api.unloadMSX()

        self.epanet_api.unload()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def get_scenario_config(self) -> ScenarioConfig:
        """
        Gets the configuration of this scenario -- i.e. all information & elements
        that completely describe this scenario.

        Returns
        -------
        :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
            Complete scenario specification.
        """
        self.__adapt_to_network_changes()

        qual_info = self.epanet_api.getQualityInfo()
        demand_info = self.epanet_api.getDemandModel()
        general_params = {"hydraulic_time_step": self.epanet_api.getTimeHydraulicStep(),
                          "quality_time_step": self.epanet_api.getTimeQualityStep(),
                          "simulation_duration": self.epanet_api.getTimeSimulationDuration(),
                          "flow_units": self.epanet_api.api.ENgetflowunits(),
                          "quality_model": {"code": qual_info.QualityCode,
                                            "type": qual_info.QualityType,
                                            "chemical_name": qual_info.QualityChemName,
                                            "units": qual_info.QualityChemUnits,
                                            "trace_node_id": qual_info.TraceNode},
                          "demand_model": {"type": demand_info.DemandModelCode,
                                           "pressure_min": demand_info.DemandModelPmin,
                                           "pressure_required": demand_info.DemandModelPreq,
                                           "pressure_exponent": demand_info.DemandModelPexp}}

        return ScenarioConfig(self.__f_inp_in, self.__f_msx_in, general_params, self.sensor_config,
                              self.controls, self.sensor_noise, self.model_uncertainty,
                              self.system_events, self.sensor_reading_events)

    def estimate_memory_consumption(self) -> float:
        """
        Estimates the memory consumption of the simulation -- i.e. the amount of memory that is
        needed on the hard disk as well as in RAM.

        Returns
        -------
        `float`
            Estimated memory consumption in MB.
        """
        self.__adapt_to_network_changes()

        n_time_steps = int(self.epanet_api.getTimeSimulationDuration() /
                           self.epanet_api.getTimeReportingStep())
        n_quantities = self.epanet_api.getNodeCount() * 3 + self.epanet_api.getNodeTankCount() + \
            self.epanet_api.getLinkValveCount() + self.epanet_api.getLinkPumpCount() + \
            self.epanet_api.getLinkCount() * 2
        n_bytes_per_quantity = 64

        return n_time_steps * n_quantities * n_bytes_per_quantity * .000001

    def get_topology(self) -> NetworkTopology:
        """
        Gets the topology (incl. information such as eleveations, pipe diameters, etc.) of this WDN.

        Returns
        -------
        `epyt_flow.topology.NetworkTopology`
            Topology of this WDN as a graph.
        """
        self.__adapt_to_network_changes()

        # Collect information about the topology of the water distribution network
        nodes_id = self.epanet_api.getNodeNameID()
        nodes_elevation = self.epanet_api.getNodeElevations()
        nodes_type = [self.epanet_api.TYPENODE[i] for i in self.epanet_api.getNodeTypeIndex()]

        links_id = self.epanet_api.getLinkNameID()
        links_data = self.epanet_api.getNodesConnectingLinksID()
        links_diameter = self.epanet_api.getLinkDiameter()
        links_length = self.epanet_api.getLinkLength()

        # Build graph describing the topology
        nodes = []
        for node, node_elevation, node_type in zip(nodes_id, nodes_elevation, nodes_type):
            nodes.append((node, {"elevation": node_elevation, "type": node_type}))

        links = []
        for link_id, link, diameter, length in zip(links_id, links_data, links_diameter,
                                                   links_length):
            links.append((link_id, link, {"diameter": diameter, "length": length}))

        return NetworkTopology(f_inp=self.f_inp_in, nodes=nodes, links=links)

    def randomize_demands(self) -> None:
        """
        Randomizes all demand patterns.
        """
        self.__adapt_to_network_changes()

        # Get all demand patterns
        demand_patterns_idx = self.epanet_api.getNodeDemandPatternIndex()
        demand_patterns_id = np.unique([idx for _, idx in demand_patterns_idx.items()])

        # Process each pattern separately
        for pattern_id in demand_patterns_id:
            if pattern_id == 0:
                continue

            pattern_length = self.epanet_api.getPatternLengths(pattern_id)
            pattern = []
            for t in range(pattern_length):  # Get pattern
                pattern.append(self.epanet_api.getPatternValue(pattern_id, t + 1))

            random.shuffle(pattern)  # Shuffle pattern

            for t in range(pattern_length):  # Set shuffled/randomized pattern
                self.epanet_api.setPatternValue(pattern_id, t + 1, pattern[t])

    def set_node_demand_pattern(self, node_id: str, base_demand: float, demand_pattern_id: str,
                                demand_pattern: np.ndarray) -> None:
        """
        Sets the demand pattern (incl. base demand) at a given node.

        Parameters
        ----------
        node_id : `str`
            ID of the node for which the demand pattern is set.
        base_demand : `float`
            Base demand.
        demand_pattern_id : `str`
            ID of the new demand pattern.
        demand_pattern : `numpy.ndarray`
            Demand pattern over time. Final demand over time = base_demand * demand_pattern
        """
        self.__adapt_to_network_changes()

        if node_id not in self.__sensor_config.nodes:
            raise ValueError(f"Unknown node '{node_id}'")
        if not isinstance(base_demand, float):
            raise TypeError("'base_demand' must be an instance of 'float' " +
                            f"but not if '{type(base_demand)}'")
        if not isinstance(demand_pattern_id, str):
            raise TypeError("'demand_pattern_id' must be an instance of 'str' " +
                            f"but not of '{type(demand_pattern_id)}'")
        if not isinstance(demand_pattern, np.ndarray):
            raise TypeError("'demand_pattern' must be an instance of 'numpy.ndarray' " +
                            f"but not of '{type(demand_pattern)}'")
        if len(demand_pattern.shape) > 1:
            raise ValueError(f"Inconsistent demand pattern shape '{demand_pattern.shape}' " +
                             "detected. Expected a one dimensional array!")

        node_idx = self.epanet_api.getNodeIndex(node_id)
        self.epanet_api.addPattern(demand_pattern_id, demand_pattern)
        self.epanet_api.setNodeJunctionData(node_idx, self.epanet_api.getNodeElevations(node_idx),
                                            base_demand, demand_pattern_id)

    def add_control(self, control: AdvancedControlModule) -> None:
        """
        Adds a control module to the scenario simulation.

        Parameters
        ----------
        control : :class:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule`
            Control module.
        """
        self.__adapt_to_network_changes()

        if not isinstance(control, AdvancedControlModule):
            raise TypeError("'control' must be an instance of " +
                            "'epyt_flow.simulation.scada.AdvancedControlModule' not of " +
                            f"'{type(control)}'")

        self.__controls.append(control)

    def add_leakage(self, leakage_event: Leakage) -> None:
        """
        Adds a leakage to the scenario simulation.

        Parameters
        ----------
        event : :class:`~epyt_flow.simulation.events.leakages.Leakage`
            Leakage.
        """
        self.__adapt_to_network_changes()

        if not isinstance(leakage_event, Leakage):
            raise TypeError("'leakage_event' must be an instance of " +
                            "'epyt_flow.simulation.events.Leakage' not of " +
                            f"'{type(leakage_event)}'")

        self.add_system_event(leakage_event)

    def add_actuator_event(self, event: ActuatorEvent) -> None:
        """
        Adds an actuator event to the scenario simulation.

        Parameters
        ----------
        event : :class:`~epyt_flow.simulation.events.actuator_events.ActuatorEvent`
            Actuator event.
        """
        self.__adapt_to_network_changes()

        if not isinstance(event, ActuatorEvent):
            raise TypeError("'event' must be an instance of " +
                            f"'epyt_flow.simulation.events.ActuatorEvent' not of '{type(event)}'")

        self.add_system_event(event)

    def add_system_event(self, event: SystemEvent) -> None:
        """
        Adds a system event to the scenario simulation -- i.e. an event directly
        affecting the EPANET simulation.

        Parameters
        ----------
        event : :class:`~epyt_flow.simulation.events.system_event.SystemEvent`
            System event.
        """
        self.__adapt_to_network_changes()

        if not isinstance(event, SystemEvent):
            raise TypeError("'event' must be an instance of " +
                            f"'epyt_flow.simulation.events.SystemEvent' not of '{type(event)}'")

        event.init(self.epanet_api)

        self.__system_events.append(event)

    def add_sensor_fault(self, sensor_fault_event: SensorFault) -> None:
        """
        Adds a sensor fault to the scenario simulation.

        Parameters
        ----------
        sensor_fault_event : :class:`~epyt_flow.simulation.events.sensor_faults.SensorFault`
            Sensor fault specifications.
        """
        self.__adapt_to_network_changes()

        sensor_fault_event.validate(self.__sensor_config)

        if not isinstance(sensor_fault_event, SensorFault):
            raise TypeError("'sensor_fault_event' must be an instance of " +
                            "'epyt_flow.simulation.events.SensorFault' not of " +
                            f"'{type(sensor_fault_event)}'")

        self.__sensor_reading_events.append(sensor_fault_event)

    def add_sensor_reading_attack(self, sensor_reading_attack: SensorReadingAttack) -> None:
        """
        Adds a sensor reading attack to the scenario simulation.

        Parameters
        ----------
        sensor_reading_attack : :class:`~epyt_flow.simulation.events.sensor_reading_attack.SensorReadingAttack`
            Sensor fault specifications.
        """
        self.__adapt_to_network_changes()

        sensor_reading_attack.validate(self.__sensor_config)

        if not isinstance(sensor_reading_attack, SensorReadingAttack):
            raise TypeError("'sensor_reading_attack' must be an instance of " +
                            "'epyt_flow.simulation.events.SensorReadingAttack' not of " +
                            f"'{type(sensor_reading_attack)}'")

        self.__sensor_reading_events.append(sensor_reading_attack)

    def add_sensor_reading_event(self, event: SensorReadingEvent) -> None:
        """
        Adds a sensor reading event to the scenario simulation.

        Parameters
        ----------
        event : :class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent`
            Sensor reading event.
        """
        self.__adapt_to_network_changes()

        event.validate(self.__sensor_config)

        if not isinstance(event, SensorReadingEvent):
            raise TypeError("'event' must be an instance of " +
                            "'epyt_flow.simulation.events.SensorReadingEvent' not of " +
                            f"'{type(event)}'")

        self.__sensor_reading_events.append(event)

    def set_sensors(self, sensor_type: int, sensor_locations: list[str]) -> None:
        """
        Specifies all sensors of a given type (e.g. pressure sensor, flow sensor, etc.)

        Parameters
        ----------
        sensor_type : `int`
            Sensor type. Must be one of the following:
                - SENSOR_TYPE_NODE_PRESSURE   = 1
                - SENSOR_TYPE_NODE_QUALITY    = 2
                - SENSOR_TYPE_NODE_DEMAND     = 3
                - SENSOR_TYPE_LINK_FLOW       = 4
                - SENSOR_TYPE_LINK_QUALITY    = 5
                - SENSOR_TYPE_VALVE_STATE     = 6
                - SENSOR_TYPE_PUMP_STATE      = 7
                - SENSOR_TYPE_TANK_VOLUME     = 8
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.__adapt_to_network_changes()

        if sensor_type == SENSOR_TYPE_NODE_PRESSURE:
            self.__sensor_config.pressure_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_LINK_FLOW:
            self.__sensor_config.flow_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_NODE_DEMAND:
            self.__sensor_config.demand_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_NODE_QUALITY:
            self.__sensor_config.quality_node_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_LINK_QUALITY:
            self.__sensor_config.quality_link_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_VALVE_STATE:
            self.__sensor_config.valve_state_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_PUMP_STATE:
            self.__sensor_config.pump_state_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_TANK_VOLUME:
            self.__sensor_config.tank_volume_sensors = sensor_locations
        else:
            raise ValueError(f"Unknown sensor type '{sensor_type}'")

        self.__sensor_config.validate(self.epanet_api)

    def set_pressure_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the pressure sensors -- i.e. measuring pressure at some nodes in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_NODE_PRESSURE, sensor_locations)

    def set_flow_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the flow sensors -- i.e. measuring flows at some links/pipes in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_LINK_FLOW, sensor_locations)

    def set_demand_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the demand sensors -- i.e. measuring demands at some nodes in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_NODE_DEMAND, sensor_locations)

    def set_node_quality_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the node quality sensors -- i.e. measuring the water quality
        (e.g. age, chlorine concentration, etc.) at some nodes in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_NODE_QUALITY, sensor_locations)

    def set_link_quality_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the link quality sensors -- i.e. measuring the water quality
        (e.g. age, chlorine concentration, etc.) at some links/pipes in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_LINK_QUALITY, sensor_locations)

    def set_valve_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the valve state sensors -- i.e. retrieving the state of some valves in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_VALVE_STATE, sensor_locations)

    def set_pump_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the pump state sensors -- i.e. retrieving the state of some pumps in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_PUMP_STATE, sensor_locations)

    def set_tank_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the tank volume sensors -- i.e. measuring water volumes in some tanks in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_TANK_VOLUME, sensor_locations)

    def __prepare_simulation(self) -> None:
        self.__adapt_to_network_changes()

        if self.__model_uncertainty is not None:
            self.__model_uncertainty.apply(self.epanet_api)

        for event in self.__system_events:
            event.reset()

        if self.__controls is not None:
            for c in self.__controls:
                c.init(self.epanet_api)

    def run_simulation(self, hyd_export: str = None, verbose: bool = False) -> ScadaData:
        """
        Runs the simulation of this scenario.

        Parameters
        ----------
        hyd_export : `str`, optional
            Path to an EPANET .hyd file for storing the simulated hydraulics -- these hydraulics
            can be used later for an advanced quality analysis using EPANET-MSX.

            If None, the simulated hydraulics will NOT be exported to a EPANET .hyd file.

            The default is None.
        verbose : `bool`, optional
            If True, method will be verbose (e.g. showing a progress bar).

            The default is False.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Simulation results as SCADA data (i.e. sensor readings).
        """
        self.__adapt_to_network_changes()

        # Step by step simulation is required in some cases
        if len(self.__controls) != 0 or len(self.__system_events) != 0 or hyd_export is not None \
                or len(self.sensor_config.tank_volume_sensors) != 0:
            result = None

            for scada_data in self.run_simulation_as_generator(hyd_export=hyd_export,
                                                               verbose=verbose):
                if result is None:
                    result = scada_data
                else:
                    result.concatenate(scada_data)

            return result
        else:
            self.__prepare_simulation()
            res = self.epanet_api.getComputedTimeSeries()

            if len(self.epanet_api.getLinkPumpIndex()) != 0:
                pumps_state = res.Status[:, self.epanet_api.getLinkPumpIndex() - 1]
            else:
                pumps_state = None

            if len(self.epanet_api.getLinkValveIndex()) != 0:
                valves_state = res.Status[:, self.epanet_api.getLinkValveIndex() - 1]
            else:
                # TODO: Differs from the step-by-step simulation!
                valves_state = None

            tanks_volume = None  # TODO: No tanks volume data available?
            pump_energy_usage_data = None  # TODO: No Energy usage data available?
            pump_efficiency_data = None   # TODO: No pump efficiency data available?

            return ScadaData(sensor_config=self.sensor_config, pressure_data_raw=res.Pressure[:, :],
                             flow_data_raw=res.Flow[:, :],
                             demand_data_raw=res.Demand[:, :],
                             node_quality_data_raw=res.NodeQuality[:, :],
                             link_quality_data_raw=res.LinkQuality[:, :],
                             pumps_state_data_raw=pumps_state, valves_state_data_raw=valves_state,
                             tanks_volume_data_raw=tanks_volume, sensor_readings_time=res.Time[:],
                             pump_energy_usage_data=pump_energy_usage_data,
                             pump_efficiency_data=pump_efficiency_data,
                             sensor_reading_events=self.__sensor_reading_events,
                             sensor_noise=self.__sensor_noise)

    def run_simulation_as_generator(self, hyd_export: str = None, verbose: bool = False,
                                    support_abort: bool = False) -> Generator[ScadaData, bool, None]:
        """
        Runs the simulation of this scenario and provides the results as a generator.

        Parameters
        ----------
        hyd_export : `str`, optional
            Path to an EPANET .hyd file for storing the simulated hydraulics -- these hydraulics
            can be used later for an advanced quality analysis using EPANET-MSX.

            If None, the simulated hydraulics will NOT be exported to a EPANET .hyd file.

            The default is None.
        verbose : `bool`, optional
            If True, method will be verbose (e.g. showing a progress bar).

            The default is False.
        support_abort : `bool`, optional
            If True, the simulation can be aborted after every time step -- i.e. the generator
            takes a boolean as an input (send) to indicate whether the simulation
            is to be aborted or not.

            The default is False.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Generator with the current simulation results/states as SCADA data
            (i.e. sensor readings).
        """
        self.__adapt_to_network_changes()

        self.__prepare_simulation()

        self.epanet_api.openHydraulicAnalysis()
        self.epanet_api.openQualityAnalysis()
        self.epanet_api.initializeHydraulicAnalysis(ToolkitConstants.EN_SAVE)
        self.epanet_api.initializeQualityAnalysis(ToolkitConstants.EN_SAVE)

        tmp_file = self.__find_temporary_file()

        requested_time_step = self.epanet_api.getTimeHydraulicStep()
        reporting_time_start = self.epanet_api.getTimeReportingStart()
        reporting_time_step = self.epanet_api.getTimeReportingStep()

        if verbose is True:
            n_iterations = math.ceil(self.epanet_api.getTimeSimulationDuration() /
                                     requested_time_step)
            progress_bar = iter(tqdm(range(n_iterations + 1), desc="Time steps"))

        try:
            # Run simulation step by step
            total_time = 0
            tstep = 1
            first_itr = True
            while tstep > 0:
                if support_abort is True:  # Can the simulation be aborted? If so, handle it.
                    abort = yield
                    if abort is not False:
                        break

                if first_itr is True:  # Fix current time in the first iteration
                    tstep = 0
                    first_itr = False

                if verbose is True:
                    if (total_time + tstep) % requested_time_step == 0:
                        next(progress_bar)

                # Apply system events in a regular time interval only!
                if (total_time + tstep) % requested_time_step == 0:
                    for event in self.__system_events:
                        event.step(total_time + tstep)

                # Compute current time step
                t = self.epanet_api.runHydraulicAnalysis()
                self.epanet_api.runQualityAnalysis()
                total_time = t

                # Fetch data
                pressure_data = None
                flow_data = None
                demand_data = None
                quality_node_data = None
                quality_link_data = None
                pumps_state_data = None
                valves_state_data = None

                pressure_data = self.epanet_api.getNodePressure().reshape(1, -1)
                flow_data = self.epanet_api.getLinkFlows().reshape(1, -1)
                demand_data = self.epanet_api.getNodeActualDemand().reshape(1,
                                                                            -1)  # TODO: Does not go back after emitter coefficient is changed back to zero
                quality_node_data = self.epanet_api.getNodeActualQuality().reshape(1, -1)
                quality_link_data = self.epanet_api.getLinkActualQuality().reshape(1, -1)
                pumps_state_data = self.epanet_api.getLinkPumpState().reshape(1, -1)
                tanks_volume_data = self.epanet_api.getNodeTankVolume().reshape(1, -1)

                pump_idx = self.epanet_api.getLinkPumpIndex()
                pump_energy_usage_data = self.epanet_api.getLinkEnergy(pump_idx).reshape(1, -1)
                pump_efficiency_data = self.epanet_api.getLinkPumpEfficiency().reshape(1, -1)

                link_valve_idx = self.epanet_api.getLinkValveIndex()
                valves_state_data = self.epanet_api.getLinkStatus(link_valve_idx).reshape(1, -1)

                scada_data = ScadaData(sensor_config=self.__sensor_config,
                                       pressure_data_raw=pressure_data,
                                       flow_data_raw=flow_data,
                                       demand_data_raw=demand_data,
                                       node_quality_data_raw=quality_node_data,
                                       link_quality_data_raw=quality_link_data,
                                       pumps_state_data_raw=pumps_state_data,
                                       valves_state_data_raw=valves_state_data,
                                       tanks_volume_data_raw=tanks_volume_data,
                                       pump_energy_usage_data=pump_energy_usage_data,
                                       pump_efficiency_data=pump_efficiency_data,
                                       sensor_readings_time=np.array([total_time]),
                                       sensor_reading_events=self.__sensor_reading_events,
                                       sensor_noise=self.__sensor_noise)

                # Yield results in a regular time interval only!
                if total_time % reporting_time_step == 0 and total_time >= reporting_time_start:
                    yield scada_data

                # Apply control modules
                for control in self.__controls:
                    control.step(scada_data)

                # Next
                tstep = self.epanet_api.nextHydraulicAnalysisStep()
                self.epanet_api.nextQualityAnalysisStep()

            self.epanet_api.closeQualityAnalysis()
            self.epanet_api.closeHydraulicAnalysis()

            if hyd_export is not None:
                self.epanet_api.saveHydraulicFile(hyd_export)
        except Exception as ex:
            if tmp_file is not None:
                os.remove(tmp_file)  # Close temporary files before raising any exceptions
            raise ex

        if tmp_file is not None:
            os.remove(tmp_file)  # Close temporary files

    def set_model_uncertainty(self, model_uncertainty: ModelUncertainty) -> None:
        """
        Specifies the model uncertainties.

        Parameters
        ----------
        model_uncertainty : :class:`~epyt_flow.uncertainties.model_uncertainty.ModelUncertainty`
            Model uncertainty specifications.
        """
        self.__adapt_to_network_changes()

        if not isinstance(model_uncertainty, ModelUncertainty):
            raise TypeError("'model_uncertainty' must be an instance of " +
                            "'epyt_flow.uncertainties.ModelUncertainty' but not of " +
                            f"'{type(model_uncertainty)}'")

        self.__model_uncertainty = model_uncertainty

    def set_sensor_noise(self, sensor_noise: SensorNoise) -> None:
        """
        Specifies the sensor noise -- i.e. uncertainties of sensor readings.

        Parameters
        ----------
        sensor_noise : :class:`~epyt_flow.uncertainties.sensor_noise.SensorNoise`
            Sensor noise specification.
        """
        self.__adapt_to_network_changes()

        if not isinstance(sensor_noise, SensorNoise):
            raise TypeError("'sensor_noise' must be an instance of " +
                            "'epyt_flow.uncertainties.SensorNoise' but not of " +
                            f"'{type(sensor_noise)}'")

        self.__sensor_noise = sensor_noise

    def set_general_parameters(self, demand_model: dict = None, simulation_duration: int = None,
                               hydraulic_time_step: int = None, quality_time_step: int = None,
                               reporting_time_step: int = None, reporting_time_start: int = None,
                               flow_units: int = None, quality_model: dict = None) -> None:
        """
        Sets some general parameters.

        Note that all these parameters can be stated in the .inp file as well.

        You only have to specify the parameters which you want to change -- all others
        can be left as None and will not be changed.

        Parameters
        ----------
        demand_model : `dict`, optional
            Specifies the demand model (e.g. pressure-driven or demand-driven) -- the dictionary
            must contain the "type", the minimal pressure ("pressure_min"),
            the required pressure ("pressure_required"), and the
            pressure exponent ("pressure_exponent").

            The default is None.

        simulation_duration : `int`, optional
            Number of seconds to be simulated.

            The default is None.
        hydraulic_time_step : `int`, optional
            Hydraulic time step -- i.e. the interval at which hydraulics are computed.

            The default is None.
        quality_time_step : `int`, optional
            Quality time step -- i.e. the interval at which qualities are computed.
            Should be much smaller than the hydraulic time step!

            The default is None.
        reporting_time_step : `int`, optional
            Report time step -- i.e. the interval at which hydraulics and quality states are
            reported.

            Must be a multiple of `hydraulic_time_step`.

            If None, it will be set equal to `hydraulic_time_step`

            The default is None.
        reporting_time_start : `int`, optional
            Start time (in seconds) at which reporting of hydraulic and quality states starts.

            The default is None.
        flow_units : `int`, optional
            Specifies the flow units -- i.e. all flows will be reported in these units.
            If None, the units from the .inp file will be used.

            Must be one of the following EPANET toolkit constants:

                - EN_CFS = 0
                - EN_GPM = 1
                - EN_MGD = 2
                - EN_IMGD = 3
                - EN_AFD = 4
                - EN_LPS = 5
                - EN_LPM = 6
                - EN_MLD = 7
                - EN_CMH = 8
                - EN_CMD = 9

            The default is None.
        quality_model : `dict`, optional
            Specifies the quality model -- the dictionary must contain,
            "type", "chemical_name", "chemical_units", and "trace_node_id", of the
            requested quality model.

            The default is None.
        """
        self.__adapt_to_network_changes()

        if demand_model is not None:
            self.epanet_api.setDemandModel(demand_model["type"], demand_model["pressure_min"],
                                           demand_model["pressure_required"],
                                           demand_model["pressure_exponent"])

        if simulation_duration is not None:
            if not isinstance(simulation_duration, int) or simulation_duration <= 0:
                raise ValueError("'simulation_duration' must be a positive integer specifying " +
                                 "the number of seconds to simulate")
            self.epanet_api.setTimeSimulationDuration(simulation_duration)  # TODO: Changing the simulation
            # duration from .inp file seems to break EPANET-MSX

        if hydraulic_time_step is not None:
            if not isinstance(hydraulic_time_step, int) or hydraulic_time_step <= 0:
                raise ValueError("'hydraulic_time_step' must be a positive integer specifying " +
                                 "the time steps of the hydraulic simulation")
            if len(self.__system_events) != 0:
                raise RuntimeError("Hydraulic time step cannot be changed after system events " +
                                   "such as leakages have been added to the scenario")
            self.epanet_api.setTimeHydraulicStep(hydraulic_time_step)
            if reporting_time_step is None:
                warnings.warn("No report time steps specified -- using 'hydraulic_time_step'")
                self.epanet_api.setTimeReportingStep(hydraulic_time_step)

        if reporting_time_step is not None:
            hydraulic_time_step = self.epanet_api.getTimeHydraulicStep()
            if not isinstance(reporting_time_step, int) or \
                    reporting_time_step % hydraulic_time_step != 0:
                raise ValueError("'reporting_time_step' must be a positive integer " +
                                 "and a multiple of 'hydraulic_time_step'")
            self.epanet_api.setTimeReportingStep(reporting_time_step)

        if reporting_time_start is not None:
            if not isinstance(reporting_time_start, int) or reporting_time_start <= 0:
                raise ValueError("'reporting_time_start' must be a positive integer specifying " +
                                 "the time at which reporting starts")
            self.epanet_api.setTimeReportingStart(reporting_time_start)

        if quality_time_step is not None:
            if not isinstance(quality_time_step, int) or quality_time_step <= 0 or \
                    quality_time_step > self.epanet_api.getTimeHydraulicStep():
                raise ValueError("'quality_time_step' must be a positive integer that is not " +
                                 "greater than the hydraulic time step")
            self.epanet_api.setTimeQualityStep(quality_time_step)

        if flow_units is not None:
            if flow_units == ToolkitConstants.EN_CFS:
                self.epanet_api.setFlowUnitsCFS()
            elif flow_units == ToolkitConstants.EN_GPM:
                self.epanet_api.setFlowUnitsGPM()
            elif flow_units == ToolkitConstants.EN_MGD:
                self.epanet_api.setFlowUnitsMGD()
            elif flow_units == ToolkitConstants.EN_IMGD:
                self.epanet_api.setFlowUnitsIMGD()
            elif flow_units == ToolkitConstants.EN_AFD:
                self.epanet_api.setFlowUnitsAFD()
            elif flow_units == ToolkitConstants.EN_LPS:
                self.epanet_api.setFlowUnitsLPS()
            elif flow_units == ToolkitConstants.EN_LPM:
                self.epanet_api.setFlowUnitsLPM()
            elif flow_units == ToolkitConstants.EN_MLD:
                self.epanet_api.setFlowUnitsMLD()
            elif flow_units == ToolkitConstants.EN_CMH:
                self.epanet_api.setFlowUnitsCMH()
            elif flow_units == ToolkitConstants.EN_CMD:
                self.epanet_api.setFlowUnitsCMD()
            else:
                raise ValueError(f"Unknown flow units '{flow_units}'")

        if quality_model is not None:
            if quality_model["type"] == "none":
                self.epanet_api.setQualityType("none")
            elif quality_model["type"] == "age":
                self.epanet_api.setQualityType("age")
            elif quality_model["type"] == "chem":
                self.epanet_api.setQualityType("chem", quality_model["chemical_name"],
                                               quality_model["chemical_units"])
            elif quality_model["type"] == "trace":
                self.epanet_api.setQualityType("trace", quality_model["trace_node_id"])
            else:
                raise ValueError(f"Unknown quality type: {quality_model['type']}")

    def __warn_if_quality_set(self):
        qual_info = self.epanet_api.getQualityInfo()
        if qual_info.QualityCode != ToolkitConstants.EN_NONE:
            warnings.warn("You are overriding current quality settings " +
                          f"'{qual_info.QualityType}'")

    def enable_waterage_analysis(self) -> None:
        """
        Sets water age analysis -- i.e. estimates the water age (in hours) at
        all places in the network.
        """
        self.__adapt_to_network_changes()

        self.__warn_if_quality_set()
        self.set_general_parameters(quality_model={"type": "age"})

    def enable_chemical_analysis(self, chemical_name: str = "Chlorine",
                                 chemical_units: str = "mg/L") -> None:
        """
        Sets chemical analysis.

        ATTENTION: Do not forget to inject this chemical into the WDN.

        Parameters
        ----------
        chemical_name : `str`, optional
            Name of the chemical being analyzed.

            The default is "Chlorine".
        chemical_units : `str`, optional
            Units that the chemical is measured in.
            Either "mg/L" or "ug/L".

            The default is "mg/L".
        """
        self.__adapt_to_network_changes()

        self.__warn_if_quality_set()
        self.set_general_parameters(quality_model={"type": "chem", "chemical_name": chemical_name,
                                                   "chemical_units": chemical_units})

    def add_quality_source(self, node_id: str, pattern: np.ndarray, source_type: int,
                           pattern_id: str = None, source_strength: int = 1.) -> None:
        """
        Adds a new external water quality source at a particular node.

        Parameters
        ----------
        node_id : `str`
            ID of the node at which this external water quality source is placed.
        pattern : `numpy.ndarray`
            1d source pattern.
        source_type : `int`,
            Types of the external water quality source -- must be of the following
            EPANET toolkit constants:

                - EN_CONCEN     = 0
                - EN_MASS       = 1
                - EN_SETPOINT   = 2
                - EN_FLOWPACED  = 3

            Description:

                - E_CONCEN Sets the concentration of external inflow entering a node
                - EN_MASS Injects a given mass/minute into a node
                - EN_SETPOINT Sets the concentration leaving a node to a given value
                - EN_FLOWPACED Adds a given value to the concentration leaving a node
        pattern_id : `str`, optional
            ID of the source pattern.

            If None, a pattern_id will be generated automatically -- be aware that this
            could conflict with existing pattern IDs (in this case, an exception is raised).

            The default is None.
        source_strength : `int`, optional
            Quality source strength -- i.e. quality-source = source_strength * pattern.

            The default is 1.
        """
        self.__adapt_to_network_changes()

        if self.epanet_api.getQualityInfo().QualityCode != ToolkitConstants.EN_CHEM:
            raise RuntimeError("Chemical analysis is not enabled -- " +
                               "call 'enable_chemical_analysis()' before calling this function.")
        if node_id not in self.__sensor_config.nodes:
            raise ValueError(f"Unknown node '{node_id}'")
        if not isinstance(pattern, np.ndarray):
            raise TypeError("'pattern' must be an instance of 'numpy.ndarray' " +
                            f"but not of '{type(pattern)}'")
        if not isinstance(source_type, int) or not 0 <= source_type <= 3:
            raise ValueError("Invalid type of water quality source")

        if pattern_id is None:
            pattern_id = f"quality_source_pattern_node={node_id}"
        if pattern_id in self.epanet_api.getPatternNameID():
            raise ValueError("Invalid 'pattern_id' -- " +
                             f"there already exists a pattern with ID '{pattern_id}'")

        node_idx = self.epanet_api.getNodeIndex(node_id)
        pattern_idx = self.epanet_api.addPattern(pattern_id, pattern)

        self.epanet_api.api.ENsetnodevalue(node_idx, ToolkitConstants.EN_SOURCETYPE, source_type)
        self.epanet_api.setNodeSourceQuality(node_idx, source_strength)
        self.epanet_api.setNodeSourcePatternIndex(node_idx, pattern_idx)

    def enable_sourcetracing_analysis(self, trace_node_id: str) -> None:
        """
        Set source tracing analysis -- i.e. tracks the percentage of flow from a given node
        reaching all other nodes over time.

        Parameters
        ----------
        trace_node_id : `str`
            ID of the node traced in the source tracing analysis.
        """
        self.__adapt_to_network_changes()

        if trace_node_id not in self.__sensor_config.nodes:
            raise ValueError(f"Invalid node ID '{trace_node_id}'")

        self.__warn_if_quality_set()
        self.set_general_parameters(quality_model={"type": "trace", "trace_node_id": trace_node_id})
