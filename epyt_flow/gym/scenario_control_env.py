"""
Module provides a base class for control environments.
"""
from abc import abstractmethod, ABC
from typing import Union
import warnings
import numpy as np

from ..simulation import ScenarioSimulator, ScenarioConfig, ScadaData


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
    """
    def __init__(self, scenario_config: ScenarioConfig, autoreset: bool = False, **kwds):
        self.__scenario_config = scenario_config
        self._scenario_sim = None
        self._sim_generator = None
        self.__autoreset = autoreset

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
                self._sim_generator.send(True)
                next(self._sim_generator)
        except StopIteration:
            pass

        if self._scenario_sim is not None:
            self._scenario_sim.close()

    def reset(self) -> ScadaData:
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
            scenario_config=self.__scenario_config)
        self._sim_generator = self._scenario_sim.run_simulation_as_generator(support_abort=True)

        return self._next_sim_itr()

    def _next_sim_itr(self) -> ScadaData:
        try:
            next(self._sim_generator)
            r = self._sim_generator.send(False)

            if self.autoreset is True:
                return r
            else:
                return r, False
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
        pump_idx = self._scenario_sim.epanet_api.getLinkPumpNameID().index(pump_id)
        pattern_idx = self._scenario_sim.epanet_api.getLinkPumpPatternIndex(pump_idx + 1)

        if pattern_idx == 0:
            warnings.warn(f"No pattern for pump '{pump_id}' found -- a new pattern is created")
            pattern_idx = self._scenario_sim.epanet_api.addPattern(f"pump_speed_{pump_id}")
            self._scenario_sim.epanet_api.setLinkPumpPatternIndex(pattern_idx)

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
        node_idx = self._scenario_sim.epanet_api.getNodeIndex(node_id)
        pattern_idx = self._scenario_sim.epanet_api.getPatternIndex(pattern_id)
        self._scenario_sim.epanet_api.setNodeSourceQuality(node_idx, 1)
        self._scenario_sim.epanet_api.setPattern(pattern_idx, np.array([qual_value]))

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
