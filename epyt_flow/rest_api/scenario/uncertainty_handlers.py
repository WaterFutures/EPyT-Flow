"""
This module provides REST API handlers for model and sensor uncertainties of scenarios.
"""
import warnings
import falcon

from .handlers import ScenarioBaseHandler
from ...simulation import SensorNoise, ModelUncertainty


class ScenarioModelUncertaintyHandler(ScenarioBaseHandler):
    """
    Class for handling GET and POST requests concerning model uncertainty.
    """
    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Gets the model uncertainties of a given scenario.

        Parameters
        ----------
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
            Response instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            if self.scenario_mgr.validate_uuid(scenario_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            my_model_uncertainties = self.scenario_mgr.get(scenario_id).model_uncertainty
            self.send_json_response(resp, my_model_uncertainties)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

    def on_post(self, req: falcon.Request, resp: falcon.Response, scenario_id: str) -> None:
        """
        Sets the model uncertainties of a given scenario.

        Parameters
        ----------
        req : `falcon.Request <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#request>`_
            Request instance.
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
            Response instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            if self.scenario_mgr.validate_uuid(scenario_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            model_uncertainty = self.load_json_data_from_request(req)
            if not isinstance(model_uncertainty, ModelUncertainty):
                self.send_json_parsing_error(resp)
                return

            self.scenario_mgr.get(scenario_id).model_uncertainty = model_uncertainty
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScenarioSensorUncertaintyHandler(ScenarioBaseHandler):
    """
    Class for handling GET and POST requests concerning sensor uncertainty (i.e. noise).
    """
    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Gets the sensor uncertainty (i.e. noise) of a given scenario.

        Parameters
        ----------
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
            Response instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            if self.scenario_mgr.validate_uuid(scenario_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            my_sensor_noise = self.scenario_mgr.get(scenario_id).sensor_noise
            self.send_json_response(resp, my_sensor_noise)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

    def on_post(self, req: falcon.Request, resp: falcon.Response, scenario_id: str) -> None:
        """
        Sets the sensor uncertainty (i.e. noise) of a given scenario.

        Parameters
        ----------
        req : `falcon.Request <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#request>`_
            Request instance.
        resp : `falcon.Response <https://falcon.readthedocs.io/en/stable/api/request_and_response_asgi.html#response>`_
            Response instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            if self.scenario_mgr.validate_uuid(scenario_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            sensor_noise = self.load_json_data_from_request(req)
            if not isinstance(sensor_noise, SensorNoise):
                self.send_json_parsing_error(resp)
                return

            self.scenario_mgr.get(scenario_id).sensor_noise = sensor_noise
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
