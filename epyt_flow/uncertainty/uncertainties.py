"""
Module provides classes for implementing different types of uncertainties.
"""
from abc import ABC, abstractmethod
import numpy as np

from .utils import generate_deep_random_gaussian_noise, create_deep_random_pattern
from ..serialization import serializable, JsonSerializable, ABSOLUTE_GAUSSIAN_UNCERTAINTY_ID, \
    RELATIVE_GAUSSIAN_UNCERTAINTY_ID, ABSOLUTE_UNIFORM_UNCERTAINTY_ID, \
    RELATIVE_UNIFORM_UNCERTAINTY_ID, ABSOLUTE_DEEP_UNIFORM_UNCERTAINTY_ID, \
    RELATIVE_DEEP_UNIFORM_UNCERTAINTY_ID, ABSOLUTE_DEEP_GAUSSIAN_UNCERTAINTY_ID, \
    RELATIVE_DEEP_GAUSSIAN_UNCERTAINTY_ID, ABSOLUTE_DEEP_UNCERTAINTY_ID, \
    RELATIVE_DEEP_UNCERTAINTY_ID, PERCENTAGE_DEVIATON_UNCERTAINTY_ID


class Uncertainty(ABC):
    """
    Base class for uncertainties -- i.e. perturbations of data/signals.

    Parameters
    ----------
    min_value : `float`, optional
        Lower bound on the data/signal that is perturbed by this uncertainty.

        The default is None.
    max_value : `float`, optional
        Upper bound on the data/signal that is perturbed by this uncertainty.

        The default is None.
    """
    def __init__(self, min_value: float = None, max_value: float = None, **kwds):
        super().__init__(**kwds)

        self.__min_value = min_value
        self.__max_value = max_value

    @property
    def min_value(self) -> float:
        """
        Gets the lower bound on the data/signal.

        Returns
        -------
        `float`
            Lower bound.
        """
        return self.__min_value

    @property
    def max_value(self) -> float:
        """
        Gets the upper bound on the data/signal.

        Returns
        -------
        `float`
            Upper bound.
        """
        return self.__max_value

    def get_attributes(self) -> dict:
        """
        Gets all attributes to be serialized -- these attributes are passed to the
        constructor when the object is deserialized.

        Returns
        -------
        `dict`
            Dictionary of attributes -- i.e. pairs of attribute name + value.
        """
        return {"min_value": self.__min_value, "max_value": self.__max_value}

    def __eq__(self, other) -> bool:
        if not isinstance(other, Uncertainty):
            raise TypeError("Can not compare 'Uncertainty' instance " +
                            f"with '{type(other)}' instance")

        return self.__min_value == other.min_value and self.__max_value == other.max_value

    def __str__(self) -> str:
        return f"min_value: {self.__min_value} max_value: {self.__max_value}"

    def clip(self, data: np.ndarray) -> np.ndarray:
        """
        Clips values in a given array -- i.e. every value must be in [min_value, max_value].

        Parameters
        ----------
        data : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Array to be clipped.

        Returns
        -------
        `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Clipped data.
        """
        if self.__min_value is not None:
            data = np.min([data, self.__min_value])
        if self.__max_value is not None:
            data = np.max([data, self.__max_value])

        return data

    @abstractmethod
    def apply(self, data: float):
        """
        Applies the uncertainty to a single value.

        Parameters
        ----------
        data : `float`
            The value to which the uncertainty is applied.

        Returns
        -------
        `float`
            Uncertainty applied to 'data'.
        """
        raise NotImplementedError()

    def apply_batch(self, data: np.ndarray) -> np.ndarray:
        """
        Applies the uncertainty to an array of values.

        Parameters
        ----------
        data : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Array of values to which the uncertainty is applied.

        Returns
        -------
        `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Uncertainty applied to `data`.
        """
        for t in range(data.shape[0]):
            data[t] = self.apply(data[t])
        return data


