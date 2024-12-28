"""
Module provides a class for implementing sensor noise (e.g. uncertainty in sensor readings).
"""
from copy import deepcopy
import warnings
from typing import Callable
import numpy

from .uncertainties import Uncertainty
from ..serialization import serializable, JsonSerializable, SENSOR_NOISE_ID


@serializable(SENSOR_NOISE_ID, ".epytflow_sensor_noise")
class SensorNoise(JsonSerializable):
    """
    Class implementing sensor noise/uncertainty.

    Parameters
    ----------
    global_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Global sensor uncertainty. If None, no global sensor uncertainties are applied.

        The default is None.
    local_uncertainties : dict[tuple[int, str], :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`], optional
        Local (i.e. sensor specific) uncertainties.
        If None, no local sensor uncertainties are applied.

        The default is None.
    """
    def __init__(self, uncertainty: Uncertainty = None,
                 global_uncertainty: Uncertainty = None,
                 local_uncertainties: dict[int, str, Uncertainty] = None,
                 **kwds):
        if uncertainty is not None:
            global_uncertainty = uncertainty
            warnings.warn("'uncertainty' is deprecated and will be removed in future releases. " +
                          "Use 'global_uncertainty' instead")

        if not isinstance(global_uncertainty, Uncertainty):
            raise TypeError("'uncertainty' must be an instance of " +
                            "'epyt_flow.uncertainty.Uncertainty' but not of " +
                            f"'{type(global_uncertainty)}'")
        if local_uncertainties is not None:
            if not isinstance(local_uncertainties, dict):
                raise TypeError("'local_uncertainties' must be an instance of " +
                                "'dict[tuple[int, str], epyt_flow.uncertainty.Uncertainty]' "+
                                f"but not of '{type(local_uncertainties)}'")
            if any(not isinstance(key[0], int) or not isinstance(key[1], str) or
                   not isinstance(local_uncertainties[key], Uncertainty)
                   for key in local_uncertainties.keys()):
                raise TypeError("'local_uncertainties' must be an instance of " +
                                "'dict[tuple[int, str], epyt_flow.uncertainty.Uncertainty]'")

        self.__global_uncertainty = global_uncertainty
        self.__local_uncertainties = local_uncertainties

        super().__init__(**kwds)

    @property
    def global_uncertainty(self) -> Uncertainty:
        """
        Returns the global sensor readings uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global sensor readings uncertainty.
        """
        return deepcopy(self.__global_uncertainty)

    @property
    def local_uncertainties(self) -> dict[int, str, Uncertainty]:
        """
        Returns the local (i.e. sensor specific) uncertainties.

        Returns
        -------
        dict[tuple[int, str], :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local (i.e. sensor specific) uncertainties.
        """
        return deepcopy(self.__local_uncertainties)

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"global_uncertainty": self.__global_uncertainty,
                                           "local_uncertainties": self.__local_uncertainties}

    def __eq__(self, other) -> bool:
        if not isinstance(other, SensorNoise):
            raise TypeError("Can not compare 'SensorNoise' instance " +
                            f"with '{type(other)}' instance")

        return super().__eq__(other) and self.__global_uncertainty == other.global_uncertainty and \
            self.__local_uncertainties == other.local_uncertainties

    def __str__(self) -> str:
        return f"global_uncertainty: {self.__global_uncertainty} " + \
            f"local_uncertainties: {self.__local_uncertainties}"

    def apply_local_uncertainty(self, map_sensor_to_idx: Callable[[int, str], int],
                                sensor_readings: numpy.ndarray) -> numpy.ndarray:
        """
        Applies the local (i.e. sensor specific) sensor uncertainties -- i.e. sensor readings
        are perturbed according to the specified uncertainties.

        Parameters
        ----------
        map_sensor_to_idx : `Callable[[int, str], int]`
            Function mapping sensor type (int) and sensor id (e.g. node id, link id, etc.) to indices
            in the final sensor readings.
        sensor_readings : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            All (global) sensor readings (no matter if ther).

        Returns
        -------
        `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Perturbed sensor readings.
        """
        if self.__local_uncertainties is None:
            return sensor_readings
        else:
            for (sensor_type, sensor_id), uncertainty in map_sensor_to_idx.items():
                idx = map_sensor_to_idx(sensor_type, sensor_id)
                sensor_readings[:, idx] = uncertainty.apply_batch(sensor_readings[:, idx])
                return sensor_readings

    def apply_global_uncertainty(self, sensor_readings: numpy.ndarray) -> numpy.ndarray:
        """
        Applies the global sensor uncertainty to given sensor readings -- i.e. sensor readings
        are perturbed according to the specified uncertainty.

        .. note::
            Note that state sensor readings such as valve states, pump states, etc.
            are NOT affected by sensor noise!

        Parameters
        ----------
        sensor_readings : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            All (global) senor readings.

        Returns
        -------
        `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Perturbed sensor readings.
        """
        if self.__global_uncertainty is None:
            return sensor_readings
        else:
            return self.__global_uncertainty.apply_batch(sensor_readings)
