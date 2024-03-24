"""
Module provides a class for representing the topology of WDN.
"""
import numpy as np
import networkx as nx
from scipy.sparse import bsr_array

from .serialization import serializable, JsonSerializable, NETWORK_TOPOLOGY_ID


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
    links : `list[tuple[tuple[str, str], dict]]`
        List of all links/pipes -- i.e. link ID, ID of connecting nodes, and link information
        such as pipe diameter, length, etc.
    """
    def __init__(self, f_inp: str, nodes: list[tuple[str, dict]],
                 links: list[tuple[str, tuple[str, str], dict]], **kwds):
        super().__init__(name=f_inp, **kwds)

        self.__nodes = nodes
        self.__links = links

        for node_id, node_info in nodes:
            node_elevation = node_info["elevation"]
            node_type = node_info["type"]
            self.add_node(node_id, info={"elevation": node_elevation, "type": node_type})

        for link_id, link, link_info in links:
            link_diameter = link_info["diameter"]
            link_length = link_info["length"]
            self.add_edge(link[0], link[1], length=link_length,
                          info={"id": link_id, "nodes": link, "diameter": link_diameter,
                                "length": link_length})

    def get_all_nodes(self) -> list[str]:
        """
        Gets a list of all nodes.

        Returns
        -------
        `list[str]`
            List of all nodes ID.
        """
        return [node_id for node_id, _ in self.__nodes]

    def get_all_links(self) -> list[tuple[str, tuple[str, str]]]:
        """
        Gets a list of all links/pipes (incl. their end points).

        Returns
        -------
        `list[tuple[str, tuple[str, str]]]`
            List of links -- (link ID, (left node ID, right node ID)).
        """
        return [(link_id, end_points) for link_id, end_points, _ in self.__links]

    def get_node_info(self, node_id) -> dict:
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

    def get_link_info(self, link_id) -> dict:
        """
        Gets all information (e.g. diameter, length, etc.) associated with a given link/pipe.

        Parameters
        ----------
        link_id : `str`
            ID of the link/pipe.

        Returns
        -------
        `dict`
            Information associated with the given link/pipe.
        """
        for link_id_, link_nodes, link_info in self.__links:
            if link_id_ == link_id:
                return {"nodes": link_nodes} | link_info

        raise ValueError(f"Unknown link '{link_id}'")

    def __eq__(self, other) -> bool:
        if not isinstance(other, NetworkTopology):
            raise TypeError("Can not compare 'NetworkTopology' instance to " +
                            f"'{type(other)}' instance")

        return super().__eq__(other) and \
            self.get_all_nodes() == other.get_all_nodes() and \
            all(link_a[0] == link_b[0] and all(link_a[1] == link_b[1])
                for link_a, link_b in zip(self.get_all_links(), other.get_all_links()))

    def __str__(self) -> str:
        return f"f_inp: {self.name} nodes: {self.__nodes} links: {self.__links}"

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"f_inp": self.name,
                                           "nodes": self.__nodes,
                                           "links": self.__links}

    def get_adj_matrix(self) -> bsr_array:
        """
        Gets the adjacency matrix of this graph.

        Returns
        -------
        `scipy.bsr_array`
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
