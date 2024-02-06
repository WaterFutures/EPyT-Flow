from abc import abstractmethod
import numpy

from .event import Event


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
    """
    def __init__(self, sensor_id:str, sensor_type:int, **kwds):
        if not isinstance(sensor_id, str):
            raise ValueError("'sensor_id' must be an instance of 'str' but not of "+\
                             f"'{type(sensor_id)}'")
        if not isinstance(sensor_type, int):
            raise ValueError("'sensor_type' mut be an instance of 'int' but not of "+\
                             f"'{type(sensor_type)}'")
        if not(sensor_type >= 1 and sensor_type <= 5):
            raise ValueError("Invalid value of 'sensor_type'")

        self.__sensor_id = sensor_id
        self.__sensor_type = sensor_type

        super().__init__(**kwds)

    @property
    def sensor_id(self) -> int:
        return self.__sensor_id

    @property
    def sensor_type(self) -> int:
        return self.__sensor_type

    def get_attributes(self) -> dict:
        return {"sensor_id": self.__sensor_id, "sensor_type": self.__sensor_type}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__sensor_id == other.sensor_id \
            and self.__sensor_type == other.sensor_type

    def __str__(self) -> str:
        return f"{super().__str__()} sensor_id: {self.__sensor_id} "+\
            f"sensor_type: {self.__sensor_type}"

    @abstractmethod
    def apply(self, sensor_readings:numpy.ndarray,
              sensor_readings_time:numpy.ndarray) -> numpy.ndarray:
        """
        Applies the sensor reading event to sensor reading values -- i.e. 
        modify the sensor readings.

        Parameters
        ----------
        sensor_readings : `numpy.ndarray`
            Original sensor readings.
        sensor_readings_time : `numpy.ndarray`
            Time (seconds since simulation start) for each sensor reading row in 'sensor_readings'.
        
        Returns
        -------
        `numpy.ndarray`
            Modified sensor readings.
        """
        raise NotImplementedError()