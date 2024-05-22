"""
The module provides all handlers for SCADA data requests.
"""
import warnings
import os
from abc import abstractmethod
import falcon

from .base_handler import BaseHandler
from .res_manager import ResourceManager
from ..simulation import SensorConfig, SensorFault
from ..utils import get_temp_folder
from ..simulation.scada import ScadaData, ScadaDataNumpyExport, ScadaDataMatlabExport, \
    ScadaDataXlsxExport


class ScadaDataManager(ResourceManager):
    """
    Class for managing SCADA data.
    """


class ScadaDataBaseHandler(BaseHandler):
    """
    Base class for all handlers concerning SCADA data.

    Parameters
    ----------
    scada_data_mgr : `~epyt_flow.rest_api.scenario_handler.ScadaDataBaseHandler`
        SCADA data manager.
    """
    def __init__(self, scada_data_mgr: ScadaDataManager):
        self.scada_data_mgr = scada_data_mgr


class ScadaDataRemoveHandler(ScadaDataBaseHandler):
    """
    Class for handling a DELETE request for a given SCADA data instance.
    """
    def on_delete(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Deletes a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data instance.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            self.scada_data_mgr.remove(data_id)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


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
        resp : `falcon.Response`
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
        resp : `falcon.Response`
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


class ScadaDataSensorConfigHandler(ScadaDataBaseHandler):
    """
    Class for handling GET and POST requests for the sensor configuration
    of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the sensor configuration of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            my_sensor_config = self.scada_data_mgr.get(data_id).sensor_config
            self.send_json_response(resp, my_sensor_config)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

    def on_post(self, req: falcon.Request, resp: falcon.Response, data_id: str) -> None:
        """
        Sets the sensor configuration of a given SCADA data instance.

        Parameters
        ----------
        req : `falcon.Request`
            Request instance.
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            sensor_config = self.load_json_data_from_request(req)
            if not isinstance(sensor_config, SensorConfig):
                self.send_json_parsing_error(resp)
                return

            self.scada_data_mgr.get(data_id).sensor_config = sensor_config
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataSensorFaultsHandler(ScadaDataBaseHandler):
    """
    Class for handling GET and POST requests concerning sensor faults in a
    given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets all sensor faults of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            sensor_faults = self.scada_data_mgr.get(data_id).sensor_faults
            self.send_json_response(resp, sensor_faults)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

    def on_post(self, req: falcon.Request, resp: falcon.Response, data_id: str) -> None:
        """
        Sets (i.e. overrides) the sensor faults in a given SCADA data instance.

        Parameters
        ----------
        req : `falcon.Request`
            Request instance.
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            sensor_faults = self.load_json_data_from_request(req)
            if not isinstance(sensor_faults, list) or \
                    any(not isinstance(e, SensorFault) for e in sensor_faults):
                self.send_json_parsing_error(resp)
                return

            self.scada_data_mgr.get(data_id).sensor_faults = sensor_faults
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataPressuresHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the pressure sensor readings of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the pressure sensor readings of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            data_pressures = self.scada_data_mgr.get(data_id).get_data_pressures().tolist()
            self.send_json_response(resp, data_pressures)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataFlowsHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the flow sensor readings of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the flow sensor readings of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            data_flows = self.scada_data_mgr.get(data_id).get_data_flows().tolist()
            self.send_json_response(resp, data_flows)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataDemandsHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the demand sensor readings of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the demand sensor readings of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            data_demands = self.scada_data_mgr.get(data_id).get_data_demands().tolist()
            self.send_json_response(resp, data_demands)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataValveStatesHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the valve state sensor readings
    of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the valve state sensor readings of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            data_demands = self.scada_data_mgr.get(data_id).get_data_valves_state().tolist()
            self.send_json_response(resp, data_demands)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataPumpStatesHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the pump state sensor readings
    of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the pump state sensor readings of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            data_demands = self.scada_data_mgr.get(data_id).get_data_pumps_state().tolist()
            self.send_json_response(resp, data_demands)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataTankVolumesHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the tank volume sensor readings
    of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the tank volume sensor readings of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            data_demands = self.scada_data_mgr.get(data_id).get_data_tanks_water_volume().tolist()
            self.send_json_response(resp, data_demands)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataNodesQualityHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the node quality sensor readings
    of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the node quality sensor readings of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            data_nodes_quality = self.scada_data_mgr.get(data_id).get_data_nodes_quality().tolist()
            self.send_json_response(resp, data_nodes_quality)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataLinksQualityHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the link quality sensor readings
    of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the link/pipe quality sensor readings of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            data_links_quality = self.scada_data_mgr.get(data_id).get_data_links_quality().tolist()
            self.send_json_response(resp, data_links_quality)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataNodeBulkSpeciesHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the bulk species node concentration sensor readings
    of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the bulk species node concentrations sensor readings of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            data_conc = self.scada_data_mgr.get(data_id).\
                get_data_bulk_species_node_concentration().tolist()
            self.send_json_response(resp, data_conc)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataLinkBulkSpeciesHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the bulk species link/pipe concentration sensor readings
    of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the bulk species link/pipe concentrations sensor readings of a
        given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            data_conc = self.scada_data_mgr.get(data_id).\
                get_data_bulk_species_link_concentration().tolist()
            self.send_json_response(resp, data_conc)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScadaDataSurfaceSpeciesHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the surface species concentration sensor readings
    of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the surface species concentrations sensor readings of a given SCADA data instance.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            data_links_quality = self.scada_data_mgr.get(data_id).\
                get_data_surface_species_concentration().tolist()
            self.send_json_response(resp, data_links_quality)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
