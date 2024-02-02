from .anomaly_detector import AnomalyDetector
from ..simulation.scada import ScadaData


class SensorInterpolationDetector(AnomalyDetector):
    """
    TODO.
    """
    def __init__(self, **kwds):
        # TODO

        super().__init__(**kwds)

    def fit(self) -> None:
        """
        TODO
        """
        pass

    def apply(self, scada_data:ScadaData) -> list[int]:
        """
        Applies this detector to given SCADA data  and returns suspicious time points.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            SCADA data in which to look for anomalies.
        
        Returns
        -------
        `list[int]`
            List of suspicious time points.
        """
        pass
