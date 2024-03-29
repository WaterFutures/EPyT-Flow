"""
Module provides a class for implementing sensor noise (e.g. uncertainty in sensor readings).
"""
from copy import deepcopy
import numpy

from .uncertainties import Uncertainty
from ..serialization import serializable, JsonSerializable, SENSOR_NOISE_ID


@serializable(SENSOR_NOISE_ID, ".epytflow_sensor_noise")
class SensorNoise(JsonSerializable):
    """
    Class implementing sensor noise/uncertainty.

    Parameters
    ----------
    uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
        Sensor uncertainty.
    """
    def __init__(self, uncertainty: Uncertainty, **kwds):
        if not isinstance(uncertainty, Uncertainty):
            raise TypeError("'uncertainty' must be an instance of " +
                            f"'epyt_flow.uncertainty.Uncertainty' not of {type(uncertainty)}")

        self.__uncertainty = uncertainty

        super().__init__(**kwds)

    @property
    def uncertainty(self) -> Uncertainty:
        """
        Gets the Sensor readings uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Sensor readings uncertainty.
        """
        return deepcopy(self.__uncertainty)

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"uncertainty": self.__uncertainty}

    def __eq__(self, other) -> bool:
        if not isinstance(other, SensorNoise):
            raise TypeError("Can not compare 'SensorNoise' instance " +
                            f"with '{type(other)}' instance")

        return self.__uncertainty == other.uncertainty

    def __str__(self) -> str:
        return f"uncertainty: {self.__uncertainty}"

    def apply(self, sensor_readings: numpy.ndarray) -> numpy.ndarray:
        """
        Applies the sensor uncertainty to given sensor readings -- i.e. sensor readings
        are perturbed according to the specified uncertainty.

        .. note::
            Note that state sensor readings such as valve states, pump states, etc.
            are NOT affected by sensor noise!

        Parameters
        ----------
        sensor_readings : `numpy.ndarray`

        Returns
        -------
        `numpy.ndarray`
            Perturbed sensor readings.
        """
        return self.__uncertainty.apply_batch(sensor_readings)
