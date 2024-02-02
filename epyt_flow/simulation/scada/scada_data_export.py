from abc import abstractmethod
import numpy as np
from scipy.io import savemat
import pandas as pd

from .scada_data import ScadaData


class ScadaDataExport():
    """
    Base class for exporting SCADA data stored in 
    :class:`~epyt_flow.simulation.scada_data.scada_data.ScadaData`.
    
    Parameters
    ----------
    f_out : `str`
        Path to the file to which the SCADA data will be exported.

    Attributes
    ----------
    f_out : `str`
        Path to the file to which the SCADA data will be exported.
    """
    def __init__(self, f_out:str, **kwds):
        self._f_out = f_out

        super().__init__(**kwds)

    @property
    def f_out(self) -> str:
        return self._f_out

    @abstractmethod
    def export(self, scada_data:ScadaData):
        """
        Exports given SCADA data.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada_data.scada_data.ScadaData`
            SCADA data to be exported.
        """
        raise NotImplementedError()


class ScadaDataNumpyExport(ScadaDataExport):
    """
    Class for exporting SCADA data to numpy (.npz file).
    """
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def export(self, scada_data:ScadaData):
        """
        Exports given SCADA data.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada_data.scada_data.ScadaData`
            SCADA data to be exported.
        """
        if not isinstance(scada_data, ScadaData):
            raise ValueError("'scada_data' must be an instance of "+\
                             "'epyt_flow.simulation.scada_data.ScadaData' and not of "+\
                                f"'{type(scada_data)}'")

        np.savez(self.f_out, sensor_readings=scada_data.get_data())


class ScadaDataXlsxExport(ScadaDataExport):
    """
    Class for exporting SCADA data to excep (.xlsx file).
    """
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def export(self, scada_data:ScadaData):
        """
        Exports given SCADA data.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada_data.scada_data.ScadaData`
            SCADA data to be exported.
        """
        if not isinstance(scada_data, ScadaData):
            raise ValueError("'scada_data' must be an instance of "+\
                             "'epyt_flow.simulation.scada_data.ScadaData' and not of "+\
                                f"'{type(scada_data)}'")

        with pd.ExcelWriter(self.f_out) as writer:
            pd.DataFrame(scada_data.get_data()).to_excel(writer, sheet_name="Sensor readings",
                                                         index=False)


class ScadaDataMatlabExport(ScadaDataExport):
    """
    Class for exporting SCADA data to MATLAB (.mat file).
    """
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def export(self, scada_data:ScadaData):
        """
        Exports given SCADA data.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada_data.scada_data.ScadaData`
            SCADA data to be exported.
        """
        if not isinstance(scada_data, ScadaData):
            raise ValueError("'scada_data' must be an instance of "+\
                             "'epyt_flow.simulation.scada_data.ScadaData' and not of "+\
                                f"'{type(scada_data)}'")

        savemat(self.f_out, {"sensor_readings": scada_data.get_data()})
