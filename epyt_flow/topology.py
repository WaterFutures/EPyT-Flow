"""
Module provides a class for representing the topology of WDN.
"""
from copy import deepcopy
import warnings
from typing import Any
import math
import numpy as np
import networkx as nx
from scipy.sparse import bsr_array
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString
from epanet_plus import EpanetConstants, EPyT

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
    curves : `dict[str, tuple[int, list[tuple[float, float]]]]`
        All curves -- i.e. curve ID, and list of points.
    patterns : `dict[str, list[float]]`
        All time patterns -- i.e., pattern ID and list of multipliers.
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
                 curves: dict[str, tuple[int, list[tuple[float, float]]]],
                 patterns: dict[str, list[float]],
                 units: int,
                 **kwds):
        nx.Graph.__init__(self, name=f_inp, **kwds)
        JsonSerializable.__init__(self)

        self.__nodes = nodes
        self.__links = links
        self.__pumps = pumps
        self.__valves = valves
        self.__curves = curves
        self.__patterns = patterns
        self.__units = units

        for key in self.__curves.keys():    # Fix value types -- tuple gets converted to list when deserializing it
            self.__curves[key] = (self.__curves[key][0],
                                  [tuple(value) for value in self.__curves[key][1]])

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

    def to_inp_file(self, inp_file_out: str) -> None:
        """
        Creates an .inp file with the network layout and parameters as specified in
        this instance.
        Note that no control rules are set!

        Parameters
        ----------
        inp_file_out : `str`
            Path to the .inp file.
        """
        with EPyT(inp_file_in=inp_file_out, use_project=False) as epanet_api:
            if self.units == UNITS_SIMETRIC:
                epanet_api.setflowunits(EpanetConstants.EN_CMH)
            else:
                epanet_api.setflowunits(EpanetConstants.EN_GPM)

            for curve_id, (curve_type, curve_data) in self.__curves.items():
                epanet_api.addcurve(curve_id)
                curve_idx = epanet_api.getcurveindex(curve_id)
                epanet_api.setcurvetype(curve_idx, curve_type)
                for i, (x, y) in enumerate(curve_data):
                    epanet_api.setcurvevalue(curve_idx, i+1, x, y)

            for pattern_id, values in self.__patterns.items():
                epanet_api.add_pattern(pattern_id, values)

            for junc_id in self.get_all_junctions():
                epanet_api.addnode(junc_id, EpanetConstants.EN_JUNCTION)

                node_idx = epanet_api.get_node_idx(junc_id)
                junc_info = self.get_node_info(junc_id)
                epanet_api.setnodevalue(node_idx, EpanetConstants.EN_ELEVATION,
                                        junc_info["elevation"])
                epanet_api.setbasedemand(node_idx, 1, junc_info["base_demand"])
                epanet_api.setcoord(node_idx, junc_info["coord"][0], junc_info["coord"][1])
                epanet_api.setcomment(EpanetConstants.EN_NODE, node_idx, junc_info["comment"])
                if "demand_patterns_id" in junc_info:
                    for i, demand_pattern_id in enumerate(junc_info["demand_patterns_id"]):
                        epanet_api.setdemandpattern(node_idx, i+1,
                                                    epanet_api.getpatternindex(demand_pattern_id))

            for reservoir_id in self.get_all_reservoirs():
                epanet_api.addnode(reservoir_id, EpanetConstants.EN_RESERVOIR)

                node_idx = epanet_api.get_node_idx(reservoir_id)
                reservoir_info = self.get_node_info(reservoir_id)
                epanet_api.setnodevalue(node_idx, EpanetConstants.EN_ELEVATION,
                                        reservoir_info["elevation"])
                epanet_api.setcoord(node_idx, reservoir_info["coord"][0],
                                    reservoir_info["coord"][1])
                epanet_api.setcomment(EpanetConstants.EN_NODE, node_idx,
                                      reservoir_info["comment"])

            for tank_id in self.get_all_tanks():
                epanet_api.addnode(tank_id, EpanetConstants.EN_TANK)

                node_idx = epanet_api.get_node_idx(tank_id)
                tank_info = self.get_node_info(tank_id)
                if tank_info["cylindric"] is False:
                    raise NotImplementedError("Non-cylindric tanks are not supported!")
                else:
                    epanet_api.setnodevalue(node_idx, EpanetConstants.EN_ELEVATION,
                                            tank_info["elevation"])
                    epanet_api.setcoord(node_idx, tank_info["coord"][0], tank_info["coord"][1])
                    epanet_api.setcomment(EpanetConstants.EN_NODE, node_idx, tank_info["comment"])
                    epanet_api.setnodevalue(node_idx, EpanetConstants.EN_TANKDIAM,
                                            tank_info["diameter"])
                    epanet_api.setnodevalue(node_idx, EpanetConstants.EN_MIXFRACTION,
                                            tank_info["mixing_fraction"])
                    epanet_api.setnodevalue(node_idx, EpanetConstants.EN_MIXMODEL,
                                            tank_info["mixing_model"])
                    epanet_api.setnodevalue(node_idx, EpanetConstants.EN_CANOVERFLOW,
                                            float(tank_info["can_overflow"]))

                    tank_info["min_level"] = tank_info["min_vol"] / \
                        (math.pi * (0.5 * tank_info["diameter"])**2)
                    tank_info["init_level"] = tank_info["init_vol"] / \
                        (math.pi * (0.5 * tank_info["diameter"])**2)

                    epanet_api.settankdata(node_idx, tank_info["elevation"],
                                           tank_info["init_level"], tank_info["min_level"],
                                           tank_info["max_level"], tank_info["diameter"],
                                           tank_info["min_vol"], tank_info["vol_curve_id"])

            for pipe_id, (node_a, node_b) in self.get_all_pipes():
                epanet_api.addlink(pipe_id, EpanetConstants.EN_PIPE, node_a, node_b)

                pipe_idx = epanet_api.get_link_idx(pipe_id)
                pipe_info = self.get_link_info(pipe_id)
                epanet_api.setlinkvalue(pipe_idx, EpanetConstants.EN_LENGTH, pipe_info["length"])
                epanet_api.setlinkvalue(pipe_idx, EpanetConstants.EN_DIAMETER,
                                        pipe_info["diameter"])
                epanet_api.setlinkvalue(pipe_idx, EpanetConstants.EN_ROUGHNESS,
                                        pipe_info["roughness_coeff"])
                epanet_api.setlinkvalue(pipe_idx, EpanetConstants.EN_KBULK, pipe_info["bulk_coeff"])
                epanet_api.setlinkvalue(pipe_idx, EpanetConstants.EN_KWALL, pipe_info["wall_coeff"])
                epanet_api.setlinkvalue(pipe_idx, EpanetConstants.EN_MINORLOSS,
                                        pipe_info["loss_coeff"])
                epanet_api.setlinkvalue(pipe_idx, EpanetConstants.EN_INITSETTING,
                                        pipe_info["init_setting"])
                epanet_api.setlinkvalue(pipe_idx, EpanetConstants.EN_INITSTATUS,
                                        pipe_info["init_status"])

            for valve_id in self.get_all_valves():
                valve_info = self.get_valve_info(valve_id)
                node_a, node_b = valve_info["end_points"]
                epanet_api.addlink(valve_id, valve_info["type"], node_a, node_b)
                link_idx = epanet_api.get_link_idx(valve_id)
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_DIAMETER,
                                        valve_info["diameter"])
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_INITSETTING,
                                        valve_info["initial_setting"])
                if valve_info["type"] not in [EpanetConstants.EN_GPV, EpanetConstants.EN_PRV,
                                              EpanetConstants.EN_CVPIPE]:
                    epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_INITSTATUS,
                                            valve_info["initial_status"])

            for pump_id in self.get_all_pumps():
                pump_info = self.get_pump_info(pump_id)
                node_a, node_b = pump_info["end_points"]
                epanet_api.addlink(pump_id, pump_info["type"], node_a, node_b)

                link_idx = link_idx = epanet_api.get_link_idx(pump_id)
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_INITSETTING,
                                        pump_info["init_setting"])
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_INITSTATUS,
                                        pump_info["init_status"])

                if pump_info["curve_id"] is not None:
                    curve_idx = epanet_api.getcurveindex(pump_info["curve_id"])
                    epanet_api.setheadcurveindex(link_idx, curve_idx)

            epanet_api.saveinpfile(inp_file_out)

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
        cubicmeter_to_cubicfeet = 35.3146667215

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

            if "max_level" in node_info:
                node_info["max_level"] *= conv_factor
            if "min_level" in node_info:
                node_info["min_level"] *= conv_factor
            if "init_level" in node_info:
                node_info["init_level"] *= conv_factor
            if "min_vol" in node_info:
                if units == UNITS_USCUSTOM:
                    node_info["min_vol"] *= cubicmeter_to_cubicfeet
                else:
                    node_info["min_vol"] *= 1. / cubicmeter_to_cubicfeet

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
                               valves=self.valves, units=units, curves=self.__curves,
                               patterns=self.__patterns)

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
            if self.get_node_info(node_id)["type"] == EpanetConstants.EN_JUNCTION:
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
            if self.get_node_info(node_id)["type"] == EpanetConstants.EN_TANK:
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
            if self.get_node_info(node_id)["type"] == EpanetConstants.EN_RESERVOIR:
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

            if link_info["type"] == EpanetConstants.EN_PIPE:
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
    def curves(self) -> dict[str, tuple[int, list[tuple[float, float]]]]:
        """
        Gets all curves -- i.e., ID and list of points.

        Returns
        -------
        `dict[str, tuple[int, list[tuple[float, float]]]]`
            All curves.
        """
        return deepcopy(self.__curves)

    @property
    def patterns(self) -> dict[str, list[float]]:
        """
        Returns all time patterns -- i.e., ID and list of multipliers.

        Returns
        -------
        `dict[str, list[float]]`
            All time patterns.
        """
        return deepcopy(self.__patterns)

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

        adj_matrix = self.get_adj_matrix()
        other_adj_matrix = other.get_adj_matrix()

        return self.name == other.name \
            and not np.any(adj_matrix.data != other_adj_matrix.data) \
            and not np.any(adj_matrix.indices != other_adj_matrix.indices) \
            and not np.any(adj_matrix.indptr != other_adj_matrix.indptr) \
            and self.get_all_nodes() == other.get_all_nodes() \
            and all(link_a[0] == link_b[0] and link_a[1] == link_b[1]
                    for link_a, link_b in zip(self.get_all_links(), other.get_all_links())) \
            and self.__units == other.units \
            and self.get_all_pumps() == other.get_all_pumps() \
            and self.get_all_valves() == other.get_all_valves() \
            and self.__curves == other.curves \
            and self.__patterns == other.patterns

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
                                           "curves": self.__curves,
                                           "patterns": self.__patterns,
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
        tank_data = {"id": [], "min_vol": [], "max_level": [], "min_level": [], "mixing_fraction": [],
                     "elevation": [], "diameter": [], "geometry": [], "init_vol": [], "mixing_model": []}
        reservoir_data = {"id": [], "elevation": [], "geometry": []}
        for node_id in self.get_all_nodes():
            node_info = self.get_node_info(node_id)

            node_data["id"].append(node_id)
            node_data["type"].append(node_info["type"])
            node_data["elevation"].append(node_info["elevation"])
            node_data["geometry"].append(Point(node_info["coord"]))

            if node_info["type"] == EpanetConstants.EN_TANK:
                tank_data["id"].append(node_id)
                tank_data["elevation"].append(node_info["elevation"])
                tank_data["diameter"].append(node_info["diameter"])
                tank_data["max_level"].append(node_info["max_level"])
                tank_data["min_level"].append(node_info["min_level"])
                tank_data["min_vol"].append(node_info["min_vol"])
                tank_data["init_vol"].append(node_info["init_vol"])
                tank_data["mixing_fraction"].append(node_info["mixing_fraction"])
                tank_data["mixing_model"].append(node_info["mixing_model"])
                tank_data["geometry"].append(Point(node_info["coord"]))
            elif node_info["type"] == EpanetConstants.EN_RESERVOIR:
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

            if link_info["type"] == EpanetConstants.EN_PIPE:
                pipe_data["id"].append(link_id)
                pipe_data["type"].append(link_info["type"])
                pipe_data["end_point_a"].append(link_nodes[0])
                pipe_data["end_point_b"].append(link_nodes[1])
                pipe_data["length"].append(link_info["length"])
                pipe_data["diameter"].append(link_info["diameter"])
                pipe_data["geometry"].append(LineString(end_points_coord))
            elif link_info["type"] == EpanetConstants.EN_PUMP:
                pump_data["id"].append(link_id)
                pump_data["type"].append(self.get_pump_info(link_id)["type"])
                if pumps_as_points is True:
                    pump_data["geometry"].append(Point(end_points_coord[0]))
                else:
                    pump_data["geometry"].append(LineString(end_points_coord))
            else:   # Valve
                valve_data["id"].append(link_id)
                valve_data["type"].append(self.get_valve_info(link_id)["type"])
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

    def get_adj_list(self) -> dict[str, list[str]]:
        """
        Returns the connectivity of the nodes (node IDs) as an adjacency list.

        Returns
        -------
        `dict[str, list[str]]`
            Adjacency list as a dictionary.
        """
        adj_list = {}

        for node_id in self.get_all_nodes():
            adj_list[node_id] = self.get_neighbors(node_id)

        return adj_list

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
