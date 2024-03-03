"""
Module provides a base classes for system events such as leakages, actuator events, etc.
"""
from abc import abstractmethod
import epyt

from .event import Event


class SystemEvent(Event):
    """
    Base class for a system event -- i.e. an event that affects the EPANET simulation.
    """
    def __init__(self, **kwds):
        self._epanet_api = None
        self.__exit_called = False

        super().__init__(**kwds)

    def init(self, epanet_api: epyt.epanet) -> None:
        """
        Initializes the event.

        Parameters
        ----------
        epanet_api : `epyt.epanet`
            API to EPANET and EPANET-MSX.
        """
        self._epanet_api = epanet_api

    def __call__(self, cur_time) -> None:
        return self.step(cur_time)

    def step(self, cur_time) -> None:
        """
        Is called at every iteration (time step) in the simulation.
        `apply` or `exit` are called if necessary.

        Parameters
        ----------
        cur_time : `int`
            Current time (seconds since the start) in the simulation.
        """
        if self.start_time <= cur_time < self.end_time:
            self.apply(cur_time)
        else:
            if self.__exit_called is False:
                self.exit(cur_time)
                self.__exit_called = True

    def exit(self, cur_time) -> None:
        """
        Is called ONCE after the event is over -- i.e. next time step after `end_time`.

        Any "clean-up" or "exiting" logic should go here.

        Parameters
        ----------
        cur_time : `int`
            Current time (seconds since the start) in the simulation.
        """

    @abstractmethod
    def apply(self, cur_time: int) -> None:
        """
        Implements the event using EPANET and EPANET-MSX.

        This function is only called when the event is active.

        Parameters
        ----------
        cur_time : `int`
            Current time (seconds since the start) in the simulation.
        """
        raise NotImplementedError()
