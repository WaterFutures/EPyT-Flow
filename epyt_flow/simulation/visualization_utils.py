from dataclasses import dataclass
import numpy as np
from typing import Optional, Union, List, Tuple, Iterable
import inspect
import networkx.drawing.nx_pylab as nxp
import matplotlib as mpl


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


# TODO: adjust!!! to pipes
@dataclass
class PipeObject:
    nodelist: list
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

        attributes = vars(self)

        if not isinstance(self.node_color, str):
            if frame_number > len(self.node_color):
                frame_number = 0
            attributes['node_color'] = self.node_color[frame_number]

        sig = inspect.signature(nxp.draw_networkx_edges)

        valid_params = {
            key: value for key, value in attributes.items()
            if key in sig.parameters and value is not None
        }

        return valid_params

    def add_attributes(self, attributes: dict):
        for key, value in attributes.items():
            setattr(self, key, value)
