"""
This module provides REST API handlers for scenario events.
"""
import warnings
import falcon

from .handlers import ScenarioBaseHandler
from ...simulation import Leakage, SensorFault


class ScenarioLeakageHandler(ScenarioBaseHandler):
    """
    Class for handling GET and POST requests concerning leakages.
    """
    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Gets all leakages of a given scenario.

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

            my_leakages = self.scenario_mgr.get(scenario_id).leakages
            self.send_json_response(resp, my_leakages)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

    def on_post(self, req: falcon.Request, resp: falcon.Response, scenario_id: str) -> None:
        """
        Adds a new leakage to a given scenario.

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

            leakage = self.load_json_data_from_request(req)
            if not isinstance(leakage, Leakage):
                self.send_json_parsing_error(resp)
                return

            self.scenario_mgr.get(scenario_id).add_leakage(leakage)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScenarioSensorFaultHandler(ScenarioBaseHandler):
    """
    Class for handling GET and POST requests concerning sensor faults.
    """
    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Gets all sensor faults of a given scenario.

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

            my_sensor_faults = self.scenario_mgr.get(scenario_id).sensor_faults
            self.send_json_response(resp, my_sensor_faults)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

    def on_post(self, req: falcon.Request, resp: falcon.Response, scenario_id: str) -> None:
        """
        Adds a new sensor fault to a given scenario.

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

            sensor_fault = self.load_json_data_from_request(req)
            if not isinstance(sensor_fault, SensorFault):
                self.send_json_parsing_error(resp)
                return

            self.scenario_mgr.get(scenario_id).add_sensor_fault(sensor_fault)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
