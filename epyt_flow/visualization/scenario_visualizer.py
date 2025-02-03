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
from .visualization_utils import JunctionObject, EdgeObject, ColorScheme

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
    def __init__(self, scenario: ScenarioSimulator, color_scheme=ColorScheme.EPYT_FLOW) -> None:
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

        if isinstance(color_scheme, dict):
            self.color_scheme = color_scheme
        else:
            self.color_scheme = color_scheme.get_color_values()

        self.pipe_parameters = EdgeObject([x[1] for x in self.topology.get_all_links()], self.color_scheme['pipe_color'])
        self.junction_parameters = JunctionObject(self.topology.get_all_junctions(), node_color=self.color_scheme['node_color'])
        self.tank_parameters = JunctionObject(self.topology.get_all_tanks(), node_size=100, node_shape=markers.tank, node_color=self.color_scheme['tank_color'])
        self.reservoir_parameters = JunctionObject(self.topology.get_all_reservoirs(), node_size=100, node_shape=markers.reservoir, node_color=self.color_scheme['reservoir_color'])
        self.valve_parameters = JunctionObject(self.topology.get_all_valves(), node_size=50, node_shape=markers.valve, node_color=self.color_scheme['valve_color'])
        self.pump_parameters = JunctionObject(self.topology.get_all_pumps(), node_size=50, node_shape=markers.pump, node_color=self.color_scheme['pump_color'])

        self.colorbars = {}
        self.labels = {}

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
                                label='Pipes', **self.pipe_parameters.get_frame(frame_number))
        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Junctions', **self.junction_parameters.get_frame(frame_number))
        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Tanks', **self.tank_parameters.get_frame(frame_number))
        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Reservoirs',
                                **self.reservoir_parameters.get_frame(frame_number))
        nxp.draw_networkx_nodes(
            self.topology,
            self.__get_midpoints(self.topology.get_all_valves()), ax=self.ax,
            label='Valves', **self.valve_parameters.get_frame(frame_number))
        nxp.draw_networkx_nodes(
            self.topology, self.__get_midpoints(self.topology.get_all_pumps()),
            ax=self.ax, label='Pumps', **self.pump_parameters.get_frame(frame_number))

        self.__draw_labels()

        self.ax.legend(fontsize=6)

    def __interpolate_frames(self, num_inter_frames):

        for node_source in [self.junction_parameters, self.tank_parameters, self.reservoir_parameters, self.valve_parameters, self.pump_parameters]:
            node_source.interpolate(num_inter_frames)
        self.pipe_parameters.interpolate(num_inter_frames)

        return num_inter_frames

    def __draw_labels(self):
        for k, v in self.labels.items():
            if k in ['pipes']:
                nxp.draw_networkx_edge_labels(self.topology, ax=self.ax, **v)
                continue
            nxp.draw_networkx_labels(self.topology, ax=self.ax, **v)

    def add_labels(self, components: list or tuple = () or str, font_size=8):
        if components == 'all':
            components = ['nodes', 'tanks', 'reservoirs', 'pipes', 'valves', 'pumps']
        # if list empty, do all nodes and nothing else
        if len(components) == 0:
            self.labels['nodes'] = {'pos': self.pos_dict, 'labels': {n: str(n) for n in self.junction_parameters.nodelist}, 'font_size': font_size}
            return
        if 'nodes' in components:
            self.labels['nodes'] = {'pos': self.pos_dict, 'labels': {n: str(n) for n in self.junction_parameters.nodelist}, 'font_size': font_size}
        if 'tanks' in components:
            self.labels['tanks'] = {'pos': self.pos_dict, 'labels': {n: str(n) for n in self.tank_parameters.nodelist}, 'font_size': font_size}
        if 'reservoirs' in components:
            self.labels['reservoirs'] = {'pos': self.pos_dict, 'labels': {n: str(n) for n in self.reservoir_parameters.nodelist}, 'font_size': font_size}
        if 'pipes' in components:
            self.labels['pipes'] = {'pos': self.pos_dict, 'edge_labels': {tuple(n[1]): n[0] for n in self.topology.get_all_links()}, 'font_size': font_size}
        if 'valves' in components:
            self.labels['valves'] = {'pos': self.__get_midpoints(self.topology.get_all_valves()), 'labels': {n: str(n) for n in self.valve_parameters.nodelist}, 'verticalalignment': 'bottom', 'font_size': font_size}
        if 'pumps' in components:
            self.labels['pumps'] = {'pos': self.__get_midpoints(self.topology.get_all_pumps()), 'labels': {n: str(n) for n in self.pump_parameters.nodelist}, 'verticalalignment': 'bottom', 'font_size': font_size}

    def show_animation(self, export_to_file: str = None,
                       return_animation: bool = False, duration: int = 5, fps=15, interpolate=True)\
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
        for node_source in [self.junction_parameters, self.tank_parameters, self.reservoir_parameters, self.valve_parameters, self.pump_parameters]:
            if not isinstance(node_source.node_color, str) and len(node_source.node_color) > 1:
                total_frames = min(total_frames, len(node_source.node_color))
        if hasattr(self.pipe_parameters, 'edge_color'):
            if not isinstance(self.pipe_parameters.edge_color, str) and len(self.pipe_parameters.edge_color) > 1:
                total_frames = min(total_frames, len(self.pipe_parameters.edge_color))
        if hasattr(self.pipe_parameters, 'width'):
            if not isinstance(self.pipe_parameters.width, str) and len(self.pipe_parameters.width) > 1:
                total_frames = min(total_frames, len(self.pipe_parameters.width))

        if total_frames == 0 or total_frames == float('inf'):
            raise RuntimeError("The color or resize functions must be called "
                               "with a time_step range (pit) to enable "
                               "animations")

        if interpolate:
            total_frames = self.__interpolate_frames(fps*duration)

        anim = FuncAnimation(self.fig, self.__get_next_frame,
                             frames=total_frames, interval=round(duration*100/total_frames))

        if export_to_file is not None:
            anim.save(export_to_file, writer='ffmpeg', fps=fps)
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
                                label='Pipes', **self.pipe_parameters.get_frame())
        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Junctions', **self.junction_parameters.get_frame())
        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Tanks', **self.tank_parameters.get_frame())
        nxp.draw_networkx_nodes(self.topology, self.pos_dict, ax=self.ax,
                                label='Reservoirs',
                                **self.reservoir_parameters.get_frame())
        nxp.draw_networkx_nodes(
            self.topology,
            self.__get_midpoints(self.topology.get_all_valves()), ax=self.ax,
            label='Valves', **self.valve_parameters.get_frame())
        nxp.draw_networkx_nodes(
            self.topology, self.__get_midpoints(self.topology.get_all_pumps()),
            ax=self.ax, label='Pumps', **self.pump_parameters.get_frame())
        self.ax.legend(fontsize=6)

        self.__draw_labels()

        for colorbar_stats in self.colorbars.values():
            self.fig.colorbar(ax=self.ax, **colorbar_stats)

        if export_to_file is not None:
            plt.savefig(export_to_file, transparent=True, bbox_inches='tight',
                        dpi=200)
        plt.show()

    def color_nodes(
            self, data: Optional[ScadaData] = None,
            parameter: str = 'pressure', statistic: str = 'mean',
            pit: Optional[Union[int, Tuple[int, int]]] = None,
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
        self.junction_parameters.cmap = colormap

        if data is not None:
            self.scada_data = data
            if isinstance(data, ScadaData):
                all_junctions = self.scada_data.sensor_config.nodes
        elif not self.scada_data:
            self.scada_data = self.__scenario.run_simulation()
            all_junctions = self.scada_data.sensor_config.nodes

        if conversion:
            self.scada_data = self.scada_data.convert_units(**conversion)

        if parameter == 'pressure':
            values = self.scada_data.pressure_data_raw
        elif parameter == 'demand':
            values = self.scada_data.demand_data_raw
        elif parameter == 'node_quality':
            values = self.scada_data.node_quality_data_raw
        elif parameter == 'custom_data':
            # Custom should have the dimensions (timesteps, nodes)
            values = self.scada_data
            all_junctions = self.topology.get_all_junctions()
        else:
            raise ValueError(
                'Parameter must be pressure, demand, node_quality or custom_data.')

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            rng = pit
            if pit[1] == -1:
                rng = (pit[0], values.shape[0])
            for frame in range(*rng):
                if frame > values.shape[0] - 1:
                    break
                # TODO same, what if scada data is np array, do I have to use all_junctions with sensor config or can I use node_list?
                self.junction_parameters.add_frame(statistic, values, frame, intervals, all_junctions)
        else:
            # TODO: what do I do here if scada data is a numpy array? (custom data)
            self.junction_parameters.add_frame(statistic, values, pit, intervals, all_junctions)

        if show_colorbar:
            if statistic == 'time_step':
                label = str(parameter).capitalize() + ' at timestep ' + str(
                    pit)
            else:
                # TODO: replace auf andere Funktionen übertragen
                label = str(statistic).capitalize() + ' ' + str(parameter).replace('_', ' ')
            self.colorbars['junctions'] = {'mappable': plt.cm.ScalarMappable(
                norm=mpl.colors.Normalize(
                    vmin=self.junction_parameters.vmin,
                    vmax=self.junction_parameters.vmin), cmap=colormap),
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
        # TODO: hier und bei resize links EdgeObject für custom data anpassen
        if scada_data is not None:
            self.scada_data = scada_data
        elif not self.scada_data:
            self.scada_data = self.__scenario.run_simulation()

        if conversion:
            self.scada_data = self.scada_data.convert_units(**conversion)

        self.pipe_parameters.edge_cmap = mpl.colormaps[colormap]

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            rng = pit
            if pit[1] == -1:
                rng = (pit[0], self.scada_data.sensor_readings_time.shape[0])
            for frame in range(*rng):
                if frame > self.scada_data.sensor_readings_time.shape[0] - 1:
                    break
                self.pipe_parameters.add_frame(self.topology, 'edge_color',
                                               self.scada_data, parameter,
                                               statistic, frame, intervals)
        else:
            self.pipe_parameters.add_frame(self.topology, 'edge_color', self.scada_data, parameter, statistic, pit, intervals)

        if show_colorbar:
            if statistic == 'time_step':
                label = (str(parameter).capitalize().replace('_', ' ')
                         + ' at timestep ' + str(pit))
            else:
                label = str(statistic).capitalize() + ' ' + str(
                    parameter).replace('_', ' ')
            self.colorbars['pipes'] = {'mappable': plt.cm.ScalarMappable(
                norm=mpl.colors.Normalize(
                    vmin=self.pipe_parameters.edge_vmin,
                    vmax=self.pipe_parameters.edge_vmax), cmap=colormap),
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

        self.pump_parameters.cmap = colormap

        if scada_data is not None:
            self.scada_data = scada_data
            if isinstance(scada_data, ScadaData):
                all_pumps = self.scada_data.sensor_config.pumps
        elif not self.scada_data:
            self.scada_data = self.__scenario.run_simulation()
            all_pumps = self.scada_data.sensor_config.pumps

        if parameter == 'efficiency':
            values = self.scada_data.pumps_efficiency_data_raw
        elif parameter == 'energy_consumption':
            values = self.scada_data.pumps_energyconsumption_data_raw
        elif parameter == 'state':
            values = self.scada_data.pumps_state_data_raw
        elif parameter == 'custom_data':
            values = self.scada_data
            all_pumps = self.topology.get_all_pumps()
        else:
            raise ValueError(
                'Parameter must be efficiency, energy_consumption, state or custom_data')

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            rng = pit
            if pit[1] == -1:
                rng = (pit[0], values.shape[0])
            for frame in range(*rng):
                if frame > values.shape[0] - 1:
                    break
                self.pump_parameters.add_frame(statistic, values, frame, intervals, all_pumps)
        else:
            self.pump_parameters.add_frame(statistic, values, pit, intervals, all_pumps)

        if show_colorbar:
            if statistic == 'time_step':
                label = str(parameter).capitalize().replace(
                    '_', ' ') + ' at timestep ' + str(pit)
            else:
                label = str(statistic).capitalize() + ' ' + str(
                    parameter).replace('_', ' ')
            self.colorbars['pumps'] = {'mappable': plt.cm.ScalarMappable(
                norm=mpl.colors.Normalize(vmin=self.pump_parameters.vmin,
                                          vmax=self.pump_parameters.vmax),
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
        self.tank_parameters.cmap = colormap

        if scada_data is not None:
            self.scada_data = scada_data
            if isinstance(scada_data, ScadaData):
                all_tanks = self.scada_data.sensor_config.tanks
        elif not self.scada_data:
            self.scada_data = self.__scenario.run_simulation()
            all_tanks = self.scada_data.sensor_config.tanks

        # TODO: tanks hat ja gar keinen Parameter, den ich auf custom data checken könnte

        if isinstance(self.scada_data, ScadaData):
            values = self.scada_data.tanks_volume_data_raw
        else:
            values = self.scada_data
            all_tanks = self.topology.get_all_tanks()

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            rng = pit
            if pit[1] == -1:
                rng = (pit[0], values.shape[0])
            for frame in range(*rng):
                if frame > values.shape[0] - 1:
                    break
                self.tank_parameters.add_frame(statistic, values, frame, intervals, all_tanks)
        else:
            self.tank_parameters.add_frame(statistic, values, pit, intervals, all_tanks)

        if show_colorbar:
            # TODO: anpassen für custom data
            if statistic == 'time_step':
                label = 'tank volume'.capitalize() + ' at timestep ' + str(pit)
            else:
                label = str(statistic).capitalize() + ' ' + 'tank volume'
            self.colorbars['tanks'] = {'mappable': plt.cm.ScalarMappable(
                norm=mpl.colors.Normalize(vmin=self.tank_parameters.vmin,
                                          vmax=self.tank_parameters.vmin),
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

        self.valve_parameters.cmap = colormap

        if scada_data is not None:
            self.scada_data = scada_data
        elif not self.scada_data:
            self.scada_data = self.__scenario.run_simulation()

        values = self.scada_data.valves_state_data_raw

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            rng = pit
            if pit[1] == -1:
                rng = (pit[0], values.shape[0])
            for frame in range(*rng):
                if frame > values.shape[0] - 1:
                    break
                self.valve_parameters.add_frame(statistic, values, frame, intervals, self.scada_data.sensor_config.valves)
        else:
            self.valve_parameters.add_frame(statistic, values, pit,
                                            intervals,
                                            self.scada_data.sensor_config.valves)

        if show_colorbar:
            if statistic == 'time_step':
                label = 'valve state'.capitalize() + ' at timestep ' + str(pit)
            else:
                label = str(statistic).capitalize() + ' ' + 'valve state'
            self.colorbars['valves'] = {'mappable': plt.cm.ScalarMappable(
                norm=mpl.colors.Normalize(vmin=self.valve_parameters.vmin,
                                          vmax=self.valve_parameters.vmax),
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

        if scada_data is not None:
            self.scada_data = scada_data
        elif not self.scada_data:
            self.scada_data = self.__scenario.run_simulation()

        if conversion:
            self.scada_data = self.scada_data.convert_units(**conversion)

        if statistic == 'time_step' and isinstance(pit, tuple) and len(
                pit) == 2 and all(isinstance(i, int) for i in pit):
            rng = pit
            if pit[1] == -1:
                rng = (pit[0], self.scada_data.sensor_readings_time.shape[0])
            for frame in range(*rng):
                if frame > self.scada_data.sensor_readings_time.shape[0] - 1:
                    break
                self.pipe_parameters.add_frame(self.topology, 'edge_width',
                                               self.scada_data, parameter,
                                               statistic, frame, intervals)
        else:
            self.pipe_parameters.add_frame(self.topology, 'edge_width', self.scada_data, parameter, statistic, pit, intervals)
        self.pipe_parameters.rescale_widths(line_widths)

    def hide_nodes(self) -> None:
        """
        Hides all nodes (junctions) in the water distribution network
        visualization.

        This method clears the node list from the `junction_parameters`
        dictionary, effectively removing all nodes from view in the current
        visualization.
        """
        self.junction_parameters.nodelist = []

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

        self.junction_parameters.add_attributes(
            {'linewidths': 1, 'edgecolors': node_edges})
        self.pipe_parameters.add_attributes({'style': pipe_style})

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
