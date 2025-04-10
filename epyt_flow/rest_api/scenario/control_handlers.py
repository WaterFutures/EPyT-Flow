"""
This module provides REST API handlers for complex and simple control modules of scenarios.
"""
import warnings
import falcon

from .handlers import ScenarioBaseHandler
from ...simulation import ComplexControlModule, SimpleControlModule


class ScenarioComplexControlHandler(ScenarioBaseHandler):
    """
    Class for handling GET and POST requests concerning complex control modules.
    """
    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Gets all complex control modules of a given scenario.

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

            my_simple_controls = self.scenario_mgr.get(scenario_id).complex_controls
            self.send_json_response(resp, my_simple_controls)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

    def on_post(self, req: falcon.Request, resp: falcon.Response, scenario_id: str) -> None:
        """
        Adds a new complex control module to a given scenario.

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

            complex_control = self.load_json_data_from_request(req)
            if not isinstance(complex_control, ComplexControlModule):
                self.send_json_parsing_error(resp)
                return

            self.scenario_mgr.get(scenario_id).add_complex_control(complex_control)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScenarioSimpleControlHandler(ScenarioBaseHandler):
    """
    Class for handling GET and POST requests concerning simple control modules.
    """
    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Gets all simple control modules of a given scenario.

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

            my_simple_controls = self.scenario_mgr.get(scenario_id).simple_controls
            self.send_json_response(resp, my_simple_controls)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

    def on_post(self, req: falcon.Request, resp: falcon.Response, scenario_id: str) -> None:
        """
        Adds a new simple control module to a given scenario.

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

            simple_control = self.load_json_data_from_request(req)
            if not isinstance(simple_control, SimpleControlModule):
                self.send_json_parsing_error(resp)
                return

            self.scenario_mgr.get(scenario_id).add_simple_control(simple_control)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
