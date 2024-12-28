"""
Module provides a base class for control environments.
"""
import os
import uuid
from abc import abstractmethod, ABC
from typing import Union
import warnings
import numpy as np

from ..simulation import ScenarioSimulator, ScenarioConfig, ScadaData, ToolkitConstants
from ..utils import get_temp_folder


class ScenarioControlEnv(ABC):
    """
    Base class for a control environment challenge.

    Parameters
    ----------
    scenario_config : :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Scenario configuration.
    autoreset : `bool`, optional
        If True, environment is automatically reset if terminated.

        The default is False.

    Attributes
    ----------
    _scenario_sim : :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`, protected
        Scenario simulator of the control scenario.
    _scenario_config : :class:`~epyt_flow.simulation.scenario_config.ScenarioConfig`
        Scenario configuration.
    _sim_generator : Generator[Union[:class:`~epyt_flow.simulation.scada.scada_data.ScadaData`, dict], bool, None], protected
        Generator for running the step-wise simulation.
    _hydraulic_scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`, protected
        SCADA data from the hydraulic simulation -- only used if EPANET-MSX is used in the control scenario.
    """
    def __init__(self, scenario_config: ScenarioConfig, autoreset: bool = False, **kwds):
        if not isinstance(scenario_config, ScenarioConfig):
            raise TypeError("'scenario_config' must be an instance of " +
                            "'epyt_flow.simulation.ScenarioConfig' " +
                            "but not of '{type(scenario_config)}'")
        if not isinstance(autoreset, bool):
            raise TypeError("'autoreset' must be an instance of 'bool' " +
                            f"but not of '{type(autoreset)}'")

        self._scenario_config = scenario_config
        self._scenario_sim = None
        self._sim_generator = None
        self.__autoreset = autoreset
        self._hydraulic_scada_data = None

        super().__init__(**kwds)

    @property
    def autoreset(self) -> bool:
        """
        True, if environment automatically resets after it terminated.

        Returns
        -------
        `bool`
            True, if environment automatically resets after it terminated.
        """
        return self.__autoreset

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self) -> None:
        """
        Frees all resources.
        """
        try:
            if self._sim_generator is not None:
                next(self._sim_generator)
                self._sim_generator.send(True)
        except StopIteration:
            pass

        if self._scenario_sim is not None:
            self._scenario_sim.close()

    def contains_events(self) -> bool:
        """
        Check if the scenario contains any events.

        Returns
        -------
        `bool`
            True is the scenario contains any events, False otherwise.
        """
        return len(self._scenario_config.system_events) != 0 or \
            len(self._scenario_config.sensor_reading_events) != 0

    def reset(self) -> Union[tuple[ScadaData, bool], ScadaData]:
        """
        Resets the environment (i.e. simulation).

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Current SCADA data (i.e. sensor readings).
        """
        if self._scenario_sim is not None:
            self._scenario_sim.close()

        self._scenario_sim = ScenarioSimulator(
            scenario_config=self._scenario_config)

        if self._scenario_sim.f_msx_in is not None:
            # Run hydraulic simulation first
            hyd_export = os.path.join(get_temp_folder(), f"epytflow_env_MSX_{uuid.uuid4()}.hyd")
            sim = self._scenario_sim.run_hydraulic_simulation
            self._hydraulic_scada_data = sim(hyd_export=hyd_export)

            # Run advanced quality analysis (EPANET-MSX) on top of the computed hydraulics
            gen = self._scenario_sim.run_advanced_quality_simulation_as_generator
            self._sim_generator = gen(hyd_export, support_abort=True)
        else:
            gen = self._scenario_sim.run_hydraulic_simulation_as_generator
            self._sim_generator = gen(support_abort=True)

        return self._next_sim_itr()

    def _next_sim_itr(self) -> Union[tuple[ScadaData, bool], ScadaData]:
        try:
            next(self._sim_generator)
            scada_data = self._sim_generator.send(False)

            if self._scenario_sim.f_msx_in is not None:
                cur_time = int(scada_data.sensor_readings_time[0])
                cur_hyd_scada_data = self._hydraulic_scada_data.\
                    extract_time_window(cur_time, cur_time)
                scada_data.join(cur_hyd_scada_data)

            if self.autoreset is True:
                return scada_data
            else:
                return scada_data, False
        except StopIteration:
            if self.__autoreset is True:
                return self.reset()
            else:
                return None, True

    def set_pump_status(self, pump_id: str, status: int) -> None:
        """
        Sets the status of a pump.

        Parameters
        ----------
        pump_id : `str`
            ID of the pump for which the status is set.
        status : `int`
            New status of the pump -- either active (i.e. open) or inactive (i.e. closed).

            Must be one of the following constants defined in
            :class:`~epyt_flow.simulation.events.actuator_events.ActuatorConstants`:

                - EN_CLOSED  = 0
                - EN_OPEN    = 1
        """
        if self._scenario_sim.f_msx_in is not None:
            raise RuntimeError("Can not execute actions affecting the hydraulics "+
                               "when running EPANET-MSX")

        pump_idx = self._scenario_sim.epanet_api.getLinkPumpNameID().index(pump_id)
        pump_link_idx = self._scenario_sim.epanet_api.getLinkPumpIndex(pump_idx + 1)
        self._scenario_sim.epanet_api.setLinkStatus(pump_link_idx, status)

    def set_pump_speed(self, pump_id: str, speed: float) -> None:
        """
        Sets the speed of a pump.

        Parameters
        ----------
        pump_id : `str`
            ID of the pump for which the pump speed is set.
        speed : `float`
            New pump speed.
        """
        if self._scenario_sim.f_msx_in is not None:
            raise RuntimeError("Can not execute actions affecting the hydraulics "+
                               "when running EPANET-MSX")

        pump_idx = self._scenario_sim.epanet_api.getLinkPumpNameID().index(pump_id)
        pattern_idx = self._scenario_sim.epanet_api.getLinkPumpPatternIndex(pump_idx + 1)

        if pattern_idx == 0:
            warnings.warn(f"No pattern for pump '{pump_id}' found -- a new pattern is created")
            pattern_idx = self._scenario_sim.epanet_api.addPattern(f"pump_speed_{pump_id}")
            self._scenario_sim.epanet_api.setLinkPumpPatternIndex(pump_idx, pattern_idx)

        self._scenario_sim.epanet_api.setPattern(pattern_idx, np.array([speed]))

    def set_valve_status(self, valve_id: str, status: int) -> None:
        """
        Sets the status of a valve.

        Parameters
        ----------
        valve_id : `str`
            ID of the valve for which the status is set.
        status : `int`
            New status of the valve -- either open or closed.

            Must be one of the following constants defined in
            :class:`~epyt_flow.simulation.events.actuator_events.ActuatorConstants`:

                - EN_CLOSED  = 0
                - EN_OPEN    = 1
        """
        if self._scenario_sim.f_msx_in is not None:
            raise RuntimeError("Can not execute actions affecting the hydraulics "+
                               "when running EPANET-MSX")

        valve_idx = self._scenario_sim.epanet_api.getLinkValveNameID().index(valve_id)
        valve_link_idx = self._scenario_sim.epanet_api.getLinkValveIndex()[valve_idx]
        self._scenario_sim.epanet_api.setLinkStatus(valve_link_idx, status)

    def set_node_quality_source_value(self, node_id: str, pattern_id: str,
                                      qual_value: float) -> None:
        """
        Sets the quality source at a particular node to a specific value -- e.g.
        setting the chlorine concentration injection to a specified value.

        Parameters
        ----------
        node_id : `str`
            ID of the node.
        pattern_id : `str`
            ID of the quality pattern at the specific node.
        qual_value : `float`
            New quality source value.
        """
        if self._scenario_sim.f_msx_in is not None:
            raise RuntimeError("Can not execute actions affecting the hydraulics "+
                               "when running EPANET-MSX")

        node_idx = self._scenario_sim.epanet_api.getNodeIndex(node_id)
        pattern_idx = self._scenario_sim.epanet_api.getPatternIndex(pattern_id)
        self._scenario_sim.epanet_api.setNodeSourceQuality(node_idx, 1)
        self._scenario_sim.epanet_api.setPattern(pattern_idx, np.array([qual_value]))

    def set_node_species_source_value(self, species_id: str, node_id: str, source_type: int,
                                      pattern_id: str, source_strength: float) -> None:
        """
        Sets the species source at a particular node to a specific value -- i.e.
        setting the species injection amount at a particular location.

        Parameters
        ----------
        species_id : `str`
            ID of the species.
        node_id : `str`
            ID of the node.
        source_type : `int`
            Type of the external species injection source -- must be one of
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
        pattern_id : `str`
            ID of the source pattern.
        source_strength : `float`
            Amount of the injected species (source strength) --
            i.e. interpreation of this number depends on `source_type`
        """
        if self._scenario_sim.f_msx_in is None:
            raise RuntimeError("You are not running EPANET-MSX")

        source_type_ = "None"
        if source_type == ToolkitConstants.EN_CONCEN:
            source_type_ = "CONCEN"
        elif source_type == ToolkitConstants.EN_MASS:
            source_type_ = "MASS"
        elif source_type == ToolkitConstants.EN_SETPOINT:
            source_type_ = "SETPOINT"
        elif source_type == ToolkitConstants.EN_FLOWPACED:
            source_type_ = "FLOWPACED"

        self._scenario_sim.epanet_api.setMSXPattern(pattern_id, [1])
        self._scenario_sim.epanet_api.setMSXSources(node_id, species_id, source_type_,
                                                    source_strength, pattern_id)

    @abstractmethod
    def step(self, *actions) -> Union[tuple[ScadaData, float, bool], tuple[ScadaData, float]]:
        """
        Performs the next step by applying an action and observing
        the consequences (SCADA data, reward, terminated).

        Note that `terminated` is only returned if `autoreset=False` otherwise
        only the current SCADA data and reward are returned.

        Returns
        -------
        `(` :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` `, float, bool)` or `(` :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` `, float)`
            Triple or tuple of observations (:class:`~epyt_flow.simulation.scada.scada_data.ScadaData`),
            reward (`float`), and terminated (`bool`).
        """
        raise NotImplementedError()
