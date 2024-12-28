"""
Module provides a class for scenario simulations.
"""
import sys
import os
import pathlib
import time
from typing import Generator, Union
from copy import deepcopy
import shutil
import warnings
import random
import math
import uuid
import numpy as np
from epyt import epanet
from epyt.epanet import ToolkitConstants
from tqdm import tqdm

from .scenario_config import ScenarioConfig
from .sensor_config import SensorConfig, areaunit_to_id, massunit_to_id, qualityunit_to_id, \
    qualityunit_to_str, MASS_UNIT_MG, \
    SENSOR_TYPE_LINK_FLOW, SENSOR_TYPE_LINK_QUALITY, SENSOR_TYPE_NODE_DEMAND, \
    SENSOR_TYPE_NODE_PRESSURE, SENSOR_TYPE_NODE_QUALITY, \
    SENSOR_TYPE_PUMP_STATE, SENSOR_TYPE_PUMP_EFFICIENCY, SENSOR_TYPE_PUMP_ENERGYCONSUMPTION, \
    SENSOR_TYPE_TANK_VOLUME, SENSOR_TYPE_VALVE_STATE, SENSOR_TYPE_NODE_BULK_SPECIES, \
    SENSOR_TYPE_LINK_BULK_SPECIES, SENSOR_TYPE_SURFACE_SPECIES
from ..uncertainty import ModelUncertainty, SensorNoise
from .events import SystemEvent, Leakage, ActuatorEvent, SensorFault, SensorReadingAttack, \
    SensorReadingEvent
