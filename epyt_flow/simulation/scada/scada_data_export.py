"""
Module provides a classes for exporting SCADA data stored in 
:class:`~epyt_flow.simulation.scada.scada_data.ScadaData`.
"""
from abc import abstractmethod
import numpy as np
from scipy.io import savemat
import pandas as pd

from .scada_data import ScadaData


class ScadaDataExport():
    """
    Base class for exporting SCADA data stored in 
    :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`.

    Parameters
    ----------
    f_out : `str`
        Path to the file to which the SCADA data will be exported.
    """
    def __init__(self, f_out: str, **kwds):
        self._f_out = f_out

        super().__init__(**kwds)

    @property
    def f_out(self) -> str:
        """
        Gets the path to the file to which the SCADA data will be exported.

        Returns
        -------
        `str`
            Path to the file to which the SCADA data will be exported.
        """
        return self._f_out

    def create_column_desc(self, scada_data: ScadaData) -> np.ndarray:
        """
        Creates columns descriptions -- i.e. sensor type and location for each column

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            SCADA data to be described.

        Returns
        -------
        `numpy.ndarray`
            2-dimensional array describing all columns of the sensor readings:
            The first dimension describes the sensor type, and the second dimension 
            describes the sensor location. 
        """
        sensor_readings = scada_data.get_data()

        col_desc = [None for _ in range(sensor_readings.shape[1])]
        sensor_config = scada_data.sensor_config
        sensors_id_to_idx = sensor_config.sensors_id_to_idx
        for sensor_type in sensors_id_to_idx:
            for item_id in sensors_id_to_idx[sensor_type]:
                col_id = sensors_id_to_idx[sensor_type][item_id]
                col_desc[col_id] = [sensor_type, item_id]

        return np.array(col_desc, dtype=object)

    @abstractmethod
    def export(self, scada_data: ScadaData):
        """
        Exports given SCADA data.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            SCADA data to be exported.
        """
        raise NotImplementedError()


class ScadaDataNumpyExport(ScadaDataExport):
    """
    Class for exporting SCADA data to numpy (.npz file).
    """

    def export(self, scada_data: ScadaData):
        """
        Exports given SCADA data.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            SCADA data to be exported.
        """
        if not isinstance(scada_data, ScadaData):
            raise TypeError("'scada_data' must be an instance of " +
                            "'epyt_flow.simulation.scada_data.ScadaData' and not of " +
                            f"'{type(scada_data)}'")

        sensor_readings = scada_data.get_data()
        sensor_readings_time = scada_data.sensor_readings_time
        col_desc = self.create_column_desc(scada_data)

        np.savez(self.f_out, sensor_readings=sensor_readings, col_desc=col_desc,
                 sensor_readings_time=sensor_readings_time)


class ScadaDataXlsxExport(ScadaDataExport):
    """
    Class for exporting SCADA data to excep (.xlsx file).
    """

    def export(self, scada_data: ScadaData):
        """
        Exports given SCADA data.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            SCADA data to be exported.
        """
        if not isinstance(scada_data, ScadaData):
            raise TypeError("'scada_data' must be an instance of " +
                            "'epyt_flow.simulation.scada_data.ScadaData' and not of " +
                            f"'{type(scada_data)}'")

        sensor_readings = scada_data.get_data()
        sensor_readings_time = scada_data.sensor_readings_time
        col_desc = self.create_column_desc(scada_data)
        sensors_name = np.array([f"Sensor {i}" for i in range(1, sensor_readings.shape[1] + 1)],
                                dtype=object).reshape(-1, 1)
        col_desc = np.concatenate((sensors_name, col_desc), axis=1)

        with pd.ExcelWriter(self.f_out) as writer:
            pd.DataFrame(sensor_readings, columns=[f"Sensor {i}" for i in
                                                   range(1, sensor_readings.shape[1] + 1)]).\
                                                    to_excel(writer,
                                                             sheet_name="Sensor readings",
                                                             index=False)
            pd.DataFrame(sensor_readings_time, columns=["Time (s)"]).\
                to_excel(writer, sheet_name="Sensor readings time", index=False)
            pd.DataFrame(col_desc, columns=["Name", "Type", "Location"]).\
                to_excel(writer, sheet_name="Sensors description", index=False)


class ScadaDataMatlabExport(ScadaDataExport):
    """
    Class for exporting SCADA data to MATLAB (.mat file).
    """

    def export(self, scada_data: ScadaData):
        """
        Exports given SCADA data.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            SCADA data to be exported.
        """
        if not isinstance(scada_data, ScadaData):
            raise TypeError("'scada_data' must be an instance of " +
                            "'epyt_flow.simulation.scada_data.ScadaData' and not of " +
                            f"'{type(scada_data)}'")

        sensor_readings = scada_data.get_data()
        sensor_readings_time = scada_data.sensor_readings_time
        col_desc = self.create_column_desc(scada_data)

        savemat(self.f_out, {"sensor_readings": sensor_readings,
                             "sensor_readings_time": sensor_readings_time, "col_desc": col_desc})