class GaussianUncertainty(Uncertainty):
    """
    Base class implementing Gaussian uncertainty

    Parameters
    ----------
    mean : `float`, optional
        Mean of the Gaussian noise.

        If None, mean will be assigned a random value between 0 and 1.

        The default is None.
    scale : `float`, optional
        Scale (i.e. standard deviation) of the Gaussian noise.

        If None, scale will be assigned a random value between 0 and 1.

        The default is None.
    """
    def __init__(self, mean: float = None, scale: float = None, **kwds):
        super().__init__(**kwds)

        self.__mean = np.random.rand() if mean is None else mean
        self.__scale = np.random.rand() if scale is None else scale

    @property
    def mean(self) -> float:
        """
        Gets the mean of the Gaussian noise.

        Returns
        -------
        `float`
            Mean of the Gaussian noise.
        """
        return self.__mean

    @property
    def scale(self) -> float:
        """
        Gets the scale (i.e. standard deviation) of the Gaussian noise.

        Returns
        -------
        `float`
            Scale (i.e. standard deviation) of the Gaussian noise.
        """
        return self.__scale

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"mean": self.__mean, "scale": self.__scale}

    def __eq__(self, other) -> bool:
        if not isinstance(other, GaussianUncertainty):
            raise TypeError("Can not compare 'GaussianUncertainty' instance " +
                            f"with '{type(other)}' instance")

        return super().__eq__(other) and self.__mean == other.mean and self.__scale == other.scale

    def __str__(self) -> str:
        return super().__str__() + f" mean: {self.__mean} scale: {self.__scale}"


@serializable(ABSOLUTE_GAUSSIAN_UNCERTAINTY_ID, ".epytflow_uncertainty_absolute_gaussian")
class AbsoluteGaussianUncertainty(GaussianUncertainty, JsonSerializable):
    """
    Class implementing absolute Gaussian uncertainty -- i.e. Gaussian noise is added to the data.
    """
    def apply(self, data: float) -> float:
        data += np.random.normal(loc=self.mean, scale=self.scale)

        return self.clip(data)


@serializable(RELATIVE_GAUSSIAN_UNCERTAINTY_ID, ".epytflow_uncertainty_relative_gaussian")
class RelativeGaussianUncertainty(GaussianUncertainty, JsonSerializable):
    """
    Class implementing relative Gaussian uncertainty -- i.e. data is perturbed by Gaussian noise
    centered at zero.

    Parameters
    ----------
    scale : `float`, optional
        Scale (i.e. standard deviation) of the Gaussian noise.

        If None, scale will be assigned a random value between 0 and 1.

        The default is None.
    """
    def __init__(self, scale: float = None, **kwds):
        super().__init__(mean=0., scale=scale, **kwds)

    def apply(self, data: float) -> float:
        data += np.random.normal(loc=0, scale=self.scale)

        return self.clip(data)


class UniformUncertainty(Uncertainty):
    """
    Base class implementing uniform uncertainty.

    Parameters
    ----------
    low : `float`, optional
        Lower bound of the uniform noise.

        The default is zero.
    high : `float`, optional
        Upper bound of the uniform noise.

        The default is one.
    """
    def __init__(self, low: float = 0., high: float = 1., **kwds):
        super().__init__(**kwds)

        self.__low = low
        self.__high = high

    @property
    def low(self) -> float:
        """
        Gets the lower bound of the uniform noise.

        Returns
        -------
        `float`
            Lower bound of the uniform noise.
        """
        return self.__low

    @property
    def high(self) -> float:
        """
        Gets the upper bound of the uniform noise.

        Returns
        -------
        `float`
            Upper bound of the uniform noise.
        """
        return self.__high

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"low": self.__low, "high": self.__high}

    def __eq__(self, other) -> bool:
        if not isinstance(other, UniformUncertainty):
            raise TypeError("Can not compare 'UniformUncertainty' instance " +
                            f"with '{type(other)}' instance")

        return super().__eq__(other) and self.__low == other.low and self.__high == other.high

    def __str__(self) -> str:
        return super().__str__() + f" low: {self.__low} high: {self.__high}"


@serializable(ABSOLUTE_UNIFORM_UNCERTAINTY_ID, ".epytflow_uncertainty_absolute_uniform")
class AbsoluteUniformUncertainty(UniformUncertainty, JsonSerializable):
    """
    Class implementing absolute uniform uncertainty -- i.e. uniform noise is added to the data.
    """
    def apply(self, data: float) -> float:
        data += np.random.uniform(low=self.low, high=self.high)

        return self.clip(data)