from .scada import ScadaData, AdvancedControlModule
from ..topology import NetworkTopology, UNITS_SIMETRIC, UNITS_USCUSTOM
from ..utils import get_temp_folder


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
    epanet_verbose : `bool`, optional
        If True, EPyT is verbose and might print messages from time to time.

        The default is False.

    Attributes
    ----------
    epanet_api : `epyt.epanet`
        API to EPANET and EPANET-MSX.
    _model_uncertainty : :class:`~epyt_flow.uncertainty.model_uncertainty.ModelUncertainty`, protected
        Model uncertainty.
    _sensor_noise : :class:`~epyt_flow.uncertainty.sensor_noise.SensorNoise`, protected
        Sensor noise.
    _sensor_config : :class:`~epyt_flow.simulation.sensor_config.SensorConfig`, protected
        Sensor configuration.
    _controls : list[:class:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule`], protected
        List of custom control modules.
    _system_events : list[:class:`~epyt_flow.simulation.events.system_event.SystemEvent`], protected
        Lsit of system events such as leakages.
    _sensor_reading_events : list[:class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent`], protected
        List of sensor reading events such as sensor override attacks.
    """

    def __init__(self, f_inp_in: str = None, f_msx_in: str = None,
                 scenario_config: ScenarioConfig = None, epanet_verbose: bool = False):
        if f_msx_in is not None and f_inp_in is None:
            raise ValueError("'f_inp_in' must be set if 'f_msx_in' is set.")
        if f_inp_in is None and scenario_config is None:
            raise ValueError("Either 'f_inp_in' or 'scenario_config' must be set.")
        if scenario_config is not None and f_inp_in is not None:
            raise ValueError("'f_inp_in' or 'scenario_config' can not be used at the same time")
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
        if not isinstance(epanet_verbose, bool):
            raise TypeError("'epanet_verbose' must be an instance of 'bool' " +
                            f"but not of '{type(epanet_verbose)}'")

        self.__f_inp_in = f_inp_in if scenario_config is None else scenario_config.f_inp_in
        self.__f_msx_in = f_msx_in if scenario_config is None else scenario_config.f_msx_in
        self._model_uncertainty = ModelUncertainty()
        self._sensor_noise = None
        self._sensor_config = None
        self._controls = []
        self._system_events = []
        self._sensor_reading_events = []
        self.__running_simulation = False

        custom_epanet_lib = None
        custom_epanetmsx_lib = None
        if sys.platform.startswith("linux") or sys.platform.startswith("darwin") :
            path_to_custom_libs = os.path.join(pathlib.Path(__file__).parent.resolve(),
                                               "..", "customlibs")

            libepanet_name = "libepanet2_2.so" if sys.platform.startswith("linux") \
                else "libepanet2_2.dylib"
            libepanetmsx_name = "libepanetmsx2_2_0.so" if sys.platform.startswith("linux") \
                else "libepanetmsx2_2_0.dylib"

            if os.path.isfile(os.path.join(path_to_custom_libs, libepanet_name)):
                custom_epanet_lib = os.path.join(path_to_custom_libs, libepanet_name)
            if os.path.isfile(os.path.join(path_to_custom_libs, libepanetmsx_name)):
                custom_epanetmsx_lib = os.path.join(path_to_custom_libs, libepanetmsx_name)

        with warnings.catch_warnings():
            # Treat all warnings as exceptions when trying to load .inp and .msx files
            warnings.simplefilter('error')

            # Workaround for EPyT bug concerning parallel simulations (see EPyT issue #54):
            # 1. Create random tmp folder (make sure it is unique!)
            # 2. Copy .inp and .msx file there
            # 3. Use those copies  when loading EPyT
            tmp_folder_path = os.path.join(get_temp_folder(), f"{random.randint(int(1e5), int(1e7))}{time.time()}")
            pathlib.Path(tmp_folder_path).mkdir(parents=True, exist_ok=False)

            def __file_exists(file_in: str) -> bool:
                try:
                    return pathlib.Path(file_in).is_file()
                except Exception:
                    return False

            if not __file_exists(self.__f_inp_in):
                my_f_inp_in = self.__f_inp_in
                self.__my_f_inp_in = None
            else:
                my_f_inp_in = os.path.join(tmp_folder_path, pathlib.Path(self.__f_inp_in).name)
                shutil.copyfile(self.__f_inp_in, my_f_inp_in)
                self.__my_f_inp_in = my_f_inp_in

            if self.__f_msx_in is not None:
                if not __file_exists(self.__f_msx_in):
                    my_f_msx_in = self.__f_msx_in
                else:
                    my_f_msx_in = os.path.join(tmp_folder_path, pathlib.Path(self.__f_msx_in).name)
                    shutil.copyfile(self.__f_msx_in, my_f_msx_in)
            else:
                my_f_msx_in = None

            self.epanet_api = epanet(my_f_inp_in, ph=self.__f_msx_in is None,
                                     customlib=custom_epanet_lib, loadfile=True,
                                     display_msg=epanet_verbose,
                                     display_warnings=False)

            if self.__f_msx_in is not None:
                self.epanet_api.loadMSXFile(my_f_msx_in, customMSXlib=custom_epanetmsx_lib)

        self._sensor_config = self._get_empty_sensor_config()
        if scenario_config is not None:
            if scenario_config.general_params is not None:
                self.set_general_parameters(**scenario_config.general_params)

            self._model_uncertainty = scenario_config.model_uncertainty
            self._sensor_noise = scenario_config.sensor_noise
            self._sensor_config = scenario_config.sensor_config

            for control in scenario_config.controls:
                self.add_control(control)
            for event in scenario_config.system_events:
                self.add_system_event(event)
            for event in scenario_config.sensor_reading_events:
                self.add_sensor_reading_event(event)

    def _get_empty_sensor_config(self, node_id_to_idx: dict = None, link_id_to_idx: dict = None,
                                 valve_id_to_idx: dict = None, pump_id_to_idx: dict = None,
                                 tank_id_to_idx: dict = None, bulkspecies_id_to_idx: dict = None,
                                 surfacespecies_id_to_idx: dict = None) -> SensorConfig:
        flow_unit = self.epanet_api.api.ENgetflowunits()
        quality_unit = qualityunit_to_id(self.epanet_api.getQualityInfo().QualityChemUnits)
        bulk_species = []
        surface_species = []
        bulk_species_mass_unit = []
        surface_species_mass_unit = []
        surface_species_area_unit = None

        if self.__f_msx_in is not None:
            surface_species_area_unit = areaunit_to_id(self.epanet_api.getMSXAreaUnits())

            for species_id, species_type, mass_unit in zip(self.epanet_api.getMSXSpeciesNameID(),
                                                           self.epanet_api.getMSXSpeciesType(),
                                                           self.epanet_api.getMSXSpeciesUnits()):
                if species_type == "BULK":
                    bulk_species.append(species_id)
                    bulk_species_mass_unit.append(massunit_to_id(mass_unit))
                elif species_type == "WALL":
                    surface_species.append(species_id)
                    surface_species_mass_unit.append(massunit_to_id(mass_unit))

        return SensorConfig(nodes=self.epanet_api.getNodeNameID(),
                            links=self.epanet_api.getLinkNameID(),
                            valves=self.epanet_api.getLinkValveNameID(),
                            pumps=self.epanet_api.getLinkPumpNameID(),
                            tanks=self.epanet_api.getNodeTankNameID(),
                            bulk_species=bulk_species,
                            surface_species=surface_species,
                            flow_unit=flow_unit,
                            quality_unit=quality_unit,
                            bulk_species_mass_unit=bulk_species_mass_unit,
                            surface_species_mass_unit=surface_species_mass_unit,
                            surface_species_area_unit=surface_species_area_unit,
                            node_id_to_idx=node_id_to_idx,
                            link_id_to_idx=link_id_to_idx,
                            valve_id_to_idx=valve_id_to_idx,
                            pump_id_to_idx=pump_id_to_idx,
                            tank_id_to_idx=tank_id_to_idx,
                            bulkspecies_id_to_idx=bulkspecies_id_to_idx,
                            surfacespecies_id_to_idx=surfacespecies_id_to_idx)

    @property
    def f_inp_in(self) -> str:
        """
        Gets the path to the .inp file.

        Returns
        -------
        `str`
            Path to the .inp file.
        """
        self._adapt_to_network_changes()

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
        self._adapt_to_network_changes()

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
        self._adapt_to_network_changes()

        return deepcopy(self._model_uncertainty)

    @model_uncertainty.setter
    def model_uncertainty(self, model_uncertainty: ModelUncertainty) -> None:
        self._adapt_to_network_changes()

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
        self._adapt_to_network_changes()

        return deepcopy(self._sensor_noise)

    @sensor_noise.setter
    def sensor_noise(self, sensor_noise: SensorNoise) -> None:
        self._adapt_to_network_changes()

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
        self._adapt_to_network_changes()

        return deepcopy(self._sensor_config)

    @sensor_config.setter
    def sensor_config(self, sensor_config: SensorConfig) -> None:
        if not isinstance(sensor_config, SensorConfig):
            raise TypeError("'sensor_config' must be an instance of " +
                            "'epyt_flow.simulation.SensorConfig' but not of " +
                            f"'{type(sensor_config)}'")

        sensor_config.validate(self.epanet_api)

        self._sensor_config = sensor_config

    @property
    def controls(self) -> list[AdvancedControlModule]:
        """
        Gets all control modules.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.scada.advanced_control.AdvancedControlModule`]
            All control modules.
        """
        self._adapt_to_network_changes()

        return deepcopy(self._controls)

    @property
    def leakages(self) -> list[Leakage]:
        """
        Gets all leakages.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.events.leakages.Leakage`]
            All leakages.
        """
        self._adapt_to_network_changes()

        return deepcopy(list(filter(lambda e: isinstance(e, Leakage), self._system_events)))

    @property
    def actuator_events(self) -> list[ActuatorEvent]:
        """
        Gets all actuator events.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.events.actuator_event.ActuatorEvent`]
            All actuator events.
        """
        self._adapt_to_network_changes()

        return deepcopy(list(filter(lambda e: isinstance(e, ActuatorEvent), self._system_events)))

    @property
    def system_events(self) -> list[SystemEvent]:
        """
        Gets all system events (e.g. leakages, etc.).

        Returns
        -------
        list[:class:`~epyt_flow.simulation.events.system_event.SystemEvent`]
            All system events.
        """
        self._adapt_to_network_changes()

        return deepcopy(self._system_events)

    @property
    def sensor_faults(self) -> list[SensorFault]:
        """
        Gets all sensor faults.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.events.sensor_faults.SensorFault`]
            All sensor faults.
        """
        self._adapt_to_network_changes()

        return deepcopy(list(filter(lambda e: isinstance(e, SensorFault),
                                    self._sensor_reading_events)))

    @property
    def sensor_reading_attacks(self) -> list[SensorReadingAttack]:
        """
        Gets all sensor reading attacks.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.events.sensor_reading_attacks.SensorReadingAttack`]
            All sensor reading attacks.
        """
        self._adapt_to_network_changes()

        return deepcopy(list(filter(lambda e: isinstance(e, SensorReadingAttack)),
                             self._sensor_reading_events))

    @property
    def sensor_reading_events(self) -> list[SensorReadingEvent]:
        """
        Gets all sensor reading events (e.g. sensor faults, etc.).

        Returns
        -------
        list[:class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent`]
            All sensor reading events.
        """
        self._adapt_to_network_changes()

        return deepcopy(self._sensor_reading_events)

    def _adapt_to_network_changes(self):
        nodes = self.epanet_api.getNodeNameID()
        links = self.epanet_api.getLinkNameID()

        node_id_to_idx = {node_id: self.epanet_api.getNodeIndex(node_id) - 1 for node_id in nodes}
        link_id_to_idx = {link_id: self.epanet_api.getLinkIndex(link_id) - 1 for link_id in links}
        valve_id_to_idx = None  # {valve_id: self.epanet_api.getLinkValveIndex(valve_id) for valve_id in valves}
        pump_id_to_idx = None  # {pump_id: self.epanet_api.getLinkPumpIndex(pump_id) - 1 for pump_id in pumps}
        tank_id_to_idx = None  # {tank_id: self.epanet_api.getNodeTankIndex(tank_id) - 1 for tank_id in tanks}
        bulkspecies_id_to_idx = None
        surfacespecies_id_to_idx = None

        # Adapt sensor configuration to potential cahnges in the network's topology
        new_sensor_config = self._get_empty_sensor_config(node_id_to_idx, link_id_to_idx,
                                                          valve_id_to_idx, pump_id_to_idx,
                                                          tank_id_to_idx, bulkspecies_id_to_idx,
                                                          surfacespecies_id_to_idx)
        new_sensor_config.pressure_sensors = self._sensor_config.pressure_sensors
        new_sensor_config.flow_sensors = self._sensor_config.flow_sensors
        new_sensor_config.demand_sensors = self._sensor_config.demand_sensors
        new_sensor_config.quality_node_sensors = self._sensor_config.quality_node_sensors
        new_sensor_config.quality_link_sensors = self._sensor_config.quality_link_sensors
        new_sensor_config.pump_state_sensors = self._sensor_config.pump_state_sensors
        new_sensor_config.pump_efficiency_sensors = self._sensor_config.pump_efficiency_sensors
        new_sensor_config.pump_energyconsumption_sensors = self._sensor_config.\
            pump_energyconsumption_sensors
        new_sensor_config.valve_state_sensors = self._sensor_config.valve_state_sensors
        new_sensor_config.tank_volume_sensors = self._sensor_config.tank_volume_sensors
        new_sensor_config.bulk_species_node_sensors = self._sensor_config.bulk_species_node_sensors
        new_sensor_config.bulk_species_link_sensors = self._sensor_config.bulk_species_link_sensors
        new_sensor_config.surface_species_sensors = self._sensor_config.surface_species_sensors

        self._sensor_config = new_sensor_config

    def close(self):
        """
        Closes & unloads all resources and libraries.

        Call this function after the simulation is done -- do not call this function before!
        """
        if self.__f_msx_in is not None:
            self.epanet_api.unloadMSX()

        self.epanet_api.unload()

        if self.__my_f_inp_in is not None:
            shutil.rmtree(pathlib.Path(self.__my_f_inp_in).parent)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def save_to_epanet_file(self, inp_file_path: str, msx_file_path: str = None,
                            export_sensor_config: bool = True, undo_system_events: bool = True
                            ) -> None:
        """
        Exports this scenario to EPANET files -- i.e. an .inp file
        and (optionally) a .msx file if EPANET-MSX was loaded.

        Parameters
        ----------
        inp_file_path : `str`
            Path to the .inp file where this scenario will be stored.

            If 'inp_file_path' is None, 'msx_file_path' must not be None!
        msx_file_path : `str`, optional
            Path to the .msx file where this MSX component of this scneario will be stored.

            Note that this is only applicable if EPANET-MSX was loaded.

            The default is None.
        export_sensor_config : `bool`, optional
            If True, the current sensor placement is exported as well.

            The default is True.
        """
        if inp_file_path is None and msx_file_path is None:
            raise ValueError("At least one of the paths (.inp and .msx) must not be None")
        if inp_file_path is not None:
            if not isinstance(inp_file_path, str):
                raise TypeError("'inp_file_path' must be an instance of 'str' " +
                                f"but not of '{type(inp_file_path)}'")
        if msx_file_path is not None:
            if not isinstance(msx_file_path, str):
                raise TypeError("msx_file_path' msut be an instance of 'str' " +
                                f"but not of {type(msx_file_path)}")
        if not isinstance(export_sensor_config, bool):
            raise TypeError("'export_sensor_config' must be an instance of 'bool' " +
                            f"but not of '{type(export_sensor_config)}'")

        def __override_report_section(file_in: str, report_desc: str) -> None:
            with open(file_in, mode="r+", encoding="utf-8") as f_in:
                # Find and remove exiting REPORT section
                content = f_in.read()
                try:
                    report_section_start_idx = content.index("[REPORT]")
                    report_section_end_idx = content.index("[", report_section_start_idx + 1)

                    content = content[:report_section_start_idx] + content[report_section_end_idx:]
                    f_in.seek(0)
                    f_in.write(content)
                    f_in.truncate()
                except ValueError:
                    pass

                # Write new REPORT section in the very end of the file
                write_end_section = False
                try:
                    end_idx = content.index("[END]")
                    write_end_section = True
                    f_in.seek(end_idx)
                except ValueError:
                    pass
                f_in.write(report_desc)
                if write_end_section is True:
                    f_in.write("\n[END]")

        if undo_system_events is True:
            for event in self._system_events:
                event.cleanup()

        if inp_file_path is not None:
            self.epanet_api.saveInputFile(inp_file_path)
            self.__f_inp_in = inp_file_path

            if export_sensor_config is True:
                report_desc = "\n\n[REPORT]\n"
                report_desc += "ENERGY YES\n"
                report_desc += "STATUS YES\n"

                nodes = []
                links = []

                # Parse sensor config
                pressure_sensors = self._sensor_config.pressure_sensors
                if len(pressure_sensors) != 0:
                    report_desc += "Pressure YES\n"
                    nodes += pressure_sensors

                flow_sensors = self._sensor_config.flow_sensors
                if len(flow_sensors) != 0:
                    report_desc += "Flow YES\n"
                    links += flow_sensors

                demand_sensors = self._sensor_config.demand_sensors
                if len(demand_sensors) != 0:
                    report_desc += "Demand YES\n"
                    nodes += demand_sensors

                node_quality_sensors = self._sensor_config.quality_node_sensors
                if len(node_quality_sensors) != 0:
                    report_desc += "Quality YES\n"
                    nodes += node_quality_sensors

                link_quality_sensors = self._sensor_config.quality_link_sensors
                if len(link_quality_sensors) != 0:
                    if len(node_quality_sensors) == 0:
                        report_desc += "Quality YES\n"
                    links += link_quality_sensors

                # Create final REPORT section
                nodes = list(set(nodes))
                links = list(set(links))

                if len(nodes) != 0:
                    if set(nodes) == set(self._sensor_config.nodes):
                        nodes = ["ALL"]
                    report_desc += f"NODES {' '.join(nodes)}\n"

                if len(links) != 0:
                    if set(links) == set(self._sensor_config.links):
                        links = ["ALL"]
                    report_desc += f"LINKS {' '.join(links)}\n"

                __override_report_section(inp_file_path, report_desc)

        if self.__f_msx_in is not None and msx_file_path is not None:
            self.epanet_api.saveMSXFile(msx_file_path)
            self.__f_msx_in = msx_file_path

            if export_sensor_config is True:
                report_desc = "\n\n[REPORT]\n"
                species = []
                nodes = []
                links = []

                # Parse sensor config
                bulk_species_node_sensors = self._sensor_config.bulk_species_node_sensors
                for bulk_species_id in bulk_species_node_sensors.keys():
                    species.append(bulk_species_id)
                    nodes += bulk_species_node_sensors[bulk_species_id]

                bulk_species_link_sensors = self._sensor_config.bulk_species_link_sensors
                for bulk_species_id in bulk_species_link_sensors.keys():
                    species.append(bulk_species_id)
                    links += bulk_species_link_sensors[bulk_species_id]

                surface_species_link_sensors = self._sensor_config.surface_species_sensors
                for surface_species_id in surface_species_link_sensors.keys():
                    species.append(surface_species_id)
                    links += surface_species_link_sensors[surface_species_id]

                nodes = list(set(nodes))
                links = list((set(links)))
                species = list(set(species))

                # Create REPORT section
                if len(nodes) != 0:
                    if set(nodes) == set(self._sensor_config.nodes):
                        nodes = ["ALL"]
                    report_desc += f"NODES {' '.join(nodes)}\n"

                if len(links) != 0:
                    if set(links) == set(self._sensor_config.links):
                        links = ["ALL"]
                    report_desc += f"LINKS {' '.join(links)}\n"

                for species_id in species:
                    report_desc += f"SPECIES {species_id} YES\n"

                __override_report_section(msx_file_path, report_desc)

        if undo_system_events is True:
            for event in self._system_events:
                event.init(self.epanet_api)

    def get_flow_units(self) -> int:
        """
        Gets the flow units.

        Will be one of the following EPANET toolkit constants:

            - EN_CFS = 0 (cu foot/sec)
            - EN_GPM = 1 (gal/min)
            - EN_MGD = 2 (Million gal/day)
            - EN_IMGD = 3 (Imperial MGD)
            - EN_AFD = 4 (ac-foot/day)
            - EN_LPS = 5 (liter/sec)
            - EN_LPM = 6 (liter/min)
            - EN_MLD = 7 (Megaliter/day)
            - EN_CMH = 8 (cubic meter/hr)
            - EN_CMD = 9 (cubic meter/day)

        Returns
        -------
        `int`
            Flow units.
        """
        return self.epanet_api.api.ENgetflowunits()

    def get_units_category(self) -> int:
        """
        Gets the category of units -- i.e. US Customary or SI Metric units.

        Will be one of the following constants:

            - UNITS_USCUSTOM = 0  (US Customary)
            - UNITS_SIMETRIC = 1  (SI Metric)

        Returns
        -------
        `int`
            Units category.
        """
        if self.get_flow_units() in [ToolkitConstants.EN_CFS, ToolkitConstants.EN_GPM,
                                     ToolkitConstants.EN_MGD, ToolkitConstants.EN_IMGD,
                                     ToolkitConstants.EN_AFD]:
            return UNITS_USCUSTOM
        else:
            return UNITS_SIMETRIC

    def get_hydraulic_time_step(self) -> int:
        """
        Gets the hydraulic time step -- i.e. time step in the hydraulic simulation.

        Returns
        -------
        `int`
            Hydraulic time step in seconds.
        """
        return self.epanet_api.getTimeHydraulicStep()

    def get_quality_time_step(self) -> int:
        """
        Gets the quality time step -- i.e. time step in the simple quality simulation.

        Returns
        -------
        `int`
            Quality time step in seconds.
        """
        return self.epanet_api.getTimeQualityStep()

    def get_simulation_duration(self) -> int:
        """
        Gets the simulation duration -- i.e. time length to be simulated.

        Returns
        -------
        `int`
            Simulation duration in seconds.
        """
        return self.epanet_api.getTimeSimulationDuration()

    def get_demand_model(self) -> dict:
        """
        Gets the demand model and its parameters.

        Returns
        -------
        `dict`
            Demand model.
        """
        demand_info = self.epanet_api.getDemandModel()

        return {"type": "PDA" if demand_info.DemandModelCode == 1 else "DDA",
                "pressure_min": demand_info.DemandModelPmin,
                "pressure_required": demand_info.DemandModelPreq,
                "pressure_exponent": demand_info.DemandModelPexp}

    def get_quality_model(self) -> dict:
        """
        Gets the quality model and its parameters.

        Note that this quality model refers to the basic quality analysis
        as implemented in EPANET.

        Returns
        -------
        `dict`
            Quality model.
        """
        qual_info = self.epanet_api.getQualityInfo()

        return {"code": qual_info.QualityCode,
                "type": qual_info.QualityType,
                "chemical_name": qual_info.QualityChemName,
                "units": qualityunit_to_id(qual_info.QualityChemUnits),
                "trace_node_id": qual_info.TraceNode}

    def get_reporting_time_step(self) -> int:
        """
        Gets the reporting time steps -- i.e. time steps at which sensor readings are provided.

        Is always a multiple of the hydraulic time step.

        Returns
        -------
        `int`
            Reporting time steps in seconds.
        """
        return self.epanet_api.getTimeReportingStep()

    def get_scenario_config(self) -> ScenarioConfig:
        """
        Gets the configuration of this scenario -- i.e. all information & elements
        that completely describe this scenario.

        Returns
        -------
        :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
            Complete scenario specification.
        """
        self._adapt_to_network_changes()

        general_params = {"hydraulic_time_step": self.get_hydraulic_time_step(),
                          "quality_time_step": self.get_quality_time_step(),
                          "reporting_time_step": self.get_reporting_time_step(),
                          "simulation_duration": self.get_simulation_duration(),
                          "flow_units_id": self.get_flow_units(),
                          "quality_model": self.get_quality_model(),
                          "demand_model": self.get_demand_model()}

        return ScenarioConfig(f_inp_in=self.__f_inp_in, f_msx_in=self.__f_msx_in,
                              general_params=general_params, sensor_config=self.sensor_config,
                              memory_consumption_estimate=self.estimate_memory_consumption(),
                              controls=self.controls, sensor_noise=self.sensor_noise,
                              model_uncertainty=self.model_uncertainty,
                              system_events=self.system_events,
                              sensor_reading_events=self.sensor_reading_events)

    def estimate_memory_consumption(self) -> float:
        """
        Estimates the memory consumption of the simulation -- i.e. the amount of memory that is
        needed on the hard disk as well as in RAM.

        Returns
        -------
        `float`
            Estimated memory consumption in MB.
        """
        self._adapt_to_network_changes()

        n_time_steps = int(self.epanet_api.getTimeSimulationDuration() /
                           self.epanet_api.getTimeReportingStep())
        n_quantities = self.epanet_api.getNodeCount() * 3 + self.epanet_api.getNodeTankCount() + \
                       self.epanet_api.getLinkValveCount() + self.epanet_api.getLinkPumpCount() + \
                       self.epanet_api.getLinkCount() * 2

        if self.__f_msx_in is not None:
            n_quantities += self.epanet_api.getLinkCount() * 2 + self.epanet_api.getNodeCount()

        n_bytes_per_quantity = 64

        return n_time_steps * n_quantities * n_bytes_per_quantity * .000001

    def get_topology(self) -> NetworkTopology:
        """
        Gets the topology (incl. information such as elevations, pipe diameters, etc.) of this WDN.

        Returns
        -------
        :class:`~epyt_flow.topology.NetworkTopology`
            Topology of this WDN as a graph.
        """
        self._adapt_to_network_changes()

        # Collect information about the topology of the water distribution network
        nodes_id = self.epanet_api.getNodeNameID()
        nodes_elevation = self.epanet_api.getNodeElevations()
        nodes_type = [self.epanet_api.TYPENODE[i] for i in self.epanet_api.getNodeTypeIndex()]
        nodes_coord = [self.epanet_api.api.ENgetcoord(node_idx)
                       for node_idx in self.epanet_api.getNodeIndex()]
        node_tank_names = self.epanet_api.getNodeTankNameID()

        links_id = self.epanet_api.getLinkNameID()
        links_type = self.epanet_api.getLinkType()
        links_data = self.epanet_api.getNodesConnectingLinksID()
        links_diameter = self.epanet_api.getLinkDiameter()
        links_length = self.epanet_api.getLinkLength()
        links_roughness_coeff = self.epanet_api.getLinkRoughnessCoeff()
        links_bulk_coeff = self.epanet_api.getLinkBulkReactionCoeff()
        links_wall_coeff = self.epanet_api.getLinkWallReactionCoeff()
        links_loss_coeff = self.epanet_api.getLinkMinorLossCoeff()

        pumps_id = self.epanet_api.getLinkPumpNameID()
        pumps_type = self.epanet_api.getLinkPumpType()

        valves_id = self.epanet_api.getLinkValveNameID()

        # Build graph describing the topology
        nodes = []
        for node_id, node_elevation, node_type, node_coord in zip(nodes_id, nodes_elevation,
                                                                  nodes_type, nodes_coord):
            node_info = {"elevation": node_elevation,
                         "coord": node_coord,
                         "type": node_type}
            if node_type == "TANK":
                node_tank_idx = node_tank_names.index(node_id) + 1
                node_info["diameter"] = float(self.epanet_api.getNodeTankDiameter(node_tank_idx))

            nodes.append((node_id, node_info))

        links = []
        for link_id, link_type, link, diameter, length, roughness_coeff, bulk_coeff, wall_coeff, loss_coeff \
                in zip(links_id, links_type, links_data, links_diameter, links_length,
                       links_roughness_coeff, links_bulk_coeff, links_wall_coeff, links_loss_coeff):
            links.append((link_id, list(link),
                          {"type": link_type, "diameter": diameter, "length": length,
                           "roughness_coeff": roughness_coeff,
                           "bulk_coeff": bulk_coeff, "wall_coeff": wall_coeff,
                           "loss_coeff": loss_coeff}))

        pumps = {}
        for pump_id, pump_type in zip(pumps_id, pumps_type):
            link_idx = links_id.index(pump_id)
            link = links_data[link_idx]
            pumps[pump_id] = {"type": pump_type, "end_points": link}

        valves = {}
        for valve_id in valves_id:
            link_idx = links_id.index(valve_id)
            link = links_data[link_idx]
            valve_type = links_type[link_idx]
            valves[valve_id] = {"type": valve_type, "end_points": link}

        return NetworkTopology(f_inp=self.f_inp_in, nodes=nodes, links=links, pumps=pumps,
                               valves=valves, units=self.get_units_category())

    def plot_topology(self, export_to_file: str = None) -> None:
        """
        Plots the topology of the water distribution network.

        Parameters
        ----------
        export_to_file : `str`, optional
            Path to the file where the visualization will be stored.
            If None, visualization will be just shown but NOT be stored
            anywhere.

            The default is None.
        """
        from .scenario_visualizer import ScenarioVisualizer
        ScenarioVisualizer(self).show_plot(export_to_file)

    def randomize_demands(self) -> None:
        """
        Randomizes all demand patterns.
        """
        if self.__running_simulation is True:
            raise RuntimeError("Can not change general parameters when simulation is running.")

        self._adapt_to_network_changes()

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

    def get_pattern(self, pattern_id: str) -> np.ndarray:
        """
        Returns the EPANET pattern (i.e. all multiplier factors over time) given its ID.

        Parameters
        ----------
        pattern_id : `str`
            ID of the pattern.

        Returns
        -------
        `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            The pattern -- i.e. multiplier factors over time.
        """
        pattern_idx = self.epanet_api.getPatternIndex(pattern_id)
        pattern_length = self.epanet_api.getPatternLengths(pattern_idx)
        return np.array([self.epanet_api.getPatternValue(pattern_idx, t+1)
                         for t in range(pattern_length)])

    def add_pattern(self, pattern_id: str, pattern: np.ndarray) -> None:
        """
        Adds a pattern to the EPANET scenario.

        Parameters
        ----------
        pattern_id : `str`
            ID of the pattern.
        pattern : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Pattern of multipliers over time.
        """
        self._adapt_to_network_changes()

        if not isinstance(pattern_id, str):
            raise TypeError("'pattern_id' must be an instance of 'str' " +
                            f"but not of '{type(pattern_id)}'")
        if not isinstance(pattern, np.ndarray):
            raise TypeError("'pattern' must be an instance of 'numpy.ndarray' " +
                            f"but not of '{type(pattern)}'")
        if len(pattern.shape) > 1:
            raise ValueError(f"Inconsistent pattern shape '{pattern.shape}' " +
                             "detected. Expected a one dimensional array!")

        self.epanet_api.addPattern(pattern_id, pattern)

    def get_node_demand_pattern(self, node_id: str) -> np.ndarray:
        """
        Returns the values of the demand pattern of a given node --
        i.e. multiplier factors that are applied to the base demand.

        Parameters
        ----------
        node_id : `str`
            ID of the node.

        Returns
        -------
        `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            The demand pattern -- i.e. multiplier factors over time.
        """
        node_idx = self.epanet_api.getNodeIndex(node_id)
        demand_category = self.epanet_api.getNodeDemandCategoriesNumber()[node_idx]
        demand_pattern_id = self.epanet_api.getNodeDemandPatternNameID()[demand_category][node_idx - 1]
        return self.get_pattern(demand_pattern_id)

    def set_node_demand_pattern(self, node_id: str, base_demand: float, demand_pattern_id: str,
                                demand_pattern: np.ndarray = None) -> None:
        """
        Sets the demand pattern (incl. base demand) at a given node.

        Parameters
        ----------
        node_id : `str`
            ID of the node for which the demand pattern is set.
        base_demand : `float`
            Base demand.
        demand_pattern_id : `str`
            ID of the (new) demand pattern. Existing demand pattern will be overriden if it already exisits.
        demand_pattern : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_, optional
            Demand pattern over time. Final demand over time = base_demand * demand_pattern
            If None, the pattern demand_pattern_id is assumed to already exist.

            The default is None.
        """
        self._adapt_to_network_changes()

        if node_id not in self._sensor_config.nodes:
            raise ValueError(f"Unknown node '{node_id}'")
        if not isinstance(base_demand, float):
            raise TypeError("'base_demand' must be an instance of 'float' " +
                            f"but not if '{type(base_demand)}'")
        if not isinstance(demand_pattern_id, str):
            raise TypeError("'demand_pattern_id' must be an instance of 'str' " +
                            f"but not of '{type(demand_pattern_id)}'")
        if demand_pattern is not None:
            if not isinstance(demand_pattern, np.ndarray):
                raise TypeError("'demand_pattern' must be an instance of 'numpy.ndarray' " +
                                f"but not of '{type(demand_pattern)}'")
            if len(demand_pattern.shape) > 1:
                raise ValueError(f"Inconsistent demand pattern shape '{demand_pattern.shape}' " +
                                 "detected. Expected a one dimensional array!")

        node_idx = self.epanet_api.getNodeIndex(node_id)

        if demand_pattern_id not in self.epanet_api.getPatternNameID():
            if demand_pattern is None:
                raise ValueError("'demand_pattern' can not be None if " +
                                 "'demand_pattern_id' does not already exist.")
            self.epanet_api.addPattern(demand_pattern_id, demand_pattern)
        else:
            if demand_pattern is not None:
                pattern_idx = self.epanet_api.getPatternIndex(demand_pattern_id)
                self.epanet_api.setPattern(pattern_idx, demand_pattern)

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
        self._adapt_to_network_changes()

        if not isinstance(control, AdvancedControlModule):
            raise TypeError("'control' must be an instance of " +
                            "'epyt_flow.simulation.scada.AdvancedControlModule' not of " +
                            f"'{type(control)}'")

        self._controls.append(control)

    def add_leakage(self, leakage_event: Leakage) -> None:
        """
        Adds a leakage to the scenario simulation.

        Parameters
        ----------
        event : :class:`~epyt_flow.simulation.events.leakages.Leakage`
            Leakage.
        """
        self._adapt_to_network_changes()

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
        self._adapt_to_network_changes()

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
        if self.__running_simulation is True:
            raise RuntimeError("Can not add events when simulation is running.")

        self._adapt_to_network_changes()

        if not isinstance(event, SystemEvent):
            raise TypeError("'event' must be an instance of " +
                            f"'epyt_flow.simulation.events.SystemEvent' not of '{type(event)}'")

        event.init(self.epanet_api)

        self._system_events.append(event)

    def add_sensor_fault(self, sensor_fault_event: SensorFault) -> None:
        """
        Adds a sensor fault to the scenario simulation.

        Parameters
        ----------
        sensor_fault_event : :class:`~epyt_flow.simulation.events.sensor_faults.SensorFault`
            Sensor fault specifications.
        """
        if self.__running_simulation is True:
            raise RuntimeError("Can not add events when simulation is running.")

        self._adapt_to_network_changes()

        sensor_fault_event.validate(self._sensor_config)

        if not isinstance(sensor_fault_event, SensorFault):
            raise TypeError("'sensor_fault_event' must be an instance of " +
                            "'epyt_flow.simulation.events.SensorFault' not of " +
                            f"'{type(sensor_fault_event)}'")

        self._sensor_reading_events.append(sensor_fault_event)

    def add_sensor_reading_attack(self, sensor_reading_attack: SensorReadingAttack) -> None:
        """
        Adds a sensor reading attack to the scenario simulation.

        Parameters
        ----------
        sensor_reading_attack : :class:`~epyt_flow.simulation.events.sensor_reading_attack.SensorReadingAttack`
            Sensor fault specifications.
        """
        if self.__running_simulation is True:
            raise RuntimeError("Can not add events when simulation is running.")

        self._adapt_to_network_changes()

        sensor_reading_attack.validate(self._sensor_config)

        if not isinstance(sensor_reading_attack, SensorReadingAttack):
            raise TypeError("'sensor_reading_attack' must be an instance of " +
                            "'epyt_flow.simulation.events.SensorReadingAttack' not of " +
                            f"'{type(sensor_reading_attack)}'")

        self._sensor_reading_events.append(sensor_reading_attack)

    def add_sensor_reading_event(self, event: SensorReadingEvent) -> None:
        """
        Adds a sensor reading event to the scenario simulation.

        Parameters
        ----------
        event : :class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent`
            Sensor reading event.
        """
        if self.__running_simulation is True:
            raise RuntimeError("Can not add events when simulation is running.")

        self._adapt_to_network_changes()

        event.validate(self._sensor_config)

        if not isinstance(event, SensorReadingEvent):
            raise TypeError("'event' must be an instance of " +
                            "'epyt_flow.simulation.events.SensorReadingEvent' not of " +
                            f"'{type(event)}'")

        self._sensor_reading_events.append(event)

    def set_sensors(self, sensor_type: int, sensor_locations: Union[list[str], dict]) -> None:
        """
        Specifies all sensors of a given type (e.g. pressure sensor, flow sensor, etc.)

        Parameters
        ----------
        sensor_type : `int`
            Sensor type. Must be one of the following:
                - SENSOR_TYPE_NODE_PRESSURE          = 1
                - SENSOR_TYPE_NODE_QUALITY           = 2
                - SENSOR_TYPE_NODE_DEMAND            = 3
                - SENSOR_TYPE_LINK_FLOW              = 4
                - SENSOR_TYPE_LINK_QUALITY           = 5
                - SENSOR_TYPE_VALVE_STATE            = 6
                - SENSOR_TYPE_PUMP_STATE             = 7
                - SENSOR_TYPE_TANK_VOLUME            = 8
                - SENSOR_TYPE_BULK_SPECIES           = 9
                - SENSOR_TYPE_SURFACE_SPECIES        = 10
                - SENSOR_TYPE_PUMP_EFFICIENCY        = 12
                - SENSOR_TYPE_PUMP_ENERGYCONSUMPTION = 13
        sensor_locations : `list[str]` or `dict`
            Locations (IDs) of sensors either as a list or as a dict in the case of
            bulk and surface species.
        """
        self._adapt_to_network_changes()

        if sensor_type == SENSOR_TYPE_NODE_PRESSURE:
            self._sensor_config.pressure_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_LINK_FLOW:
            self._sensor_config.flow_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_NODE_DEMAND:
            self._sensor_config.demand_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_NODE_QUALITY:
            self._sensor_config.quality_node_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_LINK_QUALITY:
            self._sensor_config.quality_link_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_VALVE_STATE:
            self._sensor_config.valve_state_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_PUMP_STATE:
            self._sensor_config.pump_state_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_PUMP_EFFICIENCY:
            self._sensor_config.pump_efficiency_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_PUMP_ENERGYCONSUMPTION:
            self._sensor_config.pump_energyconsumption_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_TANK_VOLUME:
            self._sensor_config.tank_volume_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_NODE_BULK_SPECIES:
            self._sensor_config.bulk_species_node_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_LINK_BULK_SPECIES:
            self._sensor_config.bulk_species_link_sensors = sensor_locations
        elif sensor_type == SENSOR_TYPE_SURFACE_SPECIES:
            self._sensor_config.surface_species_sensors = sensor_locations
        else:
            raise ValueError(f"Unknown sensor type '{sensor_type}'")

        self._sensor_config.validate(self.epanet_api)

    def set_pressure_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the pressure sensors -- i.e. measuring pressure at some nodes in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_NODE_PRESSURE, sensor_locations)

    def place_pressure_sensors_everywhere(self, junctions_only: bool = False) -> None:
        """
        Places a pressure sensor at every node in the network.

        Parameters
        ----------
        junctions_only : `bool`, optional
            If True, pressure sensors are only placed at junctions but not at tanks and reservoirs.

            The default is False.
        """
        if junctions_only is True:
            self.set_pressure_sensors(self.epanet_api.getNodeJunctionNameID())
        else:
            self.set_pressure_sensors(self._sensor_config.nodes)

    def set_flow_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the flow sensors -- i.e. measuring flows at some links/pipes in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_LINK_FLOW, sensor_locations)

    def place_flow_sensors_everywhere(self) -> None:
        """
        Places a flow sensors at every link/pipe in the network.
        """
        self.set_flow_sensors(self._sensor_config.links)

    def set_demand_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the demand sensors -- i.e. measuring demands at some nodes in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_NODE_DEMAND, sensor_locations)

    def place_demand_sensors_everywhere(self) -> None:
        """
        Places a demand sensor at every node in the network.
        """
        self.set_demand_sensors(self._sensor_config.nodes)

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

    def place_node_quality_sensors_everywhere(self) -> None:
        """
        Places a water quality sensor at every node in the network.
        """
        self.set_node_quality_sensors(self._sensor_config.nodes)

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

    def place_link_quality_sensors_everywhere(self) -> None:
        """
        Places a water quality sensor at every link/pipe in the network.
        """
        self.set_link_quality_sensors(self._sensor_config.links)

    def set_valve_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the valve state sensors -- i.e. retrieving the state of some valves in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_VALVE_STATE, sensor_locations)

    def place_valve_sensors_everywhere(self) -> None:
        """
        Places a valve state sensor at every valve in the network.
        """
        if len(self._sensor_config.valves) == 0:
            warnings.warn("Network does not contain any valves", UserWarning)

        self.set_valve_sensors(self._sensor_config.valves)

    def set_pump_state_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the pump state sensors -- i.e. retrieving the state of some pumps in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_PUMP_STATE, sensor_locations)

    def place_pump_state_sensors_everywhere(self) -> None:
        """
        Places a pump state sensor at every pump in the network.
        """
        if len(self._sensor_config.pumps) == 0:
            warnings.warn("Network does not contain any pumps", UserWarning)

        self.set_pump_state_sensors(self._sensor_config.pumps)

    def set_pump_efficiency_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the pump efficiency sensors -- i.e. retrieving the efficiency of
        some pumps in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_PUMP_EFFICIENCY, sensor_locations)

    def place_pump_efficiency_sensors_everywhere(self) -> None:
        """
        Places a pump efficiency sensor at every pump in the network.
        """
        if len(self._sensor_config.pumps) == 0:
            warnings.warn("Network does not contain any pumps", UserWarning)

        self.set_pump_efficiency_sensors(self._sensor_config.pumps)

    def set_pump_energyconsumption_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the pump energy consumption sensors -- i.e. retrieving the energy consumption of
        some pumps in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_PUMP_ENERGYCONSUMPTION, sensor_locations)

    def place_pump_energyconsumption_sensors_everywhere(self) -> None:
        """
        Places a pump energy consumption sensor at every pump in the network.
        """
        if len(self._sensor_config.pumps) == 0:
            warnings.warn("Network does not contain any pumps", UserWarning)

        self.set_pump_energyconsumption_sensors(self._sensor_config.pumps)

    def set_pump_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the pump sensors -- i.e. retrieving the state, efficiency, and energy consumption
        of some pumps in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_PUMP_STATE, sensor_locations)
        self.set_sensors(SENSOR_TYPE_PUMP_EFFICIENCY, sensor_locations)
        self.set_sensors(SENSOR_TYPE_PUMP_ENERGYCONSUMPTION, sensor_locations)

    def place_pump_sensors_everywhere(self) -> None:
        """
        Palces pump sensors at every pump in the network -- i.e. retrieving the state, efficiency,
        and energy consumption of all pumps in the network.
        """
        if len(self._sensor_config.pumps) == 0:
            warnings.warn("Network does not contain any pumps", UserWarning)

        self.set_pump_sensors(self._sensor_config.pumps)

    def set_tank_sensors(self, sensor_locations: list[str]) -> None:
        """
        Sets the tank volume sensors -- i.e. measuring water volumes in some tanks in the network.

        Parameters
        ----------
        sensor_locations : `list[str]`
            Locations (IDs) of sensors.
        """
        self.set_sensors(SENSOR_TYPE_TANK_VOLUME, sensor_locations)

    def place_tank_sensors_everywhere(self) -> None:
        """
        Places a water tank volume sensor at every tank in the network.
        """
        if len(self._sensor_config.tanks) == 0:
            warnings.warn("Network does not contain any tanks", UserWarning)

        self.set_tank_sensors(self._sensor_config.tanks)

    def set_bulk_species_node_sensors(self, sensor_info: dict) -> None:
        """
        Sets the bulk species node sensors -- i.e. measuring bulk species concentrations
        at nodes in the network.

        Parameters
        ----------
        sensor_info : `dict`
            Bulk species sensors -- keys: bulk species IDs, values: node IDs.
        """
        self.set_sensors(SENSOR_TYPE_NODE_BULK_SPECIES, sensor_info)

    def place_bulk_species_node_sensors_everywhere(self, bulk_species: list[str] = None) -> None:
        """
        Places bulk species concentration sensors at every node in the network for
        every bulk species.

        Parameters
        ----------
        bulk_species : `list[str]`, optional
            List of bulk species IDs which we want to monitor at every node.
            If None, every bulk species will be monitored at every node.

            The default is None.
        """
        if bulk_species is None:
            self.set_bulk_species_node_sensors({species_id: self._sensor_config.nodes
                                                for species_id in
                                                    self._sensor_config.bulk_species})
        else:
            if any(species_id not in self._sensor_config.bulk_species
                   for species_id in bulk_species):
                raise ValueError("Invalid bulk species ID in 'bulk_species'")

            self.set_bulk_species_node_sensors({species_id: self._sensor_config.nodes
                                                for species_id in bulk_species})

    def set_bulk_species_link_sensors(self, sensor_info: dict) -> None:
        """
        Sets the bulk species link/pipe sensors -- i.e. measuring bulk species concentrations
        at links/pipes in the network.

        Parameters
        ----------
        sensor_info : `dict`
            Bulk species sensors -- keys: bulk species IDs, values: node IDs.
        """
        self.set_sensors(SENSOR_TYPE_LINK_BULK_SPECIES, sensor_info)

    def place_bulk_species_link_sensors_everywhere(self, bulk_species: list[str] = None) -> None:
        """
        Places bulk species concentration sensors at every link/pipe in the network
        for every bulk species.

        Parameters
        ----------
        bulk_species : `list[str]`, optional
            List of bulk species IDs which we want to monitor at every link/pipe.
            If None, every bulk species will be monitored at every link/pipe.

            The default is None.
        """
        if bulk_species is None:
            self.set_bulk_species_link_sensors({species_id: self._sensor_config.links
                                                for species_id in
                                                self._sensor_config.bulk_species})
        else:
            if any(species_id not in self._sensor_config.bulk_species
                   for species_id in bulk_species):
                raise ValueError("Invalid bulk species ID in 'bulk_species'")

            self.set_bulk_species_link_sensors({species_id: self._sensor_config.links
                                                for species_id in bulk_species})

    def set_surface_species_sensors(self, sensor_info: dict) -> None:
        """
        Sets the surface species sensors -- i.e. measuring surface species concentrations
        at nodes in the network.

        Parameters
        ----------
        sensor_info : `dict`
            Surface species sensors -- keys: surface species IDs, values: link/pipe IDs.
        """
        self.set_sensors(SENSOR_TYPE_SURFACE_SPECIES, sensor_info)

    def place_surface_species_sensors_everywhere(self, surface_species_id: list[str] = None
                                                 ) -> None:
        """
        Places surface species concentration sensors at every link/pipe in the network
        for every surface species.

        Parameters
        ----------
        surface_species_id : `list[str]`, optional
            List of surface species IDs which we want to monitor at every link/pipe.
            If None, every surface species will be monitored at every link/pipe.

            The default is None.
        """
        if surface_species_id is None:
            self.set_bulk_species_node_sensors({species_id: self._sensor_config.links
                                                for species_id in
                                                self._sensor_config.surface_species})
        else:
            if any(species_id not in self._sensor_config.surface_species
                   for species_id in surface_species_id):
                raise ValueError("Invalid surface species ID in 'surface_species_id'")

            self.set_bulk_species_node_sensors({species_id: self._sensor_config.links
                                                for species_id in surface_species_id})

    def place_sensors_everywhere(self) -> None:
        """
        Places sensors everywhere -- i.e. every possible quantity is monitored
        at every position in the network.
        """
        self._sensor_config.place_sensors_everywhere()

    def _prepare_simulation(self) -> None:
        self._adapt_to_network_changes()

        if self._model_uncertainty is not None:
            self._model_uncertainty.apply(self.epanet_api)

        for event in self._system_events:
            event.reset()

        if self._controls is not None:
            for c in self._controls:
                c.init(self.epanet_api)

    def run_advanced_quality_simulation(self, hyd_file_in: str, verbose: bool = False,
                                        frozen_sensor_config: bool = False) -> ScadaData:
        """
        Runs an advanced quality analysis using EPANET-MSX.

        Parameters
        ----------
        hyd_file_in : `str`
            Path to an EPANET .hyd file for storing the simulated hydraulics --
            the quality analysis is computed using those hydraulics.
        verbose : `bool`, optional
            If True, method will be verbose (e.g. showing a progress bar).

            The default is False.
        frozen_sensor_config : `bool`, optional
            If True, the sensor config can not be changed and only the required sensor nodes/links
            will be stored -- this usually leads to a significant reduction in memory consumption.

            The default is False.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Quality simulation results as SCADA data.
        """
        if self.__running_simulation is True:
            raise RuntimeError("A simulation is already running.")

        if self.__f_msx_in is None:
            raise ValueError("No .msx file specified")

        result = None

        gen = self.run_advanced_quality_simulation_as_generator
        for scada_data in gen(hyd_file_in=hyd_file_in,
                              verbose=verbose,
                              return_as_dict=True,
                              frozen_sensor_config=frozen_sensor_config):
            if result is None:
                result = {}
                for data_type, data in scada_data.items():
                    result[data_type] = [data]
            else:
                for data_type, data in scada_data.items():
                    result[data_type].append(data)

        # Build ScadaData instance
        for data_type in result:
            if not any(d is None for d in result[data_type]):
                result[data_type] = np.concatenate(result[data_type], axis=0)
            else:
                result[data_type] = None

        return ScadaData(**result,
                         sensor_config=self._sensor_config,
                         sensor_reading_events=self._sensor_reading_events,
                         sensor_noise=self._sensor_noise,
                         frozen_sensor_config=frozen_sensor_config)

    def run_advanced_quality_simulation_as_generator(self, hyd_file_in: str, verbose: bool = False,
                                                     support_abort: bool = False,
                                                     return_as_dict: bool = False,
                                                     frozen_sensor_config: bool = False
                                                     ) -> Generator[Union[ScadaData, dict], bool, None]:
        """
        Runs an advanced quality analysis using EPANET-MSX.

        Parameters
        ----------
        support_abort : `bool`, optional
        hyd_file_in : `str`
            Path to an EPANET .hyd file for storing the simulated hydraulics --
            the quality analysis is computed using those hydraulics.
        verbose : `bool`
            If True, method will be verbose (e.g. showing a progress bar).
        return_as_dict : `bool`, optional
            If True, simulation results/states are returned as a dictionary instead of a
            :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.

            The default is False.
        frozen_sensor_config : `bool`, optional
            If True, the sensor config can not be changed and only the required sensor nodes/links
            will be stored -- this usually leads to a significant reduction in memory consumption.

            The default is False.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Generator containing the current EPANET-MSX simulation results as SCADA data
            (i.e. species concentrations).
        """
        if self.__running_simulation is True:
            raise RuntimeError("A simulation is already running.")

        if self.__f_msx_in is None:
            raise ValueError("No .msx file specified")

        # Load pre-computed hydraulics
        self.epanet_api.useMSXHydraulicFile(hyd_file_in)

        # Initialize simulation
        n_nodes = self.epanet_api.getNodeCount()
        n_links = self.epanet_api.getLinkCount()

        reporting_time_start = self.epanet_api.getTimeReportingStart()
        reporting_time_step = self.epanet_api.getTimeReportingStep()
        hyd_time_step = self.epanet_api.getTimeHydraulicStep()

        self.epanet_api.initializeMSXQualityAnalysis(ToolkitConstants.EN_NOSAVE)

        self.__running_simulation = True

        bulk_species_idx = self.epanet_api.getMSXSpeciesIndex(self._sensor_config.bulk_species)
        surface_species_idx = self.epanet_api.getMSXSpeciesIndex(
            self._sensor_config.surface_species)

        if verbose is True:
            print("Running EPANET-MSX ...")
            n_iterations = math.ceil(self.epanet_api.getTimeSimulationDuration() /
                                     hyd_time_step)
            progress_bar = iter(tqdm(range(n_iterations + 1), ascii=True, desc="Time steps"))

        def __get_concentrations(init_qual=False):
            if init_qual is True:
                msx_get_cur_value = self.epanet_api.msx.MSXgetinitqual
            else:
                msx_get_cur_value = self.epanet_api.getMSXSpeciesConcentration

            # Bulk species
            bulk_species_node_concentrations = []
            bulk_species_link_concentrations = []
            for species_idx in bulk_species_idx:
                cur_species_concentrations = []
                for node_idx in range(1, n_nodes + 1):
                    concen = msx_get_cur_value(0, node_idx, species_idx)
                    cur_species_concentrations.append(concen)
                bulk_species_node_concentrations.append(cur_species_concentrations)

                cur_species_concentrations = []
                for link_idx in range(1, n_links + 1):
                    concen = msx_get_cur_value(1, link_idx, species_idx)
                    cur_species_concentrations.append(concen)
                bulk_species_link_concentrations.append(cur_species_concentrations)

            if len(bulk_species_node_concentrations) == 0:
                bulk_species_node_concentrations = None
            else:
                bulk_species_node_concentrations = np.array(bulk_species_node_concentrations). \
                    reshape((1, len(bulk_species_idx), n_nodes))

            if len(bulk_species_link_concentrations) == 0:
                bulk_species_link_concentrations = None
            else:
                bulk_species_link_concentrations = np.array(bulk_species_link_concentrations). \
                    reshape((1, len(bulk_species_idx), n_links))

            # Surface species
            surface_species_concentrations = []
            for species_idx in surface_species_idx:
                cur_species_concentrations = []

                for link_idx in range(1, n_links + 1):
                    concen = msx_get_cur_value(1, link_idx, species_idx)
                    cur_species_concentrations.append(concen)

                surface_species_concentrations.append(cur_species_concentrations)

            if len(surface_species_concentrations) == 0:
                surface_species_concentrations = None
            else:
                surface_species_concentrations = np.array(surface_species_concentrations). \
                    reshape((1, len(surface_species_idx), n_links))

            return bulk_species_node_concentrations, bulk_species_link_concentrations, \
                surface_species_concentrations

        # Initial concentrations:
        bulk_species_node_concentrations, bulk_species_link_concentrations, \
            surface_species_concentrations = __get_concentrations(init_qual=True)

        if verbose is True:
            try:
                next(progress_bar)
            except StopIteration:
                pass

        if reporting_time_start == 0:
            if return_as_dict is True:
                data = {"bulk_species_node_concentration_raw": bulk_species_node_concentrations,
                        "bulk_species_link_concentration_raw": bulk_species_link_concentrations,
                        "surface_species_concentration_raw": surface_species_concentrations,
                        "sensor_readings_time": np.array([0])}
            else:
                data = ScadaData(sensor_config=self._sensor_config,
                                 bulk_species_node_concentration_raw=bulk_species_node_concentrations,
                                 bulk_species_link_concentration_raw=bulk_species_link_concentrations,
                                 surface_species_concentration_raw=surface_species_concentrations,
                                 sensor_readings_time=np.array([0]),
                                 sensor_reading_events=self._sensor_reading_events,
                                 sensor_noise=self._sensor_noise,
                                 frozen_sensor_config=frozen_sensor_config)

            if support_abort is True:  # Can the simulation be aborted? If so, handle it.
                abort = yield
                if abort is True:
                    return None

            yield data

        # Run step-by-step simulation
        tleft = 1
        total_time = 0
        while tleft > 0:
            # Compute current time step
            total_time, tleft = self.epanet_api.stepMSXQualityAnalysisTimeLeft()

            # Fetch data at regular time intervals
            if total_time % hyd_time_step == 0:
                if verbose is True:
                    try:
                        next(progress_bar)
                    except StopIteration:
                        pass

                bulk_species_node_concentrations, bulk_species_link_concentrations, \
                    surface_species_concentrations = __get_concentrations()

                # Report results in a regular time interval only!
                if total_time % reporting_time_step == 0 and total_time >= reporting_time_start:
                    if return_as_dict is True:
                        data = {"bulk_species_node_concentration_raw":
                                    bulk_species_node_concentrations,
                                "bulk_species_link_concentration_raw":
                                    bulk_species_link_concentrations,
                                "surface_species_concentration_raw": surface_species_concentrations,
                                "sensor_readings_time": np.array([total_time])}
                    else:
                        data = ScadaData(sensor_config=self._sensor_config,
                                         bulk_species_node_concentration_raw=
                                            bulk_species_node_concentrations,
                                         bulk_species_link_concentration_raw=
                                            bulk_species_link_concentrations,
                                         surface_species_concentration_raw=
                                            surface_species_concentrations,
                                         sensor_readings_time=np.array([total_time]),
                                         sensor_reading_events=self._sensor_reading_events,
                                         sensor_noise=self._sensor_noise,
                                         frozen_sensor_config=frozen_sensor_config)

                    if support_abort is True:  # Can the simulation be aborted? If so, handle it.
                        abort = yield
                        if abort is not False:
                            break

                    yield data

        self.__running_simulation = False

    def run_basic_quality_simulation(self, hyd_file_in: str, verbose: bool = False,
                                     frozen_sensor_config: bool = False) -> ScadaData:
        """
        Runs a basic quality analysis using EPANET.

        Parameters
        ----------
        hyd_file_in : `str`
            Path to an EPANET .hyd file for storing the simulated hydraulics --
            the quality analysis is computed using those hydraulics.
        verbose : `bool`, optional
            If True, method will be verbose (e.g. showing a progress bar).

            The default is False.
        frozen_sensor_config : `bool`, optional
            If True, the sensor config can not be changed and only the required sensor nodes/links
            will be stored -- this usually leads to a significant reduction in memory consumption.

            The default is False.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Quality simulation results as SCADA data.
        """
        if self.__running_simulation is True:
            raise RuntimeError("A simulation is already running.")

        result = None

        # Run simulation step-by-step
        gen = self.run_basic_quality_simulation_as_generator
        for scada_data in gen(hyd_file_in=hyd_file_in,
                              verbose=verbose,
                              return_as_dict=True,
                              frozen_sensor_config=frozen_sensor_config):
            if result is None:
                result = {}
                for data_type, data in scada_data.items():
                    result[data_type] = [data]
            else:
                for data_type, data in scada_data.items():
                    result[data_type].append(data)

        # Build ScadaData instance
        for data_type in result:
            result[data_type] = np.concatenate(result[data_type], axis=0)

        return ScadaData(**result,
                         sensor_config=self._sensor_config,
                         sensor_reading_events=self._sensor_reading_events,
                         sensor_noise=self._sensor_noise,
                         frozen_sensor_config=frozen_sensor_config)

    def run_basic_quality_simulation_as_generator(self, hyd_file_in: str, verbose: bool = False,
                                                  support_abort: bool = False,
                                                  return_as_dict: bool = False,
                                                  frozen_sensor_config: bool = False,
                                                  ) -> Generator[Union[ScadaData, dict], bool, None]:
        """
        Runs a basic quality analysis using EPANET.

        Parameters
        ----------
        support_abort : `bool`, optional
        hyd_file_in : `str`
            Path to an EPANET .hyd file for storing the simulated hydraulics --
            the quality analysis is computed using those hydraulics.
        verbose : `bool`, optional
            If True, method will be verbose (e.g. showing a progress bar).

            The default is False.
        return_as_dict : `bool`, optional
            If True, simulation results/states are returned as a dictionary instead of a
            :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.

            The default is False.
        frozen_sensor_config : `bool`, optional
            If True, the sensor config can not be changed and only the required sensor nodes/links
            will be stored -- this usually leads to a significant reduction in memory consumption.

            The default is False.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Generator with the current simulation results/states as SCADA data.
        """
        if self.__running_simulation is True:
            raise RuntimeError("A simulation is already running.")

        requested_time_step = self.epanet_api.getTimeHydraulicStep()
        reporting_time_start = self.epanet_api.getTimeReportingStart()
        reporting_time_step = self.epanet_api.getTimeReportingStep()

        self.epanet_api.useHydraulicFile(hyd_file_in)

        self.epanet_api.openQualityAnalysis()
        self.epanet_api.initializeQualityAnalysis(ToolkitConstants.EN_NOSAVE)

        if verbose is True:
            print("Running basic quality analysis using EPANET ...")
            n_iterations = math.ceil(self.epanet_api.getTimeSimulationDuration() /
                                     requested_time_step)
            progress_bar = iter(tqdm(range(n_iterations + 1), ascii=True, desc="Time steps"))

        # Run simulation step by step
        total_time = 0
        tstep = 1
        first_itr = True
        while tstep > 0:
            if first_itr is True:  # Fix current time in the first iteration
                tstep = 0
                first_itr = False

            if verbose is True:
                if (total_time + tstep) % requested_time_step == 0:
                    try:
                        next(progress_bar)
                    except StopIteration:
                        pass

            # Compute current time step
            t = self.epanet_api.runQualityAnalysis()
            total_time = t

            # Fetch data
            quality_node_data = self.epanet_api.getNodeActualQuality().reshape(1, -1)
            quality_link_data = self.epanet_api.getLinkActualQuality().reshape(1, -1)

            # Yield results in a regular time interval only!
            if total_time % reporting_time_step == 0 and total_time >= reporting_time_start:
                if return_as_dict is True:
                    data = {"node_quality_data_raw": quality_node_data,
                            "link_quality_data_raw": quality_link_data,
                            "sensor_readings_time": np.array([total_time])}
                else:
                    data = ScadaData(sensor_config=self._sensor_config,
                                     node_quality_data_raw=quality_node_data,
                                     link_quality_data_raw=quality_link_data,
                                     sensor_readings_time=np.array([total_time]),
                                     sensor_reading_events=self._sensor_reading_events,
                                     sensor_noise=self._sensor_noise,
                                     frozen_sensor_config=frozen_sensor_config)

                if support_abort is True:  # Can the simulation be aborted? If so, handle it.
                    abort = yield
                    if abort is True:
                        break

                yield data

            # Next
            tstep = self.epanet_api.nextQualityAnalysisStep()

        self.epanet_api.closeHydraulicAnalysis()

    def run_hydraulic_simulation(self, hyd_export: str = None, verbose: bool = False,
                                 frozen_sensor_config: bool = False) -> ScadaData:
        """
        Runs the hydraulic simulation of this scenario (incl. basic quality if set).

        Note that this function does not call EPANET-MSX even if an .msx file was provided.

        Parameters
        ----------
        hyd_export : `str`, optional
            Path to an EPANET .hyd file for storing the simulated hydraulics -- these hydraulics
            can be used later for an advanced quality analysis using EPANET-MSX.

            If None, the simulated hydraulics will NOT be exported to an EPANET .hyd file.

            The default is None.
        verbose : `bool`, optional
            If True, method will be verbose (e.g. showing a progress bar).

            The default is False.
        frozen_sensor_config : `bool`, optional
            If True, the sensor config can not be changed and only the required sensor nodes/links
            will be stored -- this usually leads to a significant reduction in memory consumption.

            The default is False.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Simulation results as SCADA data (i.e. sensor readings).
        """
        if self.__running_simulation is True:
            raise RuntimeError("A simulation is already running.")

        self._adapt_to_network_changes()

        result = None

        # Run hydraulic simulation step-by-step
        gen = self.run_hydraulic_simulation_as_generator
        for scada_data in gen(hyd_export=hyd_export,
                              verbose=verbose,
                              return_as_dict=True,
                              frozen_sensor_config=frozen_sensor_config):
            if result is None:
                result = {}
                for data_type, data in scada_data.items():
                    result[data_type] = [data]
            else:
                for data_type, data in scada_data.items():
                    result[data_type].append(data)

        for data_type in result:
            result[data_type] = np.concatenate(result[data_type], axis=0)

        result = ScadaData(**result,
                           sensor_config=self._sensor_config,
                           sensor_reading_events=self._sensor_reading_events,
                           sensor_noise=self._sensor_noise,
                           frozen_sensor_config=frozen_sensor_config)

        return result

    def run_hydraulic_simulation_as_generator(self, hyd_export: str = None, verbose: bool = False,
                                              support_abort: bool = False,
                                              return_as_dict: bool = False,
                                              frozen_sensor_config: bool = False,
                                              ) -> Generator[Union[ScadaData, dict], bool, None]:
        """
        Runs the hydraulic simulation of this scenario (incl. basic quality if set) and
        provides the results as a generator.

        Note that this function does not run EPANET-MSX, even if an .msx file was provided.

        Parameters
        ----------
        hyd_export : `str`, optional
            Path to an EPANET .hyd file for storing the simulated hydraulics -- these hydraulics
            can be used later for an advanced quality analysis using EPANET-MSX.

            If None, the simulated hydraulics will NOT be exported to an EPANET .hyd file.

            The default is None.
        verbose : `bool`, optional
            If True, method will be verbose (e.g. showing a progress bar).

            The default is False.
        support_abort : `bool`, optional
            If True, the simulation can be aborted after every time step -- i.e. the generator
            takes a boolean as an input (send) to indicate whether the simulation
            is to be aborted or not.

            The default is False.
        return_as_dict : `bool`, optional
            If True, simulation results/states are returned as a dictionary instead of a
            :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance.

            The default is False.
        frozen_sensor_config : `bool`, optional
            If True, the sensor config can not be changed and only the required sensor nodes/links
            will be stored -- this usually leads to a significant reduction in memory consumption.

            The default is False.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Generator with the current simulation results/states as SCADA data
            (i.e. sensor readings).
        """
        if self.__running_simulation is True:
            raise RuntimeError("A simulation is already running.")

        self._adapt_to_network_changes()

        self._prepare_simulation()

        self.__running_simulation = True

        self.epanet_api.openHydraulicAnalysis()
        self.epanet_api.openQualityAnalysis()
        self.epanet_api.initializeHydraulicAnalysis(ToolkitConstants.EN_SAVE)
        self.epanet_api.initializeQualityAnalysis(ToolkitConstants.EN_SAVE)

        requested_time_step = self.epanet_api.getTimeHydraulicStep()
        reporting_time_start = self.epanet_api.getTimeReportingStart()
        reporting_time_step = self.epanet_api.getTimeReportingStep()

        if verbose is True:
            print("Running EPANET ...")
            n_iterations = math.ceil(self.epanet_api.getTimeSimulationDuration() /
                                     requested_time_step)
            progress_bar = iter(tqdm(range(n_iterations + 1), ascii=True, desc="Time steps"))

        try:
            # Run simulation step by step
            total_time = 0
            tstep = 1
            first_itr = True
            while tstep > 0:
                if first_itr is True:  # Fix current time in the first iteration
                    tstep = 0
                    first_itr = False

                if verbose is True:
                    if (total_time + tstep) % requested_time_step == 0:
                        try:
                            next(progress_bar)
                        except StopIteration:
                            pass

                # Apply system events in a regular time interval only!
                if (total_time + tstep) % requested_time_step == 0:
                    for event in self._system_events:
                        event.step(total_time + tstep)

                # Compute current time step
                t = self.epanet_api.runHydraulicAnalysis()
                self.epanet_api.runQualityAnalysis()
                total_time = t

                # Fetch data
                pressure_data = self.epanet_api.getNodePressure().reshape(1, -1)
                flow_data = self.epanet_api.getLinkFlows().reshape(1, -1)
                demand_data = self.epanet_api.getNodeActualDemand().reshape(1, -1)
                quality_node_data = self.epanet_api.getNodeActualQuality().reshape(1, -1)
                quality_link_data = self.epanet_api.getLinkActualQuality().reshape(1, -1)
                pumps_state_data = self.epanet_api.getLinkPumpState().reshape(1, -1)
                tanks_volume_data = self.epanet_api.getNodeTankVolume().reshape(1, -1)

                pump_idx = self.epanet_api.getLinkPumpIndex()
                pumps_energy_usage_data = self.epanet_api.getLinkEnergy(pump_idx).reshape(1, -1)
                pumps_efficiency_data = self.epanet_api.getLinkPumpEfficiency().reshape(1, -1)

                link_valve_idx = self.epanet_api.getLinkValveIndex()
                valves_state_data = self.epanet_api.getLinkStatus(link_valve_idx).reshape(1, -1)

                scada_data = ScadaData(sensor_config=self._sensor_config,
                                       pressure_data_raw=pressure_data,
                                       flow_data_raw=flow_data,
                                       demand_data_raw=demand_data,
                                       node_quality_data_raw=quality_node_data,
                                       link_quality_data_raw=quality_link_data,
                                       pumps_state_data_raw=pumps_state_data,
                                       valves_state_data_raw=valves_state_data,
                                       tanks_volume_data_raw=tanks_volume_data,
                                       pumps_energy_usage_data_raw=pumps_energy_usage_data,
                                       pumps_efficiency_data_raw=pumps_efficiency_data,
                                       sensor_readings_time=np.array([total_time]),
                                       sensor_reading_events=self._sensor_reading_events,
                                       sensor_noise=self._sensor_noise,
                                       frozen_sensor_config=frozen_sensor_config)

                # Yield results in a regular time interval only!
                if total_time % reporting_time_step == 0 and total_time >= reporting_time_start:
                    if return_as_dict is True:
                        data = {"pressure_data_raw": pressure_data,
                                "flow_data_raw": flow_data,
                                "demand_data_raw": demand_data,
                                "node_quality_data_raw": quality_node_data,
                                "link_quality_data_raw": quality_link_data,
                                "pumps_state_data_raw": pumps_state_data,
                                "valves_state_data_raw": valves_state_data,
                                "tanks_volume_data_raw": tanks_volume_data,
                                "pumps_energy_usage_data_raw": pumps_energy_usage_data,
                                "pumps_efficiency_data_raw": pumps_efficiency_data,
                                "sensor_readings_time": np.array([total_time])}
                    else:
                        data = scada_data

                    if support_abort is True:  # Can the simulation be aborted? If so, handle it.
                        abort = yield
                        if abort is True:
                            break

                    yield data

                # Apply control modules
                for control in self._controls:
                    control.step(scada_data)

                # Next
                tstep = self.epanet_api.nextHydraulicAnalysisStep()
                self.epanet_api.nextQualityAnalysisStep()

            self.epanet_api.closeQualityAnalysis()
            self.epanet_api.closeHydraulicAnalysis()

            self.__running_simulation = False

            if hyd_export is not None:
                self.epanet_api.saveHydraulicFile(hyd_export)
        except Exception as ex:
            self.__running_simulation = False
            raise ex

    def run_simulation_as_generator(self, hyd_export: str = None, verbose: bool = False,
                                    support_abort: bool = False,
                                    return_as_dict: bool = False,
                                    frozen_sensor_config: bool = False,
                                    ) -> Generator[Union[ScadaData, dict], bool, None]:
        warnings.warn("'run_simulation_as_generator' is deprecated and will be removed in " +
                      "future releases -- use 'run_hydraulic_simulation_as_generator' instead")
        return self.run_hydraulic_simulation_as_generator(hyd_export, verbose, support_abort,
                                                          return_as_dict, frozen_sensor_config)

    def run_simulation(self, hyd_export: str = None, verbose: bool = False,
                       frozen_sensor_config: bool = False) -> ScadaData:
        """
        Runs the simulation of this scenario.

        Parameters
        ----------
        hyd_export : `str`, optional
            Path to an EPANET .hyd file for storing the simulated hydraulics -- these hydraulics
            can be used later for an advanced quality analysis using EPANET-MSX.

            If None, the simulated hydraulics will NOT be exported to an EPANET .hyd file.

            The default is None.
        verbose : `bool`, optional
            If True, method will be verbose (e.g. showing a progress bar).

            The default is False.
        frozen_sensor_config : `bool`, optional
            If True, the sensor config can not be changed and only the required sensor nodes/links
            will be stored -- this usually leads to a significant reduction in memory consumption.

            The default is False.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Simulation results as SCADA data (i.e. sensor readings).
        """
        if self.__running_simulation is True:
            raise RuntimeError("A simulation is already running.")

        self._adapt_to_network_changes()

        result = None

        hyd_export_old = hyd_export
        if self.__f_msx_in is not None:
            hyd_export = os.path.join(get_temp_folder(), f"epytflow_MSX_{uuid.uuid4()}.hyd")

        # Run hydraulic simulation step-by-step
        result = self.run_hydraulic_simulation(hyd_export=hyd_export, verbose=verbose,
                                               frozen_sensor_config=frozen_sensor_config)

        # If necessary, run advanced quality simulation utilizing the computed hydraulics
        if self.f_msx_in is not None:
            gen = self.run_advanced_quality_simulation
            result_msx = gen(hyd_file_in=hyd_export,
                             verbose=verbose,
                             frozen_sensor_config=frozen_sensor_config)
            result.join(result_msx)

            if hyd_export_old is not None:
                shutil.copyfile(hyd_export, hyd_export_old)

            try:
                # temp solution
                os.remove(hyd_export)
            except:
                warnings.warn(f"Failed to remove temporary file '{hyd_export}'")

        return result

    def set_model_uncertainty(self, model_uncertainty: ModelUncertainty) -> None:
        """
        Specifies the model uncertainties.

        Parameters
        ----------
        model_uncertainty : :class:`~epyt_flow.uncertainty.model_uncertainty.ModelUncertainty`
            Model uncertainty specifications.
        """
        if self.__running_simulation is True:
            raise RuntimeError("Can not set uncertainties when simulation is running.")

        self._adapt_to_network_changes()

        if not isinstance(model_uncertainty, ModelUncertainty):
            raise TypeError("'model_uncertainty' must be an instance of " +
                            "'epyt_flow.uncertainty.ModelUncertainty' but not of " +
                            f"'{type(model_uncertainty)}'")

        self._model_uncertainty = model_uncertainty

    def set_sensor_noise(self, sensor_noise: SensorNoise) -> None:
        """
        Specifies the sensor noise -- i.e. uncertainties of sensor readings.

        Parameters
        ----------
        sensor_noise : :class:`~epyt_flow.uncertainties.sensor_noise.SensorNoise`
            Sensor noise specification.
        """
        if self.__running_simulation is True:
            raise RuntimeError("Can not set sensor noise when simulation is running.")

        self._adapt_to_network_changes()

        if not isinstance(sensor_noise, SensorNoise):
            raise TypeError("'sensor_noise' must be an instance of " +
                            "'epyt_flow.uncertainties.SensorNoise' but not of " +
                            f"'{type(sensor_noise)}'")

        self._sensor_noise = sensor_noise

    def set_general_parameters(self, demand_model: dict = None, simulation_duration: int = None,
                               hydraulic_time_step: int = None, quality_time_step: int = None,
                               reporting_time_step: int = None, reporting_time_start: int = None,
                               flow_units_id: int = None, quality_model: dict = None) -> None:
        """
        Sets some general parameters.

        Note that all these parameters can be stated in the .inp file as well.

        You only have to specify the parameters that are to be changed -- all others
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
        flow_units_id : `int`, optional
            Specifies the flow units -- i.e. all flows will be reported in these units.
            If None, the units from the .inp file will be used.

            Must be one of the following EPANET toolkit constants:

                - EN_CFS  = 0  (cubic foot/sec)
                - EN_GPM  = 1  (gal/min)
                - EN_MGD  = 2  (Million gal/day)
                - EN_IMGD = 3  (Imperial MGD)
                - EN_AFD  = 4  (ac-foot/day)
                - EN_LPS  = 5  (liter/sec)
                - EN_LPM  = 6  (liter/min)
                - EN_MLD  = 7  (Megaliter/day)
                - EN_CMH  = 8  (cubic meter/hr)
                - EN_CMD  = 9  (cubic meter/day)

            The default is None.
        quality_model : `dict`, optional
            Specifies the quality model -- the dictionary must contain,
            "type", "chemical_name", "chemical_units", and "trace_node_id", of the
            requested quality model.

            The default is None.
        """
        if self.__running_simulation is True:
            raise RuntimeError("Can not change general parameters when simulation is running.")

        self._adapt_to_network_changes()

        if flow_units_id is not None:
            if flow_units_id == ToolkitConstants.EN_CFS:
                self.epanet_api.setFlowUnitsCFS()
            elif flow_units_id == ToolkitConstants.EN_GPM:
                self.epanet_api.setFlowUnitsGPM()
            elif flow_units_id == ToolkitConstants.EN_MGD:
                self.epanet_api.setFlowUnitsMGD()
            elif flow_units_id == ToolkitConstants.EN_IMGD:
                self.epanet_api.setFlowUnitsIMGD()
            elif flow_units_id == ToolkitConstants.EN_AFD:
                self.epanet_api.setFlowUnitsAFD()
            elif flow_units_id == ToolkitConstants.EN_LPS:
                self.epanet_api.setFlowUnitsLPS()
            elif flow_units_id == ToolkitConstants.EN_LPM:
                self.epanet_api.setFlowUnitsLPM()
            elif flow_units_id == ToolkitConstants.EN_MLD:
                self.epanet_api.setFlowUnitsMLD()
            elif flow_units_id == ToolkitConstants.EN_CMH:
                self.epanet_api.setFlowUnitsCMH()
            elif flow_units_id == ToolkitConstants.EN_CMD:
                self.epanet_api.setFlowUnitsCMD()
            else:
                raise ValueError(f"Unknown flow units '{flow_units_id}'")

        if demand_model is not None:
            self.epanet_api.setDemandModel(demand_model["type"], demand_model["pressure_min"],
                                           demand_model["pressure_required"],
                                           demand_model["pressure_exponent"])

        if simulation_duration is not None:
            if not isinstance(simulation_duration, int) or simulation_duration <= 0:
                raise ValueError("'simulation_duration' must be a positive integer specifying " +
                                 "the number of seconds to simulate")
            self.epanet_api.setTimeSimulationDuration(simulation_duration)

        if hydraulic_time_step is not None:
            if not isinstance(hydraulic_time_step, int) or hydraulic_time_step <= 0:
                raise ValueError("'hydraulic_time_step' must be a positive integer specifying " +
                                 "the time steps of the hydraulic simulation")
            if len(self._system_events) != 0:
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

        if quality_model is not None:
            if quality_model["type"] == "NONE":
                self.epanet_api.setQualityType("none")
            elif quality_model["type"] == "AGE":
                self.epanet_api.setQualityType("age")
            elif quality_model["type"] == "CHEM":
                self.epanet_api.setQualityType("chem", quality_model["chemical_name"],
                                               qualityunit_to_str(quality_model["units"]))
            elif quality_model["type"] == "TRACE":
                self.epanet_api.setQualityType("trace", quality_model["trace_node_id"])
            else:
                raise ValueError(f"Unknown quality type: {quality_model['type']}")

    def get_events_active_time_points(self) -> list[int]:
        """
        Gets a list of time points (i.e. seconds since simulation start) at which
        at least one event (system or sensor readinge event) is active.

        Returns
        -------
        `list[int]`
            List of time points at which at least one event is active.
        """
        events_times = []

        hyd_time_step = self.epanet_api.getTimeHydraulicStep()

        def __process_event(event) -> None:
            cur_time = event.start_time
            while cur_time < event.end_time:
                events_times.append(cur_time)
                cur_time += hyd_time_step

        for event in self._sensor_reading_events:
            __process_event(event)

        for event in self._system_events:
            __process_event(event)

        return list(set(events_times))

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
        if self.__running_simulation is True:
            raise RuntimeError("Can not change general parameters when simulation is running.")

        self._adapt_to_network_changes()

        self.__warn_if_quality_set()
        self.set_general_parameters(quality_model={"type": "AGE"})

    def enable_chemical_analysis(self, chemical_name: str = "Chlorine",
                                 chemical_units: int = MASS_UNIT_MG) -> None:
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

            Must be one of the following constants:

                - MASS_UNIT_MG = 4  (mg/L)
                - MASS_UNIT_UG = 5  (ug/L)

            The default is MASS_UNIT_MG.
        """
        if self.__running_simulation is True:
            raise RuntimeError("Can not change general parameters when simulation is running.")

        self._adapt_to_network_changes()

        self.__warn_if_quality_set()
        self.set_general_parameters(quality_model={"type": "CHEM", "chemical_name": chemical_name,
                                                   "units": chemical_units})

    def add_quality_source(self, node_id: str, source_type: int, pattern: np.ndarray = None,
                           pattern_id: str = None, source_strength: int = 1.) -> None:
        """
        Adds a new external water quality source at a particular node.

        Parameters
        ----------
        node_id : `str`
            ID of the node at which this external water quality source is placed.
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
        pattern : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_, optional
            1d source pattern multipiers over time -- i.e. quality-source = source_strength * pattern.

            If None, the pattern pattern_id is assume to already exist.

            The default is None.
        pattern_id : `str`, optional
            ID of the source pattern.

            If None, a pattern_id will be generated automatically -- be aware that this
            could conflict with existing pattern IDs (in this case, an exception is raised).

            The default is None.
        source_strength : `int`, optional
            Quality source strength -- i.e. quality-source = source_strength * pattern.

            The default is 1.
        """
        if self.__running_simulation is True:
            raise RuntimeError("Can not change general parameters when simulation is running.")

        self._adapt_to_network_changes()

        if self.epanet_api.getQualityInfo().QualityCode != ToolkitConstants.EN_CHEM:
            raise RuntimeError("Chemical analysis is not enabled -- " +
                               "call 'enable_chemical_analysis()' before calling this function.")
        if node_id not in self._sensor_config.nodes:
            raise ValueError(f"Unknown node '{node_id}'")
        if not isinstance(source_type, int) or not 0 <= source_type <= 3:
            raise ValueError("Invalid type of water quality source")
        if pattern is not None:
            if not isinstance(pattern, np.ndarray):
                raise TypeError("'pattern' must be an instance of 'numpy.ndarray' " +
                                f"but not of '{type(pattern)}'")
        if pattern is None and pattern_id is None:
            raise ValueError("'pattern_id' and 'pattern' can not be None at the same time")
        if pattern_id is None:
            pattern_id = f"quality_source_pattern_node={node_id}"

        node_idx = self.epanet_api.getNodeIndex(node_id)

        if pattern is None:
            pattern_idx = self.epanet_api.getPatternIndex(pattern_id)
        else:
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
        if self.__running_simulation is True:
            raise RuntimeError("Can not change general parameters when simulation is running.")

        self._adapt_to_network_changes()

        if trace_node_id not in self._sensor_config.nodes:
            raise ValueError(f"Invalid node ID '{trace_node_id}'")

        self.__warn_if_quality_set()
        self.set_general_parameters(quality_model={"type": "TRACE",
                                                   "trace_node_id": trace_node_id})

    def add_species_injection_source(self, species_id: str, node_id: str, pattern: np.ndarray,
                                     source_type: int, pattern_id: str = None,
                                     source_strength: int = 1.) -> None:
        """
        Adds a new external (bulk or surface) species injection source at a particular node.

        Parameters
        ----------
        species_id : `str`
            ID of the (bulk or surface) species.
        node_id : `str`
            ID of the node at which this external (bulk or surface) species injection source
            is placed.
        pattern : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            1d source pattern.
        source_type : `int`,
            Type of the external (bulk or surface) species injection source -- must be one of
            the following EPANET toolkit constants:

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
            Injection source strength -- i.e. injection = source_strength * pattern.

            The default is 1.
        """
        source_type_ = "None"
        if source_type == ToolkitConstants.EN_CONCEN:
            source_type_ = "CONCEN"
        elif source_type == ToolkitConstants.EN_MASS:
            source_type_ = "MASS"
        elif source_type == ToolkitConstants.EN_SETPOINT:
            source_type_ = "SETPOINT"
        elif source_type == ToolkitConstants.EN_FLOWPACED:
            source_type_ = "FLOWPACED"

        if pattern_id is None:
            pattern_id = f"{species_id}_{node_id}"
        if pattern_id in self.epanet_api.getMSXPatternsNameID():
            raise ValueError("Invalid 'pattern_id' -- " +
                             f"there already exists a pattern with ID '{pattern_id}'")

        self.epanet_api.addMSXPattern(pattern_id, pattern)
        self.epanet_api.setMSXSources(node_id, species_id, source_type_, source_strength,
                                      pattern_id)
