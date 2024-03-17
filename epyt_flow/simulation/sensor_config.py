"""
Module provides a class for implementing sensor configurations.
"""
from copy import deepcopy
import numpy as np

from ..serialization import SENSOR_CONFIG_ID, Serializable, serializable


SENSOR_TYPE_NODE_PRESSURE   = 1
SENSOR_TYPE_NODE_QUALITY    = 2
SENSOR_TYPE_NODE_DEMAND     = 3
SENSOR_TYPE_LINK_FLOW       = 4
SENSOR_TYPE_LINK_QUALITY    = 5
SENSOR_TYPE_VALVE_STATE     = 6
SENSOR_TYPE_PUMP_STATE      = 7
SENSOR_TYPE_TANK_LEVEL      = 8


@serializable(SENSOR_CONFIG_ID, ".epytflow_sensor_config")
class SensorConfig(Serializable):
    """
    Class for storing a sensor configuration.

    Parameters
    ----------
    nodes : `list[str]`
        List of all nodes (i.e. IDs) in the network.
    links : `list[str]`
        List of all links/pipes (i.e. IDs) in the network.
    valves : `list[str]`
        List of all valves (i.e. IDs) in the network.
    pumps : `list[str]`
        List of all pumps (i.e. IDs) in the network.
    tanks : `list[str]`
        List of all tanks (i.e. IDs) in the network.
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
    valve_state_sensors : `list[str]`, optional
        List of all valves (i.e. IDs) at which a valve state sensor is placed.

        The default is an empty list.
    pump_state_sensors : `list[str]`, optional
        List of all pumps (i.e. IDs) at which a pump state sensor is placed.

        The default is an empty list.
    tank_level_sensors : `list[str]`, optional
        List of all tanks (i.e. IDs) at which a tank level sensor is placed.

        The default is an empty list.
    """
    def __init__(self, nodes: list[str], links: list[str], valves: list[str], pumps: list[str],
                 tanks: list[str], pressure_sensors: list[str] = [],
                 flow_sensors: list[str] = [], demand_sensors: list[str] = [],
                 quality_node_sensors: list[str] = [], quality_link_sensors: list[str] = [],
                 valve_state_sensors: list[str] = [], pump_state_sensors: list[str] = [],
                 tank_level_sensors: list[str] = [], **kwds):
        if not isinstance(nodes, list):
            raise TypeError("'nodes' must be an instance of 'list(str)' " +
                            f"but not of '{type(nodes)}'")
        if len(nodes) == 0:
            raise ValueError("'nodes' must be a list of all nodes (i.e. IDs) in the network.")
        if any(not isinstance(n, str) for n in nodes):
            raise TypeError("Each item in 'nodes' must be an instance of 'str' -- " +
                            "ID of a node in the network.")
        if not isinstance(links, list):
            raise TypeError("'links' must be an instance of 'list(str)' " +
                            f"but not of '{type(links)}'")
        if len(links) == 0:
            raise ValueError("'links' must be a list of all links/pipes (i.e. IDs) in the network.")
        if any(not isinstance(link, str) for link in links):
            raise TypeError("Each item in 'links' must be an instance of 'str' -- " +
                            "ID of a link/pipe in the network.")

        if not isinstance(valves, list):
            raise TypeError("'valves' must be an instance of 'list(str)' " +
                            f"but not of '{type(valves)}'")
        if any(v not in links for v in valves):
            raise ValueError("Each item in 'valves' must be in 'links'")

        if not isinstance(pumps, list):
            raise TypeError("'pumps' must be an instance of 'list(str)' " +
                            f"but not of '{type(pumps)}'")
        if any(p not in links for p in pumps):
            raise ValueError("Each item in 'pumps' must be in 'links'")

        if not isinstance(tanks, list):
            raise TypeError("'tanks' must be an instance of 'list(str)' " +
                            f"but not of '{type(tanks)}'")
        if any(v not in nodes for v in tanks):
            raise ValueError("Each item in 'tanks' must be in 'nodes'")

        if not isinstance(pressure_sensors, list):
            raise TypeError("'pressure_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(pressure_sensors)}'")
        if any(n not in nodes for n in pressure_sensors):
            raise ValueError("Each item in 'pressure_sensors' must be in 'nodes' -- " +
                             "cannot place a sensor at a non-existing node.")
        if not isinstance(flow_sensors, list):
            raise TypeError("'flow_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(flow_sensors)}'")
        if any(link not in links for link in flow_sensors):
            raise ValueError("Each item in 'flow_sensors' must be in 'links' -- cannot " +
                             "place a sensor at a non-existing link/pipe.")
        if not isinstance(demand_sensors, list):
            raise TypeError("'demand_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(demand_sensors)}'")
        if any(n not in nodes for n in demand_sensors):
            raise ValueError("Each item in 'demand_sensors' must be in 'nodes' -- cannot " +
                             "place a sensor at a non-existing node.")
        if not isinstance(quality_node_sensors, list):
            raise TypeError("'quality_node_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(quality_node_sensors)}'")
        if any(n not in nodes for n in quality_node_sensors):
            raise ValueError("Each item in 'quality_node_sensors' must be in 'nodes' -- cannot " +
                             "place a sensor at a non-existing node.")
        if not isinstance(quality_link_sensors, list):
            raise TypeError("'quality_link_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(quality_link_sensors)}'")
        if any(link not in links for link in quality_link_sensors):
            raise ValueError("Each item in 'quality_link_sensors' must be in 'links' -- cannot " +
                             "place a sensor at a non-existing link/pipe.")
        if not isinstance(valve_state_sensors, list):
            raise TypeError("'valve_state_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(valve_state_sensors)}'")
        if any(link not in valves for link in valve_state_sensors):
            raise ValueError("Each item in 'valve_state_sensors' must be in 'valves' -- cannot " +
                             "place a sensor at a non-existing valve.")
        if not isinstance(pump_state_sensors, list):
            raise TypeError("'pump_state_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(pump_state_sensors)}'")
        if any(link not in pumps for link in pump_state_sensors):
            raise ValueError("Each item in 'pump_state_sensors' must be in 'pumps' -- cannot " +
                             "place a sensor at a non-existing pump.")
        if not isinstance(tank_level_sensors, list):
            raise TypeError("'tank_level_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(tank_level_sensors)}'")
        if any(n not in tanks for n in tank_level_sensors):
            raise ValueError("Each item in 'tank_level_sensors' must be in 'tanks' -- cannot " +
                             "place a sensor at a non-existing tanks.")

        self.__nodes = nodes
        self.__links = links
        self.__valves = valves
        self.__pumps = pumps
        self.__tanks = tanks
        self.__pressure_sensors = pressure_sensors
        self.__flow_sensors = flow_sensors
        self.__demand_sensors = demand_sensors
        self.__quality_node_sensors = quality_node_sensors
        self.__quality_link_sensors = quality_link_sensors
        self.__valve_state_sensors = valve_state_sensors
        self.__pump_state_sensors = pump_state_sensors
        self.__tank_level_sensors = tank_level_sensors

        self.__compute_indices()    # Compute indices

        super().__init__(**kwds)

    def __compute_indices(self):
        self.__pressure_idx = np.array([self.__nodes.index(n)
                                        for n in self.__pressure_sensors], dtype=np.int32)
        self.__flow_idx = np.array([self.__links.index(link)
                                    for link in self.__flow_sensors], dtype=np.int32)
        self.__demand_idx = np.array([self.__nodes.index(n)
                                      for n in self.__demand_sensors], dtype=np.int32)
        self.__quality_node_idx = np.array([self.__nodes.index(n)
                                            for n in self.__quality_node_sensors], dtype=np.int32)
        self.__quality_link_idx = np.array([self.__links.index(link)
                                            for link in self.__quality_link_sensors],
                                           dtype=np.int32)
        self.__valve_state_idx = np.array([self.__valves.index(v)
                                           for v in self.__valve_state_sensors], dtype=np.int32)
        self.__pump_state_idx = np.array([self.__pumps.index(p)
                                          for p in self.__pump_state_sensors], dtype=np.int32)
        self.__tank_level_idx = np.array([self.__tanks.index(t)
                                          for t in self.__tank_level_sensors], dtype=np.int32)

        n_pressure_sensors = len(self.__pressure_sensors)
        n_flow_sensors = len(self.__flow_sensors)
        n_demand_sensors = len(self.__demand_sensors)
        n_node_quality_sensors = len(self.__quality_node_sensors)
        n_link_quality_sensors = len(self.__quality_link_sensors)
        n_valve_state_sensors = len(self.__valve_state_sensors)
        n_pump_state_sensors = len(self.__pump_state_sensors)
        n_tank_level_sensors = len(self.__tank_level_sensors)

        pressure_idx_shift = 0
        flow_idx_shift = pressure_idx_shift + n_pressure_sensors
        demand_idx_shift = flow_idx_shift + n_flow_sensors
        node_quality_idx_shift = demand_idx_shift + n_demand_sensors
        link_quality_idx_shift = node_quality_idx_shift + n_node_quality_sensors
        valve_state_idx_shift = link_quality_idx_shift + n_link_quality_sensors
        pump_state_idx_shift = valve_state_idx_shift + n_valve_state_sensors
        tank_level_idx_shift = pump_state_idx_shift + n_pump_state_sensors

        self.__sensors_id_to_idx = {"pressure": {n: i + pressure_idx_shift for n, i in
                                                 zip(self.__pressure_sensors,
                                                     range(n_pressure_sensors))},
                                    "flow": {link: i + flow_idx_shift for link, i in
                                             zip(self.__flow_sensors, range(n_flow_sensors))},
                                    "demand": {n: i + demand_idx_shift for n, i in
                                               zip(self.__demand_sensors, range(n_demand_sensors))},
                                    "quality_node": {n: i + node_quality_idx_shift for n, i in
                                                     zip(self.__quality_node_sensors,
                                                         range(n_node_quality_sensors))},
                                    "quality_link": {link: i + link_quality_idx_shift for link, i in
                                                     zip(self.__quality_link_sensors,
                                                         range(n_link_quality_sensors))},
                                    "valve_state": {v: i + valve_state_idx_shift
                                                    for v, i in zip(self.__valve_state_sensors,
                                                                    range(n_valve_state_sensors))},
                                    "pump_state": {p: i + pump_state_idx_shift
                                                   for p, i in zip(self.__pump_state_sensors,
                                                                   range(n_pump_state_sensors))},
                                    "tank_level": {t: i + tank_level_idx_shift
                                                   for t, i in zip(self.__tank_level_sensors,
                                                                   range(n_tank_level_sensors))}}

    @property
    def nodes(self) -> list[str]:
        """
        Gets all node IDs.

        Returns
        -------
        `list[str]`
            All node IDs.
        """
        return self.__nodes.copy()

    @property
    def links(self) -> list[str]:
        """
        Gets all link IDs.

        Returns
        -------
        `list[str]`
            All link IDs.
        """
        return self.__links.copy()

    @property
    def valves(self) -> list[str]:
        """
        Gets all valve IDs (subset of link IDs).

        Returns
        -------
        `list[str]`
            All valve IDs.
        """
        return self.__valves.copy()

    @property
    def pumps(self) -> list[str]:
        """
        Gets all pump IDs (subset of link IDs).

        Returns
        -------
        `list[str]`
            All pump IDs.
        """
        return self.__pumps.copy()

    @property
    def tanks(self) -> list[str]:
        """
        Gets all tank IDs (subset of node IDs).

        Returns
        -------
        `list[str]`
            All tank IDs.
        """
        return self.__tanks.copy()

    @property
    def pressure_sensors(self) -> list[str]:
        """
        Gets all pressure sensors (i.e. IDs of nodes at which a pressure sensor is placed).

        Returns
        -------
        `list[str]`
            All node IDs with a pressure sensor.
        """
        return self.__pressure_sensors.copy()

    @pressure_sensors.setter
    def pressure_sensors(self, pressure_sensors: list[str]) -> None:
        if not isinstance(pressure_sensors, list):
            raise TypeError("'pressure_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(pressure_sensors)}'")
        if any(n not in self.__nodes for n in pressure_sensors):
            raise ValueError("Each item in 'pressure_sensors' must be in 'nodes' -- cannot " +
                             "place a sensor at a non-existing node.")

        self.__pressure_sensors = pressure_sensors

        self.__compute_indices()

    @property
    def flow_sensors(self) -> list[str]:
        """
        Gets all flow sensors (i.e. IDs of links at which a flow sensor is placed).

        Returns
        -------
        `list[str]`
            All link IDs with a flow sensor.
        """
        return self.__flow_sensors.copy()

    @flow_sensors.setter
    def flow_sensors(self, flow_sensors: list[str]) -> None:
        if not isinstance(flow_sensors, list):
            raise TypeError("'pressure_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(flow_sensors)}'")
        if any(link not in self.__links for link in flow_sensors):
            raise ValueError("Each item in 'flow_sensors' must be in 'links' -- cannot " +
                             "place a sensor at a non-existing link/pipe.")

        self.__flow_sensors = flow_sensors

        self.__compute_indices()

    @property
    def demand_sensors(self) -> list[str]:
        """
        Gets all demand sensors (i.e. IDs of nodes at which a demand sensor is placed).

        Returns
        -------
        `list[str]`
            All node IDs with a demand sensor.
        """
        return self.__demand_sensors.copy()

    @demand_sensors.setter
    def demand_sensors(self, demand_sensors: list[str]) -> None:
        if not isinstance(demand_sensors, list):
            raise TypeError("'demand_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(demand_sensors)}'")
        if any(n not in self.__nodes for n in demand_sensors):
            raise ValueError("Each item in 'demand_sensors' must be in 'nodes' -- cannot " +
                             "place a sensor at a non-existing node.")

        self.__demand_sensors = demand_sensors

        self.__compute_indices()

    @property
    def quality_node_sensors(self) -> list[str]:
        """
        Gets all node quality sensors (i.e. IDs of nodes at which a node quality sensor is placed).

        Returns
        -------
        `list[str]`
            All node IDs with a node quality sensor.
        """
        return self.__quality_node_sensors.copy()

    @quality_node_sensors.setter
    def quality_node_sensors(self, quality_node_sensors: list[str]) -> None:
        if not isinstance(quality_node_sensors, list):
            raise TypeError("'quality_node_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(quality_node_sensors)}'")
        if any(n not in self.__nodes for n in quality_node_sensors):
            raise ValueError("Each item in 'quality_node_sensors' must be in 'nodes' -- cannot " +
                             "place a sensor at a non-existing node.")

        self.__quality_node_sensors = quality_node_sensors

        self.__compute_indices()

    @property
    def quality_link_sensors(self) -> list[str]:
        """
        Gets all link quality sensors (i.e. IDs of links at which a link quality sensor is placed).

        Returns
        -------
        `list[str]`
            All link IDs with a link quality sensor.
        """
        return self.__quality_link_sensors.copy()

    @quality_link_sensors.setter
    def quality_link_sensors(self, quality_link_sensors: list[str]) -> None:
        if not isinstance(quality_link_sensors, list):
            raise TypeError("'quality_link_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(quality_link_sensors)}'")
        if any(link not in self.__links for link in quality_link_sensors):
            raise ValueError("Each item in 'quality_link_sensors' must be in 'links' -- cannot " +
                             "place a sensor at a non-existing link/pipe.")

        self.__quality_link_sensors = quality_link_sensors

        self.__compute_indices()

    @property
    def valve_state_sensors(self) -> list[str]:
        """
        Gets all valve state sensors (i.e. IDs of valves at which a valve state sensor is placed).

        Returns
        -------
        `list[str]`
            All valve IDs with a valve state sensor.
        """
        return self.__valve_state_sensors.copy()

    @valve_state_sensors.setter
    def valve_state_sensors(self, valve_state_sensors: list[str]) -> None:
        if not isinstance(valve_state_sensors, list):
            raise TypeError("'valve_state_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(valve_state_sensors)}'")
        if any(link not in self.__valves for link in valve_state_sensors):
            raise ValueError("Each item in 'valve_state_sensors' must be in 'valves' -- cannot " +
                             "place a sensor at a non-existing valves.")

        self.__valve_state_sensors = valve_state_sensors

        self.__compute_indices()

    @property
    def pump_state_sensors(self) -> list[str]:
        """
        Gets all pump state sensors (i.e. IDs of pumps at which a pump state sensor is placed).

        Returns
        -------
        `list[str]`
            All link IDs with a pump state sensor.
        """
        return self.__pump_state_sensors.copy()

    @pump_state_sensors.setter
    def pump_state_sensors(self, pump_state_sensors: list[str]) -> None:
        if not isinstance(pump_state_sensors, list):
            raise TypeError("'pump_state_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(pump_state_sensors)}'")
        if any(link not in self.__pumps for link in pump_state_sensors):
            raise ValueError("Each item in 'pump_state_sensors' must be in 'pumps' -- cannot " +
                             "place a sensor at a non-existing pump.")

        self.__pump_state_sensors = pump_state_sensors

        self.__compute_indices()

    @property
    def tank_level_sensors(self) -> list[str]:
        """
        Gets all tank level sensors (i.e. IDs of tanks at which a tank level sensor is placed).

        Returns
        -------
        `list[str]`
            All tank IDs with a tank level sensor.
        """
        return self.__tank_level_sensors.copy()

    @tank_level_sensors.setter
    def tank_level_sensors(self, tank_level_sensors: list[str]) -> None:
        if not isinstance(tank_level_sensors, list):
            raise TypeError("'tank_level_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(tank_level_sensors)}'")
        if any(n not in self.__tanks for n in tank_level_sensors):
            raise ValueError("Each item in 'tank_level_sensors' must be in 'tanks' -- cannot " +
                             "place a sensor at a non-existing tanks.")

        self.__tank_level_sensors = tank_level_sensors

        self.__compute_indices()

    @property
    def sensors_id_to_idx(self) -> dict:
        """
        Gets a mapping of sensor IDs to indices in the final Numpy array returned by `get_data()`.

        Returns
        -------
        `dict`
            Mapping of sensor IDs to indices in the final Numpy array.
        """
        return deepcopy(self.__sensors_id_to_idx)

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"nodes": self.__nodes, "links": self.__links,
                                           "valves": self.__valves, "pumps": self.__pumps,
                                           "tanks": self.__tanks,
                                           "pressure_sensors": self.__pressure_sensors,
                                           "flow_sensors": self.__flow_sensors,
                                           "demand_sensors": self.__demand_sensors,
                                           "quality_node_sensors": self.__quality_node_sensors,
                                           "quality_link_sensors": self.__quality_link_sensors,
                                           "valve_state_sensors": self.__valve_state_sensors,
                                           "pump_state_sensors": self.__pump_state_sensors,
                                           "tank_level_sensors": self.__tank_level_sensors}

    def __eq__(self, other) -> bool:
        if not isinstance(other, SensorConfig):
            raise TypeError("Can not compare 'SensorConfig' instance " +
                            f"with '{type(other)}' instance")

        return self.__nodes == other.nodes and self.__links == other.links \
            and self.__valves == other.valves and self.__pumps == other.pumps \
            and self.__tanks == other.tanks \
            and self.__pressure_sensors == other.pressure_sensors \
            and self.__flow_sensors == other.flow_sensors \
            and self.__demand_sensors == other.demand_sensors \
            and self.__quality_node_sensors == other.quality_node_sensors \
            and self.__quality_link_sensors == other.quality_link_sensors \
            and self.__valve_state_sensors == other.valve_state_sensors \
            and self.__pump_state_sensors == other.pump_state_sensors \
            and self.__tank_level_sensors == other.tank_level_sensors

    def __str__(self) -> str:
        return f"nodes: {self.__nodes} links: {self.__links} valves: {self.__valves} " +\
            f"pumps: {self.__pumps} tanks: {self.__tanks} " +\
            f"pressure_sensors: {self.__pressure_sensors} flow_sensors: {self.__flow_sensors} " +\
            f"demand_sensors: {self.__demand_sensors} " +\
            f"quality_node_sensors: {self.__quality_node_sensors} " +\
            f"quality_link_sensors: {self.__quality_link_sensors} " +\
            f"valve_state_sensors: {self.__valve_state_sensors} " +\
            f"pump_state_sensors: {self.__pump_state_sensors} " +\
            f"tank_level_sensors: {self.__tank_level_sensors}"

    def compute_readings(self, pressures: np.ndarray, flows: np.ndarray, demands: np.ndarray,
                         nodes_quality: np.ndarray, links_quality: np.ndarray,
                         pumps_state: np.ndarray, valves_state: np.ndarray,
                         tanks_level: np.ndarray) -> np.ndarray:
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
        pumps_state : `numpy.ndarray`
            States of all pumps.
        valves_state : `numpy.ndarray`
            States of all valves.
        tanks_level : `numpy.ndarray`
            Water levels of all tanks.

        Returns
        -------
        `numpy.ndarray`
            Sensor readings.
        """
        data = []
        data.append(pressures[:, self.__pressure_idx])
        data.append(flows[:, self.__flow_idx])
        data.append(demands[:, self.__demand_idx])
        data.append(nodes_quality[:, self.__quality_node_idx])
        data.append(links_quality[:, self.__quality_link_idx])
        data.append(valves_state[:, self.__valve_state_idx])
        data.append(pumps_state[:, self.__pump_state_idx])
        data.append(tanks_level[:, self.__tank_level_idx])

        return np.concatenate(data, axis=1)

    def get_index_of_reading(self, pressure_sensor: str = None, flow_sensor: str = None,
                             demand_sensor: str = None, node_quality_sensor: str = None,
                             link_quality_sensor: str = None, valve_state_sensor: str = None,
                             pump_state_sensor: str = None, tank_level_sensor: str = None) -> int:
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
        valve_state_sensor : `str`
            ID of the state sensor (at a valve)
        pump_state_sensor : `str`
            ID of the state sensor (at a pump)
        tank_level_sensor : `str`
            ID of the water level sensor (at a tank)
        """
        if pressure_sensor is not None:
            return self.__sensors_id_to_idx["pressure"][pressure_sensor]
        elif flow_sensor is not None:
            return self.__sensors_id_to_idx["flow"][flow_sensor]
        elif demand_sensor is not None:
            return self.__sensors_id_to_idx["demand"][demand_sensor]
        elif node_quality_sensor is not None:
            return self.__sensors_id_to_idx["quality_node"][node_quality_sensor]
        elif link_quality_sensor is not None:
            return self.__sensors_id_to_idx["quality_link"][link_quality_sensor]
        elif valve_state_sensor is not None:
            return self.__sensors_id_to_idx["valve_state"][valve_state_sensor]
        elif pump_state_sensor is not None:
            return self.__sensors_id_to_idx["pump_state"][pump_state_sensor]
        elif tank_level_sensor is not None:
            return self.__sensors_id_to_idx["tank_level"][tank_level_sensor]
        else:
            raise ValueError("No sensor given")
