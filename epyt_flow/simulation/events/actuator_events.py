"""
Module provides implementations of different types of actuator events.
"""
import warnings
from epyt.epanet import epanet
import numpy as np

from .system_event import SystemEvent
from ...serialization import serializable, JsonSerializable, PUMP_STATE_EVENT_ID, \
    PUMP_SPEED_EVENT_ID, VALVE_STATE_EVENT_ID


class ActuatorConstants:
    """
    Class defining some constants related to actuator events.

    Attributes
    ----------
    EN_CLOSED
        Valve or pump is closed.
    EN_OPEN
        Valve or pump is open -- i.e. active.
    """
    EN_CLOSED       = 0
    EN_OPEN         = 1


class ActuatorEvent(SystemEvent):
    """
    Base class of an actuator event.

    .. note::
        Note that actuator events are one-time events -- i.e.
        they are executed only once at a given point in time.

    Parameters
    ----------
    time : int
        Time (in seconds since simulation start) at which this event is executed.
    """
    def __init__(self, time: int, **kwds):
        super().__init__(start_time=time, end_time=time+1, **kwds)

    def get_attributes(self) -> dict:
        return {"time": self.start_time}


class PumpEvent(ActuatorEvent):
    """
    Base class of a pump event.

    Parameters
    ----------
    pump_id : str
        ID of the pump that is affected by this event.
    """
    def __init__(self, pump_id: str, **kwds):
        self.__pump_id = pump_id

        super().__init__(**kwds)

    def init(self, epanet_api: epanet) -> None:
        if self.__pump_id not in epanet_api.getLinkPumpNameID():
            raise ValueError(f"Invalid pump ID '{self.__pump_id}'")

        super().init(epanet_api)

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"pump_id": self.__pump_id}

    @property
    def pump_id(self) -> str:
        """
        Gets the ID of the pump affected by this event.

        Returns
        -------
        `str`
            Pump ID.
        """
        return self.__pump_id


@serializable(PUMP_STATE_EVENT_ID, ".epytflow_pump_state_event")
class PumpStateEvent(PumpEvent, JsonSerializable):
    """
    Class implementing a pump state event.

    Parameters
    ----------
    pump_state : `str`
        New state of the pump -- i.e. the state of the pump is set to this value
        while the event is active.

        Must be one of the following constants defined in
        :class:`~epyt_flow.simulation.events.actuator_events.ActuatorConstants`:

            - EN_CLOSED  = 0
            - EN_OPEN    = 1
    """
    def __init__(self, pump_state: int, **kwds):
        if not isinstance(pump_state, int):
            raise TypeError("'pump_state' must be an instace of 'int' " +
                            f"but not of {type(pump_state)}")
        if not 0 <= pump_state <= 1:
            raise ValueError(f"Invalid pump state '{pump_state}' -- " +
                             "must be either EN_CLOSED (0) or EN_OPEN (1)")

        self.__pump_state = pump_state

        super().__init__(**kwds)

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"pump_state": self.__pump_state}

    @property
    def pump_state(self) -> int:
        """
        Gets the new pump state.

        Returns
        -------
        `int`
            New pump state.

            One of the following constants defined in
            :class:`~epyt_flow.simulation.events.actuator_events.ActuatorConstants`:

                - EN_CLOSED  = 0
                - EN_OPEN    = 1
        """
        return self.__pump_state

    def apply(self, cur_time: int) -> None:
        pump_idx = self._epanet_api.getLinkPumpNameID().index(self.pump_id) + 1
        pump_link_idx = self._epanet_api.getLinkPumpIndex(pump_idx)
        self._epanet_api.setLinkStatus(pump_link_idx, self.__pump_state)


@serializable(PUMP_SPEED_EVENT_ID, ".epytflow_pump_speed_event")
class PumpSpeedEvent(PumpEvent, JsonSerializable):
    """
    Class implementing a pump speed event.

    Parameters
    ----------
    pump_speed : float
        New pump speed -- i.e. the speed of the pump is set to this value while the event is active.
    """
    def __init__(self, pump_speed: float, **kwds):
        if not isinstance(pump_speed, float):
            raise TypeError("'pump_speed' must be an instance of 'float' " +
                            f"but not of {type(pump_speed)}")
        if pump_speed <= 0:
            raise ValueError("Pump speed must be positive")

        self.__pump_speed = pump_speed

        super().__init__(**kwds)

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"pump_speed": self.__pump_speed}

    @property
    def pump_speed(self) -> float:
        """
        Gets the new pump speed.

        Returns
        -------
        `float`
            New pump speed.
        """
        return self.__pump_speed

    def apply(self, cur_time: int) -> None:
        pump_idx = self._epanet_api.getLinkPumpNameID().index(self.pump_id) + 1
        pattern_idx = self._epanet_api.getLinkPumpPatternIndex(pump_idx)

        if pattern_idx == 0:
            warnings.warn(f"No pattern for pump '{self.pump_id}' found -- a new pattern is created")
            pattern_idx = self._epanet_api.addPattern(f"pump_speed_{self.pump_id}")
            self._epanet_api.setLinkPumpPatternIndex(pump_idx, pattern_idx)

        self._epanet_api.setPattern(pattern_idx, np.array([self.__pump_speed]))


@serializable(VALVE_STATE_EVENT_ID, ".epytflow_valve_state_event")
class ValveStateEvent(ActuatorEvent, JsonSerializable):
    """
    Class implementing a valve state event.

    Parameters
    ----------
    valve_id : `str`
        ID of the valve that is affected by this event.
    valve_state : `str`
        New state of the valve -- i.e. the valve state is set to this value this event is executed.

        Must be one of the following constants defined in
        :class:`~epyt_flow.simulation.events.actuator_events.ActuatorConstants`:

            - EN_CLOSED       = 0
            - EN_OPEN         = 1
    """
    def __init__(self, valve_id: str, valve_state: int, **kwds):
        if not isinstance(valve_state, int):
            raise TypeError("'valve_state' must be an instance of 'int' " +
                            f"but not of {type(valve_state)}")
        if not 0 <= valve_state <= 1:
            raise ValueError(f"Invalid valve state '{valve_state}' -- " +
                             "must be either EN_CLOSED (0) or EN_OPEN (1)")

        self.__valve_id = valve_id
        self.__valve_state = valve_state

        super().__init__(**kwds)

    def init(self, epanet_api: epanet) -> None:
        if self.__valve_id not in epanet_api.getLinkValveNameID():
            raise ValueError(f"Invalid valve ID '{self.__valve_id}'")

        super().init(epanet_api)

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"valve_id": self.__valve_id,
                                           "valve_state": self.__valve_state}

    @property
    def valve_id(self) -> str:
        """
        Gets the ID of the valve affected by this event.

        Returns
        -------
        `str`
            Valve ID.
        """
        return self.__valve_id

    @property
    def valve_state(self) -> int:
        """
        Gets the new state of the valve.

        Returns
        -------
        `int`
            New valve state.

            One of the following constants defined in
            :class:`~epyt_flow.simulation.events.actuator_events.ActuatorConstants`:
        """
        return self.__valve_state

    def apply(self, cur_time: int) -> None:
        valve_idx = self._epanet_api.getLinkValveNameID().index(self.__valve_id) + 1
        valve_link_idx = self._epanet_api.getLinkValveIndex(valve_idx)
        self._epanet_api.setLinkStatus(valve_link_idx, self.__valve_state)
