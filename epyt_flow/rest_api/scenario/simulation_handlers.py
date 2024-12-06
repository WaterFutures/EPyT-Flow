"""
This module provides REST API handlers concerning the simulation of scenarios.
"""
import warnings
import falcon

from .handlers import ScenarioBaseHandler
from ..scada_data.handlers import ScadaDataManager


class ScenarioSimulationHandler(ScenarioBaseHandler):
    """
    Class for handling GET requests for simulating a given scenario.

    Parameters
    ----------
    scada_data_mgr : :class:`~epyt_flow.rest_api.scada_data.handlers.ScadaDataManager`
        SCADA data manager.
    """
    def __init__(self, scada_data_mgr: ScadaDataManager, **kwds):
        self.scada_data_mgr = scada_data_mgr

        super().__init__(**kwds)

    def on_post(self, req: falcon.Request, resp: falcon.Response, scenario_id: str) -> None:
        """
        Runs the simulation of a given scenario.

        Note that in contrat to the GET request
        (:func:`~epyt_flow.rest_api.scenario.simulation_handlers.ScenarioSimulationHandler.on_get`),
        the POST request allows to specify additional arguments passed to
        :func:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator.run_simulation`.

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

            params = self.load_json_data_from_request(req)

            my_scenario = self.scenario_mgr.get(scenario_id)
            res = my_scenario.run_simulation(**params)

            data_id = self.scada_data_mgr.create_new_item(res)
            self.send_json_response(resp, {"data_id": data_id})
        except Exception as ex:
            warnings.warn(str(ex))
            resp.data = str(ex)
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Runs the simulation of a given scenario.

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

            my_scenario = self.scenario_mgr.get(scenario_id)
            res = my_scenario.run_simulation()

            data_id = self.scada_data_mgr.create_new_item(res)
            self.send_json_response(resp, {"data_id": data_id})
        except Exception as ex:
            warnings.warn(str(ex))
            resp.data = str(ex)
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScenarioBasicQualitySimulationHandler(ScenarioBaseHandler):
    """
    Class for handling POST requests for runing a basic quality simulation of a given scenario.

    Parameters
    ----------
    scada_data_mgr : :class:`~epyt_flow.rest_api.scada_data.handlers.ScadaDataManager`
        SCADA data manager.
    """
    def __init__(self, scada_data_mgr: ScadaDataManager, **kwds):
        self.scada_data_mgr = scada_data_mgr

        super().__init__(**kwds)

    def on_post(self, req: falcon.Request, resp: falcon.Response, scenario_id: str) -> None:
        """
        Runs the basic quality simulation of a given scenario.

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

            params = self.load_json_data_from_request(req)

            my_scenario = self.scenario_mgr.get(scenario_id)
            res = my_scenario.run_basic_quality_simulation(**params)

            data_id = self.scada_data_mgr.create_new_item(res)
            self.send_json_response(resp, {"data_id": data_id})
        except Exception as ex:
            warnings.warn(str(ex))
            resp.data = str(ex)
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScenarioAdvancedQualitySimulationHandler(ScenarioBaseHandler):
    """
    Class for handling POST requests for runing an advanced quality simulation of a given scenario.

    Parameters
    ----------
    scada_data_mgr : :class:`~epyt_flow.rest_api.scada_data.handlers.ScadaDataManager`
        SCADA data manager.
    """
    def __init__(self, scada_data_mgr: ScadaDataManager, **kwds):
        self.scada_data_mgr = scada_data_mgr

        super().__init__(**kwds)

    def on_post(self, req: falcon.Request, resp: falcon.Response, scenario_id: str) -> None:
        """
        Runs the advanced quality simulation of a given scenario.

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

            params = self.load_json_data_from_request(req)

            my_scenario = self.scenario_mgr.get(scenario_id)
            res = my_scenario.run_advanced_quality_simulation(**params)

            data_id = self.scada_data_mgr.create_new_item(res)
            self.send_json_response(resp, {"data_id": data_id})
        except Exception as ex:
            warnings.warn(str(ex))
            resp.data = str(ex)
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
