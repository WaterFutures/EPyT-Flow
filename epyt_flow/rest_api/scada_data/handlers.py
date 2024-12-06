"""
The module provides REST API handlers for some SCADA data requests.
"""
import warnings
import falcon

from ..base_handler import BaseHandler
from ..res_manager import ResourceManager
from ...simulation import SensorConfig, SensorFault


class ScadaDataManager(ResourceManager):
    """
    Class for managing SCADA data.
    """


class ScadaDataBaseHandler(BaseHandler):
    """
    Base class for all handlers concerning SCADA data.

    Parameters
    ----------
    scada_data_mgr : :class:`~epyt_flow.rest_api.scada_data.handlers.ScadaDataManager`
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        req : `falcon.Request <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#request>`_
            Request instance.
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        req : `falcon.Request <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#request>`_
            Request instance.
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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


class ScadaDataConvertUnitsHandler(ScadaDataBaseHandler):
    """
    Class for handling POST requests concerning unit conversion of a
    given SCADA data instance.
    """
    def on_post(self, req: falcon.Request, resp: falcon.Response, data_id: str) -> None:
        """
        Converts the units of a given SCADA data instance and returns a new SCADA data instance.

        Parameters
        ----------
        req : `falcon.Request <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#request>`_
            Request instance.
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
            Response instance.
        data_id : `str`
            UUID of the SCADA data.
        """
        try:
            if self.scada_data_mgr.validate_uuid(data_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            new_units = self.load_json_data_from_request(req)
            if not isinstance(new_units, dict):
                self.send_json_parsing_error(resp)
                return

            my_scada_data = self.scada_data_mgr.get(data_id)
            try:
                scada_data_new = my_scada_data.convert_units(**new_units)
            except Exception as ex:
                self.send_error(resp, str(ex))
                return

            new_scada_data_id = self.scada_data_mgr.create_new_item(scada_data_new)
            self.send_json_response(resp, {"data_id": new_scada_data_id})
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