@serializable(RELATIVE_UNIFORM_UNCERTAINTY_ID, ".epytflow_uncertainty_relative_uniform")
class RelativeUniformUncertainty(UniformUncertainty, JsonSerializable):
    """
    Class implementing relative uniform uncertainty -- i.e. data is multiplied by uniform noise.
    """
    def apply(self, data: float) -> float:
        data *= np.random.uniform(low=self.low, high=self.high)

        return self.clip(data)


@serializable(PERCENTAGE_DEVIATON_UNCERTAINTY_ID, ".epytflow_uncertainty_percentage_deviation")
class PercentageDeviationUncertainty(UniformUncertainty, JsonSerializable):
    """
    Class implementing a uniform data deviation -- i.e. the data can deviate up to some percentage
    from its original value.

    Parameters
    ----------
    deviation_percentage : `float`
        Percentage (0-1) the data can deviate from its original value.
    """
    def __init__(self, deviation_percentage: float, **kwds):
        if not isinstance(deviation_percentage, float):
            raise TypeError("'deviation_percentage' must be an instance of 'float' " +
                            f"but not of {type(deviation_percentage)}")
        if not 0 < deviation_percentage < 1:
            raise ValueError("'deviation_percentage' must be in (0,1)")

        if "low" in kwds:
            del kwds["low"]
        if "high" in kwds:
            del kwds["high"]

        super().__init__(low=1. - deviation_percentage, high=1. + deviation_percentage, **kwds)

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"deviation_percentage": self.high - 1.}

    def apply(self, data: float) -> float:
        data *= np.random.uniform(low=self.low, high=self.high)

        return self.clip(data)


class DeepUniformUncertainty(Uncertainty):
    """
    Base class implementing deep uniform uncertainty.
    """
    def __init__(self, **kwds):
        super().__init__(**kwds)

        self.__create_uncertainties()

    def __create_uncertainties(self, n_samples: int = 500):
        self._uncertainties_idx = 0
        rand_low = create_deep_random_pattern(n_samples)
        rand_high = create_deep_random_pattern(n_samples)
        rand_low = np.minimum(rand_low, rand_high)
        rand_high = np.maximum(rand_low, rand_high)
        self._uncertainties = [np.random.uniform(low, high)
                               for low, high in zip(rand_low, rand_high)]

    @abstractmethod
    def apply(self, data: float) -> float:
        self._uncertainties_idx += 1
        if self._uncertainties_idx >= len(self._uncertainties):
            self.__create_uncertainties()

        return self.clip(data)


@serializable(ABSOLUTE_DEEP_UNIFORM_UNCERTAINTY_ID, ".epytflow_uncertainty_absolute_deep_uniform")
class AbsoluteDeepUniformUncertainty(DeepUniformUncertainty, JsonSerializable):
    """
    Class implementing absolute deep uniform uncertainty -- i.e. random uniform noise
    (shape of the noise is changing over time) is added to the data.
    """
    def apply(self, data: float) -> float:
        data += self._uncertainties[self._uncertainties_idx]

        return super().apply(data)


@serializable(RELATIVE_DEEP_UNIFORM_UNCERTAINTY_ID, ".epytflow_uncertainty_relative_deep_uniform")
class RelativeDeepUniformUncertainty(DeepUniformUncertainty, JsonSerializable):
    """
    Class implementing relative deep uniform uncertainty -- i.e. data is multiplied by
    random uniform noise (shape of the noise is changing over time).
    """
    def apply(self, data: float) -> float:
        data *= self._uncertainties[self._uncertainties_idx]

        return super().apply(data)


class DeepGaussianUncertainty(Uncertainty, JsonSerializable):
    """
    Base class implementing deep Gaussian uncertainty.

    Parameters
    ----------
    mean : `float`, optional
        Fixed mean of Gaussian noise.
        If None, random means are generated.

        The default is None.
    """
    def __init__(self, mean: float = None, **kwds):
        self.__mean = mean

        super().__init__(**kwds)

        self.__create_uncertainties()

    def __create_uncertainties(self, n_samples: int = 500) -> None:
        self._uncertainties_idx = 0
        self._uncertainties = generate_deep_random_gaussian_noise(n_samples, self.__mean)

    @abstractmethod
    def apply(self, data: float) -> float:
        self._uncertainties_idx += 1
        if self._uncertainties_idx >= len(self._uncertainties):
            self.__create_uncertainties()

        return self.clip(data)


