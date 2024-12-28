"""
Module provides a class for visualizing scenarios.
"""
from typing import Optional, Union, List, Tuple, Iterable
from deprecated import deprecated

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
import networkx.drawing.nx_pylab as nxp
import numpy as np
from svgpath2mpl import parse_path

from .scenario_simulator import ScenarioSimulator
from .scada.scada_data import ScadaData

PUMP_PATH = ('M 202.5 93 A 41.5 42 0 0 0 161 135 A 41.5 42 0 0 0 202.5 177 A '
             '41.5 42 0 0 0 244 135 A 41.5 42 0 0 0 241.94922 122 L 278 122 '
             'L 278 93 L 203 93 L 203 93.011719 A 41.5 42 0 0 0 202.5 93 z')
RESERVOIR_PATH = ('M 325 41 A 43 24.5 0 0 0 282.05664 65 L 282 65 L 282 65.5 '
                  'L 282 163 L 282 168 L 282 216 L 305 216 L 305 168 L 345 '
                  '168 L 345 216 L 368 216 L 368 168 L 368 163 L 368 65.5 L '
                  '368 65 L 367.98047 65 A 43 24.5 0 0 0 325 41 z')
TANK_PATH = ('M 325 41 A 43 24.5 0 0 0 282.05664 65 L 282 65 L 282 65.5 L 282 '
             '185 L 368 185 L 368 65.5 L 368 65 L 367.98047 65 A 43 24.5 0 0'
             ' 0 325 41 z')
VALVE_PATH = ('M 9.9999064 9.9999064 L 9.9999064 110 L 69.999862 59.999955 L '
              '9.9999064 9.9999064 z M 69.999862 59.999955 L 129.99982 110 L '
              '129.99982 9.9999064 L 69.999862 59.999955 z')


class Marker:
    """
    The Marker class provides svg representations of hydraulic components
    (pump, reservoir, tank and valve), which are loaded from their respective
    svg paths and transformed into :class:`~matplotlib.path.Path` objects in
    order to be used with the matplotlib library.

    Attributes
    ----------
    pump : :class:`~matplotlib.path.Path` object
        Marker for the pump, loaded from PUMP_PATH.
    reservoir : :class:`~matplotlib.path.Path` object
        Marker for the reservoir, loaded from RESERVOIR_PATH.
    tank : :class:`~matplotlib.path.Path` object
        Marker for the tank, loaded from TANK_PATH.
    valve : :class:`~matplotlib.path.Path` object
        Marker for the valve, loaded from VALVE_PATH.

    Methods
    -------
    __marker_from_path(path, scale_p=1)
        Loads and applies transformations to the marker shape from the given
        path.
    """
    def __init__(self):
        """
        Initializes the Marker class and assigns :class:`~matplotlib.path.Path`
        markers for pump, reservoir, tank, and valve components.
        """
        self.pump = self.__marker_from_path(PUMP_PATH, 2)
        self.reservoir = self.__marker_from_path(RESERVOIR_PATH)
        self.tank = self.__marker_from_path(TANK_PATH)
        self.valve = self.__marker_from_path(VALVE_PATH)

    @staticmethod
    def __marker_from_path(path: str, scale_p: int = 1) -> mpl.path.Path:
        """
        Loads the marker from the specified path and adjusts it representation
        by aligning, rotating and scaling it.

        Parameters
        ----------
        path : `str`
            The svg path describing the marker shape.
        scale_p : `float`, optional
            Scaling factor for the marker (default is 1).

        Returns
        -------
        marker_tmp : :class:`~matplotlib.path.Path` object
            The transformed marker object after loading and adjusting it.
        """
        marker_tmp = parse_path(path)
        marker_tmp.vertices -= marker_tmp.vertices.mean(axis=0)
        marker_tmp = marker_tmp.transformed(
            mpl.transforms.Affine2D().rotate_deg(180))
        marker_tmp = marker_tmp.transformed(
            mpl.transforms.Affine2D().scale(-scale_p, scale_p))
        return marker_tmp


