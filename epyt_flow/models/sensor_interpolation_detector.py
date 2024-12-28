"""
Module provides a simple residual-based event detector that performs sensor interpolation.
"""
from typing import Any, Union
from copy import deepcopy
import numpy as np
from sklearn.linear_model import LinearRegression

from .event_detector import EventDetector
from ..simulation.scada import ScadaData


class SensorInterpolationDetector(EventDetector):
    """
    Class implementing a residual-based event detector based on sensor interpolation.

    Parameters
    ----------
    regressor_type : `Any`, optional
        Regressor class that will be used for the sensor interpolation.
        Must implement the usual `fit` and `predict` functions.

        The default is `sklearn.linear_model.LinearRegression <https://scikit-learn.org/dev/modules/generated/sklearn.linear_model.LinearRegression.html>`_
    """
    def __init__(self, regressor_type: Any = LinearRegression, **kwds):
        self.__regressor_type = regressor_type
        self.__regressors = []

        super().__init__(**kwds)

    @property
    def regressor_type(self) -> Any:
        """
        Gets the class used for building the regressors in the sensor interpolation.

        Returns
        -------
        `Any`
            Regressor class.
        """
        return self.__regressor_type

    @property
    def regressors(self) -> list[Any]:
        """
        Gets the fitted sensor interpolation regressors.

        Returns
        -------
        `list[Any]`
            Fitted regressors.
        """
        return deepcopy(self.__regressors)

    def __eq__(self, other) -> bool:
        return self.__regressor_type == other.regressor_type and \
            all(self.__regressors == other.regressors)

    def fit(self, scada_data: Union[ScadaData, np.ndarray]) -> None:
        """
        Fit detector to given SCADA data -- assuming the given data represents
        the normal operating state.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` or `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            SCADA data to fit this detector.
        """
        if isinstance(scada_data, ScadaData):
            data = scada_data.get_data()
        else:
            data = scada_data

        self.__regressors = []
        for output_idx in range(data.shape[1]):
            input_idx = list(range(data.shape[1]))
            input_idx.remove(output_idx)

            X = data[:, input_idx]
            y = data[:, output_idx]

            model = self.__regressor_type()
            model.fit(X, y)

            y_pred = model.predict(X)
            threshold = 1.2 * np.max(np.abs(y_pred - y))

            self.__regressors.append((input_idx, output_idx, model, threshold))

    def apply(self, scada_data: Union[ScadaData, np.ndarray]) -> list[int]:
        """
        Applies this detector to given SCADA data and returns suspicious time points.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` or `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            SCADA data in which to look for events/anomalies.

        Returns
        -------
        `list[int]`
            List of suspicious time points.
        """
        suspicious_time_points = []

        if isinstance(scada_data, ScadaData):
            X = scada_data.get_data()
        else:
            X = scada_data

        for input_idx, output_idx, model, threshold in self.__regressors:
            y_pred = model.predict(X[:, input_idx])
            y = X[:, output_idx]

            suspicious_time_points += list(np.argwhere(np.abs(y_pred - y) > threshold).
                                           flatten())

        return list(set(suspicious_time_points))
