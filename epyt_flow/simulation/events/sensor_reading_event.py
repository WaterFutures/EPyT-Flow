"""
Module provides a base class for sensor reading events such as sensor faults.
"""
from abc import abstractmethod
import warnings
import numpy

from .event import Event
from ..sensor_config import SensorConfig, SENSOR_TYPE_NODE_PRESSURE, SENSOR_TYPE_NODE_QUALITY, \
    SENSOR_TYPE_NODE_DEMAND, SENSOR_TYPE_LINK_FLOW, SENSOR_TYPE_LINK_QUALITY, \
    SENSOR_TYPE_VALVE_STATE, SENSOR_TYPE_PUMP_STATE, SENSOR_TYPE_TANK_VOLUME, \
    SENSOR_TYPE_NODE_BULK_SPECIES, SENSOR_TYPE_LINK_BULK_SPECIES, SENSOR_TYPE_SURFACE_SPECIES


class SensorReadingEvent(Event):
    """
    Base class for a sensor reading event -- i.e. an event directly affecting sensor readings.

    Parameters
    ----------
    sensor_id : `str`
        ID of the sensor that is affected by this event.
    sensor_type : `int`
        Type of the sensor that is specified in 'sensor_id'.
        Must be one of the following pre-defined constants:

        - SENSOR_TYPE_NODE_PRESSURE     = 1
        - SENSOR_TYPE_NODE_QUALITY      = 2
        - SENSOR_TYPE_NODE_DEMAND       = 3
        - SENSOR_TYPE_LINK_FLOW         = 4
        - SENSOR_TYPE_LINK_QUALITY      = 5
        - SENSOR_TYPE_VALVE_STATE       = 6
        - SENSOR_TYPE_PUMP_STATE        = 7
        - SENSOR_TYPE_TANK_VOLUME       = 8
        - SENSOR_TYPE_NODE_BULK_SPECIES = 9
        - SENSOR_TYPE_NODE_LINK_SPECIES = 10
        - SENSOR_TYPE_SURFACE_SPECIES   = 11
    """
    def __init__(self, sensor_id: str, sensor_type: int, **kwds):
        if not isinstance(sensor_id, str):
            raise TypeError("'sensor_id' must be an instance of 'str' but not of " +
                            f"'{type(sensor_id)}'")
        if not isinstance(sensor_type, int):
            raise TypeError("'sensor_type' mut be an instance of 'int' but not of " +
                            f"'{type(sensor_type)}'")
        if not 1 <= sensor_type <= 10:
            raise ValueError("Invalid value of 'sensor_type'")

        self.__sensor_id = sensor_id
        self.__sensor_type = sensor_type

        super().__init__(**kwds)

    def validate(self, sensor_config: SensorConfig) -> None:
        """
        Validates this sensor reading event -- i.e. checks whether the affected
        sensor is part of the given sensor configuration.

        Parameters
        ----------
        sensor_config : :class:`~epyt_flow.simulation.sensor_config.SensorConfig`
            Sensor configuration.
        """
        if not isinstance(sensor_config, SensorConfig):
            raise TypeError("'sensor_config' must be an instance of " +
                            "'epyt_flow.simulation.SensorConfig' but not of " +
                            f"'{type(sensor_config)}'")

        def __show_warning() -> None:
            warnings.warn("Event does not have any effect because there is " +
                          f"no sensor at '{self.__sensor_id}'")

        if self.__sensor_type == SENSOR_TYPE_NODE_PRESSURE:
            if self.__sensor_id not in sensor_config.pressure_sensors:
                __show_warning()
        elif self.__sensor_type == SENSOR_TYPE_NODE_QUALITY:
            if self.__sensor_id not in sensor_config.quality_node_sensors:
                __show_warning()
        elif self.__sensor_type == SENSOR_TYPE_NODE_DEMAND:
            if self.__sensor_id not in sensor_config.demand_sensors:
                __show_warning()
        elif self.__sensor_type == SENSOR_TYPE_LINK_FLOW:
            if self.__sensor_id not in sensor_config.flow_sensors:
                __show_warning()
        elif self.__sensor_type == SENSOR_TYPE_LINK_QUALITY:
            if self.__sensor_id not in sensor_config.quality_link_sensors:
                __show_warning()
        elif self.__sensor_type == SENSOR_TYPE_VALVE_STATE:
            if self.__sensor_id not in sensor_config.valve_state_sensors:
                __show_warning()
        elif self.__sensor_type == SENSOR_TYPE_PUMP_STATE:
            if self.__sensor_id not in sensor_config.pump_state_sensors:
                __show_warning()
        elif self.__sensor_type == SENSOR_TYPE_TANK_VOLUME:
            if self.__sensor_id not in sensor_config.tank_volume_sensors:
                __show_warning()
        elif self.__sensor_type == SENSOR_TYPE_NODE_BULK_SPECIES:
            if self.__sensor_id not in sensor_config.bulk_species_node_sensors:
                __show_warning()
        elif self.__sensor_type == SENSOR_TYPE_LINK_BULK_SPECIES:
            if self.__sensor_id not in sensor_config.bulk_species_link_sensors:
                __show_warning()
        elif self.__sensor_type == SENSOR_TYPE_SURFACE_SPECIES:
            if self.__sensor_id not in sensor_config.surface_species_sensors:
                __show_warning()

    @property
    def sensor_id(self) -> str:
        """
        Gets the ID of the node or link that is affected by this event.

        Returns
        -------
        `str`
            Node or link ID.
        """
        return self.__sensor_id

    @property
    def sensor_type(self) -> int:
        """
        Gets the sensor type code.

        Returns
        -------
        `int`
            Sensor type code.
        """
        return self.__sensor_type

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"sensor_id": self.__sensor_id,
                                           "sensor_type": self.__sensor_type}

    def __eq__(self, other) -> bool:
        if not isinstance(other, SensorReadingEvent):
            raise TypeError("Can not compare 'SensorReadingEvent' instance " +
                            f"with '{type(other)}' instance")

        return super().__eq__(other) and self.__sensor_id == other.sensor_id \
            and self.__sensor_type == other.sensor_type

    def __str__(self) -> str:
        return f"{super().__str__()} sensor_id: {self.__sensor_id} " +\
            f"sensor_type: {self.__sensor_type}"

    def __call__(self, sensor_readings: numpy.ndarray,
                 sensor_readings_time: numpy.ndarray) -> numpy.ndarray:
        return self.apply(sensor_readings, sensor_readings_time)

    @abstractmethod
    def apply(self, sensor_readings: numpy.ndarray,
              sensor_readings_time: numpy.ndarray) -> numpy.ndarray:
        """
        Applies the sensor reading event to sensor reading values -- i.e.
        modify the sensor readings.

        Parameters
        ----------
        sensor_readings : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Original sensor readings.
        sensor_readings_time : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Time (seconds since simulation start) for each sensor reading row in 'sensor_readings'.

        Returns
        -------
        `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Modified sensor readings.
        """
        raise NotImplementedError()
