from abc import abstractmethod
import numpy
import numpy as np

from .sensor_reading_event import SensorReadingEvent
from ...serialization import serializable, Serializable, SENSOR_FAULT_CONSTANT_ID,\
    SENSOR_FAULT_DRIFT_ID, SENSOR_FAULT_GAUSSIAN_ID, SENSOR_FAULT_PERCENTAGE_ID,\
    SENSOR_FAULT_STUCKATZERO_ID


class SensorFault(SensorReadingEvent):
    """
    Base class for a sensor fault

    Acknowledgement: This Python implementation is based on
    https://github.com/eldemet/sensorfaultmodels/blob/main/sensorfaultmodels.m
    and https://github.com/Mariosmsk/sensorfaultmodels/blob/main/sensorfaultmodels.py
    """
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def compute_multiplier(self, cur_time:int) -> float:
        b1 = 0
        b2 = 0
        a1 = 1
        a2 = 1

        if cur_time >= self.start_time:
            b1 = 1 - np.exp(- a1 * (cur_time - self.start_time))

        if cur_time >= self.end_time:
            b2 = 1 - np.exp(- a2 * (cur_time - self.end_time))

        return b1 - b2

    @abstractmethod
    def apply_sensor_fault(self, b, sensor_reading:float, cur_time:int) -> float:
        raise NotImplementedError()

    def apply(self, sensor_readings:numpy.ndarray,
              sensor_readings_time:numpy.ndarray) -> numpy.ndarray:
        for i in range(sensor_readings.shape[0]):
            t = sensor_readings_time[i]
            sensor_readings[i] = self.apply_sensor_fault(self.compute_multiplier(t),
                                                         sensor_readings[i], t)

        return sensor_readings


@serializable(SENSOR_FAULT_CONSTANT_ID)
class SensorFaultConstant(SensorFault, Serializable):
    """
    Class implementing a constant shift sensor fault.

    Parameters
    ----------
    constant_shift : `float`
        Constant that is added to the sensor reading.
    """
    def __init__(self, constant_shift:float, **kwds):
        if not isinstance(constant_shift, float):
            raise ValueError("'constant_shift' must be an instance of 'float' but no of "+\
                             f"'{type(constant_shift)}'")

        self.__constant_shift = constant_shift

        super().__init__(**kwds)

    @property
    def constant_shift(self) -> float:
        return self.__constant_shift

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"constant_shift": self.__constant_shift}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__constant_shift == other.constant_shift

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()} constant: {self.__constant_shift}"

    def apply_sensor_fault(self, b:float, sensor_reading:float, cur_time:int) -> float:
        return sensor_reading + b * self.__constant_shift


@serializable(SENSOR_FAULT_DRIFT_ID)
class SensorFaultDrift(SensorFault, Serializable):
    """
    Class implementing a drift sensor fault.

    Parameters
    ----------
    coef : `float`
        Coefficient of the drift.
    """
    def __init__(self, coef:float, **kwds):
        self.__coef = coef

        super().__init__(**kwds)

    @property
    def coef(self) -> float:
        return self.__coef

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"coef": self.__coef}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__coef == other.coef

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()} coef: {self.__coef}"

    def apply_sensor_fault(self, b:float, sensor_reading:float, cur_time:int) -> float:
        return sensor_reading + b * (self.__coef * (cur_time - self.start_time))


@serializable(SENSOR_FAULT_GAUSSIAN_ID)
class SensorFaultGaussian(SensorFault, Serializable):
    """
    Class implementing a Gaussian shift sensor fault -- i.e. 
    adding Gaussian noise (centered at zero) to the sensor reading.

    Parameters
    ----------
    std : `float`
        Standard deviation of the Gaussian noise.
    """
    def __init__(self, std:float, **kwds):
        if not isinstance(std, float) or not std > 0:
            raise ValueError("'std' must be an instance of 'float' and be greater than 0")

        self.__std = std

        super().__init__(**kwds)

    @property
    def std(self) -> float:
        return self.__std

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"std": self.__std}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__std == other.std

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()} std: {self.__std}"

    def apply_sensor_fault(self, b:float, sensor_reading:float, cur_time:int) -> float:
        return sensor_reading + b * np.random.normal(loc=0, scale=self.__std)


@serializable(SENSOR_FAULT_PERCENTAGE_ID)
class SensorFaultPercentage(SensorFault, Serializable):
    """
    Class implementing a percentage shift sensor fault.

    Parameters
    ----------
    coef : `float`
        Coefficient (percentage) of the shift -- i.e. coef must be in (0,].
    """
    def __init__(self, coef:float, **kwds):
        if not isinstance(coef, float) or not coef > 0:
            raise ValueError("'coef' must be an instance of 'float' and be greater than zero.")

        self.__coef = coef

        super().__init__(**kwds)

    @property
    def coef(self) -> float:
        return self.__coef

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"coef": self.__coef}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__coef == other.coef

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()} coef: {self.__coef}"

    def apply_sensor_fault(self, b:float, sensor_reading:float, cur_time:int) -> float:
        return sensor_reading + b * self.__coef * sensor_reading


@serializable(SENSOR_FAULT_STUCKATZERO_ID)
class SensorFaultStuckZero(SensorFault, Serializable):
    """
    Class implementing a stuck-at-zero sensor fault -- i.e. sensor reading is set to zero.
    """
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def get_attributes(self) -> dict:
        return super().get_attributes()

    def __eq__(self, other) -> bool:
        return super().__eq__(other)

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()}"

    def apply_sensor_fault(self, b:float, sensor_reading:float, cur_time:int) -> float:
        return sensor_reading + b * (-1. * sensor_reading)