@serializable(ABSOLUTE_DEEP_GAUSSIAN_UNCERTAINTY_ID, ".epytflow_uncertainty_absolute_deep_gaussian")
class AbsoluteDeepGaussianUncertainty(DeepGaussianUncertainty, JsonSerializable):
    """
    Class implementing absolute deep Gaussian uncertainty -- i.e. random Gaussian noise
    (mean and variance are changing over time) is added to the data.
    """
    def apply(self, data: float) -> float:
        data += self._uncertainties[self._uncertainties_idx]

        return super().apply(data)


@serializable(RELATIVE_DEEP_GAUSSIAN_UNCERTAINTY_ID, ".epytflow_uncertainty_relative_deep_gaussian")
class RelativeDeepGaussianUncertainty(DeepGaussianUncertainty, JsonSerializable):
    """
    Class implementing realtive deep Gaussian uncertainty -- i.e. data is multiplied by
    random Gaussian noise (mean and variance are changing over time).
    """
    def __init__(self, **kwds):
        super().__init__(mean=0., **kwds)

    def apply(self, data: float) -> float:
        data += self._uncertainties[self._uncertainties_idx]

        return super().apply(data)


class DeepUncertainty(Uncertainty):
    """
    Base class implementing deep uncertainty.

    Parameters
    ----------
    min_noise_value : `float`
        Lower bound on the noise.
    max_noise_value : `float`
        Upper bound on the noise.
    """
    def __init__(self, min_noise_value: float = 0., max_noise_value: float = 1., **kwds):
        super().__init__(**kwds)

        self.__min_noise_value = min_noise_value
        self.__max_noise_value = max_noise_value

        self._uncertainties_idx = None
        self._uncertainties = None
        self.__create_uncertainties()

    @property
    def min_noise_value(self) -> float:
        """
        Gets the lower bound on the noise.

        Returns
        -------
        `float`
            Lower bound on the noise.
        """
        return self.__min_noise_value

    @property
    def max_noise_value(self) -> float:
        """
        Gets the upper bound on the noise.

        Returns
        -------
        `float`
            Upper bound on the noise.
        """
        return self.__max_noise_value

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"min_noise_value": self.__min_noise_value,
                                           "max_noise_value": self.__max_noise_value}

    def __eq__(self, other) -> bool:
        if not isinstance(other, DeepUncertainty):
            raise TypeError("Can not compare 'DeepUncertainty' instance " +
                            f"with '{type(other)}' instance")

        return super().__eq__(other) and self.__min_noise_value == other.min_noise_value and \
            self.__max_noise_value == other.max_noise_value

    def __str__(self) -> str:
        return super().__str__() + f" min_noise_value: {self.__min_noise_value} " +\
            f"max_noise_value: {self.__max_noise_value}"

    def __create_uncertainties(self, n_samples: int = 500) -> None:
        init_value = None
        if self._uncertainties_idx is not None:
            init_value = self._uncertainties[-1]

        self._uncertainties_idx = 0
        self._uncertainties = create_deep_random_pattern(n_samples, self.__min_noise_value,
                                                         self.__max_noise_value, init_value)

    @abstractmethod
    def apply(self, data: float) -> float:
        self._uncertainties_idx += 1
        if self._uncertainties_idx >= len(self._uncertainties):
            self.__create_uncertainties()

        return self.clip(data)


@serializable(ABSOLUTE_DEEP_UNCERTAINTY_ID, ".epytflow_uncertainty_absolute_deep")
class AbsoluteDeepUncertainty(DeepUncertainty, JsonSerializable):
    """
    Class implementing absolute deep uncertainty -- i.e. completely random noise
    is added to the data.
    """
    def apply(self, data: float) -> float:
        data += self._uncertainties[self._uncertainties_idx]

        return super().apply(data)


@serializable(RELATIVE_DEEP_UNCERTAINTY_ID, ".epytflow_uncertainty_relative_deep")
class RelativeDeepUncertainty(DeepUncertainty, JsonSerializable):
    """
    Class implementing relative deep uncertainty -- i.e. data is multiplied by
    completely random noise.
    """
    def apply(self, data: float) -> float:
        data *= self._uncertainties[self._uncertainties_idx]

        return super().apply(data)
