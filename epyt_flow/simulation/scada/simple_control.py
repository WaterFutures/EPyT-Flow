"""
The module contains classes for representing simple control rules as used in EPANET.
"""
from typing import Union
from epyt.epanet import ToolkitConstants

from ..events import ActuatorConstants
from ...serialization import JsonSerializable, SIMPLE_CONTROL_ID, serializable


@serializable(SIMPLE_CONTROL_ID, ".epytflow_simple_control")
class SimpleControlModule(JsonSerializable):
    """
    A class for representing a simple EPANET control rule.

    Parameters
    ----------
    link_id : `str`
        Link ID.
    link_status : `int` or `float`
        Status of the link that is set when the condition is fullfilled.

        Instance of `float` if the link constitutes a pump -- in this case,
        the argument corresponds to the pump speed.

        Instance of `int` if the link constitutes a valve -- in this case,
        must be one of the followig costants defined in
        :class:`~epyt_flow.simulation.events.actuator_events.ActuatorConstants`:

            - EN_CLOSED = 0
            - EN_OPEN   = 1
    cond_type : `int`
        Condition/Rule type.

        Must be one of the following EPANET constants:

            - EN_LOWLEVEL  = 0
            - EN_HILEVEL   = 1
            - EN_TIMER     = 2
            - EN_TIMEOFDAY = 3
    cond_var_value : `str` or `int`
        Condition/Rule variable value.

        Node ID in the cases of EN_LOWLEVEL or EN_HILEVEL.
        Time of the day (in AM/PM format) in the case of EN_TIMEOFDAY.
        Number of hours (as an integer) since simulation start in the case of EN_TIMER.
    cond_comp_value : `float`
        The condition/rule comparison value at which this control rule is triggered.

        Lower or upper value on the pressure (or tank level) in the cases of
        EN_LOWLEVEL and EN_HILEVEL.

        Will be ignored in all other cases -- i.e. should be set to None.
    """
    def __init__(self, link_id: str, link_status: Union[int, float], cond_type: int,
                 cond_var_value: Union[str, int], cond_comp_value: float,
                 **kwds):
        if not isinstance(link_id, str):
            raise TypeError(f"'link_id' must be an instance of 'str' but not of '{type(link_id)}'")
        if isinstance(link_status, int):
            if link_status not in [ActuatorConstants.EN_OPEN, ActuatorConstants.EN_CLOSED]:
                raise ValueError(f"Invalid link status {link_status} in 'link_status'")
        elif isinstance(link_status, float):
            if link_status < 0:
                raise TypeError("'link_status' can not be negative")
        else:
            raise TypeError("'link_status' must be an instance of 'int' or 'float' but not " +
                            f"of '{type(link_status)}'")
        if cond_type not in [ToolkitConstants.EN_TIMEOFDAY, ToolkitConstants.EN_TIMER,
                             ToolkitConstants.EN_LOWLEVEL, ToolkitConstants.EN_HILEVEL]:
            raise ValueError(f"Invalid control type '{cond_type}' in 'cond_type'")

        if cond_type == ToolkitConstants.EN_TIMEOFDAY:
            if not isinstance(cond_var_value, str):
                raise TypeError("EN_TIMEOFDAY requires that 'cond_var_value' must be an instance " +
                                f"of 'str' but not of '{type(cond_var_value)}'")
            if not cond_var_value.endswith("AM") and not cond_var_value.endswith("PM"):
                raise ValueError(f"Invalid time of day format '{cond_var_value}' in " +
                                 "'cond_var_value'")
        elif cond_type == ToolkitConstants.EN_TIMER:
            if not isinstance(cond_var_value, int):
                raise TypeError("EN_TIMER requires that 'cond_var_value' must be an instance " +
                                f"of 'int' but not of '{type(cond_var_value)}'")
            if cond_var_value < 0:
                raise ValueError("'cond_var_value' can not be negative")
        else:
            if not isinstance(cond_var_value, str):
                raise TypeError("'cond_var_value' must be an instance of 'str' but " +
                                f"not of '{type(cond_var_value)}'")
            if not isinstance(cond_comp_value, float):
                raise TypeError("'cond_comp_value' must be an instance of 'float' " +
                                f"but not of '{type(cond_comp_value)}'")
            if cond_comp_value < 0:
                raise ValueError("'cond_comp_value' can not be negative")

        self.__link_id = link_id
        self.__link_status = link_status
        self.__cond_type = cond_type
        self.__cond_var_value = cond_var_value
        self.__cond_comp_value = cond_comp_value

        super().__init__(**kwds)

    @property
    def link_id(self) -> str:
        """
        Returns the link ID.

        Returns
        -------
        `str`
            Link ID.
        """
        return self.__link_id

    @property
    def link_status(self) -> Union[int, float]:
        """
        Returns the link status that is set when the condition is fullfilled.

        Returns
        -------
        `int` or `float`
            Pump speed if the link is a pump, otherwise one of the followig costants defined in
            :class:`~epyt_flow.simulation.events.actuator_events.ActuatorConstants`:

                - EN_CLOSED = 0
                - EN_OPEN   = 1
        """
        return self.__link_status

    @property
    def cond_type(self) -> int:
        """
        Returns the condition/rule type.

        Returns
        -------
        `int`
            Condition/Rule type -- will be one of the following EPANET constants:

                - EN_LOWLEVEL  = 0
                - EN_HILEVEL   = 1
                - EN_TIMER     = 2
                - EN_TIMEOFDAY = 3
        """
        return self.__cond_type

    @property
    def cond_var_value(self) -> Union[str, int]:
        """
        Return the condition/rule variable value.

        Node ID in the cases of EN_LOWLEVEL or EN_HILEVEL.
        Time of the day (in AM/PM format) in the case of EN_TIMEOFDAY.
        Number of hours (as an integer) since simulation start in the case of EN_TIMER.

        Returns
        -------
        `str` or `int`
            Condition/rule variable value.
        """
        return self.__cond_var_value

    @property
    def cond_comp_value(self) -> float:
        """
        Returns the condition/rule comparison value -- might be None if not needed.

        Lower or upper value on the pressure (or tank level) in the cases of
        EN_LOWLEVEL and EN_HILEVEL.

        Returns
        -------
        `float`
            Condition/Rule comparison value.
        """
        return self.__cond_comp_value

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"link_id": self.__link_id,
                                           "link_status": self.__link_status,
                                           "cond_type": self.__cond_type,
                                           "cond_var_value": self.__cond_var_value,
                                           "cond_comp_value": self.__cond_comp_value}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__link_id == other.link_id and \
            self.__link_status == other.link_status and self.__cond_type == other.cond_type and \
            self.__cond_var_value == other.cond_var_value and \
            self.__cond_comp_value == other.cond_comp_value

    def __str__(self) -> str:
        control_rule_str = f"LINK {self.__link_id} "
        if isinstance(self.__link_status, int):
            control_rule_str += "OPEN " if self.__link_status == ActuatorConstants.EN_OPEN \
                else "CLOSED "
        else:
            control_rule_str += f"{self.__link_status} "

        if self.__cond_type == ToolkitConstants.EN_TIMER:
            control_rule_str += f"AT TIME {self.__cond_var_value}"
        elif self.__cond_type == ToolkitConstants.EN_TIMEOFDAY:
            control_rule_str += f"AT CLOCKTIME {self.__cond_var_value}"
        elif self.__cond_type == ToolkitConstants.EN_LOWLEVEL:
            control_rule_str += f"IF NODE {self.__cond_var_value} BELOW {self.__cond_comp_value}"
        elif self.__cond_type == ToolkitConstants.EN_HILEVEL:
            control_rule_str += f"IF NODE {self.__cond_var_value} ABOVE {self.__cond_comp_value}"

        return control_rule_str


