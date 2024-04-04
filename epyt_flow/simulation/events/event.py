"""
Module provides a base class for events.
"""
from abc import ABC
import math


class Event(ABC):
    """
    Base class for an event.

    Parameters
    ----------
    start_time : `int`
        Starting time (seconds since the simulation start) of this event.
    end_time : `int`, optional
        Time (seconds since the simulation start) when this event ends -- None if it never ends.

        The default is None.
    """
    def __init__(self, start_time: int, end_time: int = None, **kwds):
        if not isinstance(start_time, int) or start_time < 0:
            raise ValueError("'start_time' must be a positive integer specifying the time " +
                             "at which this event starts.")
        if end_time is not None and not isinstance(end_time, int):
            raise ValueError("'end_time' must be either None or a positive integer specifiying " +
                             "the time at which this event ends.")
        if end_time is not None:
            if start_time >= end_time:
                raise ValueError("'start_time' must be smaller than 'end_time'")

        self.__start_time = start_time
        self.__end_time = end_time if end_time is not None else math.inf

        super().__init__(**kwds)

    @property
    def start_time(self) -> int:
        """
        Gets the start time (seconds since the simulation start) of this event.

        Returns
        -------
        `int`
            Start time of this event.
        """
        return self.__start_time

    @property
    def end_time(self) -> int:
        """
        Gets the end time (seconds since the simulation start) of this event.
        float("inf") if it never ends.

        Returns
        -------
        `int`
            End time of this event.
        """
        return self.__end_time

    def get_attributes(self) -> dict:
        """
        Gets all attributes to be serialized -- these attributes are passed to the
        constructor when the object is deserialized.

        Returns
        -------
        `dict`
            Dictionary of attributes -- i.e. pairs of attribute name and value.
        """
        return {"start_time": self.__start_time, "end_time": self.__end_time}

    def __str__(self) -> str:
        return f"start_time: {self.__start_time} end_time: {self.__end_time}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Event):
            raise TypeError(f"Can not compare 'Event' instance with '{type(other)}' instance")

        return self.__start_time == other.start_time and self.__end_time == other.end_time