class ScenarioVisualizer:
    """
    This class provides the necessary function to generate visualizations in
    the form of plots or animations from water network data.

    Given a :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator` object, this class
    provides the necessary functions to plot the network topology and to color
    hydraulic elements according to simulation data. The resulting plot can
    then either be displayed or saved.

    Attributes
    ----------
    __scenario : :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`
        ScenarioSimulator object containing the network topology and
        configurations to obtain the simulation data which should be displayed.
    fig : :class:`~matplotlib.pyplot.Figure` or None
        Figure object used for plotting, created and customized by calling the
        methods of this class, initialized as None.
    ax : :class:`~matplotlib.axes.Axes` or None
        The axes for plotting, initialized as None.
    scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` or None
        SCADA data created by the ScenarioSimulator object, initialized as
        None.
    topology : :class:`~epyt_flow.topology.NetworkTopology`
        Topology object retrieved from the scenario, containing the structure
        of the water distribution network.
    pos_dict : `dict`
        A dictionary mapping nodes to their coordinates in the correct format
        for drawing.
    pipe_parameters : `dict`
        Parameters for visualizing pipes in the correct format for drawing.
    junction_parameters : `dict`
        Parameters for visualizing junctions in the correct format for drawing.
    tank_parameters : `dict`
        Parameters for visualizing tanks in the correct format for drawing.
    reservoir_parameters : `dict`
        Parameters for visualizing reservoirs in the correct format for
        drawing.
    valve_parameters : `dict`
        Parameters for visualizing valves in the correct format for drawing.
    pump_parameters : `dict`
        Parameters for visualizing pumps in the correct format for drawing.
    animation_dict : `dict`
        A dictionary containing frame by frame data for the animated
        components.
    colorbars : `dict`
        A dictionary containing the necessary data for drawing the required
        colorbars.
    """
    def __init__(self, scenario: ScenarioSimulator) -> None:
        """
        Initializes the class with a given scenario, sets up the topology,
        SCADA data, and parameters for visualizing various hydraulic components
        (pipes, junctions, tanks, reservoirs, valves, and pumps).

        Parameters
        ----------
        scenario : :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`
            An instance of the `ScenarioSimulator` class, used to simulate and
            retrieve the system topology.

        Raises
        ------
        TypeError
            If `scenario` is not an instance of
            :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`.

        """
        if not isinstance(scenario, ScenarioSimulator):
            raise TypeError("'scenario' must be an instance of " +
                            "'epyt_flow.simulation.ScenarioSimulator' " +
                            f"but not of '{type(scenario)}'")

        self.__scenario = scenario
        self.fig = None
        self.ax = None
        self.scada_data = None
        markers = Marker()
        self.topology = self.__scenario.get_topology()
        self.pos_dict = {x: self.topology.get_node_info(x)['coord'] for x in
                         self.topology.get_all_nodes()}
        self.pipe_parameters = {
            'edgelist': [x[1] for x in self.topology.get_all_links()],
            'edge_color': 'k'}
        self.junction_parameters = {
            'nodelist': self.topology.get_all_junctions(), 'node_size': 10,
            'node_color': 'k'}
        self.tank_parameters = {'nodelist': self.topology.get_all_tanks(),
                                'node_size': 100, 'node_color': 'k',
                                'node_shape': markers.tank}
        self.reservoir_parameters = {
            'nodelist': self.topology.get_all_reservoirs(), 'node_size': 100,
            'node_color': 'k', 'node_shape': markers.reservoir}
        self.valve_parameters = {'nodelist': self.topology.get_all_valves(),
                                 'node_size': 75, 'node_color': 'k',
                                 'node_shape': markers.valve}
        self.pump_parameters = {'nodelist': self.topology.get_all_pumps(),
                                'node_size': 100, 'node_color': 'k',
                                'node_shape': markers.pump}
        self.animation_dict = {}
        self.colorbars = {}

    def __get_midpoints(self, elements: List[str]) -> dict[str, tuple[float, float]]:
        """
        Computes and returns the midpoints for drawing either valves or pumps
        in a water distribution network.

        For each element ID in the provided list, the method calculates the
        midpoint between its start and end nodes' coordinates.

        Parameters
        ----------
        elements : `list[str]`
            A list of element IDs (e.g., pump IDs, valve IDs) for which to
            compute the midpoints.

        Returns
        -------
        elements_dict : `dict`
            A dictionary where the keys are element IDs and the values are the
            corresponding midpoints, represented as 2D coordinates [x, y].
        """
        elements_pos_dict = {}
        for element in elements:
            if element in self.topology.pumps:
                start_node, end_node = self.topology.get_pump_info(element)[
                    'end_points']
            elif element in self.topology.valves:
                start_node, end_node = self.topology.get_valve_info(element)[
                    'end_points']
            else:
                raise ValueError(f"Unknown element '{element}'")
            start_pos = self.topology.get_node_info(start_node)['coord']
            end_pos = self.topology.get_node_info(end_node)['coord']
            pos = [(start_pos[0] + end_pos[0]) / 2,
                   (start_pos[1] + end_pos[1]) / 2]
            elements_pos_dict[element] = pos
        return elements_pos_dict

    def __get_next_frame(self, frame_number: int) -> None:
        """
        Draws the next frame of a water distribution network animation.

        This method updates a visualization animation with the hydraulic
        components colored according to the scada data corresponding to the
        current frame.

        Parameters
        ----------
        frame_number : `int`
            The current frame number used to retrieve the data corresponding to
            that frame
        """
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')

        nxp.draw_networkx_edges(self.topology, self.pos_dict, ax=self.ax,
                                label='Pipes', **self.pipe_parameters)

        if 'junctions' in self.animation_dict:
            self.junction_parameters['node_color'] = \
                self.animation_dict['junctions'][frame_number]
        if 'pipes' in self.animation_dict:
            self.pipe_parameters['edge_color'] = self.animation_dict['pipes'][
                frame_number]
        if 'pipe_sizes' in self.animation_dict:
            self.pipe_parameters['width'] = self.animation_dict['pipe_sizes'][
                frame_number]
        if 'pumps' in self.animation_dict:
            self.pump_parameters['node_color'] = self.animation_dict['pumps'][
                frame_number]
        if 'tanks' in self.animation_dict:
            self.tank_parameters['node_color'] = self.animation_dict['tanks'][
                frame_number]
        if 'valves' in self.animation_dict:
            self.valve_parameters['node_color'] = \
                self.animation_dict['valves'][frame_number]

        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Junctions', **self.junction_parameters)
        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Tanks', **self.tank_parameters)
        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Reservoirs',
                                **self.reservoir_parameters)
        nxp.draw_networkx_nodes(
            self.topology,
            self.__get_midpoints(self.topology.get_all_valves()), ax=self.ax,
            label='Valves', **self.valve_parameters)
        nxp.draw_networkx_nodes(
            self.topology, self.__get_midpoints(self.topology.get_all_pumps()),
            ax=self.ax, label='Pumps', **self.pump_parameters)

        self.ax.legend(fontsize=6)

    def __get_link_data(
            self, scada_data: Optional[ScadaData] = None,
            parameter: str = 'flow_rate', statistic: str = 'mean',
            pit: Optional[Union[int, Tuple[int]]] = None,
            intervals: Optional[Union[int, List[Union[int, float]]]] = None,
            conversion: Optional[dict] = None)\
            -> Tuple[Union[List, Iterable], int]:

        """
        Retrieves or generates SCADA data and processes it according to the
        parameters.

        The method extracts SCADA data corresponding to links. The given
        statistic is then applied and the data returned in a format suitable
        for plotting.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`, optional
            The SCADA data object to retrieve link data from. If `None`, a
            simulation is run to generate the SCADA data. Default is `None`.
        parameter : `str`, optional
            The type of link data to retrieve. Must be either 'flow_rate',
            'link_quality', or 'diameter'. Default is 'flow_rate'.
        statistic : `str`, optional
            The statistic to calculate for the link data. Can be 'mean', 'min',
            'max', or 'time_step'. Default is 'mean'.
        pit : `int` or `tuple(int, int)`, optional
            Point in time for the 'time_step' statistic. Can be either one
            point or a tuple setting a range. Required if 'time_step' is
            selected as the statistic. Default is `None`.
        intervals : `int`, `float`, or `list` of `int` or `float`, optional
            If specified, the link data will be grouped into intervals. This
            can either be an integer specifying the number of groups or a
            `list` of boundary points defining the intervals. Default is
            `None`.
        conversion : `dict`, optional
            A dictionary of conversion parameters to convert SCADA data units.
            Default is `None`.

        Returns
        -------
        sorted_values : `list`
            A list of processed and sorted values for each link in the water
            distribution network.
        sim_length : `int`
            The length of the simulation or SCADA data used.

        Raises
        ------
        ValueError
            If an invalid `parameter`, `statistic`, or `intervals` argument is
            provided, or if `pit` is not provided when using the 'time_step'
            statistic.

        """

        if scada_data:
            self.scada_data = scada_data
        elif not self.scada_data:
            self.scada_data = self.__scenario.run_simulation()

        if conversion:
            self.scada_data = self.scada_data.convert_units(**conversion)

        if parameter == 'flow_rate':
            values = self.scada_data.flow_data_raw
        elif parameter == 'link_quality':
            values = self.scada_data.link_quality_data_raw
        elif parameter == 'diameter':
            value_dict = {
                link[0]: self.topology.get_link_info(link[0])['diameter'] for
                link in self.topology.get_all_links()}
            sorted_values = [value_dict[x[0]] for x in
                             self.topology.get_all_links()]
            return (self.__rescale(sorted_values, (1, 2)),
                    self.scada_data.flow_data_raw.shape[0])
        else:
            raise ValueError('Parameter must be flow_rate or link_quality')

        sim_length = values.shape[0]

        if statistic == 'mean':
            stat_values = np.mean(values, axis=0)
        elif statistic == 'min':
            stat_values = np.min(values, axis=0)
        elif statistic == 'max':
            stat_values = np.max(values, axis=0)
        elif statistic == 'time_step':
            if not pit and pit != 0:
                raise ValueError(
                    'Please input point in time (pit) parameter when selecting'
                    ' time_step statistic')
            stat_values = np.take(values, pit, axis=0)
        else:
            raise ValueError(
                'Statistic parameter must be mean, min, max or time_step')

        if intervals is None:
            pass
        elif isinstance(intervals, (int, float)):
            interv = np.linspace(stat_values.min(), stat_values.max(),
                                 intervals + 1)
            stat_values = np.digitize(stat_values, interv) - 1
        elif isinstance(intervals, list):
            stat_values = np.digitize(stat_values, intervals) - 1
        else:
            raise ValueError(
                'Intervals must be either number of groups or list of interval'
                ' boundary points')

        value_dict = dict(zip(self.scada_data.sensor_config.links,
                              stat_values))
        sorted_values = [value_dict[x[0]] for x in
                         self.topology.get_all_links()]

        return sorted_values, sim_length

    @staticmethod
    def __get_parameters_update(statistic: str, values: np.ndarray,
                                pit: Union[int, Tuple[int]],
                                intervals: Union[int, List[Union[int, float]]],
                                all_junctions: List[str],
                                junction_sorting: List[str]) -> List:
        """
        Computes and returns statistical values for junctions in a water
        network.

        This method processes a 2D array of data (e.g., flow rates or quality)
        by calculating specified statistics (mean, min, max, or time step) and
        optionally grouping the data into intervals. It returns the data sorted
        according to the provided junction sorting order.

        Parameters
        ----------
        statistic : `str`
            The statistical operation to apply to the data. Must be one of
            'mean', 'min', 'max', or 'time_step'.
        values : :class:`~np.ndarray`
            A 2D NumPy array of shape (timesteps, junctions) containing the
            data for all junctions over time.
        pit : `int` or `tuple` of `int`
            The point in time or range of points in time for which to retrieve
            data, required if 'time_step' is selected as the statistic. If an
            integer is provided, it selects a single point in time.
        intervals : `int`, `float`, or `list[int]` or `list[float]`
            If specified, divides the data into intervals. Can be an integer
            representing the number of groups, or a list of boundary points
            defining the intervals.
        all_junctions : `list` of `str`
            A list of all junction IDs in the network, corresponding to the
            data  in the `values` array.
        junction_sorting : `list` of `str`
            The order in which to sort the junctions for the return value.

        Returns
        -------
        sorted_values : `list`
            A list of statistical values for the junctions, sorted according to
            `junction_sorting`.

        Raises
        ------
        ValueError
            If the `statistic` is not 'mean', 'min', 'max', or 'time_step', or
            if `pit` is not provided for the 'time_step' statistic, or if
            `intervals` is not in a valid format.

        """

        if statistic == 'mean':
            stat_values = np.mean(values, axis=0)
        elif statistic == 'min':
            stat_values = np.min(values, axis=0)
        elif statistic == 'max':
            stat_values = np.max(values, axis=0)
        elif statistic == 'time_step':
            if not pit and pit != 0:
                raise ValueError(
                    'Please input point in time (pit) parameter when selecting'
                    ' time_step statistic')
            stat_values = np.take(values, pit, axis=0)
        else:
            raise ValueError(
                'Statistic parameter must be mean, min, max or time_step')

        if intervals is None:
            pass
        elif isinstance(intervals, (int, float)):
            interv = np.linspace(stat_values.min(), stat_values.max(),
                                 intervals + 1)
            stat_values = np.digitize(stat_values, interv) - 1
        elif isinstance(intervals, list):
            stat_values = np.digitize(stat_values, intervals) - 1
        else:
            raise ValueError(
                'Intervals must be either number of groups or list of interval'
                ' boundary points')

        value_dict = dict(zip(all_junctions, stat_values))
        sorted_values = [value_dict[x] for x in junction_sorting]

        return sorted_values

    @staticmethod
    def __rescale(values: np.ndarray, scale_min_max: List,
                  values_min_max: List = None) -> List:
        """
        Rescales the given values to a new range.

        This method rescales an array of values to fit within a specified
        minimum and maximum scale range. Optionally, the minimum and maximum
        of the input values can be manually provided; otherwise, they are
        automatically determined from the data.

        Parameters
        ----------
        values : :class:`~np.ndarray`
            The array of numerical values to be rescaled.
        scale_min_max : `list`
            A list containing two elements: the minimum and maximum values
            of the desired output range.
        values_min_max : `list`, optional
            A list containing two elements: the minimum and maximum values
            of the input data. If not provided, they are computed from the
            input `values`. Default is `None`.

        Returns
        -------
        rescaled_values : `list`
            A list of values rescaled to the range specified by
            `scale_min_max`.

        """

        if not values_min_max:
            min_val, max_val = min(values), max(values)
        else:
            min_val, max_val = values_min_max
        scale = scale_min_max[1] - scale_min_max[0]

        def range_map(x):
            return scale_min_max[0] + (x - min_val) / (
                    max_val - min_val) * scale

        return [range_map(x) for x in values]

    def show_animation(self, export_to_file: str = None,
                       return_animation: bool = False)\
            -> Optional[FuncAnimation]:
        """
        Displays, exports, or returns an animation of a water distribution
        network over time.

        This method generates an animation of a network and either shows it or
        returns the :class:`~FuncAnimation` object. Optionally, the animation
        is saved to a file.

        Parameters
        ----------
        export_to_file : `str`, optional
            The file path where the animation should be saved, if provided.
            Default is `None`.
        return_animation : `bool`, optional
            If `True`, the animation object is returned. If `False`, the
            animation will be shown, but not returned. Default is `False`.

        Returns
        -------
        anim : :class:`~FuncAnimation` or None
            Returns the animation object if `return_animation` is `True`.
            Otherwise, returns `None`.

        """
        self.fig = plt.figure(figsize=(6.4, 4.8), dpi=200)

        total_frames = float('inf')
        for ll in self.animation_dict.values():
            total_frames = min(total_frames, len(ll))

        if not self.animation_dict or total_frames == 0:
            raise RuntimeError("The color or resize functions must be called "
                               "with a time_step range (pit) to enable "
                               "animations")

        anim = FuncAnimation(self.fig, self.__get_next_frame,
                             frames=total_frames, interval=25)

        if export_to_file is not None:
            anim.save(export_to_file, writer='ffmpeg', fps=4)
        if return_animation:
            plt.close(self.fig)
            return anim
        plt.show()
        return None

    def show_plot(self, export_to_file: str = None) -> None:
        """
        Displays a static plot of the water distribution network.

        This method generates a static plot of the water distribution network,
        visualizing pipes, junctions, tanks, reservoirs, valves, and pumps.
        The plot can be displayed and saved to a file.

        Parameters
        ----------
        export_to_file : `str`, optional
            The file path where the plot should be saved, if provided.
            Default is `None`.

        """
        self.fig = plt.figure(figsize=(6.4, 4.8), dpi=200)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')

        nxp.draw_networkx_edges(self.topology, self.pos_dict, ax=self.ax,
                                label='Pipes', **self.pipe_parameters)
        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Junctions', **self.junction_parameters)
        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Tanks', **self.tank_parameters)
        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Reservoirs',
                                **self.reservoir_parameters)
        nxp.draw_networkx_nodes(
            self.topology,
            self.__get_midpoints(self.topology.get_all_valves()), ax=self.ax,
            label='Valves', **self.valve_parameters)
        nxp.draw_networkx_nodes(
            self.topology, self.__get_midpoints(self.topology.get_all_pumps()),
            ax=self.ax, label='Pumps', **self.pump_parameters)
        self.ax.legend(fontsize=6)

        for colorbar_stats in self.colorbars.values():
            self.fig.colorbar(ax=self.ax, **colorbar_stats)

        if export_to_file is not None:
            plt.savefig(export_to_file, transparent=True, bbox_inches='tight',
                        dpi=200)
        plt.show()

    def color_nodes(
            self, scada_data: Optional[ScadaData] = None,
            parameter: str = 'pressure', statistic: str = 'mean',
            pit: Optional[Union[int, Tuple[int]]] = None,
            colormap: str = 'viridis',
            intervals: Optional[Union[int, List[Union[int, float]]]] = None,
            conversion: Optional[dict] = None, show_colorbar: bool = False) ->\
            None:
        """
        Colors the nodes (junctions) in the water distribution network based on
        the SCADA data and the specified parameters.

        This method either takes or generates SCADA data, applies a statistic
        to the chosen parameter, optionally groups the results and prepares the
        results to be either displayed statically ot animated.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`, optional
            The SCADA data object containing node data. If `None`, a simulation
            will be run to generate SCADA data. Default is `None`.
        parameter : `str`, optional
            The node data to visualize. Must be 'pressure', 'demand', or
            'node_quality'. Default is 'pressure'.
        statistic : `str`, optional
            The statistic to calculate for the data. Can be 'mean', 'min',
            'max', or 'time_step'. Default is 'mean'.
        pit : `int`, `tuple(int, int)`, optional
            The point in time or range of time steps for the 'time_step'
            statistic. If a tuple is provided, it should contain two integers
            representing the start and end time steps. A tuple is necessary to
            process the data for the :meth:`~ScenarioVisualizer.show_animation`
            method. Default is `None`.
        colormap : `str`, optional
            The colormap to use for visualizing node values. Default is
            'viridis'.
        intervals : `int`, `list[int]` or `list[float]`, optional
            If provided, the data will be grouped into intervals. It can be an
            integer specifying the number of groups or a list of boundary
            points. Default is `None`.
        conversion : `dict`, optional
            A dictionary of conversion parameters to convert SCADA data units.
            Default is `None`.
        show_colorbar : `bool`, optional
            If `True`, a colorbar will be displayed on the plot to indicate the
            range of node values. Default is `False`.

        Raises
        ------
        ValueError
            If the `parameter` is not one of 'pressure', 'demand', or
            'node_quality', or if `pit` is not correctly provided for the
            'time_step' statistic.

        """

        self.junction_parameters.update({'cmap': colormap})

        if scada_data:
            self.scada_data = scada_data
        elif not self.scada_data:
            self.scada_data = self.__scenario.run_simulation()

        if conversion:
            self.scada_data = self.scada_data.convert_units(**conversion)

        if parameter == 'pressure':
            values = self.scada_data.pressure_data_raw
        elif parameter == 'demand':
            values = self.scada_data.demand_data_raw
        elif parameter == 'node_quality':
            values = self.scada_data.node_quality_data_raw
        else:
            raise ValueError(
                'Parameter must be pressure, demand or node_quality')

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            sorted_values = self.__get_parameters_update(
                statistic, values, pit[0], intervals,
                self.scada_data.sensor_config.nodes,
                self.topology.get_all_junctions())
            self.animation_dict['junctions'] = []
            vmin, vmax = min(sorted_values), max(sorted_values)
            for frame in range(*pit):
                if frame > values.shape[0] - 1:
                    break
                sorted_values = self.__get_parameters_update(
                    statistic, values, frame, intervals,
                    self.scada_data.sensor_config.nodes,
                    self.topology.get_all_junctions())
                vmin, vmax = (min(*sorted_values, vmin),
                              max(*sorted_values, vmax))
                self.animation_dict['junctions'].append(sorted_values)
            self.junction_parameters['vmin'] = vmin
            self.junction_parameters['vmax'] = vmax
        else:
            sorted_values = self.__get_parameters_update(
                statistic, values, pit, intervals,
                self.scada_data.sensor_config.nodes,
                self.topology.get_all_junctions())
            self.junction_parameters.update(
                {'node_color': sorted_values, 'vmin': min(sorted_values),
                 'vmax': max(sorted_values)})

        if show_colorbar:
            if statistic == 'time_step':
                label = str(parameter).capitalize() + ' at timestep ' + str(
                    pit)
            else:
                label = str(statistic).capitalize() + ' ' + str(parameter)
            self.colorbars['junctions'] = {'mappable': plt.cm.ScalarMappable(
                norm=mpl.colors.Normalize(
                    vmin=self.junction_parameters['vmin'],
                    vmax=self.junction_parameters['vmax']), cmap=colormap),
                'label': label}

    def color_links(
            self, scada_data: Optional[ScadaData] = None,
            parameter: str = 'flow_rate', statistic: str = 'mean',
            pit: Optional[Union[int, Tuple[int]]] = None,
            colormap: str = 'coolwarm',
            intervals: Optional[Union[int, List[Union[int, float]]]] = None,
            conversion: Optional[dict] = None, show_colorbar: bool = False) ->\
            None:
        """
        Colors the links (pipes) in the water distribution network based on the
        SCADA data and the specified parameters.

        This method either takes or generates SCADA data, applies a statistic
        to the chosen parameter, optionally groups the results and prepares the
        results to be either displayed statically ot animated.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`, optional
            The SCADA data object. If `None`, the method will run a simulation.
            Default is `None`.
        parameter : `str`, optional
            The link data to visualize. Options are 'flow_rate', 'velocity', or
            'status'. Default is 'flow_rate'.
        statistic : `str`, optional
            The statistic to calculate for the data. Can be 'mean', 'min',
            'max', or 'time_step'. Default is 'mean'.
        pit : `int` or `tuple(int, int)`, optional
            The point in time or range of time steps for the 'time_step'
            statistic. If a tuple is provided, it should contain two integers
            representing the start and end time steps. A tuple is necessary to
            process the data for the :meth:`~ScenarioVisualizer.show_animation`
            method. Default is `None`.
        colormap : `str`, optional
            The colormap to use for visualizing link values. Default is
            'coolwarm'.
        intervals : `int`, `list[int]`, `list[float]`, optional
            If provided, the data will be grouped into intervals. It can be an
            integer specifying the number of groups or a list of boundary
            points. Default is `None`.
        conversion : `dict`, optional
            A dictionary of conversion parameters to convert SCADA data units.
            Default is `None`.
        show_colorbar : `bool`, optional
            If `True`, a colorbar will be displayed on the plot to indicate the
            range of values. Default is `False`.

        Raises
        ------
        ValueError
            If `parameter` is not a valid link data parameter or if `pit` is
            incorrectly provided for the 'time_step' statistic.

        """

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            sorted_values, sim_length = self.__get_link_data(scada_data,
                                                             parameter,
                                                             statistic, pit[0],
                                                             intervals,
                                                             conversion)
            self.pipe_parameters.update({'edge_color': sorted_values,
                                         'edge_cmap': mpl.colormaps[colormap],
                                         'edge_vmin': min(sorted_values),
                                         'edge_vmax': max(sorted_values)})
            self.animation_dict['pipes'] = []
            vmin = min(sorted_values)
            vmax = max(sorted_values)
            for frame in range(*pit):
                if frame > sim_length - 1:
                    break
                sorted_values, _ = self.__get_link_data(scada_data, parameter,
                                                        statistic, frame,
                                                        intervals, conversion)
                vmin = min(*sorted_values, vmin)
                vmax = max(*sorted_values, vmax)
                self.animation_dict['pipes'].append(sorted_values)
            self.pipe_parameters['edge_vmin'] = vmin
            self.pipe_parameters['edge_vmax'] = vmax
        else:
            sorted_values, _ = self.__get_link_data(scada_data, parameter,
                                                    statistic, pit, intervals,
                                                    conversion)
            self.pipe_parameters.update({'edge_color': sorted_values,
                                         'edge_cmap': mpl.colormaps[colormap],
                                         'edge_vmin': min(sorted_values),
                                         'edge_vmax': max(sorted_values)})

        if show_colorbar:
            if statistic == 'time_step':
                label = (str(parameter).capitalize().replace('_', ' ')
                         + ' at timestep ' + str(pit))
            else:
                label = str(statistic).capitalize() + ' ' + str(
                    parameter).replace('_', ' ')
            self.colorbars['pipes'] = {'mappable': plt.cm.ScalarMappable(
                norm=mpl.colors.Normalize(
                    vmin=self.pipe_parameters['edge_vmin'],
                    vmax=self.pipe_parameters['edge_vmax']), cmap=colormap),
                'label': label}

    def color_pumps(
            self, scada_data: Optional[ScadaData] = None,
            parameter: str = 'efficiency', statistic: str = 'mean',
            pit: Optional[Union[int, Tuple[int]]] = None,
            intervals: Optional[Union[int, List[Union[int, float]]]] = None,
            colormap: str = 'viridis', show_colorbar: bool = False) -> None:
        """
        Colors the pumps in the water distribution network based on SCADA data
        and the specified parameters.

        This method either takes or generates SCADA data, applies a statistic
        to the chosen parameter, optionally groups the results and prepares the
        results to be either displayed statically ot animated.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`, optional
            The SCADA data object containing the pump data. If `None`, a
            simulation will be run to generate SCADA data. Default is `None`.
        parameter : `str`, optional
            The pump data to visualize. Must be 'efficiency',
            'energy_consumption', or 'state'. Default is 'efficiency'.
        statistic : `str`, optional
            The statistic to calculate for the data. Can be 'mean', 'min',
            'max', or 'time_step'. Default is 'mean'.
        pit : `int`, `tuple(int, int)`, optional
            The point in time or range of time steps for the 'time_step'
            statistic. If a tuple is provided, it should contain two integers
            representing the start and end time steps. A tuple is necessary to
            process the data for the :meth:`~ScenarioVisualizer.show_animation`
            method. Default is `None`.
        intervals : `int`, `list[int]`, `list[float]`, optional
            If provided, the data will be grouped into intervals. It can be an
            integer specifying the number of groups or a list of boundary
            points. Default is `None`.
        colormap : `str`, optional
            The colormap to use for visualizing pump values. Default is
            'viridis'.
        show_colorbar : `bool`, optional
            If `True`, a colorbar will be displayed on the plot to indicate the
            range of pump values. Default is `False`.

        Raises
        ------
        ValueError
            If the `parameter` is not one of 'efficiency',
            'energy_consumption', or 'state', or if `pit` is not correctly
            provided for the 'time_step' statistic.

        """

        self.pump_parameters.update({'cmap': colormap})

        if scada_data:
            self.scada_data = scada_data
        elif not self.scada_data:
            self.scada_data = self.__scenario.run_simulation()

        if parameter == 'efficiency':
            values = self.scada_data.pumps_efficiency_data_raw
        elif parameter == 'energy_consumption':
            values = self.scada_data.pumps_energyconsumption_data_raw
        elif parameter == 'state':
            values = self.scada_data.pumps_state_data_raw
        else:
            raise ValueError(
                'Parameter must be efficiency, energy_consumption or state')

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            sorted_values = self.__get_parameters_update(
                statistic, values, pit[0], intervals,
                self.scada_data.sensor_config.pumps,
                self.topology.get_all_pumps())
            self.animation_dict['pumps'] = []
            vmin = min(sorted_values)
            vmax = max(sorted_values)
            for frame in range(*pit):
                if frame > values.shape[0] - 1:
                    break
                sorted_values = self.__get_parameters_update(
                    statistic, values, frame, intervals,
                    self.scada_data.sensor_config.pumps,
                    self.topology.get_all_pumps())
                vmin = min(*sorted_values, vmin)
                vmax = max(*sorted_values, vmax)
                self.animation_dict['pumps'].append(sorted_values)
            self.pump_parameters['vmin'] = vmin
            self.pump_parameters['vmax'] = vmax
        else:
            sorted_values = self.__get_parameters_update(
                statistic, values, pit, intervals,
                self.scada_data.sensor_config.pumps,
                self.topology.get_all_pumps())
            self.pump_parameters.update(
                {'node_color': sorted_values, 'vmin': min(sorted_values),
                 'vmax': max(sorted_values)})

        if show_colorbar:
            if statistic == 'time_step':
                label = str(parameter).capitalize().replace(
                    '_', ' ') + ' at timestep ' + str(pit)
            else:
                label = str(statistic).capitalize() + ' ' + str(
                    parameter).replace('_', ' ')
            self.colorbars['pumps'] = {'mappable': plt.cm.ScalarMappable(
                norm=mpl.colors.Normalize(vmin=self.pump_parameters['vmin'],
                                          vmax=self.pump_parameters['vmax']),
                cmap=colormap), 'label': label}

    def color_tanks(
            self, scada_data: Optional[ScadaData] = None,
            statistic: str = 'mean',
            pit: Optional[Union[int, Tuple[int]]] = None,
            intervals: Optional[Union[int, List[Union[int, float]]]] = None,
            colormap: str = 'viridis', show_colorbar: bool = False) -> None:
        """
        Colors the tanks in the water distribution network based on the SCADA
        tank volume data and the specified statistic.

        This method either takes or generates SCADA data, applies a statistic
        to the tank volume data, optionally groups the results and prepares
        them to be either displayed statically ot animated.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`, optional
            The SCADA data object containing tank volume data.
            If `None`, a simulation will be run to generate it.
            Default is `None`.
        statistic : `str`, optional
            The statistic to calculate for the data. Can be 'mean', 'min',
            'max', or 'time_step'. Default is 'mean'.
        pit : `int`, `tuple(int, int)`, optional
            The point in time or range of time steps for the 'time_step'
            statistic. If a tuple is provided, it should contain two integers
            representing the start and end time steps. A tuple is necessary to
            process the data for the :meth:`~ScenarioVisualizer.show_animation`
            method. Default is `None`.
        intervals : `int`, `list[int]`, `list[float]`, optional
            If provided, the data will be grouped into intervals. It can be an
            integer specifying the number of groups or a list of boundary
            points. Default is `None`.
        colormap : `str`, optional
            The colormap to use for visualizing tank values. Default is
            'viridis'.
        show_colorbar : `bool`, optional
            If `True`, a colorbar will be displayed on the plot to indicate the
            range of tank volume values. Default is `False`.

        Raises
        ------
        ValueError
            If `pit` is not correctly provided for the 'time_step' statistic.

        """
        self.pump_parameters.update({'node_size': 10, 'cmap': colormap})

        if scada_data:
            self.scada_data = scada_data
        elif not self.scada_data:
            self.scada_data = self.__scenario.run_simulation()

        values = self.scada_data.tanks_volume_data_raw

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            sorted_values = self.__get_parameters_update(
                statistic, values, pit[0], intervals,
                self.scada_data.sensor_config.tanks,
                self.topology.get_all_tanks())
            self.animation_dict['tanks'] = []
            vmin = min(sorted_values)
            vmax = max(sorted_values)
            for frame in range(*pit):
                if frame > values.shape[0] - 1:
                    break
                sorted_values = self.__get_parameters_update(
                    statistic, values, frame, intervals,
                    self.scada_data.sensor_config.tanks,
                    self.topology.get_all_tanks())
                vmin = min(*sorted_values, vmin)
                vmax = max(*sorted_values, vmax)
                self.animation_dict['tanks'].append(sorted_values)
            self.tank_parameters['vmin'] = vmin
            self.tank_parameters['vmax'] = vmax
        else:
            sorted_values = self.__get_parameters_update(
                statistic, values, pit, intervals,
                self.scada_data.sensor_config.tanks,
                self.topology.get_all_tanks())
            self.tank_parameters.update(
                {'node_color': sorted_values, 'vmin': min(sorted_values),
                 'vmax': max(sorted_values)})

        if show_colorbar:
            if statistic == 'time_step':
                label = 'tank volume'.capitalize() + ' at timestep ' + str(pit)
            else:
                label = str(statistic).capitalize() + ' ' + 'tank volume'
            self.colorbars['tanks'] = {'mappable': plt.cm.ScalarMappable(
                norm=mpl.colors.Normalize(vmin=self.tank_parameters['vmin'],
                                          vmax=self.tank_parameters['vmax']),
                cmap=colormap), 'label': label}

    def color_valves(
            self, scada_data: Optional[ScadaData] = None,
            statistic: str = 'mean',
            pit: Optional[Union[int, Tuple[int]]] = None,
            intervals: Optional[Union[int, List[Union[int, float]]]] = None,
            colormap: str = 'viridis', show_colorbar: bool = False) -> None:
        """
        Colors the valves in the water distribution network based on SCADA
        valve state data and the specified statistic.

        This method either takes or generates SCADA data, applies a statistic
        to the valve state data, optionally groups the results and prepares
        them to be either displayed statically ot animated.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`, optional
            The SCADA data object containing valve state data. If `None`, a
            simulation is run to generate SCADA data. Default is `None`.
        statistic : `str`, optional
            The statistic to calculate for the data. Can be 'mean', 'min',
            'max', or 'time_step'. Default is 'mean'.
        pit : `int`, `tuple(int)`, optional
            The point in time or range of time steps for the 'time_step'
            statistic. If a tuple is provided, it should contain two integers
            representing the start and end time steps. A tuple is necessary to
            process the data for the :meth:`~ScenarioVisualizer.show_animation`
            method. Default is `None`.
        intervals : `int`, `list[int]`, `list[float]`, optional
            If provided, the data will be grouped into intervals. It can be an
            integer specifying the number of groups or a list of
            boundary points. Default is `None`.
        colormap : `str`, optional
            The colormap to use for visualizing valve state values. Default is
            'viridis'.
        show_colorbar : `bool`, optional
            If `True`, a colorbar will be displayed on the plot to indicate the
            range of valve state values. Default is `False`.

        Raises
        ------
        ValueError
            If `pit` is not correctly provided for the 'time_step' statistic.

        """

        self.valve_parameters.update({'node_size': 15, 'cmap': colormap})

        if scada_data:
            self.scada_data = scada_data
        elif not self.scada_data:
            self.scada_data = self.__scenario.run_simulation()

        values = self.scada_data.valves_state_data_raw

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            sorted_values = self.__get_parameters_update(
                statistic, values, pit[0], intervals,
                self.scada_data.sensor_config.valves,
                self.topology.get_all_valves())
            self.animation_dict['valves'] = []
            vmin = min(sorted_values)
            vmax = max(sorted_values)
            for frame in range(*pit):
                if frame > values.shape[0] - 1:
                    break
                sorted_values = self.__get_parameters_update(
                    statistic, values, frame, intervals,
                    self.scada_data.sensor_config.valves,
                    self.topology.get_all_valves())
                vmin = min(*sorted_values, vmin)
                vmax = max(*sorted_values, vmax)
                self.animation_dict['valves'].append(sorted_values)
            self.valve_parameters['vmin'] = vmin
            self.valve_parameters['vmax'] = vmax
        else:
            sorted_values = self.__get_parameters_update(
                statistic, values, pit, intervals,
                self.scada_data.sensor_config.valves,
                self.topology.get_all_valves())
            self.valve_parameters.update(
                {'node_color': sorted_values, 'vmin': min(sorted_values),
                 'vmax': max(sorted_values)})

        if show_colorbar:
            if statistic == 'time_step':
                label = 'valve state'.capitalize() + ' at timestep ' + str(pit)
            else:
                label = str(statistic).capitalize() + ' ' + 'valve state'
            self.colorbars['valves'] = {'mappable': plt.cm.ScalarMappable(
                norm=mpl.colors.Normalize(vmin=self.valve_parameters['vmin'],
                                          vmax=self.valve_parameters['vmax']),
                cmap=colormap), 'label': label}

    def resize_links(
            self, scada_data: Optional[ScadaData] = None,
            parameter: str = 'flow_rate', statistic: str = 'mean',
            line_widths: Tuple[int] = (1, 2),
            pit: Optional[Union[int, Tuple[int]]] = None,
            intervals: Optional[Union[int, List[Union[int, float]]]] = None,
            conversion: Optional[dict] = None) -> None:
        """
        Resizes the width of the links (pipes) in the water distribution
        network based on SCADA data and the specified parameters.

        This method either takes or generates SCADA data, applies a statistic,
        optionally groups the results and prepares them to be either displayed
        statically ot animated as link width.

        Parameters
        ----------
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`, optional
            The SCADA data object. If `None`, a simulation will be run to
            generate it. Default is `None`.
        parameter : `str`, optional
            The data used to resize to. Default is 'flow_rate'.
        statistic : `str`, optional
            The statistic to calculate for the data. Can be 'mean', 'min',
            'max', or 'time_step'. Default is 'mean'.
        line_widths : `tuple(int, int)`, optional
            A tuple specifying the range of line widths to use when resizing
            links based on the data. Default is (1, 2).
        pit : `int` or `tuple(int, int)`, optional
            The point in time or range of time steps for the 'time_step'
            statistic. If a tuple is provided, it should contain two integers
            representing the start and end time steps. A tuple is necessary to
            process the data for the :meth:`~ScenarioVisualizer.show_animation`
            method. Default is `None`.
        intervals : `int` or `list[int]` or `list[float]`, optional
            If provided, the data will be grouped into intervals. It can be an
            integer specifying the number of groups or a list of boundary
            points. Default is `None`.
        conversion : `dict`, optional
            A dictionary of conversion parameters to convert SCADA data units.
            Default is `None`.
        """

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            sorted_values, sim_length = self.__get_link_data(scada_data,
                                                             parameter,
                                                             statistic, pit[0],
                                                             intervals,
                                                             conversion)
            pipe_size_list = []
            vmin = min(sorted_values)
            vmax = max(sorted_values)
            for frame in range(*pit):
                if frame > sim_length - 1:
                    break
                sorted_values, _ = self.__get_link_data(scada_data, parameter,
                                                        statistic, frame,
                                                        intervals, conversion)
                vmin = min(*sorted_values, vmin)
                vmax = max(*sorted_values, vmax)
                pipe_size_list.append(sorted_values)
            self.animation_dict['pipe_sizes'] = []
            for vals in pipe_size_list:
                self.animation_dict['pipe_sizes'].append(
                    self.__rescale(vals, line_widths,
                                   values_min_max=(vmin, vmax)))
        else:
            sorted_values, _ = self.__get_link_data(scada_data, parameter,
                                                    statistic, pit, intervals,
                                                    conversion)
            self.pipe_parameters.update(
                {'width': self.__rescale(sorted_values, line_widths)})

    def hide_nodes(self) -> None:
        """
        Hides all nodes (junctions) in the water distribution network
        visualization.

        This method clears the node list from the `junction_parameters`
        dictionary, effectively removing all nodes from view in the current
        visualization.
        """
        self.junction_parameters['nodelist'] = []

    def highlight_sensor_config(self) -> None:
        """
        Highlights nodes and links that have sensors in the sensor_config in
        the water distribution network visualization.

        This method identifies nodes and links equipped with different types of
        sensors from the :class:`~epyt_flow.simulation.sensor_config.SensorConfig` and
        updates their visual appearance. Nodes with sensors are highlighted
        with an orange border, while links with sensors are displayed with a
        dashed line style.
        """
        highlighted_nodes = []
        highlighted_links = []

        sensor_config = self.__scenario.sensor_config
        highlighted_nodes += (sensor_config.pressure_sensors
                              + sensor_config.demand_sensors
                              + sensor_config.quality_node_sensors)
        highlighted_links += (sensor_config.flow_sensors
                              + sensor_config.quality_link_sensors)

        node_edges = [
            (17, 163, 252) if node in highlighted_nodes else (0, 0, 0) for node
            in self.topology]
        pipe_style = ['dashed' if link in highlighted_links else 'solid' for
                      link in self.topology]

        self.junction_parameters.update(
            {'linewidths': 1, 'edgecolors': node_edges})
        self.pipe_parameters.update({'style': pipe_style})

    @deprecated(reason="This function will be removed in feature versions, "
                       "please use show_plot() instead.")
    def plot_topology(self, show_sensor_config: bool = False,
                      export_to_file: str = None) -> None:
        """
        Plots the topology of the water distribution network in the given
        scenario.

        Parameters
        ----------
        show_sensor_config : `bool`, optional
            Indicates whether the sensor configuration should be shown as well.

            The default is False.
        export_to_file : `str`, optional
            Path to the file where the visualization will be stored.
            If None, visualization will be just shown but NOT be stored
            anywhere.

            The default is None.
        """
        _ = plt.figure()

        highlighted_links = None
        highlighted_nodes = None
        if show_sensor_config is True:
            highlighted_nodes = []
            highlighted_links = []

            sensor_config = self.__scenario.sensor_config
            highlighted_nodes += (sensor_config.pressure_sensors
                                  + sensor_config.demand_sensors
                                  + sensor_config.quality_node_sensors)
            highlighted_links += (sensor_config.flow_sensors
                                  + sensor_config.quality_link_sensors)

        self.__scenario.epanet_api.plot(highlightlink=highlighted_links,
                                        highlightnode=highlighted_nodes,
                                        figure=False)

        if export_to_file is not None:
            plt.savefig(export_to_file, transparent=True, bbox_inches='tight')
        else:
            plt.show()
