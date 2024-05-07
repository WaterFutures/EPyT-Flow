"""
Module provides a class for implementing sensor configurations.
"""
from copy import deepcopy
import numpy as np
import epyt

from ..serialization import SENSOR_CONFIG_ID, JsonSerializable, serializable


SENSOR_TYPE_NODE_PRESSURE     = 1
SENSOR_TYPE_NODE_QUALITY      = 2
SENSOR_TYPE_NODE_DEMAND       = 3
SENSOR_TYPE_LINK_FLOW         = 4
SENSOR_TYPE_LINK_QUALITY      = 5
SENSOR_TYPE_VALVE_STATE       = 6
SENSOR_TYPE_PUMP_STATE        = 7
SENSOR_TYPE_TANK_VOLUME       = 8
SENSOR_TYPE_NODE_BULK_SPECIES = 9
SENSOR_TYPE_LINK_BULK_SPECIES = 10
SENSOR_TYPE_SURFACE_SPECIES   = 11


@serializable(SENSOR_CONFIG_ID, ".epytflow_sensor_config")
class SensorConfig(JsonSerializable):
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
    species : `list[str]`
        List of all (EPANET-MSX) species (i.e. IDs) in the network    
    pressure_sensors : `list[str]`, optional
        List of all nodes (i.e. IDs) at which a pressure sensor is placed.

        The default is an empty list.
    flow_sensors : `list[str]`, optional
        List of all links/pipes (i.e. IDs) at which a flow sensor is placed.

        The default is an empty list.
    demand_sensors : `list[str]`, optional
        List of all nodes (i.e. IDs) at which a demand sensor is placed.

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
    tank_volume_sensors : `list[str]`, optional
        List of all tanks (i.e. IDs) at which a tank volume sensor is placed.

        The default is an empty list.
    bulk_species_node_sensors : `dict`, optional
        Bulk species node sensors as a dictionary -- i.e. bulk species ID are the keys,
        and the sensor locations (node IDs) are the values.

        The default is an empty list.
    bulk_species_link_sensors : `dict`, optional
        Bulk species link/pipe sensors as a dictionary -- i.e. bulk species ID are the keys,
        and the sensor locations (link/pipe IDs) are the values.

        The default is an empty list.
    surface_species_sensors : `dict`, optional
        Surface species sensors as a dictionary -- i.e. surface species ID are the keys,
        and the sensor locations (link/pipe IDs) are the values.

        The default is an empty list.
    node_id_to_idx : `dict`, optional
        Mapping of a node ID to the EPANET index (i.e. position in the raw sensor reading data).

        If None is given, it is assumed that the nodes (in 'nodes') are
        sorted according to their EPANET index.

        The default is None.
    link_id_to_idx : `dict`, optional
        Mapping of a link/pipe ID to the EPANET index
        (i.e. position in the raw sensor reading data).

        If None is given, it is assumed that the links/pipes (in 'links') are
        sorted according to their EPANET index..

        The default is None.
    valve_id_to_idx : `dict`, optional
        Mapping of a valve ID to the EPANET index (i.e. position in the raw sensor reading data).

        If None is given, it is assumed that the valves (in 'valves') are
        sorted according to their EPANET index.

        The default is None.
    pump_id_to_idx : `dict`, optional
        Mapping of a pump ID to the EPANET index (i.e. position in the raw sensor reading data).

        If None is given, it is assumed that the pumps (in 'pumps') are
        sorted according to their EPANET index.

        The default is None.
    tank_id_to_idx : `dict`, optional
        Mapping of a tank ID to the EPANET index (i.e. position in the raw sensor reading data).

        If None is given, it is assumed that the tanks (in 'tanks') are
        sorted according to their EPANET index.

        The default is None.
    bulkspecies_id_to_idx : `dict`, optional
        Mapping of a surface species ID to the EPANET index
        (i.e. position in the raw sensor reading data).

        If None is given, it is assumed that the surface species (in 'surface_species') are
        sorted according to their EPANET index.

        The default is None.
    """
    def __init__(self, nodes: list[str], links: list[str], valves: list[str], pumps: list[str],
                 tanks: list[str], bulk_species: list[str], surface_species: list[str],
                 pressure_sensors: list[str] = [],
                 flow_sensors: list[str] = [],
                 demand_sensors: list[str] = [],
                 quality_node_sensors: list[str] = [],
                 quality_link_sensors: list[str] = [],
                 valve_state_sensors: list[str] = [],
                 pump_state_sensors: list[str] = [],
                 tank_volume_sensors: list[str] = [],
                 bulk_species_node_sensors: dict = {},
                 bulk_species_link_sensors: dict = {},
                 surface_species_sensors: dict = {},
                 node_id_to_idx: dict = None, link_id_to_idx: dict = None,
                 valve_id_to_idx: dict = None, pump_id_to_idx: dict = None,
                 tank_id_to_idx: dict = None, bulkspecies_id_to_idx: dict = None,
                 surfacespecies_id_to_idx: dict = None, **kwds):
        if not isinstance(nodes, list):
            raise TypeError("'nodes' must be an instance of 'list[str]' " +
                            f"but not of '{type(nodes)}'")
        if len(nodes) == 0:
            raise ValueError("'nodes' must be a list of all nodes (i.e. IDs) in the network.")
        if any(not isinstance(n, str) for n in nodes):
            raise TypeError("Each item in 'nodes' must be an instance of 'str' -- " +
                            "ID of a node in the network.")

        if not isinstance(links, list):
            raise TypeError("'links' must be an instance of 'list[str]' " +
                            f"but not of '{type(links)}'")
        if len(links) == 0:
            raise ValueError("'links' must be a list of all links/pipes (i.e. IDs) in the network.")
        if any(not isinstance(link, str) for link in links):
            raise TypeError("Each item in 'links' must be an instance of 'str' -- " +
                            "ID of a link/pipe in the network.")

        if not isinstance(valves, list):
            raise TypeError("'valves' must be an instance of 'list[str]' " +
                            f"but not of '{type(valves)}'")
        if any(v not in links for v in valves):
            raise ValueError("Each item in 'valves' must be in 'links'")

        if not isinstance(pumps, list):
            raise TypeError("'pumps' must be an instance of 'list[str]' " +
                            f"but not of '{type(pumps)}'")
        if any(p not in links for p in pumps):
            raise ValueError("Each item in 'pumps' must be in 'links'")

        if not isinstance(tanks, list):
            raise TypeError("'tanks' must be an instance of 'list[str]' " +
                            f"but not of '{type(tanks)}'")
        if any(v not in nodes for v in tanks):
            raise ValueError("Each item in 'tanks' must be in 'nodes'")

        if not isinstance(bulk_species, list):
            raise TypeError("'bulk_species' must be an instance of 'list[str]' " +
                            f"but not of '{type(bulk_species)}'")
        if any(not isinstance(bulk_species_id, str) for bulk_species_id in bulk_species):
            raise TypeError("Each item in 'bulk_species' must be an instance of 'str'")

        if not isinstance(surface_species, list):
            raise TypeError("'surface_species' must be an instance of 'list[str]' " +
                            f"but not of '{type(surface_species)}'")
        if any(not isinstance(surface_species_id, str) for surface_species_id in surface_species):
            raise TypeError("Each item in 'surface_species' must be an instance of 'str'")

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

        if not isinstance(tank_volume_sensors, list):
            raise TypeError("'tank_volume_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(tank_volume_sensors)}'")
        if any(n not in tanks for n in tank_volume_sensors):
            raise ValueError("Each item in 'tank_volume_sensors' must be in 'tanks' -- cannot " +
                             "place a sensor at a non-existing tanks.")

        if not isinstance(bulk_species_node_sensors, dict):
            raise TypeError("'bulk_species_node_sensors' must be an instance of 'dict' but not " +
                            f"of '{type(bulk_species_node_sensors)}'")
        if any(bulk_species_id not in bulk_species
               for bulk_species_id in bulk_species_node_sensors.keys()):
            raise ValueError("Unknown bulk species ID in 'bulk_species_node_sensors'")
        if any(node_id not in nodes for node_id in bulk_species_node_sensors.values()):
            raise ValueError("Unknown node ID in 'bulk_species_node_sensors'")

        if not isinstance(bulk_species_link_sensors, dict):
            raise TypeError("'bulk_species_link_sensors' must be an instance of 'dict' but not " +
                            f"of '{type(bulk_species_link_sensors)}'")
        if any(bulk_species_id not in bulk_species
               for bulk_species_id in bulk_species_link_sensors.keys()):
            raise ValueError("Unknown bulk species ID in 'bulk_species_link_sensors'")
        if any(link_id not in links for link_id in bulk_species_link_sensors.values()):
            raise ValueError("Unknown link/pipe ID in 'bulk_species_link_sensors'")

        if not isinstance(surface_species_sensors, dict):
            raise TypeError("'surface_species_sensors' must be an instance of 'dict' but not " +
                            f"of '{type(surface_species_sensors)}'")
        if any(surface_species_id not in surface_species_sensors
               for surface_species_id in surface_species_sensors.keys()):
            raise ValueError("Unknown surface species ID in 'surface_species_sensors'")
        if any(link_id not in links for link_id in surface_species_sensors.values()):
            raise ValueError("Unknown link ID in 'surface_species_sensors'")

        if node_id_to_idx is not None:
            if not isinstance(node_id_to_idx, dict):
                raise TypeError("'node_id_to_idx' must be an instance of 'dict' " +
                                f"but not of '{type(node_id_to_idx)}'")
            if any(n not in nodes for n in node_id_to_idx.keys()):
                raise ValueError("Unknown node ID in 'node_id_to_idx'")

        if link_id_to_idx is not None:
            if not isinstance(link_id_to_idx, dict):
                raise TypeError("'link_id_to_idx' must be an instance of 'dict' " +
                                f"but not of '{type(link_id_to_idx)}'")
            if any(link_id not in links for link_id in link_id_to_idx.keys()):
                raise ValueError("Unknown link/pipe ID in 'link_id_to_idx'")

        if valve_id_to_idx is not None:
            if not isinstance(valve_id_to_idx, dict):
                raise TypeError("'valve_id_to_idx' must be an instance of 'dict' " +
                                f"but not of '{type(valve_id_to_idx)}'")
            if any(v not in valves for v in valve_id_to_idx.keys()):
                raise ValueError("Unknown valve ID in 'valve_id_to_idx'")

        if pump_id_to_idx is not None:
            if not isinstance(pump_id_to_idx, dict):
                raise TypeError("'pump_id_to_idx' must be an instance of 'dict' " +
                                f"but not of '{type(pump_id_to_idx)}'")
            if any(p not in valves for p in pump_id_to_idx.keys()):
                raise ValueError("Unknown pump ID in 'pump_id_to_idx'")

        if tank_id_to_idx is not None:
            if not isinstance(tank_id_to_idx, dict):
                raise TypeError("'tank_id_to_idx' must be an instance of 'dict' " +
                                f"but not of '{type(tank_id_to_idx)}'")
            if any(t not in tanks for t in tank_id_to_idx.keys()):
                raise ValueError("Unknown tank ID in 'tank_id_to_idx'")

        if bulkspecies_id_to_idx is not None:
            if not isinstance(bulkspecies_id_to_idx, dict):
                raise TypeError("'bulkspecies_id_to_idx' must be an instance of 'dict' " +
                                f"but not of '{type(bulkspecies_id_to_idx)}'")
            if any(s not in bulk_species for s in bulkspecies_id_to_idx.keys()):
                raise ValueError("Unknown bulk species ID in 'bulkspecies_id_to_idx'")

        if surfacespecies_id_to_idx is not None:
            if not isinstance(surfacespecies_id_to_idx, dict):
                raise TypeError("'surfacespecies_id_to_idx' must be an instance of 'dict' " +
                                f"but not of '{type(surfacespecies_id_to_idx)}'")
            if any(s not in surface_species for s in surfacespecies_id_to_idx.keys()):
                raise ValueError("Unknown surface species ID in 'surfacespecies_id_to_idx'")

        self.__nodes = nodes
        self.__links = links
        self.__valves = valves
        self.__pumps = pumps
        self.__tanks = tanks
        self.__bulk_species = bulk_species
        self.__surface_species = surface_species
        self.__pressure_sensors = pressure_sensors
        self.__flow_sensors = flow_sensors
        self.__demand_sensors = demand_sensors
        self.__quality_node_sensors = quality_node_sensors
        self.__quality_link_sensors = quality_link_sensors
        self.__valve_state_sensors = valve_state_sensors
        self.__pump_state_sensors = pump_state_sensors
        self.__tank_volume_sensors = tank_volume_sensors
        self.__bulk_species_node_sensors = bulk_species_node_sensors
        self.__bulk_species_link_sensors = bulk_species_link_sensors
        self.__surface_species_sensors = surface_species_sensors
        self.__node_id_to_idx = node_id_to_idx
        self.__link_id_to_idx = link_id_to_idx
        self.__valve_id_to_idx = valve_id_to_idx
        self.__pump_id_to_idx = pump_id_to_idx
        self.__tank_id_to_idx = tank_id_to_idx
        self.__bulkspecies_id_to_idx = bulkspecies_id_to_idx
        self.__surfacespecies_id_to_idx = surfacespecies_id_to_idx

        self.__compute_indices()    # Compute indices

        super().__init__(**kwds)

    def node_id_to_idx(self, node_id: str) -> int:
        """
        Gets the index of a given node ID.

        Parameters
        ----------
        node_id : `str`
            Node ID.

        Returns
        -------
        `int`
            Index of the given node.
        """
        if self.__node_id_to_idx is not None:
            return self.__node_id_to_idx[node_id]
        else:
            return self.__nodes.index(node_id)

    def link_id_to_idx(self, link_id: str) -> int:
        """
        Gets the index of a given link ID.

        Parameters
        ----------
        link_id : `str`
            Link ID.

        Returns
        -------
        `int`
            Index of the given link.
        """
        if self.__node_id_to_idx is not None:
            return self.__link_id_to_idx[link_id]
        else:
            return self.__links.index(link_id)

    def valve_id_to_idx(self, valve_id: str) -> int:
        """
        Gets the index of a given valve ID.

        Parameters
        ----------
        valve_id : `str`
            Valve ID.

        Returns
        -------
        `int`
            Index of the given valve.
        """
        if self.__valve_id_to_idx is not None:
            return self.__valve_id_to_idx[valve_id]
        else:
            return self.__valves.index(valve_id)

    def pump_id_to_idx(self, pump_id: str) -> int:
        """
        Gets the index of a given pump ID.

        Parameters
        ----------
        pump_id : `str`
            Pump ID.

        Returns
        -------
        `int`
            Index of the given pump.
        """
        if self.__pump_id_to_idx is not None:
            return self.__pump_id_to_idx[pump_id]
        else:
            return self.__pumps.index(pump_id)

    def tank_id_to_idx(self, tank_id: str) -> int:
        """
        Gets the index of a given tank ID.

        Parameters
        ----------
        tank_id : `str`
            Tank ID.

        Returns
        -------
        `int`
            Index of the given tank.
        """
        if self.__tank_id_to_idx is not None:
            return self.__tank_id_to_idx[tank_id]
        else:
            return self.__tanks.index(tank_id)

    def bulkspecies_id_to_idx(self, bulk_species_id: str) -> int:
        """
        Gets the index of a given bulk species ID.

        Parameters
        ----------
        bulk_species_id : `str`
            Bulk species ID.

        Returns
        -------
        `int`
            Index of the given bulk species.
        """
        if self.__bulkspecies_id_to_idx is not None:
            return self.__bulkspecies_id_to_idx[bulk_species_id]
        else:
            return self.__bulk_species.index(bulk_species_id)

    def surfacespecies_id_to_idx(self, surface_species_id: str) -> int:
        """
        Gets the index of a given surface species ID.

        Parameters
        ----------
        surface_species_id : `str`
            Surface species ID.

        Returns
        -------
        `int`
            Index of the given surface species.
        """
        if self.__surfacespecies_id_to_idx is not None:
            return self.__surfacespecies_id_to_idx[surface_species_id]
        else:
            return self.__surface_species.index(surface_species_id)

    def __compute_indices(self):
        self.__pressure_idx = np.array([self.node_id_to_idx(n)
                                        for n in self.__pressure_sensors], dtype=np.int32)
        self.__flow_idx = np.array([self.link_id_to_idx(link)
                                    for link in self.__flow_sensors], dtype=np.int32)
        self.__demand_idx = np.array([self.node_id_to_idx(n)
                                      for n in self.__demand_sensors], dtype=np.int32)
        self.__quality_node_idx = np.array([self.node_id_to_idx(n)
                                            for n in self.__quality_node_sensors], dtype=np.int32)
        self.__quality_link_idx = np.array([self.link_id_to_idx(link)
                                            for link in self.__quality_link_sensors],
                                           dtype=np.int32)
        self.__valve_state_idx = np.array([self.valve_id_to_idx(v)
                                           for v in self.__valve_state_sensors], dtype=np.int32)
        self.__pump_state_idx = np.array([self.pump_id_to_idx(p)
                                          for p in self.__pump_state_sensors], dtype=np.int32)
        self.__tank_volume_idx = np.array([self.tank_id_to_idx(t)
                                           for t in self.__tank_volume_sensors], dtype=np.int32)
        self.__bulk_species_node_idx = np.array([(self.bulkspecies_id_to_idx(s),
                                                  [self.node_id_to_idx(node_id)
                                                for node_id in self.__bulk_species_node_sensors[s]])
                                                for s in self.__bulk_species_node_sensors.keys()],
                                                dtype=object)
        self.__bulk_species_link_idx = np.array([(self.bulkspecies_id_to_idx(s),
                                                  [self.link_id_to_idx(link_id)
                                                for link_id in self.__bulk_species_link_sensors[s]])
                                                for s in self.__bulk_species_link_sensors.keys()],
                                                dtype=object)
        self.__surface_species_idx = np.array([(self.surfacespecies_id_to_idx(s),
                                                [self.link_id_to_idx(link_id)
                                                 for link_id in self.__surface_species_sensors[s]])
                                               for s in self.__surface_species_sensors.keys()],
                                              dtype=object)

        n_pressure_sensors = len(self.__pressure_sensors)
        n_flow_sensors = len(self.__flow_sensors)
        n_demand_sensors = len(self.__demand_sensors)
        n_node_quality_sensors = len(self.__quality_node_sensors)
        n_link_quality_sensors = len(self.__quality_link_sensors)
        n_valve_state_sensors = len(self.__valve_state_sensors)
        n_pump_state_sensors = len(self.__pump_state_sensors)
        n_tank_volume_sensors = len(self.__tank_volume_sensors)
        n_bulk_species_node_sensors = len(self.__bulk_species_node_sensors.values())
        n_bulk_species_link_sensors = len(self.__bulk_species_link_sensors.values())

        pressure_idx_shift = 0
        flow_idx_shift = pressure_idx_shift + n_pressure_sensors
        demand_idx_shift = flow_idx_shift + n_flow_sensors
        node_quality_idx_shift = demand_idx_shift + n_demand_sensors
        link_quality_idx_shift = node_quality_idx_shift + n_node_quality_sensors
        valve_state_idx_shift = link_quality_idx_shift + n_link_quality_sensors
        pump_state_idx_shift = valve_state_idx_shift + n_valve_state_sensors
        tank_volume_idx_shift = pump_state_idx_shift + n_pump_state_sensors
        bulk_species_node_idx_shift = tank_volume_idx_shift + n_tank_volume_sensors
        bulk_species_link_idx_shift = bulk_species_node_idx_shift + n_bulk_species_node_sensors
        surface_species_idx_shift = bulk_species_link_idx_shift + n_bulk_species_link_sensors

        def __build_sensors_id_to_idx(sensors: list[str], initial_idx_shift: int) -> dict:
            return {sensor_id: i + initial_idx_shift
                    for sensor_id, i in zip(sensors, range(len(sensors)))}

        def __build_species_sensors_id_to_idx(species_sensors: dict, initial_idx_shift) -> dict:
            r = {}

            cur_idx_shift = initial_idx_shift
            for species_id in species_sensors:
                r[species_id] = {}
                for sensor_id in species_sensors[species_id]:
                    r[species_id][sensor_id] = cur_idx_shift
                    cur_idx_shift += 1

            return r

        mapping = {"pressure": __build_sensors_id_to_idx(self.__pressure_sensors,
                                                         pressure_idx_shift),
                   "flow": __build_sensors_id_to_idx(self.__flow_sensors,flow_idx_shift),
                   "demand": __build_sensors_id_to_idx(self.__demand_sensors,demand_idx_shift),
                   "quality_node": __build_sensors_id_to_idx(self.__quality_node_sensors,
                                                             node_quality_idx_shift),
                   "quality_link": __build_sensors_id_to_idx(self.__quality_link_sensors,
                                                             link_quality_idx_shift),
                   "valve_state": __build_sensors_id_to_idx(self.__valve_state_sensors,
                                                            valve_state_idx_shift),
                   "pump_state": __build_sensors_id_to_idx(self.__pump_state_sensors,
                                                           pump_state_idx_shift),
                   "tank_volume": __build_sensors_id_to_idx(self.__tank_volume_sensors,
                                                            tank_volume_idx_shift),
                   "bulk_species_node":
                   __build_species_sensors_id_to_idx(self.__bulk_species_node_sensors,
                                                     bulk_species_node_idx_shift),
                   "bulk_species_link":
                   __build_species_sensors_id_to_idx(self.__bulk_species_link_sensors,
                                                     bulk_species_link_idx_shift),
                   "surface_species":
                   __build_species_sensors_id_to_idx(self.__surface_species_sensors,
                                                     surface_species_idx_shift)}
        self.__sensors_id_to_idx = mapping

    def validate(self, epanet_api: epyt.epanet) -> None:
        """
        Validates this sensor configuration --
        i.e. checks whether all nodes, etc. exist in the .inp file.

        Parameters
        ----------
        epanet_api : `epyt.epanet`
            EPANET and EPANET-MSX API.
        """
        if not isinstance(epanet_api, epyt.epanet):
            raise TypeError("'epanet_api' must be an instance of 'epyt.epanet' " +
                            f"but not of '{type(epanet_api)}'")

        nodes = epanet_api.getNodeNameID()
        links = epanet_api.getLinkNameID()
        valves = epanet_api.getLinkValveNameID()
        pumps = epanet_api.getLinkPumpNameID()
        tanks = epanet_api.getNodeTankNameID()

        bulk_species = []
        surface_species = []
        if hasattr(epanet_api, "msx"):
            for species_id, species_type in zip(epanet_api.getMSXSpeciesNameID(),
                                                epanet_api.getMSXSpeciesType()):
                if species_type == "BULK":
                    bulk_species.append(species_id)
                elif species_type == "WALL":
                    surface_species.append(species_id)

        if any(node_id not in nodes for node_id in self.__nodes):
            raise ValueError("Invalid node ID detected -- " +
                             "all given node IDs must exist in the .inp file")
        if any(link_id not in links for link_id in self.__links):
            raise ValueError("Invalid link/pipe ID detected -- all given link/pipe IDs " +
                             "must exist in the .inp file")
        if any(valve_id not in valves for valve_id in self.__valves):
            raise ValueError("Invalid valve ID detected -- all given valve IDs must exist " +
                             "in the .inp file")
        if any(pump_id not in pumps for pump_id in self.__pumps):
            raise ValueError("Invalid pump ID detected -- all given pump IDs must exist " +
                             "in the .inp file")
        if any(tank_id not in tanks for tank_id in self.__tanks):
            raise ValueError("Invalid tank ID detected -- all given tank IDs must exist " +
                             "in the .inp file")
        if any(surface_species_id not in surface_species
               for surface_species_id in self.__surface_species):
            raise ValueError("Invalid surface species ID detected")
        if any(bulk_species_id not in bulk_species for bulk_species_id in self.__bulk_species):
            raise ValueError("Invalid bulk species ID detected")

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
    def bulk_species(self) -> list[str]:
        """
        Gets all bulk species IDs -- i.e. species that live in the water.

        Returns
        -------
        `list[str]`
            All species IDs.
        """
        return self.__bulk_species.copy()

    @property
    def surface_species(self) -> list[str]:
        """
        Gets all surface species IDs -- i.e. species that live links/pipes.

        Returns
        -------
        `list[str]`
            All species IDs.
        """
        return self.__surface_species.copy()

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
    def tank_volume_sensors(self) -> list[str]:
        """
        Gets all tank volume sensors (i.e. IDs of tanks at which a tank volume sensor is placed).

        Returns
        -------
        `list[str]`
            All tank IDs with a tank volume sensor.
        """
        return self.__tank_volume_sensors.copy()

    @tank_volume_sensors.setter
    def tank_volume_sensors(self, tank_volume_sensors: list[str]) -> None:
        if not isinstance(tank_volume_sensors, list):
            raise TypeError("'tank_volume_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(tank_volume_sensors)}'")
        if any(n not in self.__tanks for n in tank_volume_sensors):
            raise ValueError("Each item in 'tank_volume_sensors' must be in 'tanks' -- cannot " +
                             "place a sensor at a non-existing tanks.")

        self.__tank_volume_sensors = tank_volume_sensors

        self.__compute_indices()

    @property
    def bulk_species_node_sensors(self) -> dict:
        """
        Gets all bulk species node sensors as a dictionary --
        i.e. bulk species IDs as keys and node IDs as values.

        Returns
        -------
        `dict`
            Bulk species sensors -- keys: bulk species IDs, values: node IDs.
        """
        return deepcopy(self.__bulk_species_node_sensors)

    @bulk_species_node_sensors.setter
    def bulk_species_node_sensors(self, bulk_species_sensors: dict) -> None:
        if not isinstance(bulk_species_sensors, dict):
            raise TypeError("'bulk_species_sensors' must be an instance of 'dict' " +
                            f"but not of '{type(bulk_species_sensors)}'")
        if any(species_id not in self.__bulk_species for species_id in bulk_species_sensors.keys()):
            raise ValueError("Unknown bulk species ID in 'bulk_species_sensors'")
        if any(node_id not in self.__nodes for node_id in sum(bulk_species_sensors.values(), [])):
            raise ValueError("Unknown node ID in 'bulk_species_sensors'")

        self.__bulk_species_node_sensors = bulk_species_sensors

        self.__compute_indices()

    @property
    def bulk_species_link_sensors(self) -> dict:
        """
        Gets all bulk species link/pipe sensors as a dictionary --
        i.e. bulk species IDs as keys and link/pipe IDs as values.

        Returns
        -------
        `dict`
            Bulk species sensors -- keys: bulk species IDs, values: link/pipe IDs.
        """
        return deepcopy(self.__bulk_species_link_sensors)

    @bulk_species_link_sensors.setter
    def bulk_species_link_sensors(self, bulk_species_sensors: dict) -> None:
        if not isinstance(bulk_species_sensors, dict):
            raise TypeError("'bulk_species_sensors' must be an instance of 'dict' " +
                            f"but not of '{type(bulk_species_sensors)}'")
        if any(species_id not in self.__bulk_species for species_id in bulk_species_sensors.keys()):
            raise ValueError("Unknown bulk species ID in 'bulk_species_sensors'")
        if any(link_id not in self.__links for link_id in sum(bulk_species_sensors.values(), [])):
            raise ValueError("Unknown link/pipe ID in 'bulk_species_sensors'")

        self.__bulk_species_link_sensors = bulk_species_sensors

        self.__compute_indices()

    @property
    def surface_species_sensors(self) -> dict:
        """
        Gets all surface species sensors as a dictionary --
        i.e. surface species IDs as keys and link/pipe IDs as values.

        Returns
        -------
        `dict`
            Surface species sensors -- keys: surface species IDs, values: link/pipe IDs.
        """
        return deepcopy(self.__surface_species_sensors)

    @surface_species_sensors.setter
    def surface_species_sensors(self, surface_species_sensors: dict) -> None:
        if not isinstance(surface_species_sensors, dict):
            raise TypeError("'surface_species_sensors' must be an instance of 'dict' " +
                            f"but not of '{type(surface_species_sensors)}'")
        if any(species_id not in self.__surface_species
               for species_id in surface_species_sensors.keys()):
            raise ValueError("Unknown surface species ID in 'surface_species_sensors'")
        if any(link_id not in self.__links
               for link_id in sum(surface_species_sensors.values(), [])):
            raise ValueError("Unknown link/pipe ID in 'surface_species_sensors'")

        self.__surface_species_sensors = surface_species_sensors

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
        attr = {"nodes": self.__nodes, "links": self.__links,
                "valves": self.__valves, "pumps": self.__pumps,
                "tanks": self.__tanks, "bulk_species": self.__bulk_species,
                "surface_species": self.__surface_species,
                "pressure_sensors": self.__pressure_sensors,
                "flow_sensors": self.__flow_sensors,
                "demand_sensors": self.__demand_sensors,
                "quality_node_sensors": self.__quality_node_sensors,
                "quality_link_sensors": self.__quality_link_sensors,
                "valve_state_sensors": self.__valve_state_sensors,
                "pump_state_sensors": self.__pump_state_sensors,
                "tank_volume_sensors": self.__tank_volume_sensors,
                "bulk_species_node_sensors": self.__bulk_species_node_sensors,
                "bulk_species_link_sensors": self.__bulk_species_link_sensors,
                "surface_species_sensors": self.__surface_species_sensors,
                "node_id_to_idx": self.__node_id_to_idx,
                "link_id_to_idx": self.__link_id_to_idx,
                "valve_id_to_idx": self.__valve_id_to_idx,
                "pump_id_to_idx": self.__pump_id_to_idx,
                "tank_id_to_idx": self.__tank_id_to_idx,
                "bulkspecies_id_to_idx": self.__bulkspecies_id_to_idx,
                "surfacespecies_id_to_idx": self.__surfacespecies_id_to_idx}

        return super().get_attributes() | attr

    def __eq__(self, other) -> bool:
        if not isinstance(other, SensorConfig):
            raise TypeError("Can not compare 'SensorConfig' instance " +
                            f"with '{type(other)}' instance")

        return self.__nodes == other.nodes and self.__links == other.links \
            and self.__valves == other.valves and self.__pumps == other.pumps \
            and self.__tanks == other.tanks and self.__bulk_species == other.bulk_species \
            and self.__surface_species == other.surface_species \
            and self.__pressure_sensors == other.pressure_sensors \
            and self.__flow_sensors == other.flow_sensors \
            and self.__demand_sensors == other.demand_sensors \
            and self.__quality_node_sensors == other.quality_node_sensors \
            and self.__quality_link_sensors == other.quality_link_sensors \
            and self.__valve_state_sensors == other.valve_state_sensors \
            and self.__pump_state_sensors == other.pump_state_sensors \
            and self.__tank_volume_sensors == other.tank_volume_sensors \
            and self.__bulk_species_node_sensors == other.bulk_species_node_sensors \
            and self.__bulk_species_link_sensors == other.bulk_species_link_sensors \
            and self.__surface_species_sensors == other.surface_species_sensors

    def __str__(self) -> str:
        return f"nodes: {self.__nodes} links: {self.__links} valves: {self.__valves} " +\
            f"pumps: {self.__pumps} tanks: {self.__tanks} bulk_species: {self.__bulk_species} " +\
            f"surface_species: {self.__surface_species}" + \
            f"pressure_sensors: {self.__pressure_sensors} flow_sensors: {self.__flow_sensors} " +\
            f"demand_sensors: {self.__demand_sensors} " +\
            f"quality_node_sensors: {self.__quality_node_sensors} " +\
            f"quality_link_sensors: {self.__quality_link_sensors} " +\
            f"valve_state_sensors: {self.__valve_state_sensors} " +\
            f"pump_state_sensors: {self.__pump_state_sensors} " +\
            f"tank_volume_sensors: {self.__tank_volume_sensors}" +\
            f"bulk_species_node_sensors: {self.__bulk_species_node_sensors}" +\
            f"bulk_species_link_sensors: {self.__bulk_species_link_sensors}" +\
            f"surface_species_sensors: {self.__surface_species_sensors}"

    def compute_readings(self, pressures: np.ndarray, flows: np.ndarray, demands: np.ndarray,
                         nodes_quality: np.ndarray, links_quality: np.ndarray,
                         pumps_state: np.ndarray, valves_state: np.ndarray,
                         tanks_volume: np.ndarray, bulk_species_node_concentrations: np.ndarray,
                         bulk_species_link_concentrations: np.ndarray,
                         surface_species_concentrations: np.ndarray) -> np.ndarray:
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
        tanks_volume : `numpy.ndarray`
            Water volume in all tanks.
        bulk_species_node_concentrations : `numpy.ndarray`
            Bulk species concentrations at all nodes.

            Expect a three-dimensional array: First dimension denotes time,
            second dimension corresponds to species ID,
            and third dimension contains the concentration.
        bulk_species_link_concentrations : `numpy.ndarray`
            Bulk species concentrations at all links/pipes.

            Expect a three-dimensional array: First dimension denotes time,
            second dimension corresponds to species ID,
            and third dimension contains the concentration.
        surface_species_concentrations : `numpy.ndarray`
            Surface species concentrations at all links/pipes.

            Expect a three-dimensional array: First dimension denotes time,
            second dimension corresponds to species ID,
            and third dimension contains the concentration.

        Returns
        -------
        `numpy.ndarray`
            Sensor readings.
        """
        data = []

        if pressures is not None:
            data.append(pressures[:, self.__pressure_idx])
        else:
            if len(self.__pressure_sensors) != 0:
                raise ValueError("Pressure readings requested but no pressure data is given")

        if flows is not None:
            data.append(flows[:, self.__flow_idx])
        else:
            if len(self.__flow_sensors) != 0:
                raise ValueError("Flow readings requested but no flow data is given")

        if demands is not None:
            data.append(demands[:, self.__demand_idx])
        else:
            if len(self.__demand_sensors) != 0:
                raise ValueError("Demand readings requested but no demand data is given")

        if nodes_quality is not None:
            data.append(nodes_quality[:, self.__quality_node_idx])
        else:
            if len(self.__quality_node_sensors) != 0:
                raise ValueError("Node water quality readings requested " +
                                 "but no water quality data at nodes is given")

        if links_quality is not None:
            data.append(links_quality[:, self.__quality_link_idx])
        else:
            if len(self.__quality_link_sensors) != 0:
                raise ValueError("Link/Pipe water quality readings requested " +
                                 "but no water quality data at links/pipes is given")

        if valves_state is not None:
            data.append(valves_state[:, self.__valve_state_idx])
        else:
            if len(self.__valve_state_sensors) != 0:
                raise ValueError("Valve states readings requested " +
                                 "but no valve state data is given")

        if pumps_state is not None:
            data.append(pumps_state[:, self.__pump_state_idx])
        else:
            if len(self.__pump_state_sensors) != 0:
                raise ValueError("Pump states readings requested " +
                                 "but no pump state data is given")

        if tanks_volume is not None:
            data.append(tanks_volume[:, self.__tank_volume_idx])
        else:
            if len(self.__tank_volume_sensors) != 0:
                raise ValueError("Water volumes in tanks is requested but no " +
                                 "tank water volume data is given")

        if surface_species_concentrations is not None:
            for species_idx, links_idx in self.__surface_species_idx:
                data.append(surface_species_concentrations[:, species_idx, links_idx].
                            reshape(-1, len(links_idx)))
        else:
            if len(self.__surface_species_sensors) != 0:
                raise ValueError("Surface species concentratinons requested but no " +
                                 "surface species concentration data is given")

        if bulk_species_node_concentrations is not None:
            for species_idx, nodes_idx in self.__bulk_species_node_idx:
                data.append(bulk_species_node_concentrations[:, species_idx, nodes_idx].
                            reshape(-1, len(nodes_idx)))
        else:
            if len(self.__bulk_species_node_sensors) != 0:
                raise ValueError("Bulk species concentratinons requested but no " +
                                 "bulk species node concentration data is given")

        if bulk_species_link_concentrations is not None:
            for species_idx, links_idx in self.__bulk_species_link_idx:
                data.append(bulk_species_link_concentrations[:, species_idx, links_idx].
                            reshape(-1, len(links_idx)))
        else:
            if len(self.__bulk_species_link_sensors) != 0:
                raise ValueError("Bulk species concentratinons requested but no " +
                                 "bulk species link/pipe concentration data is given")

        return np.concatenate(data, axis=1)

    def get_index_of_reading(self, pressure_sensor: str = None, flow_sensor: str = None,
                             demand_sensor: str = None, node_quality_sensor: str = None,
                             link_quality_sensor: str = None, valve_state_sensor: str = None,
                             pump_state_sensor: str = None, tank_volume_sensor: str = None,
                             bulk_species_node_sensor: tuple[str, str] = None,
                             bulk_species_link_sensor: tuple[str, str] = None,
                             surface_species_sensor: tuple[str, str] = None) -> int:
        """
        Gets the index of a particular sensor in the final sensor readings array.

        Note that only one sensor ID is converted to an index. In case of multiple sensor IDs,
        call this function for each sensor ID separately.

        .. note::

            This function only returns the correct results if the sensor configuraton is NOT frozen!

        Parameters
        ----------
        pressure_sensor : `str`
            ID of the pressure sensor.
        flow_sensor : `str`
            ID of the flow sensor.
        demand_sensor : `str`
            ID of the demand sensor.
        node_quality_sensor : `str`
            ID of the quality sensor (at a node).
        link_quality_sensor : `str`
            ID of the quality sensor (at a link/pipe).
        valve_state_sensor : `str`
            ID of the state sensor (at a valve).
        pump_state_sensor : `str`
            ID of the state sensor (at a pump).
        tank_volume_sensor : `str`
            ID of the water volume sensor (at a tank)
        bulk_species_node_sensor : `tuple[str, str]`
            Tuple of bulk species ID and sensor node ID.
        bulk_species_link_sensor : `tuple[str, str]`
            Tuple of bulk species ID and sensor link/pipe ID.
        surface_species_sensor : `tuple[str, str]`
            Tuple of surface species ID and sensor link/pipe ID.
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
        elif tank_volume_sensor is not None:
            return self.__sensors_id_to_idx["tank_volume"][tank_volume_sensor]
        elif surface_species_sensor is not None:
            species_id, sensor_id = surface_species_sensor
            return self.__sensors_id_to_idx["surface_species"][species_id][sensor_id]
        elif bulk_species_node_sensor is not None:
            species_id, sensor_id = bulk_species_node_sensor
            return self.__sensors_id_to_idx["bulk_species_node"][species_id][sensor_id]
        elif bulk_species_link_sensor is not None:
            species_id, sensor_id = bulk_species_link_sensor
            return self.__sensors_id_to_idx["bulk_species_link"][species_id][sensor_id]
        else:
            raise ValueError("No sensor given")
