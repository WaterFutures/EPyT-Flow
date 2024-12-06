"""
Module provides some helper functions regarding the implementation of uncertainty.
"""
import numpy as np
from scipy.ndimage import gaussian_filter1d


def smoothing(pattern: np.ndarray, sigma: float = 10.) -> np.ndarray:
    """
    Smoothes a given pattern by applying a Gaussian filter.

    Parameters
    ----------
    pattern : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        The original pattern
    sigma : `float`, optional
        Standard deviation for the Gaussian filter.

        The default is 10.

    Returns
    -------
    `numpy.ndarray`
        The smoothed pattern.
    """
    return gaussian_filter1d(pattern, sigma=sigma)


def scale_to_range(pattern: np.ndarray, min_value: float, max_value: float) -> np.ndarray:
    """
    Scales a given pattern to an interval.

    Parameters
    ----------
    pattern : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        The pattern to be scaled.
    min_value : `float`
        Lower bound of the pattern.
    max_value : `float`
        Upper bound of the pattern.

    Returns
    -------
    `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        The scaled pattern.
    """
    if min_value is None or max_value is None:
        return pattern

    min_pattern_val = np.min(pattern)
    max_pattern_val = np.max(pattern)

    return [(x - min_pattern_val) / (max_pattern_val - min_pattern_val) * (max_value - min_value)
            + min_value for x in pattern]


def generate_random_gaussian_noise(n_samples: int):
    """
    Generates Gaussian noise using a random mean ([0,1]) and random standard deviation ([0,1]).

    Parameters
    ----------
    n_samples : `int`
        Number of random samples.

    Returns
    -------
    `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        Gaussian noise.
    """
    return np.random.normal(np.random.rand(), np.random.rand(), size=n_samples)


def generate_deep_random_gaussian_noise(n_samples: int, mean: float = None):
    """
    Generates random Gaussian noise where the standard deviations (and mean) are changing over time.

    Parameters
    ----------
    n_samples : `int`
        Number of random samples.
    mean : `float`, optional
        Fixed mean at all points in time.
        If None, random means are generated.

        The default is None.

    Returns
    -------
    `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        Random Gaussian noise.
    """
    noise = []

    if mean is None:
        mean = create_deep_random_pattern(n_samples, min_value=-1., max_value=1.)
    else:
        mean = [mean] * n_samples
    rand_std = create_deep_random_pattern(n_samples)
    noise = np.array([np.random.normal(m, s) for m, s in zip(mean, rand_std)])

    return noise


def create_deep_random_pattern(n_samples: int, min_value: float = 0., max_value: float = 1.,
                               init_value: float = None) -> np.ndarray:
    """
    Generates a random pattern.

    Parameters
    ----------
    n_samples : `int`
        Number of random samples -- i.e. length of the pattern.
    min_value : `float`, optional
        Lower bound of the pattern.

        The default is zero.
    max_value : `float`, optional
        Upper bound of the pattern.

        The default is one.
    init_value : `float`, optional
        Value of the first sample in the pattern.
        If None, a random value is used.

        The default is None.

    Returns
    -------
    `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        Random pattern.
    """
    pattern = []
    start_value = init_value

    while len(pattern) < n_samples:
        if len(pattern) != 0:
            start_value = pattern[-1]

        pattern += _create_deep_random_pattern(start_value, min_value=min_value,
                                               max_value=max_value)

    pattern = pattern[:n_samples]

    # Scaling to value range
    pattern = scale_to_range(pattern, min_value, max_value)

    return np.array(pattern)


def _create_deep_random_pattern(start_value: float = None, min_length: int = 2, max_length: int = 5,
                                min_value: float = None, max_value: float = None) -> np.ndarray:
    """
    Generates a random pattern of random length.

    Parameters
    ----------
    start_value : `float`, optional
        First value in the pattern.
        If None, a random value is used.

        The default is None.
    min_length : `int`, optional
        Minium length of the pattern.

        The default is 2.
    max_length : `int`
        Maximum length of the pattern.

        The default is 5.
    min_value : `float`, optional
        Lower bound of the pattern.

        The default is zero.
    max_value : `float`, optional
        Upper bound of the pattern.

        The default is one.

    Returns
    -------
    `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        Random pattern.
    """
    pattern = []

    # Random parameters of pattern
    if start_value is None:
        start_value = np.random.rand()
    length = np.random.randint(low=min_length, high=max_length)
    vec = np.random.choice([-.1, .1])

    # Generate pattern
    cur_value = start_value
    pattern.append(start_value)

    for _ in range(length):
        cur_value = cur_value + np.random.rand() * vec
        pattern.append(cur_value)
        if min_value is not None and max_value is not None:
            if cur_value < min_value:
                vec = .1
            elif cur_value > max_value:
                vec = -.1

    return pattern
