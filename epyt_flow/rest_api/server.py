"""
This module provides the EPyT-Flow REST API server.
"""
from wsgiref.simple_server import make_server, WSGIServer
import falcon

from .scenario.handlers import ScenarioManager, ScenarioNewHandler, \
    ScenarioRemoveHandler, ScenarioGeneralParamsHandler, ScenarioSensorConfigHandler, \
    ScenarioExportHandler, ScenarioTopologyHandler, ScenarioConfigHandler, \
    ScenarioNodeDemandPatternHandler
from .scenario.uncertainty_handlers import ScenarioModelUncertaintyHandler, \
    ScenarioSensorUncertaintyHandler
from .scenario.event_handlers import ScenarioLeakageHandler, ScenarioSensorFaultHandler
from .scenario.simulation_handlers import ScenarioSimulationHandler, \
    ScenarioBasicQualitySimulationHandler, ScenarioAdvancedQualitySimulationHandler
from .scada_data.handlers import ScadaDataManager, ScadaDataSensorConfigHandler, \
    ScadaDataRemoveHandler, ScadaDataSensorFaultsHandler, ScadaDataConvertUnitsHandler
from .scada_data.data_handlers import ScadaDataPressuresHandler, ScadaDataDemandsHandler, \
    ScadaDataFlowsHandler, ScadaDataLinksQualityHandler, ScadaDataNodesQualityHandler, \
    ScadaDataNodeBulkSpeciesHandler, ScadaDataLinkBulkSpeciesHandler, \
    ScadaDataSurfaceSpeciesHandler, ScadaDataTankVolumesHandler, ScadaDataPumpStatesHandler, \
    ScadaDataValveStatesHandler
from .scada_data.export_handlers import ScadaDataExportHandler, ScadaDataXlsxExportHandler, \
    ScadaDataMatlabExportHandler, ScadaDataNumpyExportHandler


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
        self.app.add_route("/scenario/{scenario_id}/export",
                           ScenarioExportHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/topology",
                           ScenarioTopologyHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/scenario_config",
                           ScenarioConfigHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/general_params",
                           ScenarioGeneralParamsHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/sensor_config",
                           ScenarioSensorConfigHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/uncertainty/model",
                           ScenarioModelUncertaintyHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/uncertainty/sensors",
                           ScenarioSensorUncertaintyHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/events/leakages",
                           ScenarioLeakageHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/events/sensor_faults",
                           ScenarioSensorFaultHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/node/{node_id}/demand_pattern",
                           ScenarioNodeDemandPatternHandler(self.scenario_mgr))
        self.app.add_route("/scenario/{scenario_id}/simulation",
                           ScenarioSimulationHandler(scenario_mgr=self.scenario_mgr,
                                                     scada_data_mgr=self.scada_data_mgr))
        self.app.add_route("/scenario/{scenario_id}/simulation/advanced_quality",
                           ScenarioBasicQualitySimulationHandler(scenario_mgr=self.scenario_mgr,
                                                                 scada_data_mgr=
                                                                 self.scada_data_mgr))
        self.app.add_route("/scenario/{scenario_id}/simulation/basic_quality",
                           ScenarioAdvancedQualitySimulationHandler(scenario_mgr=self.scenario_mgr,
                                                                    scada_data_mgr=
                                                                    self.scada_data_mgr))

        self.app.add_route("/scada_data/{data_id}",
                           ScadaDataRemoveHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/sensor_config",
                           ScadaDataSensorConfigHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/sensor_faults",
                           ScadaDataSensorFaultsHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/nodes/pressures",
                           ScadaDataPressuresHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/nodes/demands",
                           ScadaDataDemandsHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/nodes/quality",
                           ScadaDataNodesQualityHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/nodes/bulk_species",
                           ScadaDataNodeBulkSpeciesHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/links/flows",
                           ScadaDataFlowsHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/links/quality",
                           ScadaDataLinksQualityHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/links/bulk_species",
                           ScadaDataLinkBulkSpeciesHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/links/surface_species",
                           ScadaDataSurfaceSpeciesHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/pump_states",
                           ScadaDataPumpStatesHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/valve_states",
                           ScadaDataValveStatesHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/tank_volumes",
                           ScadaDataTankVolumesHandler(self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/export/xlsx",
                           ScadaDataXlsxExportHandler(scada_data_mgr=self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/export/matlab",
                           ScadaDataMatlabExportHandler(scada_data_mgr=self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/export/numpy",
                           ScadaDataNumpyExportHandler(scada_data_mgr=self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/export",
                           ScadaDataExportHandler(scada_data_mgr=self.scada_data_mgr))
        self.app.add_route("/scada_data/{data_id}/convert_units",
                           ScadaDataConvertUnitsHandler(scada_data_mgr=self.scada_data_mgr))

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
