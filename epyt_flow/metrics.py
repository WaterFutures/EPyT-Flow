"""
This module provides different metrics for evaluation.
"""
import numpy as np
from sklearn.metrics import roc_auc_score as skelarn_roc_auc_score, f1_score as skelarn_f1_scpre, \
    mean_absolute_error


def running_mse(y_pred: np.ndarray, y: np.ndarray):
    """
    Computes the running Mean Squared Error (MSE).

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Predicted outputs.
    y : `numpy.ndarray`
        Ground truth outputs.

    Returns
    -------
    `float`
        Running MSE.
    """
    e_sq = np.square(y - y_pred)
    r_mse = list(esq for esq in e_sq)

    for i in range(1, len(y)):
        r_mse[i] = ((i * r_mse[i - 1]) / (i + 1)) + (r_mse[i] / (i + 1))

    return r_mse


def mape(y_pred: np.ndarray, y: np.ndarray, epsilon: float = .05) -> float:
    """
    Computes the Mean Absolute Percentage Error (MAPE).

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Predicted outputs.
    y : `numpy.ndarray`
        Ground truth outputs.
    epsilon : `float`, optional
        Small number added to predictions and ground truth to avoid division-by-zero.

        The default is 0.05

    Returns
    -------
    `float`
        MAPE score.
    """
    y_ = y + epsilon
    y_pred_ = y_pred + epsilon
    return np.mean(np.abs((y_ - y_pred_) / y_))


def smape(y_pred: np.ndarray, y: np.ndarray, epsilon: float = .05) -> float:
    """
    Computes the Symmetric Mean Absolute Percentage Error (SMAPE).

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Predicted outputs.
    y : `numpy.ndarray`
        Ground truth outputs.
    epsilon : `float`, optional
        Small number added to predictions and ground truth to avoid division-by-zero.

        The default is 0.05

    Returns
    -------
    `float`
        SMAPE score.
    """
    y_ = y + epsilon
    y_pred_ = y_pred + epsilon
    return 2. * np.mean(np.abs(y_ - y_pred_) / (np.abs(y_) + np.abs(y_pred_)))


def mase(y_pred: np.ndarray, y: np.ndarray, epsilon: float = .05) -> float:
    """
    Computes the Mean Absolute Scaled Error (MASE).

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Predicted outputs.
    y : `numpy.ndarray`
        Ground truth outputs.
    epsilon : `float`, optional
        Small number added to predictions and ground truth to avoid division-by-zero.

        The default is 0.05

    Returns
    -------
    `float`
        MASE score.
    """
    try:
        y_ = y + epsilon
        y_pred_ = y_pred + epsilon

        mae = mean_absolute_error(y_, y_pred_)
        naive_error = np.mean(np.abs(y_[1:] - y_pred_[:-1]))
        return mae / naive_error
    except Exception:
        return None


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


def true_positive_rate(y_pred: np.ndarray, y: np.ndarray) -> float:
    """
    Computes the true positive rate (also called sensitivity).

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Predicted labels.
    y : `numpy.ndarray`
        Ground truth labels.

    Returns
    -------
    `float`
        True positive rate.
    """
    tp = np.sum((y == 1) & (y_pred == 1))
    fn = np.sum((y == 1) & (y_pred == 0))

    return tp / (tp + fn)


def true_negative_rate(y_pred: np.ndarray, y: np.ndarray) -> float:
    """
    Computes the true negative rate (also called specificity).

    Parameters
    ----------
    y_pred : `numpy.ndarray`
        Predicted labels.
    y : `numpy.ndarray`
        Ground truth labels.

    Returns
    -------
    `float`
        True negative rate.
    """
    tn = np.sum((y == 0) & (y_pred == 0))
    fp = np.sum((y == 0) & (y_pred == 1))

    return tn / (tn + fp)


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
    tp = np.sum([np.all((y[i] == 1) & (y_pred[i] == 1)) for i in range(len(y))])
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
