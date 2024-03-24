"""
Module provides classes for implementing different sensor faults.
"""
from abc import abstractmethod
import numpy as np

from .sensor_reading_event import SensorReadingEvent
from ...serialization import serializable, JsonSerializable, SENSOR_FAULT_CONSTANT_ID, \
    SENSOR_FAULT_DRIFT_ID, SENSOR_FAULT_GAUSSIAN_ID, SENSOR_FAULT_PERCENTAGE_ID, \
    SENSOR_FAULT_STUCKATZERO_ID


class SensorFault(SensorReadingEvent):
    """
    Base class for a sensor fault
    """
    # Acknowledgement: This Python implementation is based on
    # https://github.com/eldemet/sensorfaultmodels/blob/main/sensorfaultmodels.m
    # and https://github.com/Mariosmsk/sensorfaultmodels/blob/main/sensorfaultmodels.py

    def compute_multiplier(self, cur_time: int) -> float:
        """
        Computes the multiplier for a given time stamp.

        Parameters
        ----------
        cur_time : `int`
            Time in seconds.

        Returns
        -------
        `float`
            Multiplier.
        """
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
    def apply_sensor_fault(self, cur_multiplier: float, sensor_reading: float,
                           cur_time: int) -> float:
        """
        Applies this sensor fault to a given single sensor reading value --
        i.e. the sensor reading value is perturbed by this fault.

        Parameters:
        -----------
        cur_multiplier : `float`
            Current multiplier -- i.e. controls the "strength" of the fault.
        sensor_reading : `float`
            Sensor reading value.
        cur_time : `int`
            Current time stamp (in seconds) in the simulation.

        Returns
        -------
        `float`
            Perturbed sensor reading value.
        """
        raise NotImplementedError()

    def apply(self, sensor_readings: np.ndarray,
              sensor_readings_time: np.ndarray) -> np.ndarray:
        for i in range(sensor_readings.shape[0]):
            t = sensor_readings_time[i]
            sensor_readings[i] = self.apply_sensor_fault(self.compute_multiplier(t),
                                                         sensor_readings[i], t)

        return sensor_readings


@serializable(SENSOR_FAULT_CONSTANT_ID, ".epytflow_sensorfault_constant")
class SensorFaultConstant(SensorFault, JsonSerializable):
    """
    Class implementing a constant shift sensor fault.

    Parameters
    ----------
    constant_shift : `float`
        Constant that is added to the sensor reading.
    """
    def __init__(self, constant_shift: float, **kwds):
        if not isinstance(constant_shift, float):
            raise TypeError("'constant_shift' must be an instance of 'float' but no of " +
                            f"'{type(constant_shift)}'")

        self.__constant_shift = constant_shift

        super().__init__(**kwds)

    @property
    def constant_shift(self) -> float:
        """
        Gets the Constant that is added to the sensor reading.

        Returns
        -------
        `float`
            Constant that is added to the sensor reading.
        """
        return self.__constant_shift

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"constant_shift": self.__constant_shift}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__constant_shift == other.constant_shift

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()} constant: {self.__constant_shift}"

    def apply_sensor_fault(self, cur_multiplier: float, sensor_reading: float,
                           cur_time: int) -> float:
        return sensor_reading + cur_multiplier * self.__constant_shift


@serializable(SENSOR_FAULT_DRIFT_ID, ".epytflow_sensorfault_drift")
class SensorFaultDrift(SensorFault, JsonSerializable):
    """
    Class implementing a drift sensor fault.

    Parameters
    ----------
    coef : `float`
        Coefficient of the drift.
    """
    def __init__(self, coef: float, **kwds):
        self.__coef = coef

        super().__init__(**kwds)

    @property
    def coef(self) -> float:
        """
        Gets the coefficient of the drift.

        Returns
        -------
        `float`
            Coefficient of the drift.
        """
        return self.__coef

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"coef": self.__coef}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__coef == other.coef

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()} coef: {self.__coef}"

    def apply_sensor_fault(self, cur_multiplier: float, sensor_reading: float,
                           cur_time: int) -> float:
        return sensor_reading + cur_multiplier * (self.__coef * (cur_time - self.start_time))


@serializable(SENSOR_FAULT_GAUSSIAN_ID, ".epytflow_sensorfault_gaussian")
class SensorFaultGaussian(SensorFault, JsonSerializable):
    """
    Class implementing a Gaussian shift sensor fault -- i.e.
     adding Gaussian noise (centered at zero) to the sensor reading.

    Parameters
    ----------
    std : `float`
        Standard deviation of the Gaussian noise.
    """
    def __init__(self, std: float, **kwds):
        if not isinstance(std, float) or not std > 0:
            raise ValueError("'std' must be an instance of 'float' and be greater than 0")

        self.__std = std

        super().__init__(**kwds)

    @property
    def std(self) -> float:
        """
        Gets the standard deviation of the Gaussian noise.

        Returns
        -------
        `float`
            Standard deviation of the Gaussian noise.
        """
        return self.__std

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"std": self.__std}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__std == other.std

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()} std: {self.__std}"

    def apply_sensor_fault(self, cur_multiplier: float, sensor_reading: float,
                           cur_time: int) -> float:
        return sensor_reading + cur_multiplier * np.random.normal(loc=0, scale=self.__std)


@serializable(SENSOR_FAULT_PERCENTAGE_ID, ".epytflow_sensorfault_percentage",)
class SensorFaultPercentage(SensorFault, JsonSerializable):
    """
    Class implementing a percentage shift sensor fault.

    Parameters
    ----------
    coef : `float`
        Coefficient (percentage) of the shift -- i.e. coef must be in (0,].
    """
    def __init__(self, coef: float, **kwds):
        if not isinstance(coef, float) or not coef > 0:
            raise ValueError("'coef' must be an instance of 'float' and be greater than zero.")

        self.__coef = coef

        super().__init__(**kwds)

    @property
    def coef(self) -> float:
        """
        Gets the coefficient (percentage) of the shift.

        Returns
        -------
        `float`
            Coefficient (percentage) of the shift.
        """
        return self.__coef

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"coef": self.__coef}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__coef == other.coef

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()} coef: {self.__coef}"

    def apply_sensor_fault(self, cur_multiplier: float, sensor_reading: float,
                           cur_time: int) -> float:
        return sensor_reading + cur_multiplier * self.__coef * sensor_reading


@serializable(SENSOR_FAULT_STUCKATZERO_ID, ".epytflow_sensorfault_zero")
class SensorFaultStuckZero(SensorFault, JsonSerializable):
    """
    Class implementing a stuck-at-zero sensor fault -- i.e. sensor reading is set to zero.
    """

    def __str__(self) -> str:
        return f"{type(self).__name__} {super().__str__()}"

    def apply_sensor_fault(self, cur_multiplier: float, sensor_reading: float,
                           cur_time: int) -> float:
        return sensor_reading + cur_multiplier * (-1. * sensor_reading)
