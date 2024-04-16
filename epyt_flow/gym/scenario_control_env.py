"""
Module provides a base class for control environments.
"""
from abc import abstractmethod, ABC
from copy import deepcopy

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
        """
        return deepcopy(self.__autoreset)

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

    @abstractmethod
    def step(self) -> tuple[ScadaData, float, bool]:
        """
        Performs the next step by applying an action and observing
        the consequences (SCADA data, reward, terminated).

        Note that `terminated` is only returned if `autoreset=False` otherwise
        only SCADA data and reward are returned.

        Returns
        -------
        `(ScadaData, float, bool)`
            Triple of observations (:class:`~epyt_flow.simuation.scada.scada_data.ScadaData`),
            reward (`float`), and terminated (`bool`).
        """
        raise NotImplementedError()
