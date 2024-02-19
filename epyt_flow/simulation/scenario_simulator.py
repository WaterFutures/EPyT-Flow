import os
from typing import Generator
from copy import deepcopy
import warnings
import random
import numpy as np
from epyt import epanet
from epyt.epanet import ToolkitConstants
import networkx

from .scenario_config import ScenarioConfig
from .sensor_config import *
from ..uncertainty import ModelUncertainty, SensorNoise
from .events import SystemEvent, Leakage, SensorFault, SensorReadingEvent
from .scada import ScadaData, AdvancedControlModule


class WaterDistributionNetworkScenarioSimulator():
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
    f_inp_in : `str`
        Path to the .inp file.
    f_msx_in : `str`
        Path to the .msx file.
    model_uncertainty : :class:`~epyt_flow.uncertainty.model_uncertainty.ModelUncertainty`
        Specification of model uncertainty.
    sensor_noise : :class:`~epyt_flow.uncertainty.sensor_noise.SensorNoise`
        Speciation of sensor noise -- i.e. noise/uncertainty affecting the sensor readings.
    sensor_config : :class:`~epyt_flow.simulation.sensor_config.SensorConfig`
        Specification of all sensors.
    controls : `list[`:class:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule` `]`
        List of control modules that are active during the simulation.
    system_events : `list[`:class:`~epyt_flow.simulation.events.system_event.SystemEvent` `]`
        List of system events -- i.e. events that directly affect the simulation (e.g. leakages).
    sensor_reading_events : `list[`:class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent` `]`
        List of sensor reading events -- i.e. events that affect the readings of sensors.
    """
    def __init__(self, f_inp_in:str=None, f_msx_in:str=None, scenario_config:ScenarioConfig=None):
        if f_msx_in is not None and f_inp_in is None:
            raise ValueError("'f_inp_in' must be set if 'f_msx_in' is set.")
        if f_inp_in is None and scenario_config is None:
            raise ValueError("Either 'f_inp_in' or 'scenario_config' must be set.")
        if f_inp_in is not None:
            if not isinstance(f_inp_in, str):
                raise ValueError("'f_inp_in' must be an instance of 'str' but not of "+\
                                 f"'{type(f_inp_in)}'")
        if f_msx_in is not None:
            if not isinstance(f_msx_in, str):
                raise ValueError("'f_msx_in' must be an instance of 'str' but not of "+\
                                 f"'{type(f_msx_in)}'")
        if scenario_config is not None:
            if not isinstance(scenario_config, ScenarioConfig):
                raise ValueError("'scenario_config' must be an instance of "+\
                                 "'epyt_flow.simulation.ScenarioConfig' but not of "+\
                                    f"'{type(scenario_config)}'")

        self.epanet_api = None
        self.__f_inp_in = f_inp_in
        self.__f_msx_in = f_msx_in
        self.__model_uncertainty = None
        self.__sensor_noise = None
        self.__sensor_config = None
        self.__controls = None
        self.__system_events = []
        self.__sensor_reading_events = []

        general_params = None
        if scenario_config is not None:
            general_params = scenario_config.general_params
            self.__f_inp_in = scenario_config.f_inp_in
            self.__f_msx_in = scenario_config.f_msx_in
            self.__model_uncertainty = scenario_config.model_uncertainty
            self.__sensor_noise = scenario_config.sensor_noise
            self.__sensor_config = scenario_config.sensor_config
            self.__controls = scenario_config.controls
            self.__system_events = scenario_config.system_events
            self.__sensor_reading_events = scenario_config.sensor_reading_events

        self.__init(general_params)

    @property
    def f_inp_in(self) -> str:
        return self.__f_inp_in

    @property
    def f_msx_in(self) -> str:
        return self.__f_msx_in

    @property
    def model_uncertainty(self) -> ModelUncertainty:
        return deepcopy(self.__model_uncertainty)

    @model_uncertainty.setter
    def model_uncertainty(self, model_uncertainty:ModelUncertainty) -> None:
        self.set_model_uncertainty(model_uncertainty)

    @property
    def sensor_noise(self) -> SensorNoise:
        return deepcopy(self.__sensor_noise)

    @sensor_noise.setter
    def sensor_noise(self, sensor_noise:SensorNoise) -> None:
        self.set_sensor_noise(sensor_noise)

    @property
    def sensor_config(self) -> SensorConfig:
        return deepcopy(self.__sensor_config)

    @sensor_config.setter
    def sensor_config(self, sensor_config:SensorConfig) -> None:
        if not isinstance(sensor_config, SensorConfig):
            raise ValueError("'sensor_config' must be an instance of "+\
                             "'epyt_flow.simulation.SensorConfig' but not of "+\
                                f"'{type(sensor_config)}'")

        self.__sensor_config = sensor_config

    @property
    def controls(self) -> list[AdvancedControlModule]:
        return deepcopy(self.__controls)

    @property
    def system_events(self) -> list[SystemEvent]:
        return deepcopy(self.__system_events)

    @property
    def sensor_reading_events(self) -> list[SensorReadingEvent]:
        return deepcopy(self.__sensor_reading_events)

    def __init(self, general_params:dict) -> None:
        self.epanet_api = epanet(self.f_inp_in)

        if self.sensor_config is None:
            self.sensor_config = SensorConfig(nodes=self.epanet_api.getNodeNameID(),
                                              links=self.epanet_api.getLinkNameID(),
                                              valves=self.epanet_api.getLinkValveNameID(),
                                              pumps=self.epanet_api.getLinkPumpNameID(),
                                              tanks=self.epanet_api.getNodeTankNameID())
        if general_params is not None:
            self.set_general_parameters(**general_params)


    def __find_temporary_file(self) -> str:
        files = list(filter(lambda f: os.path.isfile(f) and "." not in f, os.listdir()))
        files.sort(key=os.path.getmtime)    # Sort by time to find the temporary file created by EPANET
        return files[::-1][0]

    def close(self):
        """Closes & unloads all resources and libraries.

        Call this function after the simulation is done -- do not call this function before!
        """
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
        qual_info = self.epanet_api.getQualityInfo()
        demand_info = self.epanet_api.getDemandModel()
        general_params = {"hydraulic_time_step": self.epanet_api.getTimeHydraulicStep(),
                          "quality_time_step": self.epanet_api.getTimeQualityStep(),
                          "simulation_duration": self.epanet_api.getTimeSimulationDuration() / \
                            (24*3600),   # Days to seconds!
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

    def get_topology(self) -> networkx.Graph:
        """
        Gets the topology (incl. information such as eleveations, pipe diameters, etc.) of this WDN.

        Returns
        -------
        `networkx.Graph`
            Topology of this WDN as a graph.
        """
        # Collect information about the topology of the water distribution network
        nodes_id = self.epanet_api.getNodeIndex()
        nodes_elevation = self.epanet_api.getNodeElevations()
        nodes_type = [self.epanet_api.TYPENODE[i] for i in self.epanet_api.getNodeTypeIndex()]

        links_data = self.epanet_api.getNodesConnectingLinksID()
        links_diameter = self.epanet_api.getLinkDiameter()
        links_length = self.epanet_api.getLinkLength()

        # Build graph describing the topology
        g = networkx.Graph(name=f"{self.f_inp_in}")

        for node, node_elevation, node_type in zip(nodes_id, nodes_elevation, nodes_type):
            g.add_node(node, info={"elevation": node_elevation, "type": node_type})

        g.add_nodes_from(nodes_id)

        for link, diameter, length in zip(links_data, links_diameter, links_length):
            g.add_edge(link[0], link[1], info={"diameter": diameter, "length": length})

        return g

    def randomize_demands(self) -> None:
        """
        Randomizes all demand patterns.
        """
        # Get all demand patterns
        demand_patterns_idx = self.epanet_api.getNodeDemandPatternIndex()
        demand_patterns_id = np.unique([idx for _, idx in demand_patterns_idx.items()])

        # Process each pattern separately
        for pattern_id in demand_patterns_id:
            if pattern_id == 0:
                continue

            pattern_length = self.epanet_api.getPatternLengths(pattern_id)
            pattern = []
            for t in range(pattern_length): # Get pattern
                pattern.append(self.epanet_api.getPatternValue(pattern_id, t+1))

            random.shuffle(pattern)   # Shuffle pattern

            for t in range(pattern_length): # Set shuffled/randomized pattern
                self.epanet_api.setPatternValue(pattern_id, t+1, pattern[t])

    def set_node_demand_pattern(self, node_id:str, base_demand:float, demand_pattern_id:str,
                                demand_pattern:numpy.ndarray) -> None:
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
        if not isinstance(base_demand, float):
            raise TypeError("'base_demand' must be an instance of 'float' "+\
                            f"but not if '{type(base_demand)}'")
        if not isinstance(demand_pattern_id, str):
            raise TypeError("'demand_pattern_id' must be an instance of 'str' "+\
                            f"but not of '{type(demand_pattern_id)}'")
        if not isinstance(demand_pattern, np.ndarray):
            raise TypeError("'demand_pattern' must be an instance of 'numpy.ndarray' "+\
                            f"but not of '{type(demand_pattern)}'")
        if len(demand_pattern.shape) > 1:
            raise ValueError(f"Inconsistent demand pattern shape '{demand_pattern.shape}' "+\
                             "detected. Expected a one dimensional array!")

        node_idx = self.epanet_api.getNodeIndex(node_id)
        self.epanet_api.addPattern(demand_pattern_id, demand_pattern)
        self.epanet_api.setNodeJunctionData(node_idx, self.epanet_api.getNodeElevations(node_idx),
                                            base_demand, demand_pattern_id)

    def add_control(self, control:AdvancedControlModule) -> None:
        """
        Adds a control module to the scenario simulation.

        Parameters
        ----------
        control : :class:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule`
            Control module.
        """
        if not isinstance(control, AdvancedControlModule):
            raise ValueError("'control' must be an instance of "+\
                             "'epyt_flow.simulation.scada.AdvancedControlModule' not of "+\
                                f"'{type(control)}'")

        self.__controls.append(control)

    def add_leakage(self, leakage_event:Leakage) -> None:
        """
        Adds a leakage to the scenario simulation.

        Parameters
        ----------
        event : :class:`~epyt_flow.simulation.events.leakages.Leakage`
            Leakage.
        """
        if not isinstance(leakage_event, Leakage):
            raise ValueError("'leakage_event' must be an instance of "+\
                             "'epyt_flow.simulation.events.Leakage' not of "+\
                                f"'{type(leakage_event)}'")

        self.__system_events.append(leakage_event)

    def add_system_event(self, event:SystemEvent) -> None:
        """
        Adds a system event to the scenario simulation -- i.e. an event directly affecting 
        the EPANET simulation.

        Parameters
        ----------
        event : :class:`~epyt_flow.simulation.events.system_event.SystemEvent`
            System event.
        """
        if not isinstance(event, SystemEvent):
            raise ValueError("'event' must be an instance of "+\
                             f"'epyt_flow.simulation.events.SystemEvent' not of '{type(event)}'")

        self.__system_events.append(event)

    def add_sensor_fault(self, sensor_fault_event:SensorFault) -> None:
        """
        Adds a sensor fault to the scenario simulation.

        Parameters
        ----------
        sensor_fault_event : :class:`~epyt_flow.simulation.events.sensor_faults.SensorFault`
            Sensor fault specifications.
        """
        if not isinstance(sensor_fault_event, SensorFault):
            raise ValueError("'sensor_fault_event' must be an instance of "+\
                             "'epyt_flow.simulation.events.SensorFault' not of "+\
                                f"'{type(sensor_fault_event)}'")

        self.__sensor_reading_events.append(sensor_fault_event)

    def add_sensor_reading_event(self, event:SensorReadingEvent) -> None:
        """
        Adds a sensor reading event to the scenario simulation.

        Parameters
        ----------
        event : :class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent`
            Sensor reading event.
        """
        if not isinstance(event, SensorReadingEvent):
            raise ValueError("'event' must be an instance of "+\
                             "'epyt_flow.simulation.events.SensorReadingEvent' not of "+\
                                f"'{type(event)}'")

        self.__sensor_reading_events.append(event)

    def set_sensors(self, sensor_type:int, sensor_locations:list[str]) -> None:
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
                - SENSOR_TYPE_TANK_LEVEL      = 8
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
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
        elif sensor_type == SENSOR_TYPE_TANK_LEVEL:
            self.__sensor_config.tank_level_sensors = sensor_locations
        else:
            raise ValueError(f"Unknown sensor type '{sensor_type}'")

    def __prepare_simulation(self) -> None:
        if self.__model_uncertainty is not None:
            self.__model_uncertainty.apply(self.epanet_api)

        for e in self.__system_events:
            e.init(self.epanet_api)

        if self.__controls is not None:
            for c in self.__controls:
                c.init(self.epanet_api)

    def run_simulation(self, hyd_export:str=None) -> ScadaData:
        """
        Runs the simulation of this scenario.

        Parameters
        ----------
        hyd_export : `str`, optional
            Path to an EPANET .hyd file for storing the simulated hydraulics -- these hydraulics 
            can be used later for an advanced quality analysis using EPANET-MSX.
        
            If None, the simulated hydraulics will NOT be exported to a EPANET .hyd file.

            The default is None.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Simulation results as SCADA data (i.e. sensor readings).
        """
        # Step by step simulation is required in some cases
        if len(self.__controls) != 0 or len(self.__system_events) != 0 or hyd_export is not None:
            result = None

            for scada_data in self.run_simulation_as_generator(hyd_export):
                if result is None:
                    result = scada_data
                else:
                    result.join(scada_data)

            return result
        else:
            self.__prepare_simulation()
            res = self.epanet_api.getComputedTimeSeries()

            if len(self.epanet_api.getLinkPumpIndex()) != 0:
                pumps_state = res.Status[:,self.epanet_api.getLinkPumpIndex()-1]
            else:
                pumps_state = np.array([[] for _ in range(res.Pressure.shape[0])])

            if len(self.epanet_api.getLinkValveIndex()) != 0:
                valves_state = res.Status[:,self.epanet_api.getLinkValveIndex()-1]
            else:
                # TODO: Differs from the step-by-step simulation!
                valves_state = np.array([[] for _ in range(res.Pressure.shape[0])])

            tanks_level = np.array([[] for _ in range(res.Pressure.shape[0])])  # TODO: No tanks level data available?

            return ScadaData(self.sensor_config, res.Pressure[:,:], res.Flow[:,:], res.Demand[:,:],
                             res.NodeQuality[:,:], res.LinkQuality[:,:], pumps_state,
                             valves_state, tanks_level, res.Time[:], self.sensor_reading_events,
                             self.sensor_noise)

    def run_simulation_as_generator(self, hyd_export:str=None,
                                    support_abort=False) -> Generator[ScadaData, bool, None]:
        """
        Runs the simulation of this scenario and provides the results as a generator.

        Parameters
        ----------
        hyd_export : `str`, optional
            Path to an EPANET .hyd file for storing the simulated hydraulics -- these hydraulics 
            can be used later for an advanced quality analysis using EPANET-MSX.
        
            If None, the simulated hydraulics will NOT be exported to a EPANET .hyd file.

            The default is None.
        
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
        self.__prepare_simulation()

        self.epanet_api.openHydraulicAnalysis()
        self.epanet_api.openQualityAnalysis()
        self.epanet_api.initializeHydraulicAnalysis(self.epanet_api.ToolkitConstants.EN_SAVE)
        self.epanet_api.initializeQualityAnalysis(self.epanet_api.ToolkitConstants.EN_SAVE)

        tmp_file = self.__find_temporary_file()

        requested_time_step = self.epanet_api.getTimeHydraulicStep()

        try:
            # Run simulation step by step
            total_time = 0
            tstep = 1
            first_itr = True
            while tstep > 0:
                if support_abort is True:   # Can the simulation be aborted? If so, handle it.
                    abort = yield
                    if abort is not False:
                        break

                if first_itr is True:   # Fix current time in the first iteration
                    tstep = 0
                    first_itr = False

                # Apply system events in a regular time interval only!
                if (total_time + tstep) % requested_time_step == 0:
                    for event in self.__system_events:
                        event.apply(total_time + tstep)

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
                demand_data = self.epanet_api.getNodeActualDemand().reshape(1, -1)  # TODO: Does not go back after emitter coefficient is changed back to zero
                quality_node_data = self.epanet_api.getNodeActualQuality().reshape(1, -1)
                quality_link_data = self.epanet_api.getLinkActualQuality().reshape(1, -1)
                pumps_state_data = self.epanet_api.getLinkPumpState().reshape(1,-1)
                tanks_level_data = self.epanet_api.getNodeTankVolume().reshape(1,-1)

                link_valve_idx = self.epanet_api.getLinkValveIndex()
                valves_state_data = self.epanet_api.getLinkStatus(link_valve_idx).reshape(1,-1)


                scada_data = ScadaData(self.__sensor_config, pressure_data, flow_data, demand_data,
                                    quality_node_data, quality_link_data, pumps_state_data,
                                    valves_state_data, tanks_level_data, np.array([total_time]),
                                    self.__sensor_reading_events, self.__sensor_noise)

                # Yield results in a regular time interval only!
                if total_time % requested_time_step == 0:
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
            os.remove(tmp_file)     # Close temporary files before raising any exceptions
            raise ex

        os.remove(tmp_file)     # Close temporary files

    def set_model_uncertainty(self, model_uncertainty:ModelUncertainty) -> None:
        """
        Specifies the model uncertainties.

        Parameters
        ----------
        model_uncertainty : :class:`~epyt_flow.uncertainties.model_uncertainty.ModelUncertainty`
            Model uncertainty specifications.
        """
        if not isinstance(model_uncertainty, ModelUncertainty):
            raise ValueError("'model_uncertainty' must be an instance of "+\
                             "'epyt_flow.uncertainties.ModelUncertainty' but not of "+\
                                f"'{type(model_uncertainty)}'")

        self.__model_uncertainty = model_uncertainty

    def set_sensor_noise(self, sensor_noise:SensorNoise) -> None:
        """
        Specifies the sensor noise -- i.e. uncertainties of sensor readings.

        Parameters
        ----------
        sensor_noise : :class:`~epyt_flow.uncertainties.sensor_noise.SensorNoise`
            Sensor noise specification.
        """
        if not isinstance(sensor_noise, SensorNoise):
            raise ValueError("'sensor_noise' must be an instance of "+\
                             "'epyt_flow.uncertainties.SensorNoise' but not of "+\
                                f"'{type(sensor_noise)}'")

        self.__sensor_noise = sensor_noise

    def set_general_parameters(self, demand_model:dict=None, simulation_duration:int=None,
                               hydraulic_time_step:int=None, quality_time_step:int=None,
                               quality_model:dict=None) -> None:
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
            the required pressure ("pressure_required"),
            and the pressure exponent ("pressure_exponent").
        
            The default is None.
            
        simulation_duraction : `int`, optional
            Number of days to be simulated.

            The default is None.
        hydraulic_time_step : `int`, optional
            Hydraulic time step -- i.e. the interval at which hydraulics are computed and reported.

            The default is None.
        quality_time_step : `int`, optional
            Quality time step -- i.e. the interval at which qualities are computed.
            Should be much smaller than the hydraulic time step!

            The default is None.
        quality_model : `dict`, optional
            Specifies the quality model -- the dictionary must contain,
            "type", "chemical_name", "chemical_units", and "trace_node_id", of the requested quality model.

            The default is None.
        """
        if demand_model is not None:
            self.epanet_api.setDemandModel(demand_model["type"], demand_model["pressure_min"],
                                           demand_model["pressure_required"],
                                           demand_model["pressure_exponent"])
        if simulation_duration is not None:
            self.epanet_api.setTimeSimulationDuration(simulation_duration*24*3600)  # TODO: Changing the simulation duration from .inp file seems to break EPANET-MSX
        if hydraulic_time_step is not None:
            self.epanet_api.setTimeHydraulicStep(hydraulic_time_step)
        if quality_time_step is not None:
            self.epanet_api.setTimeQualityStep(quality_time_step)
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
            warnings.warn("You are overriding current quality settings "+\
                          f"'{qual_info.QualityType}'")

    def enable_waterage_analysis(self) -> None:
        """
        Sets water age analysis -- i.e. estimates the water age (in hours) at 
        all places in the network.
        """
        self.__warn_if_quality_set()
        self.set_general_parameters(quality_model={"type": "age"})

    def enable_chemical_analysis(self, chemical_name:str="Chlorine",
                                 chemical_units:str="mg/L") -> None:
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
        self.__warn_if_quality_set()
        self.set_general_parameters(quality_model={"type": "chem", "chemical_name": chemical_name,
                                                   "chemical_units": chemical_units})

    def add_quality_source(self, node_id:str, pattern_id:str, pattern:numpy.ndarray,
                           source_type:str, source_strength:int=1.) -> None:
        """
        Adds a new external water quality source at a particular node.

        Parameters
        ----------
        node_id : `str`
            ID of the node at which this external water quality source is placed.
        pattern_id : `str`
            ID of the source pattern.
        pattern : `numpy.ndarray`
            1d source pattern.
        source_type : `str`,
            Types of the external water quality source -- must be of the following:
                - CONCEN Sets the concentration of external inflow entering a node
                - MASS Injects a given mass/minute into a node
                - SETPOINT Sets the concentration leaving a node to a given value
                - FLOWPACED Adds a given value to the concentration leaving a node
        source_strength : `int`, optional
            Quality source strength -- i.e. quality-source = source_strength * pattern.

            The default is 1.
        """
        if self.epanet_api.getQualityInfo().QualityCode != ToolkitConstants.EN_CHEM:
            raise RuntimeError("Chemical analysis is not enabled -- "+\
                               "call 'enable_chemical_analysis()' before calling this function.")
        if not node_id in self.sensor_config.nodes:
            raise ValueError(f"Unknown node '{node_id}'")
        if not isinstance(pattern, numpy.ndarray):
            raise ValueError("'pattern' must be an instance of 'numpy.ndarray' "+\
                             f"but not of '{type(pattern)}'")

        node_idx = self.epanet_api.getNodeIndex(node_id)
        pattern_idx = self.epanet_api.addPattern(pattern_id, pattern)

        self.epanet_api.setNodeSourceType(pattern_idx, source_type)
        self.epanet_api.setNodeSourceQuality(node_idx, source_strength)
        self.epanet_api.setNodeSourcePatternIndex(node_idx, pattern_idx)

    def enable_sourcetracing_analysis(self, trace_node_id:str):
        """
        Set source tracing analysis -- i.e. tracks the percentage of flow from a given node 
        reaching all other nodes over time.

        Parameters
        ----------
        trace_node_id : `str`
            ID of the node traced in the source tracing analysis.
        """
        if not trace_node_id in self.sensor_config.nodes:
            raise ValueError(f"Invalid node ID '{trace_node_id}'")

        self.__warn_if_quality_set()
        self.set_general_parameters(quality_model={"type": "trace", "trace_node_id": trace_node_id})
