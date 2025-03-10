"""
Module provides a base class for event detectors.
"""
import warnings
from abc import abstractmethod, ABC

from ..simulation.scada import ScadaData


warnings.warn("'epyt_flow.models' is deprecated in favor of EPyT-Control " +
              "and will be removed in future releases.")


class EventDetector(ABC):
    """
    Base class for event detectors.
    """
    def __init__(self, **kwds):
        super().__init__(**kwds)

    @abstractmethod
    def apply(self, scada_data: ScadaData) -> list[int]:
        """
        Applies this detector to given SCADA data and returns suspicious time points.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            SCADA data in which to look for events (i.e. anomalies).

        Returns
        -------
        `list[int]`
            List of suspicious time points.
        """
        raise NotImplementedError()
