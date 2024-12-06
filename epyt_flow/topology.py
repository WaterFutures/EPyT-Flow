"""
Module provides a class for representing the topology of WDN.
"""
from copy import deepcopy
import warnings
from typing import Any
import numpy as np
import networkx as nx
from scipy.sparse import bsr_array
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString

from .serialization import serializable, JsonSerializable, NETWORK_TOPOLOGY_ID


UNITS_USCUSTOM = 0
UNITS_SIMETRIC = 1


def unitscategoryid_to_str(unit_category_id: int) -> str:
    """
    Converts a given units category ID to the corresponding description.

    Parameters
    ----------
    unit_category_id : `int`
        ID of the units category.

        Must be one of the following constants:

            - UNITS_USCUSTOM = 0
            - UNITS_SIMETRIC = 1

    Returns
    -------
    `str`
        Units category description.
    """
    if unit_category_id is None:
        return ""
    elif unit_category_id == UNITS_USCUSTOM:
        return "US CUSTOMARY"
    elif unit_category_id == UNITS_SIMETRIC:
        return "SI METRIC"
    else:
        raise ValueError(f"Unknown units category ID '{unit_category_id}'")


@serializable(NETWORK_TOPOLOGY_ID, ".epytflow_topology")
class NetworkTopology(nx.Graph, JsonSerializable):
    """
    Class representing the topology of a WDN.

    Parameters
    ----------
    f_inp : `str`
        Path to .inp file to which this topology belongs.
    nodes : `list[tuple[str, dict]]`
        List of all nodes -- i.e. node ID and node information such as type and elevation.
    links : `list[tuple[str, tuple[str, str], dict]]`
        List of all links/pipes -- i.e. link ID, ID of connecting nodes, and link information
        such as pipe diameter, length, etc.
    pumps : `dict`
        List of all pumps -- i.e. valve ID, and information such as
        pump type and connecting nodes.
    valves : `dict`
        List of all valves -- i.e. valve ID, and information such as
        valve type and connecting nodes.
    units : `int`
        Measurement units category -- i.e. US Customary or SI Metric.

        Must be one of the following constants:

            - UNITS_USCUSTOM = 0  (US Customary)
            - UNITS_SIMETRIC = 1  (SI Metric)
    """
    def __init__(self, f_inp: str, nodes: list[tuple[str, dict]],
                 links: list[tuple[str, tuple[str, str], dict]],
                 pumps: dict,
                 valves: dict,
                 units: int = None,
                 **kwds):
        super().__init__(name=f_inp, **kwds)

        self.__nodes = nodes
        self.__links = links
        self.__pumps = pumps
        self.__valves = valves
        self.__units = units

        if units is None:
            warnings.warn("Loading a file that was created with an outdated version of EPyT-Flow" +
                          " -- support of such old files will be removed in the next release!",
                          DeprecationWarning)

        for node_id, node_info in nodes:
            node_elevation = node_info["elevation"]
            node_type = node_info["type"]
            self.add_node(node_id, info={"elevation": node_elevation, "type": node_type})

        for link_id, link, link_info in links:
            link_type = link_info["type"]
            link_diameter = link_info["diameter"]
            link_length = link_info["length"]
            self.add_edge(link[0], link[1], length=link_length,
                          info={"id": link_id, "type": link_type, "nodes": link,
                                "diameter": link_diameter, "length": link_length})

    def convert_units(self, units: int) -> Any:
        """
        Converts this instance to a :class:`~epyt_flow.topology.NetworkTopology` instance
        where everything is measured in given measurement units category
        (US Customary or SI Metric).

        Parameters
        ----------
        units : `int`
            Measurement units category.

            Must be one of the following constants:

                - UNITS_USCUSTOM = 0  (US Customary)
                - UNITS_SIMETRIC = 1  (SI Metric)

        Returns
        -------
        :class:`~epyt_flow.topology.NetworkTopology`
            Network topology with the new measurements units.
        """
        if self.__units is None:
            raise ValueError("This instance does not contain any units!")

        if not isinstance(units, int):
            raise TypeError(f"'units' must be an instance of 'int' but not of '{type(units)}'")
        if units not in [UNITS_SIMETRIC, UNITS_USCUSTOM]:
            raise ValueError(f"Invalid units '{units}'")

        if units == self.__units:
            warnings.warn("Units already set in this NetworkTopology instance -- nothing to do!")
            return deepcopy(self)

        # Get all data and convert units
        inch_to_millimeter = 25.4
        feet_to_meter = 0.3048

        nodes = []
        for node_id in self.get_all_nodes():
            node_info = self.get_node_info(node_id)
            if units == UNITS_USCUSTOM:
                conv_factor = 1. / feet_to_meter
            else:
                conv_factor = feet_to_meter
            node_info["elevation"] *= conv_factor
            if "diameter" in node_info:
                node_info["diameter"] *= conv_factor

            nodes.append((node_id, node_info))

        links = []
        for link_id, link_nodes in self.get_all_links():
            link_info = self.get_link_info(link_id)

            if units == UNITS_USCUSTOM:
                conv_factor = 1. / feet_to_meter
            else:
                conv_factor = feet_to_meter
            link_info["length"] *= conv_factor

            if units == UNITS_USCUSTOM:
                conv_factor = 1. / inch_to_millimeter
            else:
                conv_factor = inch_to_millimeter
            link_info["diameter"] *= conv_factor

            links.append((link_id, link_nodes, link_info))

        return NetworkTopology(f_inp=self.name, nodes=nodes, links=links, pumps=self.pumps,
                               valves=self.valves, units=units)

    def get_all_nodes(self) -> list[str]:
        """
        Gets a list of all nodes.

        Returns
        -------
        `list[str]`
            List of all nodes ID.
        """
        return [node_id for node_id, _ in self.__nodes]

    def get_number_of_nodes(self) -> int:
        """
        Returns the number of nodes.

        Returns
        -------
        `int`
            Number of nodes.
        """
        return len(self.get_all_nodes())

    def get_all_links(self) -> list[tuple[str, tuple[str, str]]]:
        """
        Gets a list of all links/pipes (incl. their end points).

        Returns
        -------
        `list[tuple[str, tuple[str, str]]]`
            List of links -- (link ID, (left node ID, right node ID)).
        """
        return [(link_id, end_points) for link_id, end_points, _ in self.__links]

    def get_number_of_links(self) -> int:
        """
        Returns the number of links.

        Returns
        -------
        `int`
            Number of links.
        """
        return len(self.get_all_links())

    def get_all_junctions(self) -> list[str]:
        """
        Gets all junctions -- i.e. nodes that are not tanks or reservoirs.

        Returns
        -------
        `list[str]`
            List of all junctions.
        """
        r = []

        for node_id in self.get_all_nodes():
            if self.get_node_info(node_id)["type"] == "JUNCTION":
                r.append(node_id)

        return r

    def get_number_of_junctions(self) -> int:
        """
        Returns the number of junctions.

        Returns
        -------
        `int`
            Number of junctions.
        """
        return len(self.get_all_junctions())

    def get_all_tanks(self) -> list[str]:
        """
        Gets all tanks -- i.e. nodes that are not junctions or reservoirs.

        Returns
        -------
        `list[str]`
            List of all tanks.
        """
        r = []

        for node_id in self.get_all_nodes():
            if self.get_node_info(node_id)["type"] == "TANK":
                r.append(node_id)

        return r

    def get_number_of_tanks(self) -> int:
        """
        Returns the number of tanks.

        Returns
        -------
        `int`
            Number of tanks.
        """
        return len(self.get_all_tanks())

    def get_all_reservoirs(self) -> list[str]:
        """
        Gets all reservoirs -- i.e. nodes that are not junctions or tanks.

        Returns
        -------
        `list[str]`
            List of all reservoirs.
        """
        r = []

        for node_id in self.get_all_nodes():
            if self.get_node_info(node_id)["type"] == "RESERVOIR":
                r.append(node_id)

        return r

    def get_number_of_reservoirs(self) -> int:
        """
        Returns the number of reservoirs.

        Returns
        -------
        `int`
            Number of reservoirs.
        """
        return len(self.get_all_reservoirs())

    def get_all_pipes(self) -> list[tuple[str, tuple[str, str]]]:
        """
        Gets all pipes -- i.e. links that not valves or pumps.

        Returns
        -------
        `list[tuple[str, tuple[str, str]]]`
            List of all pipes -- (link ID, (left node ID, right node ID)).
        """
        r = []

        for link_id, link_nodes in self.get_all_links():
            link_info = self.get_link_info(link_id)

            if link_info["type"] == "PIPE":
                r.append((link_id, link_nodes))

        return r

    def get_number_of_pipes(self) -> int:
        """
        Returns the number of pipes.

        Returns
        -------
        `int`
            Number of pipes.
        """
        return len(self.get_all_pipes())

    def get_all_pumps(self) -> list[str]:
        """
        Gets the IDs of all pumps.

        Returns
        -------
        `list[str]`
            Pump IDs.
        """
        return list(self.__pumps.keys())

    def get_number_of_pumps(self) -> int:
        """
        Returns the number of pumps.

        Returns
        -------
        `int`
            Number of pumps.
        """
        return len(self.get_all_pumps())

    def get_all_valves(self) -> list[str]:
        """
        Gets the IDs of all valves.

        Returns
        -------
        `list[str]`
            Valve IDs.
        """
        return list(self.__valves.keys())

    def get_number_of_valves(self) -> int:
        """
        Returns the number of valves.

        Returns
        -------
        `int`
            Number of valves.
        """
        return len(self.get_all_valves())

    def get_node_info(self, node_id: str) -> dict:
        """
        Gets all information (e.g. elevation, type, etc.) associated with a given node.

        Parameters
        ----------
        node_id : `str`
            ID of the node.

        Returns
        -------
        `dict`
            Information associated with the given node.
        """
        for node_id_, node_info in self.__nodes:
            if node_id_ == node_id:
                return node_info

        raise ValueError(f"Unknown node '{node_id}'")

    def get_link_info(self, link_id: str) -> dict:
        """
        Gets all information (e.g. diameter, length, etc.) associated with a given link.

        Note that links can be pipes, pumps, or valves.

        Parameters
        ----------
        link_id : `str`
            ID of the link.

        Returns
        -------
        `dict`
            Information associated with the given link.
        """
        for link_id_, link_nodes, link_info in self.__links:
            if link_id_ == link_id:
                return {"nodes": link_nodes} | link_info

        raise ValueError(f"Unknown link '{link_id}'")

    def get_pump_info(self, pump_id: str) -> dict:
        """
        Gets all information associated with a given pump.

        Parameters
        ----------
        pump_id : `str`
            ID of the pump.

        Returns
        -------
        `dict`
            Pump information.
        """
        if pump_id in self.__pumps:
            return self.__pumps[pump_id]
        else:
            raise ValueError(f"Unknown pump: '{pump_id}'")

    def get_valve_info(self, valve_id: str) -> dict:
        """
        Gets all information associated with a given valve.

        Parameters
        ----------
        valve_id : `str`
            ID of the valve.

        Returns
        -------
        `dict`
            Valve information.
        """
        if valve_id in self.__valves:
            return self.__valves[valve_id]
        else:
            raise ValueError(f"Unknown valve: '{valve_id}'")

    @property
    def pumps(self) -> dict:
        """
        Gets all pumps -- i.e. ID and associated information such as the pump type.

        Returns
        -------
        `dict`
            All pumps and their associated information.
        """
        return deepcopy(self.__pumps)

    @property
    def valves(self) -> dict:
        """
        Gets all valves -- i.e. ID and associated information such as the valve type.

        Returns
        -------
        `dict`
            All valves and their associated information.
        """
        return deepcopy(self.__valves)

    @property
    def units(self) -> int:
        """
        Gets the used measurement units category.

        Will be one of the following constants:

            - UNITS_USCUSTOM = 0  (US Customary)
            - UNITS_SIMETRIC = 1  (SI Metric)

        Returns
        -------
        `int`
            Measurement units category.
        """
        return self.__units

    def __eq__(self, other) -> bool:
        if not isinstance(other, NetworkTopology):
            raise TypeError("Can not compare 'NetworkTopology' instance to " +
                            f"'{type(other)}' instance")

        return super().__eq__(other) and \
            self.get_all_nodes() == other.get_all_nodes() \
            and all(link_a[0] == link_b[0] and link_a[1] == link_b[1]
                    for link_a, link_b in zip(self.get_all_links(), other.get_all_links())) \
            and self.__units == other.units \
            and self.get_all_pumps() == other.get_all_pumps() \
            and self.get_all_valves() == other.get_all_valves()

    def __str__(self) -> str:
        return f"f_inp: {self.name} nodes: {self.__nodes} links: {self.__links} " +\
            f"pumps: {self.__pumps} valves: {self.__valves} " +\
            f"units: {unitscategoryid_to_str(self.__units)}"

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"f_inp": self.name,
                                           "nodes": self.__nodes,
                                           "links": self.__links,
                                           "pumps": self.__pumps,
                                           "valves": self.__valves,
                                           "units": self.__units}

    def to_gis(self, coord_reference_system: str = None, pumps_as_points: bool = False,
               valves_as_points: bool = False) -> dict:
        """
        Gets the network topology as a dictionary of `geopandas.GeoDataFrames` instances --
        i.e. each quantity (nodes, links/pipes, valves, etc.) is represented by a
        `geopandas.GeoDataFrames` instance.

        Parameters
        ----------
        coord_reference_system : `str`, optional
            Coordinate reference system.

            The default is None.
        pumps_as_points : `bool`, optional
            If True, pumps are represented by points, otherwise by lines.

            The default is False.

        valves_as_points : `bool`, optional
            If True, valves are represented by points, otherwise by lines.

            The default is False.

        Returns
        -------
        `dict`
            Network topology as a dictionary of `geopandas.GeoDataFrames <https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.html>`_ instances.
            If a quantity does not exist, the data frame will be None.
        """
        gis = {"nodes": None, "links": None,
               "tanks": None, "reservoirs": None,
               "valves": None, "pumps": None}

        # Nodes
        node_data = {"id": [], "type": [], "elevation": [], "geometry": []}
        tank_data = {"id": [], "elevation": [], "diameter": [], "geometry": []}
        reservoir_data = {"id": [], "elevation": [], "geometry": []}
        for node_id in self.get_all_nodes():
            node_info = self.get_node_info(node_id)

            node_data["id"].append(node_id)
            node_data["type"].append(node_info["type"])
            node_data["elevation"].append(node_info["elevation"])
            node_data["geometry"].append(Point(node_info["coord"]))

            if node_info["type"] == "TANK":
                tank_data["id"].append(node_id)
                tank_data["elevation"].append(node_info["elevation"])
                tank_data["diameter"].append(node_info["diameter"])
                tank_data["geometry"].append(Point(node_info["coord"]))
            elif node_info["type"] == "RESERVOIR":
                reservoir_data["id"].append(node_id)
                reservoir_data["elevation"].append(node_info["elevation"])
                reservoir_data["geometry"].append(Point(node_info["coord"]))

        gis["nodes"] = GeoDataFrame(node_data, crs=coord_reference_system)
        gis["tanks"] = GeoDataFrame(tank_data, crs=coord_reference_system)
        gis["reservoirs"] = GeoDataFrame(reservoir_data, crs=coord_reference_system)

        # Links
        pipe_data = {"id": [], "type": [], "end_point_a": [], "end_point_b": [],
                     "length": [], "diameter": [], "geometry": []}
        valve_data = {"id": [], "type": [], "geometry": []}
        pump_data = {"id": [], "type": [], "geometry": []}
        for link_id, link_nodes in self.get_all_links():
            link_info = self.get_link_info(link_id)
            end_points_coord = [self.get_node_info(n)["coord"] for n in link_nodes]

            if link_info["type"] == "PIPE":
                pipe_data["id"].append(link_id)
                pipe_data["type"].append(link_info["type"])
                pipe_data["end_point_a"].append(link_nodes[0])
                pipe_data["end_point_b"].append(link_nodes[1])
                pipe_data["length"].append(link_info["length"])
                pipe_data["diameter"].append(link_info["diameter"])
                pipe_data["geometry"].append(LineString(end_points_coord))
            elif link_info["type"] == "PUMP":
                pump_data["id"].append(link_id)
                pump_data["type"].append(self.get_pump_info(link_id)["type"])
                if pumps_as_points is True:
                    pump_data["geometry"].append(Point(end_points_coord[0]))
                else:
                    pump_data["geometry"].append(LineString(end_points_coord))
            else:   # Valve
                valve_data["id"].append(link_id)
                valve_data["type"].append(self.get_valve_info[link_id]["type"])
                if valves_as_points is True:
                    valve_data["geometry"].append(Point(end_points_coord[0]))
                else:
                    valve_data["geometry"].append(LineString(end_points_coord))

        gis["pipes"] = GeoDataFrame(pipe_data, crs=coord_reference_system)
        gis["valves"] = GeoDataFrame(valve_data, crs=coord_reference_system)
        gis["pumps"] = GeoDataFrame(pump_data, crs=coord_reference_system)

        return gis

    def get_adj_matrix(self) -> bsr_array:
        """
        Gets the adjacency matrix of this graph.

        Returns
        -------
        `scipy.bsr_array <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.bsr_array.html>`_
            Adjacency matrix as a sparse array.
        """
        nodes_id = [node_id for node_id, _ in self.__nodes]
        n_nodes = len(self.__nodes)

        row = []
        col = []
        for _, link_end_points, _ in self.__links:
            a = nodes_id.index(link_end_points[0])
            b = nodes_id.index(link_end_points[1])

            row.append(a)
            col.append(b)

            row.append(b)
            col.append(a)

        for i in range(n_nodes):
            row.append(i)
            col.append(i)

        return bsr_array((np.ones(len(row)), (row, col)), shape=(n_nodes, n_nodes))

    def get_neighbors(self, node_id: str) -> list[str]:
        """
        Gets all neighboring nodes of a given node.

        Parameters
        ----------
        node_id : `str`
            ID of the node.

        Returns
        -------
        `list[str]`
            IDs of neighboring nodes.
        """
        if node_id not in self.get_all_nodes():
            raise ValueError(f"Unknown node '{node_id}'")

        return list(self.neighbors(node_id))

    def get_adjacent_links(self, node_id: str) -> list[tuple[str, tuple[str, str]]]:
        """
        Gets all adjacent links/pipes of a given node.

        Parameters
        ----------
        node_id : `str`
            ID of the node.

        Returns
        -------
        `list[tuple[str, tuple[str, str]]]`
            Adjacent links -- i.e. (link ID, IDs of node end points).
        """
        if node_id not in self.get_all_nodes():
            raise ValueError(f"Unknown node '{node_id}'")

        links = []

        for link_id, nodes_id, _ in self.__links:
            if node_id in nodes_id:
                links.append((link_id, nodes_id))

        return links

    def get_shortest_path(self, start_node_id: str, end_node_id: str,
                          use_pipe_length_as_weight: bool = True) -> list[str]:
        """
        Computes the shortest path between two nodes in this graph.

        Parameters
        ----------
        start_node_id : `str`
            ID of start node.
        end_node_id : `str`
            ID of end node.
        use_pipe_length_as_weight : `bool`, optional
            If True, pipe lengths are used for the edge weights -- otherwise,
            each edge weight is set to one.

            The default is True.
        """
        if start_node_id not in self.get_all_nodes():
            raise ValueError(f"Unknown node '{start_node_id}'")
        if end_node_id not in self.get_all_nodes():
            raise ValueError(f"Unknown node '{end_node_id}'")

        weight = "length" if use_pipe_length_as_weight is True else None
        return nx.shortest_path(self, source=start_node_id, target=end_node_id, weight=weight)

    def get_all_pairs_shortest_path(self, use_pipe_length_as_weight: bool = True) -> dict:
        """
        Computes the shortest path between all pairs of nodes in this graph.

        Parameters
        ----------
        use_pipe_length_as_weight : `bool`, optional
            If True, pipe lengths are used for the edge weights -- otherwise,
            each edge weight is set to one.

            The default is True.

        Returns
        -------
        `dict`
            Shortest paths between all pairs of nodes as nested dictionaries --
            first key is the start node, second key is the end node.
        """
        weight = "length" if use_pipe_length_as_weight is True else None
        return nx.shortest_path(self, weight=weight)

    def get_shortest_path_length(self, start_node_id: str, end_node_id: str,
                                 use_pipe_length_as_weight: bool = True) -> list[str]:
        """
        Computes the shortest path length between two nodes in this graph.

        Parameters
        ----------
        start_node_id : `str`
            ID of start node.
        end_node_id : `str`
            ID of end node.
        use_pipe_length_as_weight : `bool`, optional
            If True, pipe lengths are used for the edge weights -- otherwise,
            each edge weight is set to one.

            The default is True.
        """
        if start_node_id not in self.get_all_nodes():
            raise ValueError(f"Unknown node '{start_node_id}'")
        if end_node_id not in self.get_all_nodes():
            raise ValueError(f"Unknown node '{end_node_id}'")

        weight = "length" if use_pipe_length_as_weight is True else None
        return nx.shortest_path_length(self, source=start_node_id, target=end_node_id,
                                       weight=weight)

    def get_all_pairs_shortest_path_length(self, use_pipe_length_as_weight: bool = True) -> dict:
        """
        Computes the shortest path length between all pairs of nodes in this graph.

        Parameters
        ----------
        use_pipe_length_as_weight : `bool`, optional
            If True, pipe lengths are used for the edge weights -- otherwise,
            each edge weight is set to one.

            The default is True.

        Returns
        -------
        `dict`
            Shortest paths between all pairs of nodes as nested dictionaries --
            first key is the start node, second key is the end node.
        """
        weight = "length" if use_pipe_length_as_weight is True else None
        return dict(nx.shortest_path_length(self, weight=weight))
