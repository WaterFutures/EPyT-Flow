"""
Module provides helper functions and data management classes for visualizing
scenarios.
"""
import inspect
from dataclasses import dataclass
from typing import Optional, Union, List, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx.drawing.nx_pylab as nxp
import numpy as np
from scipy.interpolate import CubicSpline

from ..serialization import COLOR_SCHEMES_ID, JsonSerializable, serializable
from ..simulation.scada.scada_data import ScadaData

# Selection of functions for processing visualization data
stat_funcs = {
    'mean': np.mean,
    'min': np.min,
    'max': np.max
}


@dataclass
class JunctionObject:
    """
    Represents a junction component (e.g. nodes, tanks, reservoirs, ...) in a
    water distribution network and manages all relevant attributes for drawing.

    Attributes
    ----------
    nodelist : `list`
        List of all nodes in WDN pertaining to this component type.
    pos : `dict`
        A dictionary mapping nodes to their coordinates in the correct format
        for drawing.
    node_shape : :class:`matplotlib.path.Path` or None
        A shape representing the object, if none, the networkx default circle
        is used.
    node_size : `int`, default = 10
        The size of each node.
    node_color : `str` or `list`, default = 'k'
        If `string`: the color for all nodes, if `list`: a list of lists
        containing a numerical value for each node per frame, which will be
        used for coloring.
    interpolated : `bool`, default = False
        Set to True, if node_colors are interpolated for smoother animation.
    """
    nodelist: list
    pos: dict
    node_shape: mpl.path.Path = None
    node_size: int = 10
    node_color: Union[str, list] = 'k'
    interpolated: bool = False

    def add_frame(self, statistic: str, values: np.ndarray,
                  pit: int, intervals: Union[int, List[Union[int, float]]]):
        """
        Adds a new frame of node_color based on a given statistic.

        Parameters
        ----------
        statistic : `str`
            The statistic to calculate for the data. Can be 'mean', 'min',
             'max' or 'time_step'.
        values : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            The node values over time as extracted from the scada data.
        pit : `int`
            The point in time for the 'time_step' statistic.
        intervals : `int`, `list[int]` or `list[float]`
            If provided, the data will be grouped into intervals. It can be an
            integer specifying the number of groups or a list of boundary
            points.

        Raises
        ------
        ValueError
            If interval, pit or statistic is not correctly provided.

        """
        if statistic in stat_funcs:
            stat_values = stat_funcs[statistic](values, axis=0)
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

        sorted_values = [v for _, v in zip(self.nodelist, stat_values)]

        if isinstance(self.node_color, str):
            # First run of this method
            self.node_color = []
            self.vmin = min(sorted_values)
            self.vmax = max(sorted_values)

        self.node_color.append(sorted_values)
        self.vmin = min(*sorted_values, self.vmin)
        self.vmax = max(*sorted_values, self.vmax)

    def get_frame(self, frame_number: int = 0):
        """
        Returns all attributes necessary for networkx to draw the specified
        frame.

        Parameters
        ----------
        frame_number : `int`, default = 0
            The frame whose parameters should be returned. Default is 0, this
            is also used if only 1 frame exists (e.g. for plots, not
            animations).

        Returns
        -------
        valid_params : `dict`
            A dictionary containing all attributes that function as parameters
            for `networkx.drawing.nx_pylab.draw_networkx_nodes() <https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx_nodes.html#draw-networkx-nodes>`_.
        """

        attributes = vars(self).copy()

        if not isinstance(self.node_color, str):
            if self.interpolated:
                if frame_number > len(self.node_color_inter):
                    frame_number = -1
                attributes['node_color'] = self.node_color_inter[frame_number]
            else:
                if frame_number > len(self.node_color):
                    frame_number = -1
                attributes['node_color'] = self.node_color[frame_number]

        sig = inspect.signature(nxp.draw_networkx_nodes)

        valid_params = {
            key: value for key, value in attributes.items()
            if key in sig.parameters and value is not None
        }

        return valid_params

    def get_frame_mask(self, mask, color):
        """
        Returns all attributes necessary for networkx to draw the specified
        frame mask. Meaning covering all masked junction objects with the
        default value.

        Parameters
        ----------
        mask: `np.ndarray`
            An array consisting of 0 and 1, where 0 means no sensor. Nodes
            without sensor are to be masked.
        color:
            The default color of masked nodes.

        Returns
        -------
        valid_params : `dict`
            A dictionary containing all attributes that function as parameters
            for `networkx.drawing.nx_pylab.draw_networkx_nodes() <https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx_nodes.html#draw-networkx-nodes>`_.
        """

        attributes = vars(self).copy()

        attributes['nodelist'] = [node for node, flag in
                                  zip(self.nodelist, mask) if not flag]
        attributes['node_color'] = color

        sig = inspect.signature(nxp.draw_networkx_nodes)

        valid_params = {
            key: value for key, value in attributes.items()
            if key in sig.parameters and key not in ['vmin', 'vmax', 'cmap']
            and value is not None
        }

        return valid_params

    def interpolate(self, num_inter_frames: int):
        """
        Interpolates node_color values for smoother animations.

        Parameters
        ----------
        num_inter_frames : `int`
            The number of total frames after interpolation.
        """
        if isinstance(self.node_color, str) or len(self.node_color) <= 1:
            return

        tmp_node_color = np.array(self.node_color)
        steps, num_nodes = tmp_node_color.shape

        x_axis = np.linspace(0, steps - 1, steps)
        new_x_axis = np.linspace(0, steps - 1, num_inter_frames)

        self.node_color_inter = np.zeros(((len(new_x_axis)), num_nodes))

        for node in range(num_nodes):
            cs = CubicSpline(x_axis, tmp_node_color[:, node])
            self.node_color_inter[:, node] = cs(new_x_axis)

        self.interpolated = True

    def add_attributes(self, attributes: dict):
        """
        Adds the given attributes dict as class attributes.

        Parameters
        ----------
        attributes : `dict`
            Attributes dict, which is to be added as class attributes.
        """
        for key, value in attributes.items():
            setattr(self, key, value)


