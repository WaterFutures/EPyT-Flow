"""
Module provides a class for implementing sensor configurations.
"""
from copy import deepcopy
import itertools
import numpy as np
import epyt
from epyt.epanet import ToolkitConstants

from ..serialization import SENSOR_CONFIG_ID, JsonSerializable, serializable


SENSOR_TYPE_NODE_PRESSURE          = 1
SENSOR_TYPE_NODE_QUALITY           = 2
SENSOR_TYPE_NODE_DEMAND            = 3
SENSOR_TYPE_LINK_FLOW              = 4
SENSOR_TYPE_LINK_QUALITY           = 5
SENSOR_TYPE_VALVE_STATE            = 6
SENSOR_TYPE_PUMP_STATE             = 7
SENSOR_TYPE_TANK_VOLUME            = 8
SENSOR_TYPE_NODE_BULK_SPECIES      = 9
SENSOR_TYPE_LINK_BULK_SPECIES      = 10
SENSOR_TYPE_SURFACE_SPECIES        = 11
SENSOR_TYPE_PUMP_EFFICIENCY        = 12
SENSOR_TYPE_PUMP_ENERGYCONSUMPTION = 13

AREA_UNIT_FT2 = 1
AREA_UNIT_M2 = 2
AREA_UNIT_CM2 = 3
MASS_UNIT_MG = 4
MASS_UNIT_UG = 5
MASS_UNIT_MOL = 6
MASS_UNIT_MMOL = 7
TIME_UNIT_HRS = 8
MASS_UNIT_CUSTOM = 9


def areaunit_to_id(unit_desc: str) -> int:
    """
    Converts a given area units string to the corresponding ID.

    Parameters
    ----------
    unit_desc : `str`
        Area units string.

    Returns
    -------
    `int`
        Corresponding area unit ID.
    """
    return {"FT2": AREA_UNIT_FT2,
            "M2": AREA_UNIT_M2,
            "CM2": AREA_UNIT_CM2}[unit_desc]


def massunit_to_id(unit_desc: str) -> int:
    """
    Converts a given mass units string to the corresponding ID.

    Parameters
    ----------
    unit_desc : `str`
        Mass units string.

    Returns
    -------
    `int`
        Corresponding mass unit ID.
    """
    mass_unit_dict = {"MG": MASS_UNIT_MG,
                      "UG": MASS_UNIT_UG,
                      "MOL": MASS_UNIT_MOL,
                      "MMOL": MASS_UNIT_MMOL}

    if unit_desc in mass_unit_dict:
        return mass_unit_dict[unit_desc]
    else:
        return MASS_UNIT_CUSTOM


def qualityunit_to_id(unit_desc: str) -> int:
    """
    Converts a given measurement unit description to the corresponding mass unit ID.

    Parameters
    ----------
    unit_desc : `str`
        Mass unit.

    Returns
    -------
    `int`
        Mass unit ID.

        Will be either None (if no water quality analysis was set up) or
        one of the following constants:

            - MASS_UNIT_MG  = 4   (mg/L)
            - MASS_UNIT_UG  = 5   (ug/L)
            - TIME_UNIT_HRS = 8  (hrs)
    """
    if unit_desc == "mg/L":
        return MASS_UNIT_MG
    elif unit_desc == "ug/L":
        return MASS_UNIT_UG
    elif unit_desc == "hrs":
        return TIME_UNIT_HRS
    else:
        return None


def massunit_to_str(unit_id: int) -> str:
    """
    Converts a given mass unit ID to the corresponding description.

    Parameters
    ----------
    unit_id : `int`
        ID of the mass unit.

        Must be one of the following constant:

            - MASS_UNIT_MG     = 4
            - MASS_UNIT_UG     = 5
            - MASS_UNIT_MOL    = 6
            - MASS_UNIT_MMOL   = 7
            - MASS_UNIT_CUSTOM = 9

    Returns
    -------
    `str`
        Mass unit description.
    """
    if unit_id is None:
        return ""
    elif unit_id == MASS_UNIT_MG:
        return "MG"
    elif unit_id == MASS_UNIT_UG:
        return "UG"
    elif unit_id == MASS_UNIT_MOL:
        return "MOL"
    elif unit_id == MASS_UNIT_MMOL:
        return "MMOL"
    elif unit_id == MASS_UNIT_CUSTOM:
        return "CUSTOM UNIT"
    else:
        raise ValueError(f"Unknown mass unit ID '{unit_id}'")


def flowunit_to_str(unit_id: int) -> str:
    """
    Converts a given flow unit ID to the corresponding description.

    Parameters
    ----------
    unit_id : `int`
        ID of the flow unit.

        Must be one of the following EPANET toolkit constants:

            - EN_CFS  = 0 (cubic foot/sec)
            - EN_GPM  = 1 (gal/min)
            - EN_MGD  = 2 (Million gal/day)
            - EN_IMGD = 3 (Imperial MGD)
            - EN_AFD  = 4 (ac-foot/day)
            - EN_LPS  = 5 (liter/sec)
            - EN_LPM  = 6 (liter/min)
            - EN_MLD  = 7 (Megaliter/day)
            - EN_CMH  = 8 (cubic meter/hr)
            - EN_CMD  = 9 (cubic meter/day)

    Returns
    -------
    `str`
        Flow unit description.
    """
    if unit_id is None:
        return ""
    elif unit_id == ToolkitConstants.EN_CFS:
        return "cubic foot/sec"
    elif unit_id == ToolkitConstants.EN_GPM:
        return "gal/min"
    elif unit_id == ToolkitConstants.EN_MGD:
        return "Million gal/day"
    elif unit_id == ToolkitConstants.EN_IMGD:
        return "Imperial MGD"
    elif unit_id == ToolkitConstants.EN_AFD:
        return "ac-foot/day"
    elif unit_id == ToolkitConstants.EN_LPS:
        return "liter/sec"
    elif unit_id == ToolkitConstants.EN_LPM:
        return "liter/min"
    elif unit_id == ToolkitConstants.EN_MLD:
        return "Megaliter/day"
    elif unit_id == ToolkitConstants.EN_CMH:
        return "cubic meter/hr"
    elif unit_id == ToolkitConstants.EN_CMD:
        return "cubic meter/day"
    else:
        raise ValueError(f"Unknown unit ID '{unit_id}'")


