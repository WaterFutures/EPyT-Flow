"""
Module provides implementations of different types of actuator events.
"""
import numpy as np

from .system_event import SystemEvent


class ActuatorEvent(SystemEvent):
    """
    Base class of an actuator event.
    """


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


class PumpStateEvent(PumpEvent):
    """
    Class implementing a pump state event.

    Parameters
    ----------
    pump_state : `str`
        New state of the pump -- i.e. the state of the pump is set to this value
        while the event is active.

        Must be one of the following:

            - EN_PUMP_CLOSED  = 2
            - EN_PUMP_OPEN    = 3
    """
    def __init__(self, pump_state: int, **kwds):
        if not isinstance(pump_state, int):
            raise TypeError("'pump_state' must be an instace of 'int' " +
                            f"but not of {type(pump_state)}")
        if not 2 <= pump_state <= 3:
            raise ValueError(f"Invalid pump state '{pump_state}' -- " +
                             "must be either EN_PUMP_CLOSED (2) or EN_PUMP_OPEN (3)")

        self.__pump_state = pump_state

        super().__init__(**kwds)

    @property
    def pump_state(self) -> int:
        """
        Gets the new pump state.

        Returns
        -------
        `int`
            New pump state.
            One of the following:

                - EN_PUMP_CLOSED  = 2
                - EN_PUMP_OPEN    = 3
        """
        return self.__pump_state

    def apply(self, cur_time: int) -> None:
        pump_idx = self._epanet_api.getLinkPumpNameID().index(self.pump_id)
        pump_link_idx = self._epanet_api.getLinkPumpIndex()[pump_idx]
        self._epanet_api.setLinkStatus(pump_link_idx, self.__pump_state)


class PumpSpeedEvent(PumpEvent):
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

        super().__init__(self, **kwds)

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
        pump_idx = self._epanet_api.getLinkPumpNameID().index(self.pump_id)
        pattern_idx = self._epanet_api.getLinkPumpPatternIndex(pump_idx + 1)
        self._epanet_api.setPattern(pattern_idx, np.array([self.__pump_speed]))


class ValveStateEvent(ActuatorEvent):
    """
    Class implementing a valve state event.

    Parameters
    ----------
    valve_id : `str`
        ID of the valve that is affected by this event.
    valve_state : `str`
        New state of the valve -- the valve state is set to this value while this event is active.
        Must be one of the following:

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
        """
        return self.__valve_state

    def apply(self, cur_time: int) -> None:
        valve_idx = self._epanet_api.getLinkValveNameID().index(self.__valve_id)
        valve_link_idx = self._epanet_api.getLinkValveIndex()[valve_idx]
        self._epanet_api.setLinkStatus(valve_link_idx, self.__valve_state)
