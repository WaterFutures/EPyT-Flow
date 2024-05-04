"""
This module provides the EPyT-Flow REST API server.
"""
from wsgiref.simple_server import make_server, WSGIServer
import falcon

from .scenario_handler import ScenarioManager, ScenarioNewHandler, ScenarioRemoveHandler, \
    ScenarioGeneralParamsHandler, ScenarioSensorConfigHandler, ScenarioSimulationHandler, \
    ScenarioTopologyHandler, ScenarioConfigHandler, ScenarioLeakageHandler
from .scada_data_handler import ScadaDataManager, ScadaDataSensorConfigHandler, \
    ScadaDataPressuresHandler, ScadaDataDemandsHandler, ScadaDataFlowsHandler, \
    ScadaDataLinksQualityHandler, ScadaDataNodesQualityHandler, ScadaDataRemoveHandler, \
    ScadaDataSensorFaultsHandler, ScadaDataNodeBulkSpeciesHandler, \
    ScadaDataLinkBulkSpeciesHandler, ScadaDataSurfaceSpeciesHandler, ScadaDataTankVolumesHandler, \
    ScadaDataPumpStatesHandler, ScadaDataValveStatesHandler


class RestApiService():
    """
    Class implementing the REST API server.

    Parameters
    ----------
    port : `int`, optional
        Port of the server.

        The default is 8080
    """
    def __init__(self, port: int = 8080):
        self.app = falcon.App()
        self.__port = port

        self.scenario_mgr = ScenarioManager()
        self.scada_data_mgr = ScadaDataManager()

        self.app.add_route("/scenario/new",
                           ScenarioNewHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}",
                           ScenarioRemoveHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/topology",
                           ScenarioTopologyHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/scenario_config",
                           ScenarioConfigHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/general_params",
                           ScenarioGeneralParamsHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/sensor_config",
                           ScenarioSensorConfigHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/leakages",
                           ScenarioLeakageHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/simulation",
                           ScenarioSimulationHandler(scenario_mgr=self.scenario_mgr,
                                                     scada_data_mgr=self.scada_data_mgr))

        self.app.add_route("/scada_data/{data_id}",
                           ScadaDataRemoveHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/sensor_config",
                           ScadaDataSensorConfigHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/sensor_faults",
                           ScadaDataSensorFaultsHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/pressures",
                           ScadaDataPressuresHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/flows",
                           ScadaDataFlowsHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/demands",
                           ScadaDataDemandsHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/pump_states",
                           ScadaDataPumpStatesHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/valve_states",
                           ScadaDataValveStatesHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/tank_volumes",
                           ScadaDataTankVolumesHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/node_qualities",
                           ScadaDataNodesQualityHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/link_qualities",
                           ScadaDataLinksQualityHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/node_bulk_species",
                           ScadaDataNodeBulkSpeciesHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/link_bulk_species",
                           ScadaDataLinkBulkSpeciesHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/surface_species",
                           ScadaDataSurfaceSpeciesHandler(self.scada_data_mgr))

    @property
    def port(self) -> int:
        """
        Gets the port of the web server.

        Returns
        -------
        `int`
            Port.
        """
        return self.__port

    def make_server(self) -> WSGIServer:
        """
        Returns a new web server.
        """
        return make_server("", self.__port, self.app)

    def run(self) -> None:
        """
        Runs the REST service.
        """
        with self.make_server() as httpd:
            httpd.serve_forever()
