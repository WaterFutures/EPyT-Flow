"""
Module provides a class for visualizing scenarios.
"""
import matplotlib.pyplot as plt

from .scenario_simulator import ScenarioSimulator


class ScenarioVisualizer():
    """
    Class for visualizing a given scenario.

    Parameters
    ----------
    scenario : :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`
        Scenario to be visualized.
    """
    def __init__(self, scenario: ScenarioSimulator):
        if not isinstance(scenario, ScenarioSimulator):
            raise TypeError("'scenario' must be an instance of " +
                            "'epyt_flow.simulation.ScenarioSimulator' " +
                            f"but not of '{type(scenario)}'")

        self.__scenario = scenario

    def plot_topology(self, show_sensor_config: bool = False, export_to_file: str = None) -> None:
        """
        Plots the topology of the water distribution network in the given scenario.

        Parameters
        ----------
        show_sensor_config : `bool`, optional
            Indicates whether the sensor configuration should be shown as well.

            The default is False.
        export_to_file : `str`, optional
            Path to the file where the visualization will be stored.
            If None, visualization will be just shown but NOT be stored anywhere.

            The default is None.
        """
        _ = plt.figure()

        highlighted_links = None
        highlighted_nodes = None
        if show_sensor_config is True:
            highlighted_nodes = []
            highlighted_links = []

            sensor_config = self.__scenario.sensor_config
            highlighted_nodes += sensor_config.pressure_sensors \
                + sensor_config.demand_sensors + sensor_config.quality_node_sensors
            highlighted_links += sensor_config.flow_sensors + sensor_config.quality_link_sensors

        self.__scenario.epanet_api.plot(highlightlink=highlighted_links,
                                        highlightnode=highlighted_nodes, figure=False)

        if export_to_file is not None:
            plt.savefig(export_to_file, transparent=True, bbox_inches='tight')
        else:
            plt.show()
