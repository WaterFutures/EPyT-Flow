"""
This module provides classes for implementing different types of sensor reading attacks.
"""
from copy import deepcopy
import numpy as np

from .sensor_reading_event import SensorReadingEvent
from ...serialization import serializable, JsonSerializable, SENSOR_ATTACK_OVERRIDE_ID, \
    SENSOR_ATTACK_REPLAY_ID


class SensorReadingAttack(SensorReadingEvent):
    """
    Base class of a sensor reading attack.
    """


@serializable(SENSOR_ATTACK_OVERRIDE_ID, ".epytflow_sensorattack_override")
class SensorOverrideAttack(SensorReadingAttack, JsonSerializable):
    """
    Class implementing a sensor override attack -- i.e. sensor reading values are overwritten
    by pre-defined values.

    If the override attack is running out of pre-defined sensor reading values,
    it repeats the given values from the beginning onwards.

    Parameters
    ----------
    new_sensor_values : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        New sensor reading values -- i.e. these values replace the true sensor reading values.
    """
    def __init__(self, new_sensor_values: np.ndarray, **kwds):
        if not isinstance(new_sensor_values, np.ndarray):
            raise TypeError("'new_sensor_values' must be an instance of 'numpy.ndarray' " +
                            f"but not of '{type(new_sensor_values)}'")
        if len(new_sensor_values.shape) != 1:
            raise ValueError("'new_sensor_values' must be a 1-dimensional array")
        if len(new_sensor_values) == 0:
            raise ValueError("'new_sensor_values' can not be empty")

        self.__new_sensor_values = new_sensor_values
        self.__cur_replay_idx = 0

        super().__init__(**kwds)

    @property
    def new_sensor_values(self) -> np.ndarray:
        """
        Get the new sensor reading values -- i.e. these values replace the
        true sensor reading values.

        Returns
        -------
        `np.ndarray`
            New sensor readings.
        """
        return deepcopy(self.__new_sensor_values)

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"new_sensor_values": self.__new_sensor_values}

    def __eq__(self, other) -> bool:
        if not isinstance(other, SensorOverrideAttack):
            raise TypeError("Can not compare 'SensorOverrideAttack' instance " +
                            f"with '{type(other)}' instance")

        return super().__eq__(other) and self.__new_sensor_values == other.new_sensor_values

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()} " +\
            f"new_sensor_values: {self.__new_sensor_values}"

    def apply(self, sensor_readings: np.ndarray,
              sensor_readings_time: np.ndarray) -> np.ndarray:
        for i in range(sensor_readings.shape[0]):
            t = sensor_readings_time[i]

            if self.start_time <= t <= self.end_time:
                sensor_readings[i] = self.__new_sensor_values[self.__cur_replay_idx]
                self.__cur_replay_idx = (self.__cur_replay_idx + 1) % len(self.__new_sensor_values)

        return sensor_readings


@serializable(SENSOR_ATTACK_REPLAY_ID, ".epytflow_sensorattack_replay")
class SensorReplayAttack(SensorReadingAttack, JsonSerializable):
    """
    Class implementing a sensor replay attack -- i.e. sensor readings are replaced by
    historical recordings.

    If the provided time window of historical recordings is smaller than the time window of the
    attack, it repeats the historical values from the beginning onwards.

    Parameters
    ----------
    replay_data_time_window_start : `int`
        Start (seconds since simulation start) of the time window that is used in the replay
        of sensor readings.
    replay_data_time_window_end : `int`
        End (seconds since simulation start) of the time window that is used in the replay
        of sensor readings.
    """
    def __init__(self, replay_data_time_window_start: int, replay_data_time_window_end: int,
                 **kwds):
        if not isinstance(replay_data_time_window_start, int):
            raise TypeError("'replay_data_time_window_start' must be an instance of 'int' " +
                            f"but not of {type(replay_data_time_window_start)}")
        if not isinstance(replay_data_time_window_end, int):
            raise TypeError("'replay_data_time_window_end' must be an instance of 'int' " +
                            f"but not of {type(replay_data_time_window_end)}")
        if replay_data_time_window_start > replay_data_time_window_end or \
                replay_data_time_window_start < 0:
            raise ValueError("Invalid values for 'replay_data_time_window_start' and/or " +
                             "'replay_data_time_window_end' detected.")

        self.__new_sensor_values = np.zeros(replay_data_time_window_end -
                                            replay_data_time_window_start)
        self.__sensor_data_time_window_start = replay_data_time_window_start
        self.__sensor_data_time_window_end = replay_data_time_window_end
        self.__cur_hist_idx = 0
        self.__cur_replay_idx = 0

        super().__init__(**kwds)

        if self.__sensor_data_time_window_start > self.start_time:
            raise ValueError("'replay_data_time_window_start' must be less than 'start_time'")

    @property
    def sensor_data_time_window_start(self) -> int:
        """
        Gets the start time (seconds since simulation start) of the time window
        that is used in the replay of sensor readings.

        Returns
        -------
        `int`
            Start time.
        """
        return self.__sensor_data_time_window_start

    @property
    def sensor_data_time_window_end(self) -> int:
        """
        Gets the end time (seconds since simulation start) of the time window
        that is used in the replay of sensor readings.

        Returns
        -------
        `int`
            End time.
        """
        return self.__sensor_data_time_window_end

    def get_attributes(self) -> dict:
        my_attributes = {"new_sensor_values": self.__new_sensor_values,
                         "replay_data_time_window_start": self.__sensor_data_time_window_start,
                         "replay_data_time_window_end": self.__sensor_data_time_window_end}

        return super().get_attributes() | my_attributes

    def __eq__(self, other) -> bool:
        if not isinstance(other, SensorReplayAttack):
            raise TypeError("Can not compare 'SensorReplayAttack' instance " +
                            f"with '{type(other)}' instance")

        return super().__eq__(other) and self.__new_sensor_values == other.new_sensor_values

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()} " +\
            f"new_sensor_values: {self.__new_sensor_values}"

    def apply(self, sensor_readings: np.ndarray,
              sensor_readings_time: np.ndarray) -> np.ndarray:
        for i in range(sensor_readings.shape[0]):
            t = sensor_readings_time[i]

            if self.__sensor_data_time_window_start <= t <= self.__sensor_data_time_window_end:
                self.__new_sensor_values[self.__cur_hist_idx] = sensor_readings[i]
                self.__cur_hist_idx += 1

            if self.start_time <= t <= self.end_time:
                sensor_readings[i] = self.__new_sensor_values[self.__cur_replay_idx]
                self.__cur_replay_idx = (self.__cur_replay_idx + 1) % len(self.__new_sensor_values)

        return sensor_readings
