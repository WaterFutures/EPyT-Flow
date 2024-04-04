"""
This module provides all handlers for requests concerning scenarios.
"""
import warnings
import falcon

from .base_handler import BaseHandler
from .res_manager import ResourceManager
from .scada_data_handler import ScadaDataManager
from ..simulation import ScenarioSimulator, Leakage, SensorConfig


class ScenarioManager(ResourceManager):
    """
    Class for managing all scenarios that are currently used by the REST API.
    """
    def create(self, **kwds) -> str:
        """
        Creates a new scenario -- e.g. loading a given .inp file or
        using a given scenario configuration.

        Returns
        -------
        `str`
            UUID of the new scenario.
        """
        return self.create_new_item(ScenarioSimulator(**kwds))

    def close_item(self, item: ScenarioSimulator) -> None:
        item.close()


class ScenarioBaseHandler(BaseHandler):
    """
    Base class for all handlers concerning scenarios.

    Parameters
    ----------
    scenario_mgr : :class:`~epyt_flow.rest_api.scenario_handler.ScenarioManager`
        Instance for managing all scenarios.
    """
    def __init__(self, scenario_mgr: ScenarioManager):
        self.scenario_mgr = scenario_mgr


class ScenarioRemoveHandler(ScenarioBaseHandler):
    """
    Class for handling a DELETE request for a given scenario.
    """
    def on_delete(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Deletes a given scenario.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            if self.scenario_mgr.validate_uuid(scenario_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            self.scenario_mgr.remove(scenario_id)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScenarioConfigHandler(ScenarioBaseHandler):
    """
    Class for handling a GET request for getting the scenario configuration of a given scenario.
    """
    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Gets the scenario configuration of a given scenario.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            if self.scenario_mgr.validate_uuid(scenario_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            my_sceanrio_config = self.scenario_mgr.get(scenario_id).get_scenario_config()
            self.send_json_response(resp, my_sceanrio_config)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScenarioNewHandler(ScenarioBaseHandler):
    """
    Class for handling POST requests for creating a new scenario.
    """
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        """
        Creates/Loads a new scenario.

        Parameters
        ----------
        req : `falcon.Request`
            Request instance.
        resp : `falcon.Response`
            Response instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            args = self.load_json_data_from_request(req)
            scenario_id = self.scenario_mgr.create(**args)
            self.send_json_response(resp, {"scenario_id": scenario_id})
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScenarioLeakageHandler(ScenarioBaseHandler):
    """
    Class for handling GET and POST requests concerning leakages.
    """
    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Gets all leakages of a given scenario.

        Parameters
        ----------
        resp : `falcon.Response`
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
        req : `falcon.Request`
            Request instance.
        resp : `falcon.Response`
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


class ScenarioTopologyHandler(ScenarioBaseHandler):
    """
    Class for handling GET requests for getting the topology of a given scenario.
    """
    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Gets the topology of a given scenario.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            if self.scenario_mgr.validate_uuid(scenario_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            my_topology = self.scenario_mgr.get(scenario_id).get_topology()
            self.send_json_response(resp, my_topology)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScenarioGeneralParamsHandler(ScenarioBaseHandler):
    """
    Class for handling GET and POST requests for the general parameters of a given scenario.
    """
    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Gets the general parameters (e.g. simulation duration, etc.) of a given scenario.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            if self.scenario_mgr.validate_uuid(scenario_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            my_general_params = self.scenario_mgr.get(scenario_id).get_scenario_config().\
                general_params
            self.send_json_response(resp, my_general_params)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

    def on_post(self, req: falcon.Request, resp: falcon.Response, scenario_id: str) -> None:
        """
        Sets the general parameters of a given scenario.

        Parameters
        ----------
        resp : `falcon.Request`
            Request instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            if self.scenario_mgr.validate_uuid(scenario_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            general_params = self.load_json_data_from_request(req)
            if not isinstance(general_params, dict):
                self.send_json_parsing_error(resp)
                return

            self.scenario_mgr.get(scenario_id).set_general_parameters(**general_params)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScenarioSensorConfigHandler(ScenarioBaseHandler):
    """
    Class for handling GET and POST requests for the sensor configuration of a given scenario.
    """
    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Gets the sensor configuration of a given scenario.

        Parameters
        ----------
        resp : `falcon.Response`
            Response instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            if self.scenario_mgr.validate_uuid(scenario_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            my_sensor_config = self.scenario_mgr.get(scenario_id).sensor_config
            self.send_json_response(resp, my_sensor_config)
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

    def on_post(self, req: falcon.Request, resp: falcon.Response, scenario_id: str) -> None:
        """
        Sets the sensor configuration of a given scenario.

        Parameters
        ----------
        resp : `falcon.Request`
            Request instance.
        scenario_id : `str`
            UUID of the scenario.
        """
        try:
            if self.scenario_mgr.validate_uuid(scenario_id) is False:
                self.send_invalid_resource_id_error(resp)
                return

            sensor_config = self.load_json_data_from_request(req)
            if not isinstance(sensor_config, SensorConfig):
                self.send_json_parsing_error(resp)
                return

            my_scenario = self.scenario_mgr.get(scenario_id)
            my_scenario.sensor_config = sensor_config
        except Exception as ex:
            warnings.warn(str(ex))
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR


class ScenarioSimulationHandler(ScenarioBaseHandler):
    """
    Class for handling GET requests for simulating a given scenario.

    Parameters
    ----------
    scada_data_mgr : :class:`~epyt_flow.rest_api.scenario_handler.ScadaDataBaseHandler`
        SCADA data manager.
    """
    def __init__(self, scada_data_mgr: ScadaDataManager, **kwds):
        self.scada_data_mgr = scada_data_mgr

        super().__init__(**kwds)

    def on_get(self, _, resp: falcon.Response, scenario_id: str) -> None:
        """
        Runs the simulation of a given scenario.

        Parameters
        ----------
        resp : `falcon.Response`
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
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
