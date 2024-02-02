from abc import abstractmethod
import epyt

from .event import Event


class SystemEvent(Event):
    """
    Base class for a system event -- i.e. an event that affects the EPANET simulation.
    """
    def __init__(self, **kwds):
        self._epanet_api = None

        super().__init__(**kwds)

    def init(self, epanet_api:epyt.epanet) -> None:
        """
        Initializes the event.

        Parameters
        ----------
        epanet_api : `epyt.epanet`
            API to EPANET and EPANET-MSX.
        """
        self._epanet_api = epanet_api

    @abstractmethod
    def apply(self, cur_time:int) -> None:
        """
        Implements the event using EPANET and EPANET-MSX.

        Parameters
        ----------
        cur_time : `int`
            Current time (seconds since the start) in the simulation.
        """
        raise NotImplementedError()
