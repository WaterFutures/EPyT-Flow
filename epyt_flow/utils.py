"""
Module provides helper functions.
"""
import tempfile
import numpy as np
from sklearn.metrics import roc_auc_score as skelarn_roc_auc_score
from sklearn.metrics import f1_score as skelarn_f1_scpre


def get_temp_folder() -> str:
    return tempfile.gettempdir()


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