@dataclass
class EdgeObject:
    """
    Represents an edge component (pipes) in a water distribution network and
    manages all relevant attributes for drawing.

    Attributes
    ----------
    edgelist : `list`
        List of all edges in WDN pertaining to this component type.
    pos : `dict`
        A dictionary mapping pipes to their coordinates in the correct format
        for drawing.
    edge_color : `str` or `list`, default = 'k'
        If `string`: the color for all edges, if `list`: a list of lists
        containing a numerical value for each edge per frame, which will be
        used for coloring.
    interpolated : `dict`, default = {}
        Filled with interpolated frames if interpolation method is called.
    """
    edgelist: list
    pos: dict
    edge_color: Union[str, list] = 'k'
    interpolated = {}

    def rescale_widths(self, line_widths: Tuple[int, int] = (1, 2)):
        """
        Rescales all edge widths to the given interval.

        Parameters
        ----------
        line_widths : `Tuple[int]`, default = (1, 2)
        Min and max value, to which the edge widths should be scaled.

        Raises
        ------
        AttributeError
            If no edge width attribute exists yet.
        """
        if not hasattr(self, 'width'):
            raise AttributeError(
                'Please call add_frame with edge_param=width before rescaling'
                ' the widths.')

        vmin = min(min(l) for l in self.width)
        vmax = max(max(l) for l in self.width)

        tmp = []
        for il in self.width:
            tmp.append(
                self.__rescale(il, line_widths, values_min_max=(vmin, vmax)))
        self.width = tmp

    def add_frame(
            self, topology, edge_param: str,
            scada_data: Optional[ScadaData],
            parameter: str = 'flow_rate', statistic: str = 'mean',
            pit: Optional[Union[int, Tuple[int]]] = None,
            species: str = None,
            intervals: Optional[Union[int, List[Union[int, float]]]] = None,
            use_sensor_data: bool = None):
        """
        Adds a new frame of edge_color or edge width based on the given data
        and statistic.

        Parameters
        ----------
        topology : :class:`~epyt_flow.topology.NetworkTopology`
            Topology object retrieved from the scenario, containing the
            structure of the water distribution network.
        edge_param : `str`
            Method can be called with edge_width or edge_color to calculate
            either the width or color for the next frame.
        scada_data : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            SCADA data created by the :class:`~epyt_flow.simulation.scenario_simulator.ScenarioSimulator`
            instance, is used to retrieve data for the next frame.
        parameter : `str`, default = 'flow_rate'
            The link data to visualize. Options are 'flow_rate', 'velocity', or
            'status'. Default is 'flow_rate'.
        statistic : `str`, default = 'mean'
            The statistic to calculate for the data. Can be 'mean', 'min',
             'max' or 'time_step'.
        pit : `int`
            The point in time for the 'time_step' statistic.
        species: `str`, optional
            Key of the species. Necessary only for parameter
            'bulk_species_concentration'.
        intervals : `int`, `list[int]` or `list[float]`
            If provided, the data will be grouped into intervals. It can be an
            integer specifying the number of groups or a list of boundary
            points.
        use_sensor_data : `bool`, optional
            If `True`, instead of using raw simulation data, the data recorded
            by the corresponding sensors in the system is used for the
            visualization. Note: Not all components may have a sensor attached
            and sensors may be subject to sensor faults or noise.

        Raises
        ------
        ValueError
            If parameter, interval, pit or statistic is not set correctly.
        """
        if edge_param == 'edge_width' and not hasattr(self, 'width'):
            self.width = []
        elif edge_param == 'edge_color':
            if isinstance(self.edge_color, str):
                self.edge_color = []
                self.edge_vmin = float('inf')
                self.edge_vmax = float('-inf')

        if parameter == 'flow_rate':
            if use_sensor_data:
                values, self.mask = scada_data.get_data_flows_as_edge_features()
                values = values[:, ::2]
                self.mask = self.mask[::2]
            else:
                values = scada_data.flow_data_raw
        elif parameter == 'link_quality':
            if use_sensor_data:
                values, self.mask = scada_data.get_data_links_quality_as_edge_features()
                values = values[:, ::2]
                self.mask = self.mask[::2]
            else:
                values = scada_data.link_quality_data_raw
        elif parameter == 'custom_data':
            values = scada_data
        elif parameter == 'bulk_species_concentration':
            if not species:
                raise ValueError('Species must be given when using '
                                 'bulk_species_concentration')
            if use_sensor_data:
                values, self.mask = scada_data.get_data_bulk_species_concentrations_as_edge_features()
                self.mask = self.mask[::2,
                            scada_data.sensor_config.bulk_species.index(
                                species)]
                values = values[:, ::2,
                         scada_data.sensor_config.bulk_species.index(species)]
            else:
                values = scada_data.bulk_species_link_concentration_raw[:,
                         scada_data.sensor_config.bulk_species.index(species),
                         :]
        elif parameter == 'diameter':
            value_dict = {
                link[0]: topology.get_link_info(link[0])['diameter'] for
                link in topology.get_all_links()}
            sorted_values = [value_dict[x[0]] for x in
                             topology.get_all_links()]

            if edge_param == 'edge_width':
                self.width.append(sorted_values)
            else:
                self.edge_color.append(sorted_values)
                self.edge_vmin = min(*sorted_values, self.edge_vmin)
                self.edge_vmax = max(*sorted_values, self.edge_vmax)
            return
        else:
            raise ValueError('Parameter must be flow_rate, link_quality, '
                             'diameter or custom_data.')

        if statistic in stat_funcs:
            stat_values = stat_funcs[statistic](values, axis=0)
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

        sorted_values = list(stat_values)

        if edge_param == 'edge_width':
            self.width.append(sorted_values)
        else:
            self.edge_color.append(sorted_values)
            self.edge_vmin = min(*sorted_values, self.edge_vmin)
            self.edge_vmax = max(*sorted_values, self.edge_vmax)

    def get_frame(self, frame_number: int = 0):
        """
        Returns all attributes necessary for networkx to draw the specified
        frame.

        Parameters
        ----------
        frame_number : `int`, default = 0
            The frame whose parameters should be returned. Default is 0, this
            is also used if only 1 frame exists (e.g. for plots, not
            animations).

        Returns
        -------
        valid_params : `dict`
            A dictionary containing all attributes that function as parameters
            for `networkx.drawing.nx_pylab.draw_networkx_edges() <https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx_edges.html#draw-networkx-edges>`_.
        """
        attributes = vars(self).copy()

        if not isinstance(self.edge_color, str):
            if 'edge_color' in self.interpolated.keys():
                if frame_number > len(self.interpolated['edge_color']):
                    frame_number = -1
                attributes['edge_color'] = self.interpolated['edge_color'][
                    frame_number]
            else:
                if frame_number > len(self.edge_color):
                    frame_number = -1
                attributes['edge_color'] = self.edge_color[frame_number]

        if hasattr(self, 'width'):
            if 'width' in self.interpolated.keys():
                if frame_number > len(self.interpolated['width']):
                    frame_number = -1
                attributes['width'] = self.interpolated['width'][frame_number]
            else:
                if frame_number > len(self.width):
                    frame_number = -1
                attributes['width'] = self.width[frame_number]

        sig = inspect.signature(nxp.draw_networkx_edges)

        valid_params = {
            key: value for key, value in attributes.items()
            if key in sig.parameters and value is not None
        }

        return valid_params

    def get_frame_mask(self, frame_number: int = 0, color='k'):
        """
        Returns all attributes necessary for networkx to draw the specified
        frame mask.

        Parameters
        ----------
        frame_number : `int`, default = 0
            The frame whose parameters should be returned. Default is 0, this
            is also used if only 1 frame exists (e.g. for plots, not
            animations).
        color:
            The default color of masked nodes.

        Returns
        -------
        valid_params : `dict`
            A dictionary containing all attributes that function as parameters
            for `networkx.drawing.nx_pylab.draw_networkx_edges() <https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx_edges.html#draw-networkx-edges>`_.
        """
        attributes = vars(self).copy()

        attributes['edgelist'] = [edge for edge, flag in
                                  zip(self.edgelist, self.mask) if not flag]
        attributes['edge_color'] = color

        if hasattr(self, 'width'):
            if 'width' in self.interpolated.keys():
                if frame_number > len(self.interpolated['width']):
                    frame_number = -1
                attributes['width'] = self.interpolated['width'][frame_number]
            else:
                if frame_number > len(self.width):
                    frame_number = -1
                attributes['width'] = self.width[frame_number]
            attributes['width'] = [edge for edge, flag in
                                   zip(attributes['width'].copy(), self.mask)
                                   if not flag]

        sig = inspect.signature(nxp.draw_networkx_edges)

        valid_params = {
            key: value for key, value in attributes.items()
            if key in sig.parameters and key not in ['vmin', 'vmax', 'cmap']
            and value is not None
        }

        return valid_params

    def interpolate(self, num_inter_frames: int):
        """
        Interpolates edge_color and width values for smoother animations.

        Parameters
        ----------
        num_inter_frames : `int`
            The number of total frames after interpolation.
        """
        targets = {'edge_color': self.edge_color}
        if hasattr(self, 'width'):
            targets['width'] = self.width

        for name, inter_target in targets.items():
            if isinstance(inter_target, str) or len(inter_target) <= 1:
                continue

            tmp_target = np.array(inter_target)
            steps, num_edges = tmp_target.shape

            x_axis = np.linspace(0, steps - 1, steps)
            new_x_axis = np.linspace(0, steps - 1, num_inter_frames)

            vals_inter = np.zeros(((len(new_x_axis)), num_edges))

            for edge in range(num_edges):
                cs = CubicSpline(x_axis, tmp_target[:, edge])
                vals_inter[:, edge] = cs(new_x_axis)

            self.interpolated[name] = vals_inter

    def add_attributes(self, attributes: dict):
        """
        Adds the given attributes dict as class attributes.

        Parameters
        ----------
        attributes : `dict`
            Attributes dict, which is to be added as class attributes.
        """
        for key, value in attributes.items():
            setattr(self, key, value)

    def __rescale(self, values: Union[np.ndarray, list],
                  scale_min_max: Union[List, Tuple[int]],
                  values_min_max: Union[
                      List, Tuple[int, int]] = None) -> np.ndarray:
        """
        Rescales the given values to a new range.

        This method rescales an array of values to fit within a specified
        minimum and maximum scale range. Optionally, the minimum and maximum
        of the input values can be manually provided; otherwise, they are
        automatically determined from the data.

        Parameters
        ----------
        values : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ or `list`
            The array of numerical values to be rescaled.
        scale_min_max : `list` or `tuple`
            A list or tuple containing two elements: the minimum and maximum
            values of the desired output range.
        values_min_max : `list` or `tuple`, optional
            A list or tuple containing two elements: the minimum and maximum
            values of the input data. If not provided, they are computed from
            the input `values`. Default is `None`.

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

        vectorized_range_map = np.vectorize(range_map)
        rescaled_widths = vectorized_range_map(np.array(values))

        if hasattr(self, 'mask'):
            rescaled_widths = np.where(self.mask == 1, rescaled_widths, 1.0)

        return rescaled_widths


@serializable(COLOR_SCHEMES_ID, ".epyt_flow_color_scheme")
class ColorScheme(JsonSerializable):
    """
    A class containing the color scheme for the
    :class:`~epyt_flow.visualization.ScenarioVisualizer`.
    """

    def __init__(self, pipe_color: str, node_color: str, pump_color: str,
                 tank_color: str, reservoir_color: str,
                 valve_color: str) -> None:
        """Initializes the ColorScheme class with the given component colors.

        Accepted formats are the string representations accepted by matplotlib:
        https://matplotlib.org/stable/users/explain/colors/colors.html#color-formats

        Parameters
        ----------
        pipe_color : str
            String color format accepted by matplotlib.
        node_color : str
            String color format accepted by matplotlib.
        pump_color : str
            String color format accepted by matplotlib.
        tank_color : str
            String color format accepted by matplotlib.
        reservoir_color : str
            String color format accepted by matplotlib.
        valve_color : str
            String color format accepted by matplotlib.
        """
        self.pipe_color = pipe_color
        self.node_color = node_color
        self.pump_color = pump_color
        self.tank_color = tank_color
        self.reservoir_color = reservoir_color
        self.valve_color = valve_color
        super().__init__()

    def get_attributes(self) -> dict:
        """
        Gets all attributes needed for serialization.

        Returns
        -------
        attr : A dictionary containing all attributes to be serialized.
        """
        attr = {
            k: v for k, v in self.__dict__.items()
            if
            not (k.startswith("__") or k.startswith("_")) and not callable(v)
        }
        return super().get_attributes() | attr

    def __eq__(self, other: any) -> bool:
        """
        Checks if two ColorScheme instances are equal.

        Parameters
        ----------
        other : :class:`~epyt_flow.visualization_utils.ColorScheme`
            The other ColorScheme instance to compare this one with.

        Returns
        -------
        bool
            True if all attributes are the same, False otherwise.
        """
        if not isinstance(other, ColorScheme):
            return False
        return (
                self.pipe_color == other.pipe_color and
                self.node_color == other.node_color and
                self.pump_color == other.pump_color and
                self.tank_color == other.tank_color and
                self.reservoir_color == other.reservoir_color and
                self.valve_color == other.valve_color
        )

    def __str__(self) -> str:
        """
        Returns a string representation of the ColorScheme instance.

        Returns
        -------
        str
            A string describing the ColorScheme instance.
        """
        return (f"ColorScheme(pipe_color={self.pipe_color}, "
                f"node_color={self.node_color}, "
                f"pump_color={self.pump_color}, "
                f"tank_color={self.tank_color}, "
                f"reservoir_color={self.reservoir_color}, "
                f"valve_color={self.valve_color})")


epanet_colors = ColorScheme(
    pipe_color="#0403ee",
    node_color="#0403ee",
    pump_color="#fe00ff",
    tank_color="#02fffd",
    reservoir_color="#00ff00",
    valve_color="#000000"
)

epyt_flow_colors = ColorScheme(
    pipe_color="#29222f",
    node_color="#29222f",
    pump_color="#d79233",
    tank_color="#607b80",
    reservoir_color="#33483d",
    valve_color="#a3320b"
)

black_colors = ColorScheme(
    pipe_color="#000000",
    node_color="#000000",
    pump_color="#000000",
    tank_color="#000000",
    reservoir_color="#000000",
    valve_color="#000000"
)
