"""
This module provides REST API handlers for accessing the final sensor readings
(e.g. pressure, flow rate, etc.).
"""
import warnings
import falcon

from .handlers import ScadaDataBaseHandler


class ScadaDataPressuresHandler(ScadaDataBaseHandler):
    """
    Class for handling GET requests for the pressure sensor readings of a given SCADA data instance.
    """
    def on_get(self, _, resp: falcon.Response, data_id: str) -> None:
        """
        Gets the pressure sensor readings of a given SCADA data instance.

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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
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
