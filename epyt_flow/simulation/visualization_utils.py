from dataclasses import dataclass
import numpy as np
from typing import Optional, Union, List, Tuple, Iterable
import inspect
import networkx.drawing.nx_pylab as nxp
import matplotlib as mpl

from .scada.scada_data import ScadaData


@dataclass
class JunctionObject:
    nodelist: list
    node_shape: mpl.path.Path = None
    node_size: int = 10
    node_color: Union[str, list] = 'k' # list of lists with frames or single letter

    def add_frame(self, statistic: str, values: np.ndarray,
                                pit: Union[int, Tuple[int]],
                                intervals: Union[int, List[Union[int, float]]],
                                all_junctions: List[str]):

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
        sorted_values = [value_dict[x] for x in self.nodelist]

        if isinstance(self.node_color, str):
            # First run of this method
            self.node_color = []
            self.vmin = min(sorted_values)
            self.vmax = max(sorted_values)

        self.node_color.append(sorted_values)
        self.vmin = min(*sorted_values, self.vmin)
        self.vmax = max(*sorted_values, self.vmin)

    def get_frame(self, frame_number: int = 0):

        attributes = vars(self).copy()

        if not isinstance(self.node_color, str):
            if frame_number > len(self.node_color):
                frame_number = -1
            attributes['node_color'] = self.node_color[frame_number]

        sig = inspect.signature(nxp.draw_networkx_nodes)

        valid_params = {
            key: value for key, value in attributes.items()
            if key in sig.parameters and value is not None
        }

        return valid_params

    def add_attributes(self, attributes: dict):
        for key, value in attributes.items():
            setattr(self, key, value)


@dataclass
class EdgeObject:
    edgelist: list
    edge_color: Union[str, list] = 'k' # list of lists with frames or single letter

    def rescale_widths(self, line_widths: Tuple[int] = (1, 2)):
        if not hasattr(self, 'width'):
            raise AttributeError("Please call add_frame with edge_param=width before rescaling the widths.")

        vmin = min(min(l) for l in self.width)
        vmax = max(max(l) for l in self.width)

        tmp = []
        for il in self.width:
            tmp.append(self.__rescale(il, line_widths, values_min_max=(vmin, vmax)))
        self.width = tmp

    def add_frame(
            self, topology, edge_param: str, scada_data: Optional[ScadaData] = None,
            parameter: str = 'flow_rate', statistic: str = 'mean',
            pit: Optional[Union[int, Tuple[int]]] = None,
            intervals: Optional[Union[int, List[Union[int, float]]]] = None):

        if edge_param == 'edge_width' and not hasattr(self, 'width'):
            self.width = []
        else:
            if isinstance(self.edge_color, str):
                self.edge_color = []
                self.edge_vmin = float('inf')
                self.edge_vmax = float('-inf')

        if parameter == 'flow_rate':
            values = scada_data.flow_data_raw
        elif parameter == 'link_quality':
            values = scada_data.link_quality_data_raw
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
            raise ValueError('Parameter must be flow_rate or link_quality')

        self.sim_length = values.shape[0]

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

        value_dict = dict(zip(scada_data.sensor_config.links,
                              stat_values))
        sorted_values = [value_dict[x[0]] for x in topology.get_all_links()]

        if edge_param == 'edge_width':
            self.width.append(values)
        else:
            self.edge_color.append(sorted_values)
            self.edge_vmin = min(*sorted_values, self.edge_vmin)
            self.edge_vmax = max(*sorted_values, self.edge_vmax)

    def get_frame(self, frame_number: int = 0):

        attributes = vars(self).copy()

        if not isinstance(self.edge_color, str):
            if frame_number > len(self.edge_color):
                frame_number = -1
            attributes['edge_color'] = self.edge_color[frame_number]

        if hasattr(self, 'width'):
            if frame_number > len(self.width):
                frame_number = -1
            attributes['width'] = self.width[frame_number]

        sig = inspect.signature(nxp.draw_networkx_edges)

        valid_params = {
            key: value for key, value in attributes.items()
            if key in sig.parameters and value is not None
        }

        return valid_params

    def add_attributes(self, attributes: dict):
        for key, value in attributes.items():
            setattr(self, key, value)

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


