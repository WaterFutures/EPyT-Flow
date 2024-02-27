"""
Module provides classes for implementing different types of uncertainties.
"""
from abc import ABC, abstractmethod
import numpy as np

from .utils import generate_deep_random_gaussian_noise, create_deep_random_pattern
from ..serialization import serializable, Serializable, GAUSSIAN_UNCERTAINTY_ID, \
    UNIFORM_UNCERTAINTY_ID, DEEP_UNIFORM_UNCERTAINTY_ID, DEEP_GAUSSIAN_UNCERTAINTY_ID, \
    DEEP_UNCERTAINTY_ID


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
        return {"min_value": self.__min_value, "max_value": self.__max_value}

    def __eq__(self, other) -> bool:
        return self.__min_value == other.min_value and self.__max_value == other.max_value

    def __str__(self) -> str:
        return f"min_value: {self.__min_value} max_value: {self.__max_value}"

    def clip(self, data: np.ndarray) -> np.ndarray:
        if self.__min_value is not None:
            data = np.min([data, self.__min_value])
        if self.__max_value is not None:
            data = np.max([data, self.__max_value])

        return data

    @abstractmethod
    def apply(self, data: float):
        raise NotImplementedError()

    def apply_batch(self, data: np.ndarray) -> np.ndarray:
        for t in range(data.shape[0]):
            data[t] = self.apply(data[t])
        return data


@serializable(GAUSSIAN_UNCERTAINTY_ID, ".epytflow_uncertainty_gaussian")
class GaussianUncertainty(Uncertainty, Serializable):
    """
    Class implementing Gaussian uncertainty -- i.e. Gaussian noise is added to the data.

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

        self.__create_uncertainties()

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
        return super().__eq__(other) and self.__mean == other.mean and self.__scale == other.scale

    def __str__(self) -> str:
        return super().__str__() + f" mean: {self.__mean} scale: {self.__scale}"

    def __create_uncertainties(self, n_samples: int = 500) -> None:
        self.__uncertainties_idx = 0
        self.__uncertainties = np.random.normal(self.__mean, self.__scale, size=n_samples)

    def apply(self, data: float) -> float:
        data += self.__uncertainties[self.__uncertainties_idx]

        self.__uncertainties_idx += 1
        if self.__uncertainties_idx >= len(self.__uncertainties):
            self.__create_uncertainties()

        return self.clip(data)


@serializable(UNIFORM_UNCERTAINTY_ID, ".epytflow_uncertainty_uniform")
class UniformUncertainty(Uncertainty, Serializable):
    """
    Class implementing uniform uncertainty -- i.e. uniform noise is added to the data.

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
        return super().__eq__(other) and self.__low == other.low and self.__high == other.high

    def __str__(self) -> str:
        return super().__str__() + f" low: {self.__low} high: {self.__high}"

    def apply(self, data: float) -> float:
        data += np.random.uniform(low=self.__low, high=self.__high)

        return self.clip(data)


@serializable(DEEP_UNIFORM_UNCERTAINTY_ID, ".epytflow_uncertainty_deep_uniform")
class DeepUniformUncertainty(Uncertainty, Serializable):
    """
    Class implementing deep uniform uncertainty -- i.e. random uniform noise
    (shape of the noise is changing over time) is added to the data.
    """
    def __init__(self, **kwds):
        super().__init__(**kwds)

        self.__create_uncertainties()

    def __create_uncertainties(self, n_samples: int = 500):
        self.__uncertainties_idx = 0
        rand_low = create_deep_random_pattern(n_samples)
        rand_high = create_deep_random_pattern(n_samples)
        rand_low = np.minimum(rand_low, rand_high)
        rand_high = np.maximum(rand_low, rand_high)
        self.__uncertainties = [np.random.uniform(low, high)
                                for low, high in zip(rand_low, rand_high)]

    def apply(self, data: float) -> float:
        data += self.__uncertainties[self.__uncertainties_idx]

        self.__uncertainties_idx += 1
        if self.__uncertainties_idx >= len(self.__uncertainties):
            self.__create_uncertainties()

        return self.clip(data)


@serializable(DEEP_GAUSSIAN_UNCERTAINTY_ID, ".epytflow_uncertainty_deep_gaussian")
class DeepGaussianUncertainty(Uncertainty, Serializable):
    """
    Class implementing deep Gaussian uncertainty -- i.e. random Gaussian noise
    (mean and variance are changing over time) is added to the data.
    """
    def __init__(self, **kwds):
        super().__init__(**kwds)

        self.__create_uncertainties()

    def __create_uncertainties(self, n_samples: int = 500) -> None:
        self.__uncertainties_idx = 0
        self.__uncertainties = generate_deep_random_gaussian_noise(n_samples)

    def apply(self, data: float) -> float:
        data += self.__uncertainties[self.__uncertainties_idx]

        self.__uncertainties_idx += 1
        if self.__uncertainties_idx >= len(self.__uncertainties):
            self.__create_uncertainties()

        return self.clip(data)


@serializable(DEEP_UNCERTAINTY_ID, ".epytflow_uncertainty_deep")
class DeepUncertainty(Uncertainty, Serializable):
    """
    Class implementing deep uncertainty -- i.e. completly random noise is added to the data.

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

        self.__uncertainties_idx = None
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
        return super().__eq__(other) and self.__min_noise_value == other.min_noise_value and \
            self.__max_noise_value == other.max_noise_value

    def __str__(self) -> str:
        return super().__str__() + f" min_noise_value: {self.__min_noise_value} " +\
            f"max_noise_value: {self.__max_noise_value}"

    def __create_uncertainties(self, n_samples: int = 500) -> None:
        init_value = None
        if self.__uncertainties_idx is not None:
            init_value = self.__uncertainties[-1]

        self.__uncertainties_idx = 0
        self.__uncertainties = create_deep_random_pattern(n_samples, self.__min_value,
                                                          self.__max_value, init_value)

    def apply(self, data: float) -> float:
        data += self.__uncertainties[self.__uncertainties_idx]

        self.__uncertainties_idx += 1
        if self.__uncertainties_idx >= len(self.__uncertainties):
            self.__create_uncertainties()

        return self.clip(data)