def qualityunit_to_str(unit_id: int) -> str:
    """
    Converts a given quality measurement unit ID to the corresponding description.

    Parameters
    ----------
    unit_id : `int`
        ID of the quality unit.

        Must be one of the following constants:

            - MASS_UNIT_MG  = 4  (mg/L)
            - MASS_UNIT_UG  = 5  (ug/L)
            - TIME_UNIT_HRS = 8  (hrs)

    Returns
    -------
    `str`
        Mass unit description.
    """
    if unit_id is None:
        return ""
    elif unit_id == MASS_UNIT_MG:
        return "mg/L"
    elif unit_id == MASS_UNIT_UG:
        return "ug/L"
    elif unit_id == TIME_UNIT_HRS:
        return "hrs"
    else:
        raise ValueError(f"Unknown unit ID '{unit_id}'")


def areaunit_to_str(unit_id: int) -> str:
    """
    Converts a given area measurement unit ID to the corresponding description.

    Parameters
    ----------
    unit_id : `int`
        ID of the area unit.

        Must be one of the following constants:

            - AREA_UNIT_FT2 = 1
            - AREA_UNIT_M2  = 2
            - AREA_UNIT_CM2 = 3

    Returns
    -------
    `str`
        Area unit description.
    """
    if unit_id is None:
        return None
    elif unit_id == AREA_UNIT_FT2:
        return "FT2"
    elif unit_id == AREA_UNIT_M2:
        return "M2"
    elif unit_id == AREA_UNIT_CM2:
        return "CM2"
    else:
        raise ValueError(f"Unknown unit ID '{unit_id}'")


