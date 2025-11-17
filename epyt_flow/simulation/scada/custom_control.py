"""
Module provides a base class for custom control modules.
"""
from abc import abstractmethod, ABC
import warnings
import numpy as np
from epanet_plus import EPyT, EpanetConstants

from . import ScadaData


class CustomControlModule(ABC):
    """
    Base class for a custom control module.

    Attributes
    ----------
    epanet_api : `epanet_plus.EPyT <https://epanet-plus.readthedocs.io/en/stable/api.html#epanet_plus.epanet_toolkit.EPyT>`_
        API to EPANET and EPANET-MSX. Is set in :func:`init`.
    """
    def __init__(self, **kwds):
        self._epanet_api = None

        super().__init__(**kwds)

    def init(self, epanet_api: EPyT) -> None:
        """
        Initializes the control module.

        Parameters
        ----------
        epanet_api : `epanet_plus.EPyT <https://epanet-plus.readthedocs.io/en/stable/api.html#epanet_plus.epanet_toolkit.EPyT>`_
            API to EPANET for implementing the control module.
        """
        if not isinstance(epanet_api, EPyT):
            raise TypeError("'epanet_api' must be an instance of 'epanet_plus.EPyT' but not of " +
                            f"'{type(epanet_api)}'")

        self._epanet_api = epanet_api

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
        pump_link_idx = self._epanet_api.get_link_idx(pump_id)
        self._epanet_api.setlinkvalue(pump_link_idx, EpanetConstants.EN_STATUS, status)

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
        pump_idx = self._epanet_api.get_link_idx(pump_id)
        pattern_idx = self._epanet_api.getlinkvalue(pump_idx, EpanetConstants.EN_LINKPATTERN)

        if pattern_idx == 0:
            warnings.warn(f"No pattern for pump '{pump_id}' found -- a new pattern is created")

            pattern_id = f"pump_speed_{pump_id}"
            self._epanet_api.add_pattern(pattern_id, [speed])
            pattern_idx = self._epanet_api.getpatternindex(pattern_id)
            self._epanet_api.setlinkvalue(pump_idx, EpanetConstants.EN_LINKPATTERN, pattern_idx)

        self._epanet_api.setpattern(pattern_idx, [speed], 1)

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
        valve_link_idx = self._epanet_api.get_link_idx(valve_id)
        self._epanet_api.setlinkvalue(valve_link_idx, EpanetConstants.EN_STATUS, status)

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
        node_idx = self._epanet_api.get_node_idx(node_id)
        pattern_idx = self._epanet_api.getpatternindex(pattern_id)
        self._epanet_api.setnodevalue(node_idx, EpanetConstants.EN_SOURCEQUAL, 1)
        self._epanet_api.set_pattern(pattern_idx, np.array([qual_value]))

    @abstractmethod
    def step(self, scada_data: ScadaData) -> None:
        """
        Implements the control algorithm -- i.e. mapping of sensor reading to actions.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Sensor readings.
        """
        raise NotImplementedError()
