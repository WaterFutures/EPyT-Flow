"""
This module provides REST API handlers for exporting a given SCADA data instance.
"""
import os
from abc import abstractmethod
import warnings
import falcon

from .handlers import ScadaDataBaseHandler
from ...utils import get_temp_folder
from ...simulation.scada import ScadaData, ScadaDataNumpyExport, ScadaDataMatlabExport, \
    ScadaDataXlsxExport


class ScadaDataBaseExportHandler(ScadaDataBaseHandler):
    """
    Base handler for exporting a given SCADA data instance.
    """
    def __init__(self, file_ext: str, **kwds):
        self.__file_ext = file_ext

        super().__init__(**kwds)

    def create_temp_file_path(self, data_id: str, file_ext: str) -> None:
        """
        Returns a path to a temporary file for storing the SCADA data instance.

        Parameters
        ----------
        data_id : `str`
            UUID of the SCADA data.
        file_ext : `str`
            File extension.
        """
        return os.path.join(get_temp_folder(), f"{data_id}.{file_ext}")

    def send_temp_file(self, resp: falcon.Response, tmp_file: str,
                       content_type: str = "application/octet-stream") -> None:
        """
        Sends a given file (`tmp_file`) to the the client.

        Parameters
        ----------
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
            Response instance.
        tmp_file : `str`
            Path to the temporary file to be send.
        """
        resp.status = falcon.HTTP_200
        resp.content_type = content_type
        with open(tmp_file, 'rb') as f:
            resp.text = f.read()

    @abstractmethod
    def export(self, scada_data: ScadaData, tmp_file: str) -> None:
        """
        Exports a given SCADA data instance to a temporary file.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            SCADA data instance to be exported.
        tmp_file : `str`
            Path to temporary file.
        """
        raise NotImplementedError()

    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            my_scada_data = self.scada_data_mgr.get(data_id)

            tmp_file = self.create_temp_file_path(data_id, self.__file_ext)
            self.export(my_scada_data, tmp_file)

            self.send_temp_file(resp, tmp_file)

            os.remove(tmp_file)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataExportHandler(ScadaDataBaseExportHandler):
    """
    Class for handling a GET requests for exporting a given SCADA data instance
    to an .epytflow_scada_data file.
    """
    def __init__(self, **kwds):
        super().__init__(file_ext=".epytflow_scada_data", **kwds)

    def export(self, scada_data: ScadaData, tmp_file: str) -> None:
        scada_data.save_to_file(tmp_file)


class ScadaDataXlsxExportHandler(ScadaDataBaseExportHandler):
    """
    Class for handling a GET requests for exporting a given SCADA data instance to a .xlsx file.
    """
    def __init__(self, **kwds):
        super().__init__(file_ext=".xlsx", **kwds)

    def export(self, scada_data: ScadaData, tmp_file: str) -> None:
        ScadaDataXlsxExport(tmp_file).export(scada_data)


class ScadaDataNumpyExportHandler(ScadaDataBaseExportHandler):
    """
    Class for handling a GET requests for exporting a given SCADA data instance to Numpy data file.
    """
    def __init__(self, **kwds):
        super().__init__(file_ext=".npz", **kwds)

    def export(self, scada_data: ScadaData, tmp_file: str) -> None:
        ScadaDataNumpyExport(tmp_file).export(scada_data)


class ScadaDataMatlabExportHandler(ScadaDataBaseExportHandler):
    """
    Class for handling a GET requests for exporting a given SCADA data instance
    to a Matlab data file.
    """
    def __init__(self, **kwds):
        super().__init__(file_ext=".mat", **kwds)

    def export(self, scada_data: ScadaData, tmp_file: str) -> None:
        ScadaDataMatlabExport(tmp_file).export(scada_data)