def is_flowunit_simetric(unit_id: int) -> bool:
    """
    Checks if a given flow unit belongs to SI metric units.

    Parameters
    ----------
    unit_id : `int`
        ID of the flow unit.

        Must be one of the following EPANET toolkit constants:

            - EN_CFS  = 0 (cubic foot/sec)
            - EN_GPM  = 1 (gal/min)
            - EN_MGD  = 2 (Million gal/day)
            - EN_IMGD = 3 (Imperial MGD)
            - EN_AFD  = 4 (ac-foot/day)
            - EN_LPS  = 5 (liter/sec)
            - EN_LPM  = 6 (liter/min)
            - EN_MLD  = 7 (Megaliter/day)
            - EN_CMH  = 8 (cubic meter/hr)
            - EN_CMD  = 9 (cubic meter/day)

    Returns
    -------
    `bool`
        True if the fiven unit is a SI metric unit, False otherwise.
    """
    return unit_id in [ToolkitConstants.EN_LPS, ToolkitConstants.EN_LPM, ToolkitConstants.EN_MLD,
                       ToolkitConstants.EN_CMH, ToolkitConstants.EN_CMD]


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
    flow_unit : `int`
        Specifies the flow units and consequently all other hydraulic units
        (US CUSTOMARY or SI METRIC) as well.

        Must be one of the following EPANET toolkit constants:

            - EN_CFS = 0 (cubic foot/sec)
            - EN_GPM = 1 (gal/min)
            - EN_MGD = 2 (Million gal/day)
            - EN_IMGD = 3 (Imperial MGD)
            - EN_AFD = 4 (ac-foot/day)
            - EN_LPS = 5 (liter/sec)
            - EN_LPM = 6 (liter/min)
            - EN_MLD = 7 (Megaliter/day)
            - EN_CMH = 8 (cubic meter/hr)
            - EN_CMD = 9 (cubic meter/day)
    quality_unit : `str`, optional
        Measurement unit (in a basic quality analysis) -- only relevant
        if basic water quality is enabled.

        Must be one of the following constants:

            - MASS_UNIT_MG = 4     (mg/L)
            - MASS_UNIT_UG = 5     (ug/L)
            - TIME_UNIT_HRS = 8    (hrs)

    bulk_species_mass_unit : `list[int]`, optional
        Specifies the mass unit for each bulk species -- only relevant if EPANET-MSX is used.

        Must be one of the following constants:

            - MASS_UNIT_MG = 4      (milligram)
            - MASS_UNIT_UG = 5      (microgram)
            - MASS_UNIT_MOL = 6     (mole)
            - MASS_UNIT_MMOL = 7    (millimole)

        Note that the assumed ordering is the same as given in 'bulk_species'.
    surface_species_mass_unit : `list[int]`, optional
        Specifies the mass unit for each surface species -- only relevant if EPANET-MSX is used.

        Must be one of the following constants:

            - MASS_UNIT_MG = 4      (milligram)
            - MASS_UNIT_UG = 5      (microgram)
            - MASS_UNIT_MOL = 6     (mole)
            - MASS_UNIT_MMOL = 7    (millimole)

        Note that the assumed ordering is the same as given in 'surface_species'.
    surface_species_area_unit : `int`, optional
        Species the area unit of all surface species -- only relevant if EPANET-MSX is used.
        Must be one of the following constants:

            - AREA_UNIT_FT2 = 1     (square feet)
            - AREA_UNIT_M2 = 2      (square meters)
            - AREA_UNIT_CM2 = 3     (square centimeters)
    """
    def __init__(self, nodes: list[str], links: list[str], valves: list[str], pumps: list[str],
                 tanks: list[str], bulk_species: list[str], surface_species: list[str],
                 flow_unit: int,
                 pressure_sensors: list[str] = [],
                 flow_sensors: list[str] = [],
                 demand_sensors: list[str] = [],
                 quality_node_sensors: list[str] = [],
                 quality_link_sensors: list[str] = [],
                 valve_state_sensors: list[str] = [],
                 pump_state_sensors: list[str] = [],
                 pump_efficiency_sensors: list[str] = [],
                 pump_energyconsumption_sensors: list[str] = [],
                 tank_volume_sensors: list[str] = [],
                 bulk_species_node_sensors: dict = {},
                 bulk_species_link_sensors: dict = {},
                 surface_species_sensors: dict = {},
                 node_id_to_idx: dict = None, link_id_to_idx: dict = None,
                 valve_id_to_idx: dict = None, pump_id_to_idx: dict = None,
                 tank_id_to_idx: dict = None, bulkspecies_id_to_idx: dict = None,
                 surfacespecies_id_to_idx: dict = None,
                 quality_unit: int = None,
                 bulk_species_mass_unit : list[int] = [],
                 surface_species_mass_unit : list[int] = [],
                 surface_species_area_unit : int = None,
                 **kwds):
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

        if not isinstance(pump_efficiency_sensors, list):
            raise TypeError("'pump_efficiency_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(pump_efficiency_sensors)}'")
        if any(link not in pumps for link in pump_efficiency_sensors):
            raise ValueError("Each item in 'pump_efficiency_sensors' must be in 'pumps' -- cannot " +
                             "place a sensor at a non-existing pump.")

        if not isinstance(pump_energyconsumption_sensors, list):
            raise TypeError("'pump_energyconsumption_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(pump_energyconsumption_sensors)}'")
        if any(link not in pumps for link in pump_energyconsumption_sensors):
            raise ValueError("Each item in 'pump_energyconsumption_sensors' must be in 'pumps' -- cannot " +
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
        if any(node_id not in nodes for node_id in list(itertools.chain(
                *bulk_species_node_sensors.values()))):
            raise ValueError("Unknown node ID in 'bulk_species_node_sensors'")

        if not isinstance(bulk_species_link_sensors, dict):
            raise TypeError("'bulk_species_link_sensors' must be an instance of 'dict' but not " +
                            f"of '{type(bulk_species_link_sensors)}'")
        if any(bulk_species_id not in bulk_species
               for bulk_species_id in bulk_species_link_sensors.keys()):
            raise ValueError("Unknown bulk species ID in 'bulk_species_link_sensors'")
        if any(link_id not in links for link_id in list(itertools.chain(
                *bulk_species_link_sensors.values()))):
            raise ValueError("Unknown link/pipe ID in 'bulk_species_link_sensors'")

        if not isinstance(surface_species_sensors, dict):
            raise TypeError("'surface_species_sensors' must be an instance of 'dict' but not " +
                            f"of '{type(surface_species_sensors)}'")
        if any(surface_species_id not in surface_species_sensors
               for surface_species_id in surface_species_sensors.keys()):
            raise ValueError("Unknown surface species ID in 'surface_species_sensors'")
        if any(link_id not in links for link_id in list(itertools.chain(
                *surface_species_sensors.values()))):
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

        if not isinstance(flow_unit, int):
            raise TypeError("'flow_unit' must be a an instance of 'int' " +
                            f"but not of '{type(flow_unit)}'")
        if flow_unit not in range(10):
            raise ValueError("Invalid value of 'flow_unit'")

        if quality_unit is not None:
            if not isinstance(quality_unit, int):
                raise TypeError("'quality_mass_unit' must be an instance of 'int' " +
                                f"but not of '{type(quality_unit)}'")
            if quality_unit not in [MASS_UNIT_MG, MASS_UNIT_UG, TIME_UNIT_HRS]:
                raise ValueError("Invalid value of 'quality_unit'")

        if len(bulk_species_mass_unit) != len(bulk_species):
            raise ValueError("Inconsistency between 'bulk_species_mass_unit' and 'bulk_species'")
        if any(not isinstance(mass_unit, int) for mass_unit in bulk_species_mass_unit):
            raise TypeError("All items in 'bulk_species_mass_unit' must be an instance of 'int'")
        if any(mass_unit not in [MASS_UNIT_MG, MASS_UNIT_UG, MASS_UNIT_MOL, MASS_UNIT_MMOL,
                                 MASS_UNIT_CUSTOM]
               for mass_unit in bulk_species_mass_unit):
            raise ValueError("Invalid mass unit in 'bulk_species_mass_unit'")

        if len(surface_species_mass_unit) != len(surface_species):
            raise ValueError("Inconsistency between 'surface_species_mass_unit' " +
                             "and 'surface_species'")
        if any(not isinstance(mass_unit, int) for mass_unit in surface_species_mass_unit):
            raise TypeError("All items in 'surface_species_mass_unit' must be an instance of 'int'")
        if any(mass_unit not in [MASS_UNIT_MG, MASS_UNIT_UG, MASS_UNIT_MOL, MASS_UNIT_MMOL,
                                 MASS_UNIT_CUSTOM]
               for mass_unit in surface_species_mass_unit):
            raise ValueError("Invalid mass unit in 'surface_species_mass_unit'")

        if surface_species_area_unit is not None:
            if not isinstance(surface_species_area_unit, int):
                raise TypeError("'surface_species_area_unit' must be a an instance of 'int' " +
                                f"but not of '{type(surface_species_area_unit)}'")
            if surface_species_area_unit not in [AREA_UNIT_FT2, AREA_UNIT_M2, AREA_UNIT_CM2]:
                raise ValueError("Invalid area unit 'surface_species_area_unit'")

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
        self.__pump_energyconsumption_sensors = pump_energyconsumption_sensors
        self.__pump_efficiency_sensors = pump_efficiency_sensors
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
        self.__flow_unit = flow_unit
        self.__quality_unit = quality_unit
        self.__bulk_species_mass_unit = bulk_species_mass_unit
        self.__surface_species_mass_unit = surface_species_mass_unit
        self.__surface_species_area_unit = surface_species_area_unit

        self.__compute_indices()    # Compute indices

        super().__init__(**kwds)

    @staticmethod
    def create_empty_sensor_config(sensor_config):
        """
        Creates an empty sensor configuration from a given sensor configuration
        -- i.e. a clone of the given sensor configuration except that no sensors are set.

        Parameters
        ----------
        sensor_config : :class:`~epyt_flow.simulation.sensor_config.SensorConfig`
            Sensor configuration used as a basis.

        Returns
        -------
        :class:`epyt_flow.simulation.sensor_config.SensorConfig`
            Empty sensor configuration.
        """
        return SensorConfig(nodes=sensor_config.nodes,
                            links=sensor_config.links,
                            valves=sensor_config.valves,
                            pumps=sensor_config.pumps,
                            tanks=sensor_config.tanks,
                            flow_unit=sensor_config.flow_unit,
                            quality_unit=sensor_config.quality_unit,
                            bulk_species=sensor_config.bulk_species,
                            surface_species=sensor_config.surface_species,
                            bulk_species_mass_unit=sensor_config.bulk_species_mass_unit,
                            surface_species_mass_unit=sensor_config.surface_species_mass_unit,
                            surface_species_area_unit=sensor_config.surface_species_area_unit,
                            node_id_to_idx=sensor_config.node_id_to_idx,
                            link_id_to_idx=sensor_config.link_id_to_idx,
                            valve_id_to_idx=sensor_config.valve_id_to_idx,
                            pump_id_to_idx=sensor_config.pump_id_to_idx,
                            tank_id_to_idx=sensor_config.tank_id_to_idx,
                            bulkspecies_id_to_idx=sensor_config.bulkspecies_id_to_idx,
                            surfacespecies_id_to_idx=sensor_config.surfacespecies_id_to_idx)

    def is_empty(self) -> bool:
        """
        Checks if the sensor configuration is empty -- i.e. no sensors are placed.

        Returns
        -------
        `bool`
            True if no sensors are placed, False otherwise.
        """
        if self.__pressure_sensors == [] and self.__flow_sensors == [] \
                and self.__demand_sensors == [] and self.__quality_node_sensors == [] \
                and self.__quality_link_sensors == [] and self.__valve_state_sensors == [] \
                and self.__pump_state_sensors == [] \
                and self.__pump_energyconsumption_sensors == [] \
                and self.__pump_efficiency_sensors == [] and self.__tank_volume_sensors == [] \
                and self.__bulk_species_node_sensors == [] \
                and self.__bulk_species_link_sensors == [] \
                and self.__surface_species_sensors == []:
            return True
        else:
            return False

    def place_sensors_everywhere(self) -> None:
        """
        Places sensors everywhere -- i.e. every possible quantity is monitored
        at every position in the network.
        """
        self.__pressure_sensors = self.__nodes[:]
        self.__demand_sensors = self.__nodes[:]
        self.__flow_sensors = self.__links[:]
        self.__quality_node_sensors = self.__nodes[:]
        self.__quality_link_sensors = self.__links[:]
        self.__pump_state_sensors = self.__pumps[:]
        self.__pump_energyconsumption_sensors = self.__pumps[:]
        self.__pump_efficiency_sensors = self.__pumps[:]
        self.__tank_volume_sensors = self.__tanks[:]
        self.__bulk_species_node_sensors = {species_id: self.__nodes[:]
                                            for species_id in self.__bulk_species}
        self.__bulk_species_link_sensors = {species_id: self.__links[:]
                                            for species_id in self.__bulk_species}
        self.__surface_species_sensors = {species_id: self.__links[:]
                                          for species_id in self.__surface_species}

        self.__compute_indices()

    @property
    def node_id_to_idx(self) -> dict:
        """
        Mapping of a surface node ID to the EPANET index
        (i.e. position in the raw sensor reading data).

        If None, it is assumed that the nodes (in 'nodes') are
        sorted according to their EPANET index.

        Returns
        -------
        `dict`
            Node ID to index mapping.
        """
        return self.__node_id_to_idx

    @property
    def link_id_to_idx(self) -> dict:
        """
        Mapping of a link/pipe ID to the EPANET index
        (i.e. position in the raw sensor reading data).

        If None is given, it is assumed that the links/pipes (in 'links') are
        sorted according to their EPANET index.

        Returns
        -------
        `dict`
            Link/Pipe ID to index mapping.
        """
        return self.__link_id_to_idx

    @property
    def valve_id_to_idx(self) -> dict:
        """
        Mapping of a valve ID to the EPANET index
        (i.e. position in the raw sensor reading data).

        If None, it is assumed that the valves (in 'valves') are
        sorted according to their EPANET index.

        Returns
        -------
        `dict`
            Valve ID to index mapping.
        """
        return self.__valve_id_to_idx

    @property
    def pump_id_to_idx(self) -> dict:
        """
        Mapping of a pump ID to the EPANET index
        (i.e. position in the raw sensor reading data).

        If None, it is assumed that the pumps (in 'pumps') are
        sorted according to their EPANET index.

        Returns
        -------
        `dict`
            Pump ID to index mapping.
        """
        return self.__pump_id_to_idx

    @property
    def tank_id_to_idx(self) -> dict:
        """
        Mapping of a tank ID to the EPANET index
        (i.e. position in the raw sensor reading data).

        If None, it is assumed that the tanks (in 'tanks') are
        sorted according to their EPANET index.

        Returns
        -------
        `dict`
            Tank ID to index mapping.
        """
        return self.__tank_id_to_idx

    @property
    def bulkspecies_id_to_idx(self) -> dict:
        """
        Mapping of a bulk species ID to the EPANET index
        (i.e. position in the raw sensor reading data).

        If None, it is assumed that the bulk species (in 'bulk_species') are
        sorted according to their EPANET index.

        Returns
        -------
        `dict`
            Bulk species ID to index mapping.
        """
        return self.__bulkspecies_id_to_idx

    @property
    def surfacespecies_id_to_idx(self) -> dict:
        """
        Mapping of a surface species ID to the EPANET index
        (i.e. position in the raw sensor reading data).

        If None, it is assumed that the surface species (in 'surface_species') are
        sorted according to their EPANET index.

        Returns
        -------
        `dict`
            Surface species ID to index mapping.
        """
        return self.__surfacespecies_id_to_idx

    def map_node_id_to_idx(self, node_id: str) -> int:
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

    def map_link_id_to_idx(self, link_id: str) -> int:
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

    def map_valve_id_to_idx(self, valve_id: str) -> int:
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

    def map_pump_id_to_idx(self, pump_id: str) -> int:
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

    def map_tank_id_to_idx(self, tank_id: str) -> int:
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

    def map_bulkspecies_id_to_idx(self, bulk_species_id: str) -> int:
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

    def map_surfacespecies_id_to_idx(self, surface_species_id: str) -> int:
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
        self.__pressure_idx = np.array([self.map_node_id_to_idx(n)
                                        for n in self.__pressure_sensors], dtype=np.int32)
        self.__flow_idx = np.array([self.map_link_id_to_idx(link)
                                    for link in self.__flow_sensors], dtype=np.int32)
        self.__demand_idx = np.array([self.map_node_id_to_idx(n)
                                      for n in self.__demand_sensors], dtype=np.int32)
        self.__quality_node_idx = np.array([self.map_node_id_to_idx(n)
                                            for n in self.__quality_node_sensors], dtype=np.int32)
        self.__quality_link_idx = np.array([self.map_link_id_to_idx(link)
                                            for link in self.__quality_link_sensors],
                                           dtype=np.int32)
        self.__valve_state_idx = np.array([self.map_valve_id_to_idx(v)
                                           for v in self.__valve_state_sensors], dtype=np.int32)
        self.__pump_state_idx = np.array([self.map_pump_id_to_idx(p)
                                          for p in self.__pump_state_sensors], dtype=np.int32)
        self.__pump_efficiency_idx = np.array([self.map_pump_id_to_idx(p)
                                               for p in self.__pump_efficiency_sensors],
                                               dtype=np.int32)
        self.__pump_energyconsumption_idx = np.array([self.map_pump_id_to_idx(p)
                                                      for p in self.__pump_energyconsumption_sensors],
                                                      dtype=np.int32)
        self.__tank_volume_idx = np.array([self.map_tank_id_to_idx(t)
                                           for t in self.__tank_volume_sensors], dtype=np.int32)
        self.__bulk_species_node_idx = np.array([(self.map_bulkspecies_id_to_idx(s),
                                                  [self.map_node_id_to_idx(node_id)
                                                for node_id in self.__bulk_species_node_sensors[s]])
                                                for s in self.__bulk_species_node_sensors.keys()],
                                                dtype=object)
        self.__bulk_species_link_idx = np.array([(self.map_bulkspecies_id_to_idx(s),
                                                  [self.map_link_id_to_idx(link_id)
                                                for link_id in self.__bulk_species_link_sensors[s]])
                                                for s in self.__bulk_species_link_sensors.keys()],
                                                dtype=object)
        self.__surface_species_idx = np.array([(self.map_surfacespecies_id_to_idx(s),
                                                [self.map_link_id_to_idx(link_id)
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
        n_pump_efficiency_sensors = len(self.__pump_efficiency_sensors)
        n_pump_energyconsumption_sensors = len(self.__pump_energyconsumption_sensors)
        n_tank_volume_sensors = len(self.__tank_volume_sensors)
        n_bulk_species_node_sensors = len(list(itertools.chain(
            *self.__bulk_species_node_sensors.values())))
        n_bulk_species_link_sensors = len(list(itertools.chain(
            *self.__bulk_species_link_sensors.values())))

        pressure_idx_shift = 0
        flow_idx_shift = pressure_idx_shift + n_pressure_sensors
        demand_idx_shift = flow_idx_shift + n_flow_sensors
        node_quality_idx_shift = demand_idx_shift + n_demand_sensors
        link_quality_idx_shift = node_quality_idx_shift + n_node_quality_sensors
        valve_state_idx_shift = link_quality_idx_shift + n_link_quality_sensors
        pump_state_idx_shift = valve_state_idx_shift + n_valve_state_sensors
        pump_efficiency_idx_shift = pump_state_idx_shift + n_pump_state_sensors
        pump_energyconsumption_idx_shift = pump_efficiency_idx_shift + n_pump_efficiency_sensors
        tank_volume_idx_shift = pump_energyconsumption_idx_shift + n_pump_energyconsumption_sensors
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
                   "pump_efficiency": __build_sensors_id_to_idx(self.__pump_efficiency_sensors,
                                                                pump_efficiency_idx_shift),
                   "pump_energyconsumption":
                   __build_sensors_id_to_idx(self.__pump_energyconsumption_sensors,
                                             pump_energyconsumption_idx_shift),
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
        if epanet_api.msx is not None:
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
    def flow_unit(self) -> int:
        """
        Gets the flow units.
        Note that this specifies all other hydraulic units as well.

        Will be one of the following EPANET toolkit constants:

            - EN_CFS = 0 (cubic foot/sec)
            - EN_GPM = 1 (gal/min)
            - EN_MGD = 2 (Million gal/day)
            - EN_IMGD = 3 (Imperial MGD)
            - EN_AFD = 4 (ac-foot/day)
            - EN_LPS = 5 (liter/sec)
            - EN_LPM = 6 (liter/min)
            - EN_MLD = 7 (Megaliter/day)
            - EN_CMH = 8 (cubic meter/hr)
            - EN_CMD = 9 (cubic meter/day)

        Returns
        -------
        `int`
            Flow unit ID.
        """
        return self.__flow_unit

    @property
    def quality_unit(self) -> int:
        """
        Gets the measurement unit ID used in the basic quality analysis.

        Will be one of the following constants:

            - MASS_UNIT_MG = 4      (milligram)
            - MASS_UNIT_UG = 5      (microgram)
            - TIME_UNIT_HRS = 6     (hours)

        Returns
        -------
        `int`
            Mass unit ID.
        """
        return self.__quality_unit

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
    def bulk_species_mass_unit(self) -> list[int]:
        """
        Gets the mass unit of each bulk species.

        Will be one of the following constants:

            - MASS_UNIT_MG = 4      (milligram)
            - MASS_UNIT_UG = 5      (microgram)
            - MASS_UNIT_MOL = 6     (mole)
            - MASS_UNIT_MMOL = 7    (millimole)

        Returns
        -------
        `int`
            Mass unit ID.
        """
        return self.__bulk_species_mass_unit

    @property
    def surface_species_mass_unit(self) -> list[int]:
        """
        Gets the mass unit of each surface species.

        Will be one of the following constants:

            - MASS_UNIT_MG = 4      (milligram)
            - MASS_UNIT_UG = 5      (microgram)
            - MASS_UNIT_MOL = 6     (mole)
            - MASS_UNIT_MMOL = 7    (millimole)

        Returns
        -------
        `int`
            Mass unit ID.
        """
        return self.__surface_species_mass_unit

    @property
    def surface_species_area_unit(self) -> int:
        """
        Gets the surface species area unit.

        Will be one of the following constants:

            - AREA_UNIT_FT2 = 1     (square feet)
            - AREA_UNIT_M2 = 2      (square meters)
            - AREA_UNIT_CM2 = 3     (square centimeters)

        Returns
        -------
        `int`
            Area unit ID.
        """
        return self.__surface_species_area_unit

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
    def pump_energyconsumption_sensors(self) -> list[str]:
        """
        Gets all pump energy consumption sensors
        (i.e. IDs of pumps at which the energy consumption is monitored).

        Returns
        -------
        `list[str]`
            All pump IDs with an energy consumption sensor.
        """
        return self.__pump_energyconsumption_sensors.copy()

    @pump_energyconsumption_sensors.setter
    def pump_energyconsumption_sensors(self, pump_energyconsumption_sensors: list[str]) -> None:
        if not isinstance(pump_energyconsumption_sensors, list):
            raise TypeError("'pump_energyconsumption_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(pump_energyconsumption_sensors)}'")
        if any(link not in self.__pumps for link in pump_energyconsumption_sensors):
            raise ValueError("Each item in 'pump_energyconsumption_sensors' must be in 'pumps' " +
                             "-- cannot place a sensor at a non-existing pump.")

        self.__pump_energyconsumption_sensors = pump_energyconsumption_sensors

        self.__compute_indices()

    @property
    def pump_efficiency_sensors(self) -> list[str]:
        """
        Gets all pump efficiency sensors
        (i.e. IDs of pumps at which the efficiency is monitored).

        Returns
        -------
        `list[str]`
            All pump IDs with an efficiency sensor.
        """
        return self.__pump_efficiency_sensors.copy()

    @pump_efficiency_sensors.setter
    def pump_efficiency_sensors(self, pump_efficiency_sensors: list[str]) -> None:
        if not isinstance(pump_efficiency_sensors, list):
            raise TypeError("'pump_efficiency_sensors' must be an instance of 'list[str]' " +
                            f"but not of '{type(pump_efficiency_sensors)}'")
        if any(link not in self.__pumps for link in pump_efficiency_sensors):
            raise ValueError("Each item in 'pump_efficiency_sensors' must be in 'pumps' " +
                             "-- cannot place a sensor at a non-existing pump.")

        self.__pump_efficiency_sensors = pump_efficiency_sensors

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
        if any(link_id not in self.__links for link_id in list(itertools.chain(
                *bulk_species_sensors.values()))):
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
               for link_id in list(itertools.chain(*surface_species_sensors.values()))):
            raise ValueError("Unknown link/pipe ID in 'surface_species_sensors'")

        self.__surface_species_sensors = surface_species_sensors

        self.__compute_indices()

    @property
    def sensors_id_to_idx(self) -> dict:
        """
        Gets a mapping of sensor IDs to indices in the final `Numpy array <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ returned by `get_data()`.

        Returns
        -------
        `dict`
            Mapping of sensor IDs to indices in the final `Numpy array <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_.
        """
        return deepcopy(self.__sensors_id_to_idx)

    def get_as_dict(self) -> dict:
        """
        Gets the sensor configuration as a dictionary.

        Returns
        -------
        `dict`
            Dictionary of set sensors -- the keys are the sensor types.
        """
        r = {}

        if self.__pressure_sensors != []:
            r["pressure"] = self.__pressure_sensors
        if self.__flow_sensors != []:
            r["flow"] = self.__flow_sensors
        if self.__demand_sensors != []:
            r["demand"] = self.__demand_sensors
        if self.__tank_volume_sensors != []:
            r["tank_volume"] = self.__tank_volume_sensors
        if self.__valve_state_sensors != []:
            r["valve_state"] = self.__valve_state_sensors
        if self.__pump_state_sensors != []:
            r["pump_state"] = self.__pump_state_sensors
        if self.__pump_efficiency_sensors != []:
            r["pump_efficiency"] = self.__pump_efficiency_sensors
        if self.__pump_energyconsumption_sensors != []:
            r["pump_energyconsumption"] = self.__pump_energyconsumption_sensors
        if self.__quality_node_sensors != []:
            r["node_quality"] = self.__quality_node_sensors
        if self.__quality_link_sensors != []:
            r["link_quality"] = self.__quality_link_sensors
        if self.__bulk_species_node_sensors != {}:
            r["node_bulk_species"] = self.__bulk_species_node_sensors
        if self.__bulk_species_link_sensors != {}:
            r["link_bulk_species"] = self.__bulk_species_link_sensors
        if self.__surface_species_sensors != {}:
            r["surface_species"] = self.__surface_species_sensors

        return r

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
                "pump_efficiency_sensors": self.__pump_efficiency_sensors,
                "pump_energyconsumption_sensors": self.__pump_energyconsumption_sensors,
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
                "surfacespecies_id_to_idx": self.__surfacespecies_id_to_idx,
                "flow_unit": self.__flow_unit,
                "quality_unit": self.__quality_unit,
                "bulk_species_mass_unit": self.__bulk_species_mass_unit,
                "surface_species_mass_unit": self.__surface_species_mass_unit,
                "surface_species_area_unit": self.__surface_species_area_unit}

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
            and self.__pump_efficiency_sensors == other.pump_efficiency_sensors \
            and self.__pump_energyconsumption_sensors == other.pump_energyconsumption_sensors \
            and self.__tank_volume_sensors == other.tank_volume_sensors \
            and self.__bulk_species_node_sensors == other.bulk_species_node_sensors \
            and self.__bulk_species_link_sensors == other.bulk_species_link_sensors \
            and self.__surface_species_sensors == other.surface_species_sensors \
            and self.__flow_unit == other.flow_unit \
            and self.__quality_unit == other.quality_unit \
            and self.__bulk_species_mass_unit == other.bulk_species_mass_unit \
            and self.__surface_species_mass_unit == other.surface_species_mass_unit \
            and self.__surface_species_area_unit == other.surface_species_area_unit \
            and self.__node_id_to_idx == other.node_id_to_idx \
            and self.__link_id_to_idx == other.link_id_to_idx \
            and self.__valve_id_to_idx == other.valve_id_to_idx \
            and self.__pump_id_to_idx == other.pump_id_to_idx \
            and self.__tank_id_to_idx == other.tank_id_to_idx \
            and self.__bulkspecies_id_to_idx == other.bulkspecies_id_to_idx \
            and self.__surfacespecies_id_to_idx == other.surfacespecies_id_to_idx

    def __str__(self) -> str:
        return f"nodes: {self.__nodes} links: {self.__links} valves: {self.__valves} " +\
            f"pumps: {self.__pumps} tanks: {self.__tanks} bulk_species: {self.__bulk_species} " +\
            f"surface_species: {self.__surface_species} " + \
            f"node_id_to_idx: {self.__node_id_to_idx} link_id_to_idx: {self.__link_id_to_idx} " +\
            f"pump_id_to_idx: {self.__pump_id_to_idx} tank_id_to_idx: {self.__tank_id_to_idx} " +\
            f"valve_id_to_idx: {self.__valve_id_to_idx} " +\
            f"bulkspecies_id_to_idx: {self.__bulkspecies_id_to_idx} " +\
            f"surfacespecies_id_to_idx: {self.__surfacespecies_id_to_idx} " +\
            f"pressure_sensors: {self.__pressure_sensors} flow_sensors: {self.__flow_sensors} " +\
            f"demand_sensors: {self.__demand_sensors} " +\
            f"quality_node_sensors: {self.__quality_node_sensors} " +\
            f"quality_link_sensors: {self.__quality_link_sensors} " +\
            f"valve_state_sensors: {self.__valve_state_sensors} " +\
            f"pump_state_sensors: {self.__pump_state_sensors} " +\
            f"pump_efficiency_sensors: {self.__pump_efficiency_sensors} " +\
            f"pump_energyconsumption_sensors: {self.__pump_energyconsumption_sensors} " +\
            f"tank_volume_sensors: {self.__tank_volume_sensors} " +\
            f"bulk_species_node_sensors: {self.__bulk_species_node_sensors} " +\
            f"bulk_species_link_sensors: {self.__bulk_species_link_sensors} " +\
            f"surface_species_sensors: {self.__surface_species_sensors} " +\
            f"flow_unit: {flowunit_to_str(self.__flow_unit)} " +\
            f"quality_unit: {qualityunit_to_str(self.__quality_unit)} " +\
            "bulk_species_mass_unit: " +\
            f"{list(map(massunit_to_str, self.__bulk_species_mass_unit))} " +\
            "surface_species_mass_unit: " +\
            f"{list(map(massunit_to_str, self.__surface_species_mass_unit))} " +\
            f"surface_species_area_unit: {areaunit_to_str(self.__surface_species_area_unit)}"

    def get_bulk_species_mass_unit_id(self, bulk_species_id: str) -> int:
        """
        Returns the mass unit of a given bulk species.

        Parameters
        ----------
        bulk_species_id : `str`
            ID of the bulk species.

        Returns
        -------
        `int`
            ID of the mass unit.

            Will be one of the following constant:

                - MASS_UNIT_MG   = 4
                - MASS_UNIT_UG   = 5
                - MASS_UNIT_MOL  = 6
                - MASS_UNIT_MMOL = 7
        """
        return self.__bulk_species_mass_unit[self.map_bulkspecies_id_to_idx(bulk_species_id)]

    def get_surface_species_mass_unit_id(self, surface_species_id: str) -> int:
        """
        Returns the mass unit of a given surface species.

        Parameters
        ----------
        surface_species_id : `str`
            ID of the surface species.

        Returns
        -------
        `int`
            ID of the mass unit.

            Will be one of the following constant:

                - MASS_UNIT_MG   = 4
                - MASS_UNIT_UG   = 5
                - MASS_UNIT_MOL  = 6
                - MASS_UNIT_MMOL = 7
        """
        return self.__surface_species_mass_unit[self.map_surfacespecies_id_to_idx(
            surface_species_id)]

    def compute_readings(self, pressures: np.ndarray, flows: np.ndarray, demands: np.ndarray,
                         nodes_quality: np.ndarray, links_quality: np.ndarray,
                         pumps_state: np.ndarray, pumps_efficiency: np.ndarray,
                         pumps_energyconsumption: np.ndarray, valves_state: np.ndarray,
                         tanks_volume: np.ndarray, bulk_species_node_concentrations: np.ndarray,
                         bulk_species_link_concentrations: np.ndarray,
                         surface_species_concentrations: np.ndarray) -> np.ndarray:
        """
        Applies the sensor configuration to a set of raw simulation results --
         i.e. computes the sensor readings as an array.

        Parameters
        ----------
        pressures : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Pressure values at all nodes.
        flows : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Flow values at all links/pipes.
        demands : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Demand values at all nodes.
        nodes_quality : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Quality values at all nodes.
        links_quality : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Quality values at all links/pipes.
        pumps_state : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            States of all pumps.
        pumps_efficiency : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Efficiency of all pumps.
        pumps_energyconsumption : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Energy consumption of all pumps.
        valves_state : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            States of all valves.
        tanks_volume : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Water volume in all tanks.
        bulk_species_node_concentrations : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Bulk species concentrations at all nodes.

            Expect a three-dimensional array: First dimension denotes time,
            second dimension corresponds to species ID,
            and third dimension contains the concentration.
        bulk_species_link_concentrations : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Bulk species concentrations at all links/pipes.

            Expect a three-dimensional array: First dimension denotes time,
            second dimension corresponds to species ID,
            and third dimension contains the concentration.
        surface_species_concentrations : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
            Surface species concentrations at all links/pipes.

            Expect a three-dimensional array: First dimension denotes time,
            second dimension corresponds to species ID,
            and third dimension contains the concentration.

        Returns
        -------
        `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
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

        if pumps_efficiency is not None:
            data.append(pumps_efficiency[:, self.__pump_efficiency_idx])
        else:
            if len(self.__pump_efficiency_sensors) != 0:
                raise ValueError("Pump efficiency readings requested " +
                                 "but no pump efficiency data is given")

        if pumps_energyconsumption is not None:
            data.append(pumps_energyconsumption[:, self.__pump_energyconsumption_idx])
        else:
            if len(self.__pump_energyconsumption_sensors) != 0:
                raise ValueError("Pump energy consumption readings requested " +
                                 "but no pump energy consumption data is given")

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
                             pump_state_sensor: str = None, pump_efficiency_sensor: str = None,
                             pump_energyconsumption_sensor: str = None,
                             tank_volume_sensor: str = None,
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
        pump_efficiency_sensor : `str`
            ID of the efficiency sensor (at a pump).
        pump_energyconsumption_sensor : `str`
            ID of the energy consumption sensor (at a pump).
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
        elif pump_efficiency_sensor is not None:
            return self.__sensors_id_to_idx["pump_efficiency"][pump_efficiency_sensor]
        elif pump_energyconsumption_sensor is not None:
            return self.__sensors_id_to_idx["pump_energyconsumption"][pump_energyconsumption_sensor]
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
