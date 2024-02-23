"""
Module provides helper functions.
"""
import tempfile
import numpy as np


def get_temp_folder() -> str:
    return tempfile.gettempdir()


def f1_score(y_pred, y) -> float:
    """
    Computes the F1-score for a binary classification.

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Event indication prediction over time
    y : `numpy.ndarray`
        Ground truth event indication over time.
    
    Returns
    -------
    `float`
        F1-score.
    """
    tp = np.sum((y == 1) & (y_pred == 1))
    fp = np.sum((y == 0) & (y_pred == 1))
    fn = np.sum((y == 1) & (y_pred == 0))

    return (2. * tp) / (2. * tp + fp + fn)
