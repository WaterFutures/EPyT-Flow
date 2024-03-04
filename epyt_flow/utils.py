"""
Module provides helper functions.
"""
import tempfile
import numpy as np
from sklearn.metrics import roc_auc_score as skelarn_roc_auc_score
from sklearn.metrics import f1_score as skelarn_f1_scpre


def get_temp_folder() -> str:
    return tempfile.gettempdir()


def to_seconds(days: int = None, hours: int = None, minutes: int = None) -> int:
    """
    Converts a time stamp (i.e. days, hours, minutes) into seconds.

    Parameters
    ----------
    days : `int`, optional
        Days.
    hours : `int`, optional
        Hours.
    minutes : `int`, optional
        Minutes.

    Returns
    -------
    `int`
        Time stamp in seconds.
    """
    sec = 0

    if days is not None:
        if not isinstance(days, int):
            raise TypeError(f"'days' must be an instance of 'int' but not of {type(days)}")
        if days <= 0:
            raise ValueError("'days' must be positive")

        sec += 24*60*60 * days
    if hours is not None:
        if not isinstance(hours, int):
            raise TypeError(f"'hours' must be an instance of 'int' but not of {type(hours)}")
        if hours <= 0:
            raise ValueError("'hours' must be positive")

        sec += 60*60 * hours
    if minutes is not None:
        if not isinstance(minutes, int):
            raise TypeError(f"'minutes' must be an instance of 'int' but not of {type(minutes)}")
        if minutes <= 0:
            raise ValueError("'minutes' must be positive")

        sec += 60 * minutes

    return sec


def f1_micro_score(y_pred: np.ndarray, y: np.ndarray) -> float:
    """
    Computes the F1 score using for a multi-class classification by
    counting the total true positives, false negatives and false positives.

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Predicted labels.
    y : `numpy.ndarray`
        Ground truth labels.

    Returns
    -------
    `float`
        F1 score.
    """
    return skelarn_f1_scpre(y, y_pred, average="micro")


def roc_auc_score(y_pred: np.ndarray, y: np.ndarray) -> float:
    """
    Computes the Area Under the Curve (AUC) of a classification.

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Predicted labels.
    y : `numpy.ndarray`
        Ground truth labels.

    Returns
    -------
    `float`
        ROC AUC score.
    """
    return skelarn_roc_auc_score(y, y_pred)


def precision_score(y_pred: np.ndarray, y: np.ndarray) -> float:
    """
    Computes the precision of a classification.

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Predicted labels.
    y : `numpy.ndarray`
        Ground truth labels.

    Returns
    -------
    `float`
        Precision score.
    """
    tp = np.sum([np.all(y[i] == y_pred[i]) for i in range(len(y))])
    fp = np.sum([np.any((y[i] == 0) & (y_pred[i] == 1)) for i in range(len(y))])

    return tp / (tp + fp)


def accuracy_score(y_pred: np.ndarray, y: np.ndarray) -> float:
    """
    Computes the accuracy of a classification.

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Predicted labels.
    y : `numpy.ndarray`
        Ground truth labels.

    Returns
    -------
    `float`
        Accuracy score.
    """
    tp = np.sum([np.all(y[i] == y_pred[i]) for i in range(len(y))])
    return tp / len(y)


def f1_score(y_pred: np.ndarray, y: np.ndarray) -> float:
    """
    Computes the F1-score for a binary classification.

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Predicted labels.
    y : `numpy.ndarray`
        Ground truth labels.

    Returns
    -------
    `float`
        F1-score.
    """
    tp = np.sum((y == 1) & (y_pred == 1))
    fp = np.sum((y == 0) & (y_pred == 1))
    fn = np.sum((y == 1) & (y_pred == 0))

    return (2. * tp) / (2. * tp + fp + fn)