class SimplePumpSpeedTimeControl(SimpleControlModule):
    """
    A class for representing a simple control rule for setting the pump speed at some point in time.

    Parameters
    ----------
    pump_id : `str`
        Pump ID.
    pump_speed : `float`
        Pump speed.
    time : `str` or `int`
        Time of the day (in AM/PM format) in the case or
        number of hours (as an integer) since simulation start.
    """
    def __init__(self, pump_id: str, pump_speed: float, time: Union[str, int]):
        super().__init__(link_id=pump_id, link_status=pump_speed,
                         cond_type=ToolkitConstants.EN_TIMER if isinstance(time, int)
                         else ToolkitConstants.EN_TIMEOFDAY,
                         cond_var_value=time, cond_comp_value=None)


class SimplePumpSpeedConditionControl(SimpleControlModule):
    """
    A class for representing a simple IF-THEN control rule for setting the pump speed.

    Parameters
    ----------
    Parameters
    ----------
    pump_id : `str`
        Pump ID.
    pump_speed : `float`
        Pump speed.
    node_id : `str`
        Node ID.
    comp_type : `int`
        Comparison type -- must be one of the following EPANET constants:

            - EN_LOWLEVEL  = 0
            - EN_HILEVEL   = 1
    comp_value : `float`:
        Lower or upper value on the pressure (or tank level) at which this
        control rule is triggered.
    """
    def __init__(self, pump_id: str, pump_speed: float, node_id: str, comp_type: int,
                 comp_value: float):
        super().__init__(link_id=pump_id, link_status=pump_speed, cond_type=comp_type,
                         cond_var_value=node_id, cond_comp_value=comp_value)


class SimpleValveTimeControl(SimpleControlModule):
    """
    A class for representing a simple control rule for setting the valve status
    at some point in time.

    Parameters
    ----------
    valve_id : `str`
        valve ID.
    valve_status : `int`
        Valve status -- must be one of the followig costants defined in
        :class:`~epyt_flow.simulation.events.actuator_events.ActuatorConstants`:

            - EN_CLOSED = 0
            - EN_OPEN   = 1
    time : `str` or `int`
        Time of the day (in AM/PM format) in the case or
        number of hours (as an integer) since simulation start.
    """
    def __init__(self, valve_id: str, valve_status: int, time: Union[str, int]):
        super().__init__(link_id=valve_id, link_status=valve_status,
                         cond_type=ToolkitConstants.EN_TIMER if isinstance(time, int)
                         else ToolkitConstants.EN_TIMEOFDAY,
                         cond_var_value=time, cond_comp_value=None)


class SimpleValveConditionControl(SimpleControlModule):
    """
    A class for representing a simple IF-THEN control rule for setting the valve status.

    Parameters
    ----------
    valve_id : `str`
        valve ID.
    valve_status : `int`
        Valve status -- must be one of the followig costants defined in
        :class:`~epyt_flow.simulation.events.actuator_events.ActuatorConstants`:

            - EN_CLOSED = 0
            - EN_OPEN   = 1
    node_id : `str`
        Node ID.
    comp_type : `int`
        Comparison type -- must be one of the following EPANET constants:

            - EN_LOWLEVEL  = 0
            - EN_HILEVEL   = 1
    comp_value : `float`:
        Lower or upper value on the pressure (or tank level) at which this
        control rule is triggered.
    """
    def __init__(self, valve_id: str, valve_status: int, node_id: str, comp_type: int,
                 comp_value: float):
        super().__init__(link_id=valve_id, link_status=valve_status, cond_type=comp_type,
                         cond_var_value=node_id, cond_comp_value=comp_value)
