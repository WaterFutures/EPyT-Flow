import numpy
import numpy as np

from ..serialization import SENSOR_CONFIG_ID, Serializable, serializable



SENSOR_TYPE_NODE_PRESSURE   = 1
SENSOR_TYPE_NODE_QUALITY    = 2
SENSOR_TYPE_NODE_DEMAND     = 3
SENSOR_TYPE_LINK_FLOW       = 4
SENSOR_TYPE_LINK_QUALITY    = 5


@serializable(SENSOR_CONFIG_ID)
class SensorConfig(Serializable):
    """
    Class for storing a sensor configuration.

    Parameters
    ----------
    nodes : `list[str]`
        List of all nodes (i.e. IDs) in the network.
    links : `list[str]`
        List of all links/pipes (i.e. IDs) in the network.
    pressure_sensors : `list[str]`, optional
        List of all nodes (i.e. IDs) at which a pressure sensor is placed.

        The default is an empty list.
    flow_sensors : `list[str]`, optional
        List of all links/pipes (i.e. IDs) at which a flow sensor is placed.

        The default is an empty list.
    demand_sensors : `list[str]`, optional
        List of all nodes (i.e. IDs) at which a demand sensor is placed..

        The default is an empty list.
    quality_node_sensors : `list[str]`, optional
        List of all nodes (i.e. IDs) at which a quality sensor is placed.

        The default is an empty list.
    quality_link_sensors : `list[str]`, optional
        List of all links/pipes (i.e. IDs) at which a flow sensor is placed.

        The default is an empty list.
    """
    def __init__(self, nodes:list[str], links:list[str], pressure_sensors:list[str]=[],
                 flow_sensors:list[str]=[], demand_sensors:list[str]=[],
                 quality_node_sensors:list[str]=[], quality_link_sensors:list[str]=[], **kwds):
        if not isinstance(nodes, list):
            raise ValueError("'nodes' must be an instance of 'list(str)' "+\
                             f"but not of '{type(nodes)}'")
        if len(nodes) == 0:
            raise ValueError("'nodes' must be a list of all nodes (i.e. IDs) in the network.")
        if any([not isinstance(n, str) for n in nodes]):
            raise ValueError("Each item in 'nodes' must be an instance of 'str' -- "+\
                             "ID of a node in the network.")
        if not isinstance(links, list):
            raise ValueError("'links' must be an instance of 'list(str)' "+\
                             f"but not of '{type(links)}'")
        if len(links) == 0:
            raise ValueError("'links' must be a list of all links/pipes (i.e. IDs) in the network.")
        if any([not isinstance(l, str) for l in links]):
            raise ValueError("Each item in 'links' must be an instance of 'str' -- "+\
                             "ID of a link/pipe in the network.")
        if not isinstance(pressure_sensors, list):
            raise ValueError("'pressure_sensors' must be an instance of 'list[str]' "+\
                             f"but not of '{type(pressure_sensors)}'")
        if any([n not in nodes for n in pressure_sensors]):
            raise ValueError("Each item in 'pressure_sensors' must be in 'nodes' -- "+\
                             "cannot place a sensor at a non-existing node.")
        if not isinstance(flow_sensors, list):
            raise ValueError("'flow_sensors' must be an instance of 'list[str]' "+\
                             f"but not of '{type(flow_sensors)}'")
        if any([l not in links for l in flow_sensors]):
            raise ValueError("Each item in 'flow_sensors' must be in 'links' -- cannot "+\
                             "place a sensor at a non-existing link/pipe.")
        if not isinstance(demand_sensors, list):
            raise ValueError("'demand_sensors' must be an instance of 'list[str]' "+\
                             f"but not of '{type(demand_sensors)}'")
        if any([n not in nodes for n in demand_sensors]):
            raise ValueError("Each item in 'demand_sensors' must be in 'nodes' -- cannot "+\
                             "place a sensor at a non-existing node.")
        if not isinstance(quality_node_sensors, list):
            raise ValueError("'quality_node_sensors' must be an instance of 'list[str]' "+\
                             f"but not of '{type(quality_node_sensors)}'")
        if any([n not in nodes for n in quality_node_sensors]):
            raise ValueError("Each item in 'quality_node_sensors' must be in 'nodes' -- cannot "+\
                             "place a sensor at a non-existing node.")
        if not isinstance(quality_link_sensors, list):
            raise ValueError("'quality_link_sensors' must be an instance of 'list[str]' "+\
                             f"but not of '{type(quality_link_sensors)}'")
        if any([l not in links for l in quality_link_sensors]):
            raise ValueError("Each item in 'quality_link_sensors' must be in 'links' -- cannot "+\
                             "place a sensor at a non-existing link/pipe.")

        self.__nodes = nodes
        self.__links = links
        self.__pressure_sensors = pressure_sensors
        self.__flow_sensors = flow_sensors
        self.__demand_sensors = demand_sensors
        self.__quality_node_sensors = quality_node_sensors
        self.__quality_link_sensors = quality_link_sensors

        self.__compute_indices()    # Compute indices

        super().__init__(**kwds)

    def __compute_indices(self):
        self.__pressure_idx = np.array([self.__nodes.index(n) \
                                        for n in self.__pressure_sensors], dtype=np.int32)
        self.__flow_idx = np.array([self.__links.index(l) \
                                    for l in self.__flow_sensors], dtype=np.int32)
        self.__demand_idx = np.array([self.__nodes.index(n) \
                                      for n in self.__demand_sensors], dtype=np.int32)
        self.__quality_node_idx = np.array([self.__nodes.index(n) \
                                            for n in self.__quality_node_sensors], dtype=np.int32)
        self.__quality_link_idx = np.array([self.__links.index(l) \
                                            for l in self.__quality_link_sensors], dtype=np.int32)

        n_pressure_sensors = len(self.__pressure_sensors)
        n_flow_sensors = len(self.__flow_sensors)
        n_demand_sensors = len(self.__demand_sensors)
        n_node_quality_sensors = len(self.__quality_node_sensors)
        n_link_quality_sensors = len(self.__quality_link_sensors)

        pressure_idx_shift = 0
        flow_idx_shift = pressure_idx_shift + n_pressure_sensors
        demand_idx_shift = flow_idx_shift + n_flow_sensors
        node_quality_idx_shift = demand_idx_shift + n_demand_sensors
        link_quality_idx_shift = node_quality_idx_shift + n_node_quality_sensors

        self.__sensord_id_to_idx = {"pressure": {n: i + pressure_idx_shift for n, i in \
                                                 zip(self.__pressure_sensors, \
                                                     range(n_pressure_sensors))},
                                    "flow": {l: i + flow_idx_shift for l, i in \
                                             zip(self.__flow_sensors, range(n_flow_sensors))},
                                    "demand": {n: i + demand_idx_shift for n, i in \
                                               zip(self.__demand_sensors, range(n_demand_sensors))},
                                    "quality_node": {n: i + node_quality_idx_shift for n, i in \
                                                     zip(self.__quality_node_sensors, \
                                                         range(n_node_quality_sensors))},
                                    "quality_link": {l: i + link_quality_idx_shift for l, i in \
                                                     zip(self.__quality_link_sensors, \
                                                         range(n_link_quality_sensors))}}

    @property
    def nodes(self) -> list[str]:
        return self.__nodes.copy()

    @property
    def links(self) -> list[str]:
        return self.__links.copy()

    @property
    def pressure_sensors(self) -> list[str]:
        return self.__pressure_sensors.copy()

    @pressure_sensors.setter
    def pressure_sensors(self, pressure_sensors:list[str]) -> None:
        if not isinstance(pressure_sensors, list):
            raise ValueError("'pressure_sensors' must be an instance of 'list[str]' "+\
                             f"but not of '{type(pressure_sensors)}'")
        if any([n not in self.__nodes for n in pressure_sensors]):
            raise ValueError("Each item in 'pressure_sensors' must be in 'nodes' -- cannot "+\
                             "place a sensor at a non-existing node.")

        self.__pressure_sensors = pressure_sensors

        self.__compute_indices()

    @property
    def flow_sensors(self) -> list[str]:
        return self.__flow_sensors.copy()

    @flow_sensors.setter
    def flow_sensors(self, flow_sensors:list[str]) -> None:
        if not isinstance(flow_sensors, list):
            raise ValueError("'pressure_sensors' must be an instance of 'list[str]' "+\
                             f"but not of '{type(flow_sensors)}'")
        if any([l not in self.__links for l in flow_sensors]):
            raise ValueError("Each item in 'flow_sensors' must be in 'links' -- cannot "+\
                             "place a sensor at a non-existing link/pipe.")

        self.__flow_sensors = flow_sensors

        self.__compute_indices()

    @property
    def demand_sensors(self) -> list[str]:
        return self.__demand_sensors.copy()

    @demand_sensors.setter
    def demand_sensors(self, demand_sensors:list[str]) -> None:
        if not isinstance(demand_sensors, list):
            raise ValueError("'demand_sensors' must be an instance of 'list[str]' "+\
                             f"but not of '{type(demand_sensors)}'")
        if any([n not in self.__nodes for n in demand_sensors]):
            raise ValueError("Each item in 'demand_sensors' must be in 'nodes' -- cannot "+\
                             "place a sensor at a non-existing node.")

        self.__demand_sensors = demand_sensors

        self.__compute_indices()

    @property
    def quality_node_sensors(self) -> list[str]:
        return self.__quality_node_sensors.copy()

    @quality_node_sensors.setter
    def quality_node_sensors(self, quality_node_sensors:list[str]) -> None:
        if not isinstance(quality_node_sensors, list):
            raise ValueError("'quality_node_sensors' must be an instance of 'list[str]' "+\
                             f"but not of '{type(quality_node_sensors)}'")
        if any([n not in self.__nodes for n in quality_node_sensors]):
            raise ValueError("Each item in 'quality_node_sensors' must be in 'nodes' -- cannot "+\
                             "place a sensor at a non-existing node.")

        self.__quality_node_sensors = quality_node_sensors

        self.__compute_indices()

    @property
    def quality_link_sensors(self) -> list[str]:
        return self.__quality_link_sensors.copy()

    @quality_link_sensors.setter
    def quality_link_sensors(self, quality_link_sensors:list[str]) -> None:
        if not isinstance(quality_link_sensors, list):
            raise ValueError("'quality_link_sensors' must be an instance of 'list[str]' "+\
                             f"but not of '{type(quality_link_sensors)}'")
        if any([n not in self.__nodes for n in quality_link_sensors]):
            raise ValueError("Each item in 'quality_link_sensors' must be in 'nodes' -- cannot "+\
                             "place a sensor at a non-existing node.")

        self.__quality_link_sensors = quality_link_sensors

        self.__compute_indices()

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"nodes": self.__nodes, "links": self.__links,
                                           "pressure_sensors": self.__pressure_sensors,
                                           "flow_sensors": self.__flow_sensors,
                                           "demand_sensors": self.__demand_sensors,
                                           "quality_node_sensors": self.__quality_node_sensors,
                                           "quality_link_sensors": self.__quality_link_sensors}

    def __eq__(self, other) -> bool:
        return self.__nodes == other.nodes and self.__links == other.links \
            and self.__pressure_sensors == other.pressure_sensors \
            and self.__flow_sensors == other.flow_sensors \
            and self.__demand_sensors == other.demand_sensors \
            and self.__quality_node_sensors == other.quality_node_sensors \
            and self.__quality_link_sensors == other.quality_link_sensors

    def __str__(self) -> str:
        return f"nodes: {self.__nodes} links: {self.__links} "+\
            f"pressure_sensors: {self.__pressure_sensors} flow_sensors: {self.__flow_sensors} "+\
            f"demand_sensors: {self.__demand_sensors} "+\
            f"quality_node_sensors: {self.__quality_node_sensors} "+\
            f"quality_link_sensors: {self.__quality_link_sensors}"

    def compute_readings(self, pressures:numpy.ndarray, flows:numpy.ndarray, demands:numpy.ndarray,
                         nodes_quality:numpy.ndarray, links_quality:numpy.ndarray) -> numpy.ndarray:
        """
        Applies the sensor configuration to a set of raw simulation results -- 
        i.e. computes the sensor readings as an array.

        Parameters
        ----------
        pressures : `numpy.ndarray`
            Pressure values at all nodes.
        flows : `numpy.ndarray`
            Flow values at all links/pipes.
        demands : `numpy.ndarray`
            Demand values at all nodes.
        nodes_quality : `numpy.ndarray`
            Quality values at all nodes.
        links_quality : `numpy.ndarray`
            Quality values at all links/pipes.
        
        Returns
        -------
        `numpy.ndarray`
            Sensor readings.
        """
        data = []
        data.append(pressures[:,self.__pressure_idx])
        data.append(flows[:,self.__flow_idx])
        data.append(demands[:,self.__demand_idx])
        data.append(nodes_quality[:,self.__quality_node_idx])
        data.append(links_quality[:,self.__quality_link_idx])

        return np.concatenate(data, axis=1)

    def get_index_of_reading(self, pressure_sensor:str=None, flow_sensor:str=None,
                             demand_sensor:str=None, node_quality_sensor:str=None,
                             link_quality_sensor:str=None) -> int:
        """
        Gets the index of a particular sensor in the final sensor readings array.

        Note that only one sensor ID is converted to an index. In case of multiple sensor IDs, 
        call this function for each sensor ID separately.

        Parameters
        ----------
        pressure_sensor : `str`
            ID of the pressure sensor.
        flow_sensor : `str`
            ID of the flow sensor.
        demand_sensor : `str`
            ID of the demand sensor
        node_quality_sensor : `str`
            ID of the quality sensor (at a node).
        link_quality_sensor : `str`
            ID of the quality sensor (at a link/pipe)
        """
        if pressure_sensor is not None:
            return self.__sensord_id_to_idx["pressure"][pressure_sensor]
        elif flow_sensor is not None:
            return self.__sensord_id_to_idx["flow"][flow_sensor]
        elif demand_sensor is not None:
            return self.__sensord_id_to_idx["demand"][demand_sensor]
        elif node_quality_sensor is not None:
            return self.__sensord_id_to_idx["quality_node"][node_quality_sensor]
        elif link_quality_sensor is not None:
            return self.__sensord_id_to_idx["quality_link"][link_quality_sensor]
        else:
            raise ValueError("No sensor given")
