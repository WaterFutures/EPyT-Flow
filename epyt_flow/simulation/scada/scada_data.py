"""
Module provides a class for storing and processing SCADA data.
"""
import warnings
from typing import Callable, Any
from copy import deepcopy
import numpy as np
import matplotlib
from epyt.epanet import ToolkitConstants

from ..sensor_config import SensorConfig, is_flowunit_simetric, massunit_to_str, flowunit_to_str,\
    qualityunit_to_str, areaunit_to_str,\
    MASS_UNIT_MG, MASS_UNIT_UG, TIME_UNIT_HRS, MASS_UNIT_MOL, MASS_UNIT_MMOL, \
    AREA_UNIT_CM2, AREA_UNIT_FT2, AREA_UNIT_M2, \
    SENSOR_TYPE_LINK_FLOW, SENSOR_TYPE_LINK_QUALITY,  SENSOR_TYPE_NODE_DEMAND, \
    SENSOR_TYPE_NODE_PRESSURE, SENSOR_TYPE_NODE_QUALITY, SENSOR_TYPE_PUMP_STATE, \
    SENSOR_TYPE_PUMP_EFFICIENCY, SENSOR_TYPE_PUMP_ENERGYCONSUMPTION, \
    SENSOR_TYPE_TANK_VOLUME, SENSOR_TYPE_VALVE_STATE, SENSOR_TYPE_NODE_BULK_SPECIES, \
    SENSOR_TYPE_LINK_BULK_SPECIES, SENSOR_TYPE_SURFACE_SPECIES
from ..events import SensorFault, SensorReadingAttack, SensorReadingEvent
from ...uncertainty import SensorNoise
from ...serialization import serializable, Serializable, SCADA_DATA_ID
from ...utils import plot_timeseries_data


@serializable(SCADA_DATA_ID, ".epytflow_scada_data")
class ScadaData(Serializable):
    """
    Class for storing and processing SCADA data.

    Parameters
    ----------
    sensor_config : :class:`~epyt_flow.simulation.sensor_config.SensorConfig`
        Specifications of all sensors.
    sensor_readings_time : `numpy.ndarray`
        Time (seconds since simulation start) for each sensor reading row
        in `sensor_readings_data_raw`.

        This parameter is expected to be a 1d array with the same size as
        the number of rows in `sensor_readings_data_raw`.
    pressure_data_raw : `numpy.ndarray`, optional
        Raw pressure values of all nodes as a two-dimensional array --
        first dimension encodes time, second dimension pressure at nodes.

        The default is None,
    flow_data_raw : `numpy.ndarray`, optional
        Raw flow values of all links/pipes --
        first dimension encodes time, second dimension pressure at links/pipes.

        The default is None.
    demand_data_raw : `numpy.ndarray`, optional
        Raw demand values of all nodes --
        first dimension encodes time, second dimension demand at nodes.

        The default is None.
    node_quality_data_raw : `numpy.ndarray`, optional
        Raw quality values of all nodes --
        first dimension encodes time, second dimension quality at nodes.

        The default is None.
    link_quality_data_raw : `numpy.ndarray`, optional
        Raw quality values of all links/pipes --
        first dimension encodes time, second dimension quality at links/pipes.

        The default is None.
    pumps_state_data_raw : `numpy.ndarray`, optional
        States of all pumps --
        first dimension encodes time, second dimension states of pumps.

        The default is None.
    valves_state_data_raw : `numpy.ndarray`, optional
        States of all valves --
        first dimension encodes time, second dimension states of valves.

        The default is None.
    tanks_volume_data_raw : `numpy.ndarray`, optional
        Water volumes in all tanks --
        first dimension encodes time, second dimension water volume in tanks.

        The default is None.
    surface_species_concentration_raw : `numpy.ndarray`, optional
        Raw concentrations of surface species as a tree dimensional array --
        first dimension encodes time, second dimension denotes the different surface species,
        third dimension denotes species concentrations at links/pipes.

        The default is None.
    bulk_species_node_concentration_raw : `numpy.ndarray`, optional
        Raw concentrations of bulk species at nodes as a tree dimensional array --
        first dimension encodes time, second dimension denotes the different bulk species,
        third dimension denotes species concentrations at nodes.

        The default is None.
    bulk_species_link_concentration_raw : `numpy.ndarray`, optional
        Raw concentrations of bulk species at links as a tree dimensional array --
        first dimension encodes time, second dimension denotes the different bulk species,
        third dimension denotes species concentrations at nodes.

        The default is None.
    pumps_energy_usage_data_raw : `numpy.ndarray`, optional
        Energy usage data of each pump.

        The default is None.
    pumps_efficiency_data_raw : `numpy.ndarray`, optional
        Pump efficiency data of each pump.

        The default is None.
    sensor_faults : list[:class:`~epyt_flow.simulation.events.sensor_faults.SensorFault`], optional
        List of sensor faults to be applied to the sensor readings.

        The default is an empty list.
    sensor_reading_attacks : list[:class:`~epyt_flow.simulation.events.sensor_reading_attack.SensorReadingAttack`], optional
        List of sensor reading attacks to be applied to the sensor readings.

        The default is an empty list.
    sensor_reading_events : list[`:class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent`], optional
        List of additional sensor reading events that are to be applied to the sensor readings.

        The default is an empty list.
    sensor_noise : :class:`~epyt_flow.uncertainty.sensor_noise.SensorNoise`, optional
        Specification of the sensor noise/uncertainty to be added to the sensor readings.

        The default is None.
    frozen_sensor_config : `bool`, optional
        If True, the sensor config can not be changed and only the required sensor nodes/links
        will be stored -- this usually leads to a significant reduction in memory consumption.

        The default is False.
    """
    def __init__(self, sensor_config: SensorConfig, sensor_readings_time: np.ndarray,
                 pressure_data_raw: np.ndarray = None, flow_data_raw: np.ndarray = None,
                 demand_data_raw: np.ndarray = None, node_quality_data_raw: np.ndarray = None,
                 link_quality_data_raw: np.ndarray = None, pumps_state_data_raw: np.ndarray = None,
                 valves_state_data_raw: np.ndarray = None, tanks_volume_data_raw: np.ndarray = None,
                 surface_species_concentration_raw: np.ndarray = None,
                 bulk_species_node_concentration_raw: np.ndarray = None,
                 bulk_species_link_concentration_raw: np.ndarray = None,
                 pump_energy_usage_data = None,
                 pump_efficiency_data = None,
                 pumps_energy_usage_data_raw: np.ndarray = None,
                 pumps_efficiency_data_raw: np.ndarray = None,
                 sensor_faults: list[SensorFault] = [],
                 sensor_reading_attacks: list[SensorReadingAttack] = [],
                 sensor_reading_events: list[SensorReadingEvent] = [],
                 sensor_noise: SensorNoise = None, frozen_sensor_config: bool = False,
                 **kwds):
        if not isinstance(sensor_config, SensorConfig):
            raise TypeError("'sensor_config' must be an instance of " +
                            "'epyt_flow.simulation.SensorConfig' but not of " +
                            f"'{type(sensor_config)}'")
        if not isinstance(sensor_readings_time, np.ndarray):
            raise TypeError("'sensor_readings_time' must be an instance of 'numpy.ndarray' " +
                            f"but not of '{type(sensor_readings_time)}'")
        if pressure_data_raw is not None:
            if not isinstance(pressure_data_raw, np.ndarray):
                raise TypeError("'pressure_data_raw' must be an instance of 'numpy.ndarray'" +
                                f" but not of '{type(pressure_data_raw)}'")
        if flow_data_raw is not None:
            if not isinstance(flow_data_raw, np.ndarray):
                raise TypeError("'flow_data_raw' must be an instance of 'numpy.ndarray' " +
                                f"but not of '{type(flow_data_raw)}'")
        if demand_data_raw is not None:
            if not isinstance(demand_data_raw, np.ndarray):
                raise TypeError("'demand_data_raw' must be an instance of 'numpy.ndarray' " +
                                f"but not of '{type(demand_data_raw)}'")
        if node_quality_data_raw is not None:
            if not isinstance(node_quality_data_raw, np.ndarray):
                raise TypeError("'node_quality_data_raw' must be an instance of 'numpy.ndarray'" +
                                f" but not of '{type(node_quality_data_raw)}'")
        if link_quality_data_raw is not None:
            if not isinstance(link_quality_data_raw, np.ndarray):
                raise TypeError("'link_quality_data_raw' must be an instance of 'numpy.ndarray'" +
                                f" but not of '{type(link_quality_data_raw)}'")
        if pumps_state_data_raw is not None:
            if not isinstance(pumps_state_data_raw, np.ndarray):
                raise TypeError("'pumps_state_data_raw' must be an instance of 'numpy.ndarray' " +
                                f"but no of '{type(pumps_state_data_raw)}'")
        if valves_state_data_raw is not None:
            if not isinstance(valves_state_data_raw, np.ndarray):
                raise TypeError("'valves_state_data_raw' must be an instance of 'numpy.ndarray' " +
                                f"but no of '{type(valves_state_data_raw)}'")
        if tanks_volume_data_raw is not None:
            if not isinstance(tanks_volume_data_raw, np.ndarray):
                raise TypeError("'tanks_volume_data_raw' must be an instance of 'numpy.ndarray'" +
                                f" but not of '{type(tanks_volume_data_raw)}'")
        if sensor_faults is None or not isinstance(sensor_faults, list):
            raise TypeError("'sensor_faults' must be a list of " +
                            "'epyt_flow.simulation.events.SensorFault' instances but " +
                            f"'{type(sensor_faults)}'")
        if surface_species_concentration_raw is not None:
            if not isinstance(surface_species_concentration_raw, np.ndarray):
                raise TypeError("'surface_species_concentration_raw' must be an instance of " +
                                "'numpy.ndarray' but not of " +
                                f"'{type(surface_species_concentration_raw)}'")
        if bulk_species_node_concentration_raw is not None:
            if not isinstance(bulk_species_node_concentration_raw, np.ndarray):
                raise TypeError("'bulk_species_node_concentration_raw' must be an instance of " +
                                "'numpy.ndarray' but not of " +
                                f"'{type(bulk_species_node_concentration_raw)}'")
        if bulk_species_link_concentration_raw is not None:
            if not isinstance(bulk_species_link_concentration_raw, np.ndarray):
                raise TypeError("'bulk_species_link_concentration_raw' must be an instance of " +
                                "'numpy.ndarray' but not of " +
                                f"'{type(bulk_species_link_concentration_raw)}'")
        if pumps_energy_usage_data_raw is not None:
            if not isinstance(pumps_energy_usage_data_raw, np.ndarray):
                raise TypeError("'pumps_energy_usage_data_raw' must be an instance of 'numpy.ndarray' " +
                                f"but not of '{type(pumps_energy_usage_data_raw)}'")
        if pumps_efficiency_data_raw is not None:
            if not isinstance(pumps_efficiency_data_raw, np.ndarray):
                raise TypeError("'pumps_efficiency_data_raw' must be an instance of 'numpy.ndarray' " +
                                f"but not of '{type(pumps_efficiency_data_raw)}'")
        if len(sensor_faults) != 0:
            if any(not isinstance(f, SensorFault) for f in sensor_faults):
                raise TypeError("'sensor_faults' must be a list of " +
                                "'epyt_flow.simulation.event.SensorFault' instances")
        if len(sensor_reading_attacks) != 0:
            if any(not isinstance(f, SensorReadingAttack) for f in sensor_reading_attacks):
                raise TypeError("'sensor_reading_attacks' must be a list of " +
                                "'epyt_flow.simulation.event.SensorReadingAttack' instances")
        if len(sensor_reading_events) != 0:
            if any(not isinstance(f, SensorReadingEvent) for f in sensor_reading_events):
                raise TypeError("'sensor_reading_events' must be a list of " +
                                "'epyt_flow.simulation.event.SensorReadingEvent' instances")
        if sensor_noise is not None and not isinstance(sensor_noise, SensorNoise):
            raise TypeError("'sensor_noise' must be an instance of " +
                            "'epyt_flow.uncertainty.SensorNoise' but not of " +
                            f"'{type(sensor_noise)}'")
        if not isinstance(frozen_sensor_config, bool):
            raise TypeError("'frozen_sensor_config' must be an instance of 'bool' " +
                            f"but not of '{type(frozen_sensor_config)}'")

        if pump_efficiency_data is not None or pump_energy_usage_data is not None:
            warnings.warn("Loading a file that was created with an outdated version of EPyT-Flow" +
                          " -- support of such old files will be removed in the next release!",
                          DeprecationWarning)

        def __raise_shape_mismatch(var_name: str) -> None:
            raise ValueError(f"Shape mismatch in '{var_name}' -- " +
                             "i.e number of time steps in 'sensor_readings_time' " +
                             "must match number of raw measurements.")

        n_time_steps = sensor_readings_time.shape[0]
        if pressure_data_raw is not None:
            if pressure_data_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("pressure_data_raw")
        if flow_data_raw is not None:
            if flow_data_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("flow_data_raw")
        if demand_data_raw is not None:
            if demand_data_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("demand_data_raw")
        if node_quality_data_raw is not None:
            if node_quality_data_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("node_quality_data_raw")
        if link_quality_data_raw is not None:
            if link_quality_data_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("link_quality_data_raw")
        if valves_state_data_raw is not None:
            if valves_state_data_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("valves_state_data_raw")
        if pumps_state_data_raw is not None:
            if pumps_state_data_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("pumps_state_data_raw")
        if tanks_volume_data_raw is not None:
            if tanks_volume_data_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("tanks_volume_data_raw")
        if valves_state_data_raw is not None:
            if not valves_state_data_raw.shape[0] == n_time_steps:
                __raise_shape_mismatch("valves_state_data_raw")
        if pumps_state_data_raw is not None:
            if not pumps_state_data_raw.shape[0] == n_time_steps:
                __raise_shape_mismatch("pumps_state_data_raw")
        if tanks_volume_data_raw is not None:
            if not tanks_volume_data_raw.shape[0] == n_time_steps:
                __raise_shape_mismatch("tanks_volume_data_raw")
        if bulk_species_node_concentration_raw is not None:
            if bulk_species_node_concentration_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("bulk_species_node_concentration_raw")
        if bulk_species_link_concentration_raw is not None:
            if bulk_species_link_concentration_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("bulk_species_link_concentration_raw")
        if surface_species_concentration_raw is not None:
            if surface_species_concentration_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("surface_species_concentration_raw")
        if pumps_energy_usage_data_raw is not None:
            if pumps_energy_usage_data_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("pumps_energy_usage_data_raw")
        if pumps_efficiency_data_raw is not None:
            if pumps_efficiency_data_raw.shape[0] != n_time_steps:
                __raise_shape_mismatch("pumps_efficiency_data_raw")

        self.__sensor_config = sensor_config
        self.__sensor_noise = sensor_noise
        self.__sensor_reading_events = sensor_faults + sensor_reading_attacks + \
            sensor_reading_events

        self.__sensor_readings = None
        self.__frozen_sensor_config = frozen_sensor_config
        self.__sensor_readings_time = sensor_readings_time

        if self.__frozen_sensor_config is False:
            self.__pressure_data_raw = pressure_data_raw
            self.__flow_data_raw = flow_data_raw
            self.__demand_data_raw = demand_data_raw
            self.__node_quality_data_raw = node_quality_data_raw
            self.__link_quality_data_raw = link_quality_data_raw
            self.__pumps_state_data_raw = pumps_state_data_raw
            self.__valves_state_data_raw = valves_state_data_raw
            self.__tanks_volume_data_raw = tanks_volume_data_raw
            self.__surface_species_concentration_raw = surface_species_concentration_raw
            self.__bulk_species_node_concentration_raw = bulk_species_node_concentration_raw
            self.__bulk_species_link_concentration_raw = bulk_species_link_concentration_raw
            self.__pumps_energy_usage_data_raw = pumps_energy_usage_data_raw
            self.__pumps_efficiency_data_raw = pumps_efficiency_data_raw
        else:
            sensor_config = self.__sensor_config

            node_to_idx = sensor_config.map_node_id_to_idx
            link_to_idx = sensor_config.map_link_id_to_idx
            pump_to_idx = sensor_config.map_pump_id_to_idx
            valve_to_idx = sensor_config.map_valve_id_to_idx
            tank_to_idx = sensor_config.map_tank_id_to_idx

            # EPANET quantities
            def __reduce_data(data: np.ndarray, sensors: list[str],
                              item_to_idx: Callable[[str], int]) -> np.ndarray:
                idx = [item_to_idx(item_id) for item_id in sensors]

                if data is None or len(idx) == 0:
                    return None
                else:
                    return data[:, idx]

            self.__pressure_data_raw = __reduce_data(data=pressure_data_raw,
                                                     item_to_idx=node_to_idx,
                                                     sensors=sensor_config.pressure_sensors)
            self.__flow_data_raw = __reduce_data(data=flow_data_raw,
                                                 item_to_idx=link_to_idx,
                                                 sensors=sensor_config.flow_sensors)
            self.__demand_data_raw = __reduce_data(data=demand_data_raw,
                                                   item_to_idx=node_to_idx,
                                                   sensors=sensor_config.demand_sensors)
            self.__node_quality_data_raw = __reduce_data(data=node_quality_data_raw,
                                                         item_to_idx=node_to_idx,
                                                         sensors=sensor_config.quality_node_sensors)
            self.__link_quality_data_raw = __reduce_data(data=link_quality_data_raw,
                                                         item_to_idx=link_to_idx,
                                                         sensors=sensor_config.quality_link_sensors)
            self.__pumps_state_data_raw = __reduce_data(data=pumps_state_data_raw,
                                                        item_to_idx=pump_to_idx,
                                                        sensors=sensor_config.pump_state_sensors)
            self.__pumps_energy_usage_data_raw = \
                __reduce_data(data=pumps_energy_usage_data_raw,
                              item_to_idx=pump_to_idx,
                              sensors=sensor_config.pump_energyconsumption_sensors)
            self.__pumps_efficiency_data_raw = \
                __reduce_data(data=pumps_efficiency_data_raw,
                              item_to_idx=pump_to_idx,
                              sensors=sensor_config.pump_efficiency_sensors)
            self.__valves_state_data_raw = __reduce_data(data=valves_state_data_raw,
                                                         item_to_idx=valve_to_idx,
                                                         sensors=sensor_config.valve_state_sensors)
            self.__tanks_volume_data_raw = __reduce_data(data=tanks_volume_data_raw,
                                                         item_to_idx=tank_to_idx,
                                                         sensors=sensor_config.tank_volume_sensors)

            # EPANET-MSX quantities
            def __reduce_msx_data(data: np.ndarray, sensors: list[tuple[list[int], list[int]]]
                                  ) -> np.ndarray:
                if data is None or len(sensors) == 0:
                    return None
                else:
                    r = []
                    for species_idx, item_idx in sensors:
                        r.append(data[:, species_idx, item_idx].reshape(-1, len(item_idx)))

                    return np.concatenate(r, axis=1)

            node_bulk_species_idx = [(sensor_config.map_bulkspecies_id_to_idx(s),
                                      [sensor_config.map_node_id_to_idx(node_id)
                                       for node_id in sensor_config.bulk_species_node_sensors[s]
                                       ]) for s in sensor_config.bulk_species_node_sensors.keys()]
            self.__bulk_species_node_concentration_raw = \
                __reduce_msx_data(data=bulk_species_node_concentration_raw,
                                  sensors=node_bulk_species_idx)

            bulk_species_link_idx = [(sensor_config.map_bulkspecies_id_to_idx(s),
                                      [sensor_config.map_link_id_to_idx(link_id)
                                       for link_id in sensor_config.bulk_species_link_sensors[s]
                                       ]) for s in sensor_config.bulk_species_link_sensors.keys()]
            self.__bulk_species_link_concentration_raw = \
                __reduce_msx_data(data=bulk_species_link_concentration_raw,
                                  sensors=bulk_species_link_idx)

            surface_species_idx = [(sensor_config.map_surfacespecies_id_to_idx(s),
                                    [sensor_config.map_link_id_to_idx(link_id)
                                     for link_id in sensor_config.surface_species_sensors[s]
                                     ]) for s in sensor_config.surface_species_sensors.keys()]
            self.__surface_species_concentration_raw = \
                __reduce_msx_data(data=surface_species_concentration_raw,
                                  sensors=surface_species_idx)

        self.__init()

        super().__init__(**kwds)

    def convert_units(self, flow_unit: int = None, quality_unit: int = None,
                      bulk_species_mass_unit: list[int] = None,
                      surface_species_mass_unit: list[int] = None,
                      surface_species_area_unit: int = None) -> Any:
        """
        Changes the units of some measurement units.

        .. note::

            Beaware of potential rounding errors.

        Parameters
        ----------
        flow_unit : `int`, optional
            New units of hydraulic measurements -- note that the flow unit specifies all other
            hydraulic measurement units.

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

            If None, units of hydraulic measurement are not changed.

            The default is None.
        quality_unit : `int`, optional
            New unit of quality measurements -- i.e. chemical concentration.
            Only relevant if basic quality analysis was performed.

            Must be one of the following constants:

                - MASS_UNIT_MG = 4     (mg/L)
                - MASS_UNIT_UG = 5     (ug/L)

            If None, units of quality measurements are not changed.

            The default is None.
        bulk_species_mass_unit : `list[int]`, optional
            New units of all bulk species measurements -- i.e. for each
            bulk species the measurement unit is specified.
            Note that the assumed ordering is the same as given in 'bulk_species'
            in the sensor configuration -- only relevant if EPANET-MSX is used.

            Must be one of the following constants:

                - MASS_UNIT_MG   = 4      (milligram)
                - MASS_UNIT_UG   = 5      (microgram)
                - MASS_UNIT_MOL  = 6      (mole)
                - MASS_UNIT_MMOL = 7      (millimole)

            If None, measurement units of bulk species are not changed.

            The default is None.
        surface_species_mass_unit : `list[int]`, optional
            New units of all surface species measurements -- i.e. for each
            surface species the measurement unit is specified.
            Note that the assumed ordering is the same as given in 'surface_species'
            in the sensor configuration -- only relevant if EPANET-MSX is used.

            Must be one of the following constants:

                - MASS_UNIT_MG   = 4      (milligram)
                - MASS_UNIT_UG   = 5      (microgram)
                - MASS_UNIT_MOL  = 6      (mole)
                - MASS_UNIT_MMOL = 7      (millimole)

            If None, measurement units of surface species are not changed.

            The default is None.
        surface_species_area_unit : `int`, optional
            New area unit of all surface species -- only relevant if EPANET-MSX is used.

            Must be one of the following constants:

                - AREA_UNIT_FT2 = 1     (square feet)
                - AREA_UNIT_M2  = 2     (square meters)
                - AREA_UNIT_CM2 = 3     (square centimeters)

            If None, are units of surface species are not changed.

            The default is None.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            SCADA data instance with the new units.
        """
        if flow_unit is not None:
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

        if bulk_species_mass_unit is not None:
            if not isinstance(bulk_species_mass_unit, list):
                raise TypeError("'bulk_species_mass_unit' must be an instance of 'list[int]' " +
                                f"but not of '{type(bulk_species_mass_unit)}'")            
            if len(bulk_species_mass_unit) != len(self.__sensor_config.bulk_species):
                raise ValueError("Inconsistency between 'bulk_species_mass_unit' and " +
                                 "'bulk_species'")
            if any(not isinstance(mass_unit, int) for mass_unit in bulk_species_mass_unit):
                raise TypeError("All items in 'bulk_species_mass_unit' must be an instance " +
                                "of 'int'")
            if any(mass_unit not in [MASS_UNIT_MG, MASS_UNIT_UG, MASS_UNIT_MOL, MASS_UNIT_MMOL]
                   for mass_unit in bulk_species_mass_unit):
                raise ValueError("Invalid mass unit in 'bulk_species_mass_unit'")

        if surface_species_mass_unit is not None:
            if not isinstance(surface_species_mass_unit, list):
                raise TypeError("'surface_species_mass_unit' must be an instance of 'list[int]' " +
                                f"but not of '{type(surface_species_mass_unit)}'")            
            if len(surface_species_mass_unit) != len(self.__sensor_config.surface_species):
                raise ValueError("Inconsistency between 'surface_species_mass_unit' and " +
                                 "'surface_species'")
            if any(not isinstance(mass_unit, int) for mass_unit in surface_species_mass_unit):
                raise TypeError("All items in 'surface_species_mass_unit' must be an instance " +
                                "of 'int'")
            if any(mass_unit not in [MASS_UNIT_MG, MASS_UNIT_UG, MASS_UNIT_MOL, MASS_UNIT_MMOL]
                   for mass_unit in surface_species_mass_unit):
                raise ValueError("Invalid mass unit in 'surface_species_mass_unit'")

        if surface_species_area_unit is not None:
            if surface_species_area_unit is not None:
                if not isinstance(surface_species_area_unit, int):
                    raise TypeError("'surface_species_area_unit' must be a an instance of 'int' " +
                                    f"but not of '{type(surface_species_area_unit)}'")
                if surface_species_area_unit not in [AREA_UNIT_FT2, AREA_UNIT_M2, AREA_UNIT_CM2]:
                    raise ValueError("Invalid area unit 'surface_species_area_unit'")

        def __get_mass_convert_factor(new_unit_id: int, old_unit_id: int) -> float:
            if new_unit_id == MASS_UNIT_MG and old_unit_id == MASS_UNIT_UG:
                return .001
            elif new_unit_id == MASS_UNIT_UG and old_unit_id == MASS_UNIT_MG:
                return 1000.
            elif new_unit_id == MASS_UNIT_MOL and old_unit_id == MASS_UNIT_MMOL:
                return .001
            elif new_unit_id == MASS_UNIT_MMOL and old_unit_id == MASS_UNIT_MOL:
                return 1000.
            else:
                raise NotImplementedError(f"Can not convert '{massunit_to_str(old_unit_id)}' to " +
                                          f"'{massunit_to_str(new_unit_id)}'")

        def __get_flow_convert_factor(new_unit_id: int, old_unit: int) -> float:
            if new_unit_id == ToolkitConstants.EN_CFS:
                if old_unit == ToolkitConstants.EN_GPM:
                    return .0022280093
                elif old_unit == ToolkitConstants.EN_MGD:
                    return 1.5472286523
                elif old_unit == ToolkitConstants.EN_IMGD:
                    return 1.8581441347
                elif old_unit == ToolkitConstants.EN_AFD:
                    return .5041666667
                elif old_unit == ToolkitConstants.EN_LPS:
                    return .0353146667
                elif old_unit == ToolkitConstants.EN_LPM:
                    return .0005885778
                elif old_unit == ToolkitConstants.EN_MLD:
                    return .40873456853575
                elif old_unit == ToolkitConstants.EN_CMH:
                    return .0098096296
                elif old_unit == ToolkitConstants.EN_CMD:
                    return .0004087346
            elif new_unit_id == ToolkitConstants.EN_GPM:
                if old_unit == ToolkitConstants.EN_CFS:
                    return 448.8325660485
                elif old_unit == ToolkitConstants.EN_MGD:
                    return 694.44444444
                elif old_unit == ToolkitConstants.EN_IMGD:
                    return 833.99300382
                elif old_unit == ToolkitConstants.EN_AFD:
                    return 226.28571429
                elif old_unit == ToolkitConstants.EN_LPS:
                    return 15.850323141
                elif old_unit == ToolkitConstants.EN_LPM:
                    return .2641720524
                elif old_unit == ToolkitConstants.EN_MLD:
                    return 183.4528141376
                elif old_unit == ToolkitConstants.EN_CMH:
                    return 4.4028675393
                elif old_unit == ToolkitConstants.EN_CMD:
                    return .1834528141
            elif new_unit_id == ToolkitConstants.EN_MGD:
                if old_unit == ToolkitConstants.EN_CFS:
                    return .6463168831
                elif old_unit == ToolkitConstants.EN_GPM:
                    return .00144
                elif old_unit == ToolkitConstants.EN_IMGD:
                    return 1.2009499255
                elif old_unit == ToolkitConstants.EN_AFD:
                    return 0.3258514286
                elif old_unit == ToolkitConstants.EN_LPS:
                    return .0228244653
                elif old_unit == ToolkitConstants.EN_LPM:
                    return .0003804078
                elif old_unit == ToolkitConstants.EN_MLD:
                    return .26417205124156
                elif old_unit == ToolkitConstants.EN_CMH:
                    return .0063401293
                elif old_unit == ToolkitConstants.EN_CMD:
                    return .0002641721
            elif new_unit_id == ToolkitConstants.EN_IMGD:
                if old_unit == ToolkitConstants.EN_CFS:
                    return .5381713837
                elif old_unit == ToolkitConstants.EN_MGD:
                    return .8326741846
                elif old_unit == ToolkitConstants.EN_GPM:
                    return .0011990508
                elif old_unit == ToolkitConstants.EN_AFD:
                    return .2713280726
                elif old_unit == ToolkitConstants.EN_LPS:
                    return .0190053431
                elif old_unit == ToolkitConstants.EN_LPM:
                    return .0003167557
                elif old_unit == ToolkitConstants.EN_MLD:
                    return .21996924829908776
                elif old_unit == ToolkitConstants.EN_CMH:
                    return .005279262
                elif old_unit == ToolkitConstants.EN_CMD:
                    return .0002199692
            elif new_unit_id == ToolkitConstants.EN_AFD:
                if old_unit == ToolkitConstants.EN_CFS:
                    return 1.9834710744
                elif old_unit == ToolkitConstants.EN_MGD:
                    return 3.0688832772
                elif old_unit == ToolkitConstants.EN_GPM:
                    return .0044191919
                elif old_unit == ToolkitConstants.EN_IMGD:
                    return 3.6855751432
                elif old_unit == ToolkitConstants.EN_LPS:
                    return .0700456199
                elif old_unit == ToolkitConstants.EN_LPM:
                    return .001167427
                elif old_unit == ToolkitConstants.EN_MLD:
                    return .81070995093708
                elif old_unit == ToolkitConstants.EN_CMH:
                    return .0194571167
                elif old_unit == ToolkitConstants.EN_CMD:
                    return .0008107132
            elif new_unit_id == ToolkitConstants.EN_LPS:
                if old_unit == ToolkitConstants.EN_CFS:
                    return 28.316846592
                elif old_unit == ToolkitConstants.EN_MGD:
                    return 43.812636389
                elif old_unit == ToolkitConstants.EN_IMGD:
                    return 52.616782407
                elif old_unit == ToolkitConstants.EN_GPM:
                    return .0630901964
                elif old_unit == ToolkitConstants.EN_AFD:
                    return 14.276410157
                elif old_unit == ToolkitConstants.EN_LPM:
                    return .0166666667
                elif old_unit == ToolkitConstants.EN_MLD:
                    return 11.574074074074
                elif old_unit == ToolkitConstants.EN_CMH:
                    return .2777777778
                elif old_unit == ToolkitConstants.EN_CMD:
                    return .0115740741
            elif new_unit_id == ToolkitConstants.EN_LPM:
                if old_unit == ToolkitConstants.EN_CFS:
                    return 1699.0107955
                elif old_unit == ToolkitConstants.EN_MGD:
                    return 2628.7581833
                elif old_unit == ToolkitConstants.EN_IMGD:
                    return 3157.0069444
                elif old_unit == ToolkitConstants.EN_AFD:
                    return 856.58460941
                elif old_unit == ToolkitConstants.EN_LPS:
                    return 60
                elif old_unit == ToolkitConstants.EN_GPM:
                    return 3.785411784
                elif old_unit == ToolkitConstants.EN_MLD:
                    return 694.44444444443
                elif old_unit == ToolkitConstants.EN_CMH:
                    return 16.666666667
                elif old_unit == ToolkitConstants.EN_CMD:
                    return 0.6944444444
            elif new_unit_id == ToolkitConstants.EN_MLD:
                if old_unit == ToolkitConstants.EN_CFS:
                    return 2.4465755456688
                elif old_unit == ToolkitConstants.EN_MGD:
                    return 3.7854117999999777
                elif old_unit == ToolkitConstants.EN_IMGD:
                    return 4.54609
                elif old_unit == ToolkitConstants.EN_AFD:
                    return 1.2334867714947
                elif old_unit == ToolkitConstants.EN_LPS:
                    return .0864
                elif old_unit == ToolkitConstants.EN_LPM:
                    return .00144
                elif old_unit == ToolkitConstants.EN_GPM:
                    return .00545099296896
                elif old_unit == ToolkitConstants.EN_CMH:
                    return .024
                elif old_unit == ToolkitConstants.EN_CMD:
                    return .00099999999999999
            elif new_unit_id == ToolkitConstants.EN_CMH:
                if old_unit == ToolkitConstants.EN_CFS:
                    return 101.94064773
                elif old_unit == ToolkitConstants.EN_MGD:
                    return 157.725491
                elif old_unit == ToolkitConstants.EN_IMGD:
                    return 189.42041667
                elif old_unit == ToolkitConstants.EN_AFD:
                    return 51.395076564
                elif old_unit == ToolkitConstants.EN_LPS:
                    return 3.6
                elif old_unit == ToolkitConstants.EN_LPM:
                    return .06
                elif old_unit == ToolkitConstants.EN_MLD:
                    return 41.666666666666
                elif old_unit == ToolkitConstants.EN_GPM:
                    return .227124707
                elif old_unit == ToolkitConstants.EN_CMD:
                    return 0.0416666667
            elif new_unit_id == ToolkitConstants.EN_CMD:
                if old_unit == ToolkitConstants.EN_CFS:
                    return 2446.5755455
                elif old_unit == ToolkitConstants.EN_MGD:
                    return 3785.411784
                elif old_unit == ToolkitConstants.EN_IMGD:
                    return 4546.09
                elif old_unit == ToolkitConstants.EN_AFD:
                    return 1233.4818375
                elif old_unit == ToolkitConstants.EN_LPS:
                    return 86.4
                elif old_unit == ToolkitConstants.EN_LPM:
                    return 1.44
                elif old_unit == ToolkitConstants.EN_MLD:
                    return 1000.
                elif old_unit == ToolkitConstants.EN_CMH:
                    return 24
                elif old_unit == ToolkitConstants.EN_GPM:
                    return 5.450992969

        # Convert units
        pressure_data = self.pressure_data_raw
        flow_data = self.flow_data_raw
        demand_data = self.demand_data_raw
        quality_node_data = self.node_quality_data_raw
        quality_link_data = self.link_quality_data_raw
        tanks_volume_data = self.tanks_volume_data_raw
        surface_species_concentrations = self.surface_species_concentration_raw
        bulk_species_node_concentrations = self.bulk_species_node_concentration_raw
        bulk_species_link_concentrations = self.bulk_species_link_concentration_raw

        if flow_unit is not None:
            old_flow_unit = self.__sensor_config.flow_unit
            if flow_unit == old_flow_unit:
                warnings.warn("'flow_unit' is identical to the current flow units " +
                              "-- nothing to do!", UserWarning)
            else:
                # Convert flows and demands
                convert_factor = __get_flow_convert_factor(flow_unit, old_flow_unit)

                flow_data *= convert_factor
                demand_data *= convert_factor

                if is_flowunit_simetric(flow_unit) != is_flowunit_simetric(old_flow_unit):
                    # Convert tank volume and pressure
                    convert_factor = None
                    convert_factor_pressure = None
                    if is_flowunit_simetric(flow_unit) is True and \
                            is_flowunit_simetric(old_flow_unit) is False:
                        convert_factor_volume = .0283168
                        convert_factor_pressure = .70325
                    else:
                        convert_factor_volume = 35.3147
                        convert_factor_pressure = 1.4219702084872

                    pressure_data *= convert_factor_pressure
                    tanks_volume_data *= convert_factor_volume

        if quality_unit is not None:
            old_quality_unit = self.__sensor_config.quality_unit()
            if quality_unit == old_quality_unit:
                warnings.warn("'quality_unit' are identical to the current quality units " +
                              "-- nothing to do!", UserWarning)
            else:
                # Convert chemical concentration and time (basic quality analysis)
                if quality_unit != TIME_UNIT_HRS:
                    convert_factor = __get_mass_convert_factor(quality_unit, old_quality_unit)

                    quality_node_data *= convert_factor
                    quality_link_data *= convert_factor

        if bulk_species_mass_unit is not None:
            # Convert bulk species concentrations
            if self.__frozen_sensor_config is True:
                for i, species_id, _ in enumerate(self.__sensor_config.bulk_species_node_sensors):
                    species_idx = self.__sensor_config.bulk_species.index(species_id)
                    new_mass_unit = bulk_species_mass_unit[species_idx]
                    old_mass_unit = self.__sensor_config.bulk_species_mass_unit[species_idx]

                    if new_mass_unit != old_mass_unit:
                        convert_factor = __get_mass_convert_factor(new_mass_unit, old_mass_unit)
                        bulk_species_node_concentrations[:, i, :] *= convert_factor

                for i, species_id, _ in enumerate(self.__sensor_config.bulk_species_link_sensors):
                    species_idx = self.__sensor_config.bulk_species.index(species_id)
                    new_mass_unit = bulk_species_mass_unit[species_idx]
                    old_mass_unit = self.__sensor_config.bulk_species_mass_unit[species_idx]

                    if new_mass_unit != old_mass_unit:
                        convert_factor = __get_mass_convert_factor(new_mass_unit, old_mass_unit)
                        bulk_species_link_concentrations[:, i, :] *= convert_factor
            else:
                for i in range(bulk_species_node_concentrations.shape[1]):
                    if bulk_species_mass_unit[i] != self.__sensor_config.bulk_species_mass_unit[i]:
                        old_mass_unit = self.__sensor_config.bulk_species_mass_unit[i]
                        convert_factor = __get_mass_convert_factor(bulk_species_mass_unit[i],
                                                                   old_mass_unit)

                        bulk_species_node_concentrations[:, i, :] *= convert_factor
                        bulk_species_link_concentrations[:, i, :] *= convert_factor

        if surface_species_mass_unit is not None:
            # Convert surface species concentrations
            if self.__frozen_sensor_config is True:
                for i, species_id, _ in enumerate(self.__sensor_config.surface_species_sensors):
                    species_idx = self.__sensor_config.surface_species.index(species_id)
                    new_mass_unit = surface_species_mass_unit[species_idx]
                    old_mass_unit = self.__sensor_config.surface_species_mass_unit[species_idx]

                    if new_mass_unit != old_mass_unit:
                        convert_factor = __get_mass_convert_factor(new_mass_unit, old_mass_unit)
                        surface_species_concentrations[:, i, :] *= convert_factor
            else:
                for i in range(surface_species_concentrations.shape[1]):
                    old_mass_unit = self.__sensor_config.surface_species_mass_unit[i]
                    if surface_species_mass_unit[i] != old_mass_unit:
                        convert_factor = __get_mass_convert_factor(surface_species_mass_unit[i],
                                                                   old_mass_unit)

                        surface_species_concentrations[:, i, :] *= convert_factor

        # Create new SCADA data instance
        new_flow_unit = self.__sensor_config.flow_unit
        if flow_unit is not None:
            new_flow_unit = flow_unit

        new_quality_unit = self.__sensor_config.quality_unit
        if quality_unit is not None:
            new_quality_unit = quality_unit

        new_bulk_species_mass_unit = self.__sensor_config.bulk_species_mass_unit
        if bulk_species_mass_unit is not None:
            new_bulk_species_mass_unit = bulk_species_mass_unit

        new_surface_species_mass_unit = self.__sensor_config.surface_species_mass_unit
        if surface_species_mass_unit is not None:
            new_surface_species_mass_unit = surface_species_mass_unit

        new_surface_species_area_unit = self.__sensor_config.surface_species_area_unit
        if surface_species_area_unit is not None:
            new_surface_species_mass_unit = surface_species_area_unit

        sensor_config = SensorConfig(nodes=self.__sensor_config.nodes,
                                     links=self.__sensor_config.links,
                                     valves=self.__sensor_config.valves,
                                     pumps=self.__sensor_config.pumps,
                                     tanks=self.__sensor_config.tanks,
                                     bulk_species=self.__sensor_config.bulk_species,
                                     surface_species=self.__sensor_config.surface_species,
                                     node_id_to_idx=self.__sensor_config.node_id_to_idx,
                                     link_id_to_idx=self.__sensor_config.link_id_to_idx,
                                     valve_id_to_idx=self.__sensor_config.valve_id_to_idx,
                                     pump_id_to_idx=self.__sensor_config.pump_id_to_idx,
                                     tank_id_to_idx=self.__sensor_config.tank_id_to_idx,
                                     bulkspecies_id_to_idx=self.__sensor_config.
                                        bulkspecies_id_to_idx,
                                     surfacespecies_id_to_idx=self.__sensor_config.
                                        surfacespecies_id_to_idx,
                                     flow_unit=new_flow_unit,
                                     pressure_sensors=self.__sensor_config.pressure_sensors,
                                     flow_sensors=self.__sensor_config.flow_sensors,
                                     demand_sensors=self.__sensor_config.demand_sensors,
                                     quality_node_sensors=self.__sensor_config.quality_node_sensors,
                                     quality_link_sensors=self.__sensor_config.quality_link_sensors,
                                     valve_state_sensors=self.__sensor_config.valve_state_sensors,
                                     pump_state_sensors=self.__sensor_config.pump_state_sensors,
                                     pump_efficiency_sensors=
                                     self.__sensor_config.pump_efficiency_sensors,
                                     pump_energyconsumption_sensors=
                                     self.__sensor_config.pump_energyconsumption_sensors,
                                     tank_volume_sensors=self.__sensor_config.tank_volume_sensors,
                                     bulk_species_node_sensors=
                                     self.__sensor_config.bulk_species_node_sensors,
                                     bulk_species_link_sensors=
                                     self.__sensor_config.bulk_species_link_sensors,
                                     surface_species_sensors=
                                     self.__sensor_config.surface_species_sensors,
                                     quality_unit=new_quality_unit,
                                     bulk_species_mass_unit=new_bulk_species_mass_unit,
                                     surface_species_mass_unit=new_surface_species_mass_unit,
                                     surface_species_area_unit=new_surface_species_area_unit)

        return ScadaData(sensor_config=sensor_config,
                         sensor_readings_time=self.sensor_readings_time,
                         sensor_reading_events=self.sensor_reading_events,
                         sensor_noise=self.sensor_noise,
                         frozen_sensor_config=self.frozen_sensor_config,
                         pressure_data_raw=pressure_data,
                         flow_data_raw=flow_data,
                         demand_data_raw=demand_data,
                         node_quality_data_raw=quality_node_data,
                         link_quality_data_raw=quality_link_data,
                         pumps_state_data_raw=self.pumps_state_data_raw,
                         valves_state_data_raw=self.valves_state_data_raw,
                         tanks_volume_data_raw=tanks_volume_data,
                         pumps_energy_usage_data_raw=self.pumps_energyconsumption_data_raw,
                         pumps_efficiency_data_raw=self.pumps_efficiency_data_raw,
                         bulk_species_node_concentration_raw=bulk_species_node_concentrations,
                         bulk_species_link_concentration_raw=bulk_species_link_concentrations,
                         surface_species_concentration_raw=surface_species_concentrations)

    @property
    def frozen_sensor_config(self) -> bool:
        """
        Checks if the sensor configuration is frozen or not.

        Returns
        -------
        `bool`
            True if the sensor configuration is frozen, False otherwise.
        """
        return self.__frozen_sensor_config

    @property
    def sensor_config(self) -> SensorConfig:
        """
        Gets the sensor configuration.

        Returns
        -------
        :class:`~epyt_flow.simulation.sensor_config.SensorConfig`
            Sensor configuration.
        """
        return deepcopy(self.__sensor_config)

    @sensor_config.setter
    def sensor_config(self, sensor_config: SensorConfig) -> None:
        if self.__frozen_sensor_config is True:
            raise RuntimeError("Sensor config can not be changed because it is frozen")

        self.change_sensor_config(sensor_config)

    @property
    def sensor_noise(self) -> SensorNoise:
        """
        Gets the sensor noise.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.sensor_noise.SensorNoise`
            Sensor noise.
        """
        return deepcopy(self.__sensor_noise)

    @sensor_noise.setter
    def sensor_noise(self, sensor_noise: SensorNoise) -> None:
        self.change_sensor_noise(sensor_noise)

    @property
    def sensor_faults(self) -> list[SensorFault]:
        """
        Gets all sensor faults.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.events.sensor_faults.SensorFault`]
            All sensor faults.
        """
        return deepcopy(list(filter(lambda e: isinstance(e, SensorFault),
                                    self.__sensor_reading_events)))

    @sensor_faults.setter
    def sensor_faults(self, sensor_faults: list[SensorFault]) -> None:
        self.change_sensor_faults(sensor_faults)

    @property
    def sensor_reading_attacks(self) -> list[SensorReadingAttack]:
        """
        Gets all sensor reading attacks.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.events.sensor_reading_attack.SensorReadingAttack`]
            All sensor reading attacks.
        """
        return deepcopy(list(filter(lambda e: isinstance(e, SensorReadingAttack),
                                    self.__sensor_reading_events)))

    @sensor_reading_attacks.setter
    def sensor_reading_attacks(self, sensor_reading_attacks: list[SensorReadingAttack]) -> None:
        self.change_sensor_reading_attacks(sensor_reading_attacks)

    @property
    def sensor_reading_events(self) -> list[SensorReadingEvent]:
        """
        Gets all sensor reading events.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent`]
            All sensor faults.
        """
        return deepcopy(self.__sensor_reading_events)

    @sensor_reading_events.setter
    def sensor_reading_events(self, sensor_reading_events: list[SensorReadingEvent]) -> None:
        self.change_sensor_reading_events(sensor_reading_events)

    @property
    def pressure_data_raw(self) -> np.ndarray:
        """
        Gets the raw pressure readings.

        Returns
        -------
        `numpy.ndarray`
            Raw pressure readings.
        """
        return deepcopy(self.__pressure_data_raw)

    @property
    def flow_data_raw(self) -> np.ndarray:
        """
        Gets the raw flow readings.

        Returns
        -------
        `numpy.ndarray`
            Raw flow readings.
        """
        return deepcopy(self.__flow_data_raw)

    @property
    def demand_data_raw(self) -> np.ndarray:
        """
        Gets the raw demand readings.

        Returns
        -------
        `numpy.ndarray`
            Raw demand readings.
        """
        return deepcopy(self.__demand_data_raw)

    @property
    def node_quality_data_raw(self) -> np.ndarray:
        """
        Gets the raw node quality readings.

        Returns
        -------
        `numpy.ndarray`
            Raw node quality readings.
        """
        return deepcopy(self.__node_quality_data_raw)

    @property
    def link_quality_data_raw(self) -> np.ndarray:
        """
        Gets the raw link quality readings.

        Returns
        -------
        `numpy.ndarray`
            Raw link quality readings.
        """
        return deepcopy(self.__link_quality_data_raw)

    @property
    def sensor_readings_time(self) -> np.ndarray:
        """
        Gets the sensor readings time stamps.

        Returns
        -------
        `numpy.ndarray`
            Sensor readings time stamps.
        """
        return deepcopy(self.__sensor_readings_time)

    @property
    def pumps_state_data_raw(self) -> np.ndarray:
        """
        Gets the raw pump state readings.

        Returns
        -------
        `numpy.ndarray`
            Raw pump state readings.
        """
        return deepcopy(self.__pumps_state_data_raw)

    @property
    def valves_state_data_raw(self) -> np.ndarray:
        """
        Gets the raw valve state readings.

        Returns
        -------
        `numpy.ndarray`
            Raw valve state readings.
        """
        return deepcopy(self.__valves_state_data_raw)

    @property
    def tanks_volume_data_raw(self) -> np.ndarray:
        """
        Gets the raw tank volume readings.

        Returns
        -------
        `numpy.ndarray`
            Raw tank volume readings.
        """
        return deepcopy(self.__tanks_volume_data_raw)

    @property
    def surface_species_concentration_raw(self) -> np.ndarray:
        """
        Gets the raw surface species concentrations at links/pipes.

        Returns
        -------
        `numpy.ndarray`
            Raw species concentrations.
        """
        return deepcopy(self.__surface_species_concentration_raw)

    @property
    def bulk_species_node_concentration_raw(self) -> np.ndarray:
        """
        Gets the raw bulk species concentrations at nodes.

        Returns
        -------
        `numpy.ndarray`
            Raw species concentrations.
        """
        return deepcopy(self.__bulk_species_node_concentration_raw)

    @property
    def bulk_species_link_concentration_raw(self) -> np.ndarray:
        """
        Gets the raw bulk species concentrations at links/pipes.

        Returns
        -------
        `numpy.ndarray`
            Raw species concentrations.
        """
        return deepcopy(self.__bulk_species_link_concentration_raw)

    @property
    def pumps_energyconsumption_data_raw(self) -> np.ndarray:
        """
        Gets the raw energy consumption of each pump.

        Returns
        -------
        `numpy.ndarray`
            Energy consumption of each pump.
        """
        return deepcopy(self.__pumps_energy_usage_data_raw)

    @property
    def pumps_efficiency_data_raw(self) -> np.ndarray:
        """
        Gets the raw efficiency of each pump.

        Returns
        -------
        `numpy.ndarray`
            Pumps' efficiency.
        """
        return deepcopy(self.__pumps_efficiency_data_raw)

    def __init(self):
        self.__apply_sensor_noise = lambda x: x
        if self.__sensor_noise is not None:
            self.__apply_sensor_noise = self.__sensor_noise.apply

        self.__apply_sensor_reading_events = []
        for sensor_event in self.__sensor_reading_events:
            idx = None
            if sensor_event.sensor_type == SENSOR_TYPE_NODE_PRESSURE:
                idx = self.__sensor_config.get_index_of_reading(
                    pressure_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_NODE_QUALITY:
                idx = self.__sensor_config.get_index_of_reading(
                    node_quality_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_NODE_DEMAND:
                idx = self.__sensor_config.get_index_of_reading(
                    demand_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_LINK_FLOW:
                idx = self.__sensor_config.get_index_of_reading(
                    flow_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_LINK_QUALITY:
                idx = self.__sensor_config.get_index_of_reading(
                    link_quality_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_VALVE_STATE:
                idx = self.__sensor_config.get_index_of_reading(
                    valve_state_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_PUMP_STATE:
                idx = self.__sensor_config.get_index_of_reading(
                    pump_state_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_PUMP_EFFICIENCY:
                idx = self.__sensor_config.get_index_of_reading(
                    pump_efficiency_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_PUMP_ENERGYCONSUMPTION:
                idx = self.__sensor_config.get_index_of_reading(
                    pump_energyconsumption_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_TANK_VOLUME:
                idx = self.__sensor_config.get_index_of_reading(
                    tank_volume_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_NODE_BULK_SPECIES:
                idx = self.__sensor_config.get_index_of_reading(
                    bulk_species_node_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_LINK_BULK_SPECIES:
                idx = self.__sensor_config.get_index_of_reading(
                    bulk_species_link_sensor=sensor_event.sensor_id)
            elif sensor_event.sensor_type == SENSOR_TYPE_SURFACE_SPECIES:
                idx = self.__sensor_config.get_index_of_reading(
                    surface_species_sensor=sensor_event.sensor_id)

            self.__apply_sensor_reading_events.append((idx, sensor_event.apply))

        self.__sensor_readings = None

    def get_attributes(self) -> dict:
        attr = {"sensor_config": self.__sensor_config,
                "frozen_sensor_config": self.__frozen_sensor_config,
                "sensor_noise": self.__sensor_noise,
                "sensor_reading_events": self.__sensor_reading_events,
                "pressure_data_raw": self.__pressure_data_raw,
                "flow_data_raw": self.__flow_data_raw,
                "demand_data_raw": self.__demand_data_raw,
                "node_quality_data_raw": self.__node_quality_data_raw,
                "link_quality_data_raw": self.__link_quality_data_raw,
                "sensor_readings_time": self.__sensor_readings_time,
                "pumps_state_data_raw": self.__pumps_state_data_raw,
                "valves_state_data_raw": self.__valves_state_data_raw,
                "tanks_volume_data_raw": self.__tanks_volume_data_raw,
                "surface_species_concentration_raw": self.__surface_species_concentration_raw,
                "bulk_species_node_concentration_raw": self.__bulk_species_node_concentration_raw,
                "bulk_species_link_concentration_raw": self.__bulk_species_link_concentration_raw,
                "pumps_energy_usage_data_raw": self.__pumps_energy_usage_data_raw,
                "pumps_efficiency_data_raw": self.__pumps_efficiency_data_raw}

        return super().get_attributes() | attr

    def __eq__(self, other) -> bool:
        if not isinstance(other, ScadaData):
            raise TypeError(f"Can not compare 'ScadaData' instance to '{type(other)}' instance")

        try:
            return self.__sensor_config == other.sensor_config \
                and self.__frozen_sensor_config == other.frozen_sensor_config \
                and self.__sensor_noise == other.sensor_noise \
                and all(a == b for a, b in
                        zip(self.__sensor_reading_events, other.sensor_reading_events)) \
                and np.all(self.__pressure_data_raw == other.pressure_data_raw) \
                and np.all(self.__flow_data_raw == other.flow_data_raw) \
                and np.all(self.__demand_data_raw == self.demand_data_raw) \
                and np.all(self.__node_quality_data_raw == other.node_quality_data_raw) \
                and np.all(self.__link_quality_data_raw == other.link_quality_data_raw) \
                and np.all(self.__sensor_readings_time == other.sensor_readings_time) \
                and np.all(self.__pumps_state_data_raw == other.pumps_state_data_raw) \
                and np.all(self.__valves_state_data_raw == other.valves_state_data_raw) \
                and np.all(self.__tanks_volume_data_raw == other.tanks_volume_data_raw) \
                and np.all(self.__surface_species_concentration_raw ==
                           other.surface_species_concentration_raw) \
                and np.all(self.__bulk_species_node_concentration_raw ==
                           other.bulk_species_node_concentration_raw) \
                and np.all(self.__bulk_species_link_concentration_raw ==
                           other.bulk_species_link_concentration_raw) \
                and np.all(self.__pumps_energy_usage_data_raw ==
                           other.pumps_energyconsumption_data_raw) \
                and np.all(self.__pumps_efficiency_data_raw == other.pumps_efficiency_data_raw)
        except Exception as ex:
            warnings.warn(ex.__str__())
            return False

    def __str__(self) -> str:
        return f"sensor_config: {self.__sensor_config} " + \
            f"frozen_sensor_config: {self.__frozen_sensor_config} " + \
            f"sensor_noise: {self.__sensor_noise} " + \
            f"sensor_reading_events: {self.__sensor_reading_events} " + \
            f"pressure_data_raw: {self.__pressure_data_raw} " + \
            f"flow_data_raw: {self.__flow_data_raw} demand_data_raw: {self.__demand_data_raw} " + \
            f"node_quality_data_raw: {self.__node_quality_data_raw} " + \
            f"link_quality_data_raw: {self.__link_quality_data_raw} " + \
            f"sensor_readings_time: {self.__sensor_readings_time} " + \
            f"pumps_state_data_raw: {self.__pumps_state_data_raw} " + \
            f"valves_state_data_raw: {self.__valves_state_data_raw} " + \
            f"tanks_volume_data_raw: {self.__tanks_volume_data_raw} " + \
            f"surface_species_concentration_raw: {self.__surface_species_concentration_raw} " + \
            f"bulk_species_node_concentration_raw: {self.__bulk_species_node_concentration_raw}" +\
            f" bulk_species_link_concentration_raw: {self.__bulk_species_link_concentration_raw}" +\
            f" pumps_efficiency_data_raw: {self.__pumps_efficiency_data_raw} " + \
            f"pumps_energy_usage_data_raw: {self.__pumps_energy_usage_data_raw}"

    def change_sensor_config(self, sensor_config: SensorConfig) -> None:
        """
        Changes the sensor configuration.

        Parameters
        ----------
        sensor_config : :class:`~epyt_flow.simulation.sensor_config.SensorConfig`
            New sensor configuration.
        """
        if self.__frozen_sensor_config is True:
            raise RuntimeError("Sensor configuration can not be changed because it is frozen")
        if not isinstance(sensor_config, SensorConfig):
            raise TypeError("'sensor_config' must be an instance of " +
                            "'epyt_flow.simulation.SensorConfig' but not of " +
                            f"'{type(sensor_config)}'")

        self.__sensor_config = sensor_config
        self.__init()

    def change_sensor_noise(self, sensor_noise: SensorNoise) -> None:
        """
        Changes the sensor noise/uncertainty.

        Parameters
        ----------
        sensor_noise : :class:`~epyt_flow.uncertainty.sensor_noise.SensorNoise`
            New sensor noise/uncertainty specification.
        """
        if not isinstance(sensor_noise, SensorNoise):
            raise TypeError("'sensor_noise' must be an instance of " +
                            "'epyt_flow.uncertainty.SensorNoise' but not of " +
                            f"'{type(sensor_noise)}'")

        self.__sensor_noise = sensor_noise
        self.__init()

    def change_sensor_faults(self, sensor_faults: list[SensorFault]) -> None:
        """
        Changes the sensor faults -- overrides all previous sensor faults!

        sensor_faults : list[:class:`~epyt_flow.simulation.events.sensor_faults.SensorFault`]
            List of new sensor faults.
        """
        if len(sensor_faults) != 0:
            if any(not isinstance(e, SensorFault) for e in sensor_faults):
                raise TypeError("'sensor_faults' must be a list of " +
                                "'epyt_flow.simulation.events.SensorFault' instances")

        self.__sensor_reading_events = list(filter(lambda e: not isinstance(e, SensorFault),
                                                   self.__sensor_reading_events))
        self.__sensor_reading_events += sensor_faults
        self.__init()

    def change_sensor_reading_attacks(self,
                                      sensor_reading_attacks: list[SensorReadingAttack]) -> None:
        """
        Changes the sensor reading attacks -- overrides all previous sensor reading attacks!

        sensor_reading_attacks : list[:class:`~epyt_flow.simulation.events.sensor_reading_attack.SensorReadingAttack`]
            List of new sensor reading attacks.
        """
        if len(sensor_reading_attacks) != 0:
            if any(not isinstance(e, SensorReadingAttack) for e in sensor_reading_attacks):
                raise TypeError("'sensor_reading_attacks' must be a list of " +
                                "'epyt_flow.simulation.events.SensorReadingAttack' instances")

        self.__sensor_reading_events = list(filter(lambda e: not isinstance(e, SensorReadingAttack),
                                                   self.__sensor_reading_events))
        self.__sensor_reading_events += sensor_reading_attacks
        self.__init()

    def change_sensor_reading_events(self, sensor_reading_events: list[SensorReadingEvent]) -> None:
        """
        Changes the sensor reading events -- overrides all previous sensor reading events
        (incl. sensor faults)!

        sensor_reading_events : list[:class:`~epyt_flow.simulation.events.sensor_reading_event.SensorReadingEvent`]
            List of new sensor reading events.
        """
        if len(sensor_reading_events) != 0:
            if any(not isinstance(e, SensorReadingEvent) for e in sensor_reading_events):
                raise TypeError("'sensor_reading_events' must be a list of " +
                                "'epyt_flow.simulation.events.SensorReadingEvent' instances")

        self.__sensor_reading_events = sensor_reading_events
        self.__init()

    def join(self, other) -> None:
        """
        Joins two :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances based
        on the sensor reading times. Consequently, **both instances must be equal in their
        sensor reading times**.
        Attributes (i.e. types of sensor readings) that are NOT present in THIS instance
        but in `others` will be added to this instance -- all other attributes are ignored.
        The sensor configuration is updated according to the sensor readings in `other`.

        Parameters
        ----------
        other : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Other scada data to be concatenated to this data.
        """
        if not isinstance(other, ScadaData):
            raise TypeError("'other' must be an instance of 'ScadaData' " +
                            f"but not of '{type(other)}'")
        if self.__frozen_sensor_config != other.frozen_sensor_config:
            raise ValueError("Sensor configurations of both instances must be " +
                             "either frozen or not frozen")
        if not np.all(self.__sensor_readings_time == other.sensor_readings_time):
            raise ValueError("Both 'ScadaData' instances must be equal in their " +
                             "sensor readings times")
        if any(e1 != e2 for e1, e2 in zip(self.__sensor_reading_events,
                                          other.sensor_reading_events)):
            raise ValueError("'other' must have the same sensor reading events as this instance!")
        if self.__sensor_config.nodes != other.sensor_config.nodes:
            raise ValueError("Inconsistency in nodes found")
        if self.__sensor_config.links != other.sensor_config.links:
            raise ValueError("Inconsistency in links/pipes found")
        if self.__sensor_config.valves != other.sensor_config.valves:
            raise ValueError("Inconsistency in valves found")
        if self.__sensor_config.pumps != other.sensor_config.pumps:
            raise ValueError("Inconsistency in pumps found")
        if self.__sensor_config.tanks != other.sensor_config.tanks:
            raise ValueError("Inconsistency in tanks found")
        if self.__sensor_config.bulk_species != other.sensor_config.bulk_species:
            raise ValueError("Inconsistency in bulk species found")
        if self.__sensor_config.surface_species != other.sensor_config.surface_species:
            raise ValueError("Inconsistency in surface species found")

        self.__sensor_readings = None

        if self.__pressure_data_raw is None and other.pressure_data_raw is not None:
            self.__pressure_data_raw = other.pressure_data_raw
            self.__sensor_config.pressure_sensors = other.sensor_config.pressure_sensors

        if self.__flow_data_raw is None and other.flow_data_raw is not None:
            self.__flow_data_raw = other.flow_data_raw
            self.__sensor_config.flow_sensors = other.sensor_config.flow_sensors

        if self.__demand_data_raw is None and other.demand_data_raw is not None:
            self.__demand_data_raw = other.demand_data_raw
            self.__sensor_config.demand_sensors = other.sensor_config.demand_sensors

        if self.__node_quality_data_raw is None and other.node_quality_data_raw is not None:
            self.__node_quality_data_raw = other.node_quality_data_raw
            self.__sensor_config.quality_node_sensors = other.sensor_config.quality_node_sensors

        if self.__link_quality_data_raw is None and other.link_quality_data_raw is not None:
            self.__link_quality_data_raw = other.link_quality_data_raw
            self.__sensor_config.quality_node_sensors = other.sensor_config.quality_node_sensors

        if self.__valves_state_data_raw is None and other.valves_state_data_raw is not None:
            self.__valves_state_data_raw = other.valves_state_data_raw
            self.__sensor_config.valve_state_sensors = other.sensor_config.valve_state_sensors

        if self.__pumps_state_data_raw is None and other.pumps_state_data_raw is not None:
            self.__pumps_state_data_raw = other.pumps_state_data_raw
            self.__sensor_config.pump_state_sensors = other.sensor_config.pump_state_sensors

        if self.__tanks_volume_data_raw is None and other.tanks_volume_data_raw is not None:
            self.__tanks_volume_data_raw = other.tanks_volume_data_raw
            self.__sensor_config.tank_volume_sensors = other.sensor_config.tank_volume_sensors

        if self.__bulk_species_node_concentration_raw is None and \
                other.bulk_species_node_concentration_raw is not None:
            self.__bulk_species_node_concentration_raw = other.bulk_species_node_concentration_raw
            self.__sensor_config.bulk_species_node_sensors = \
                other.sensor_config.bulk_species_node_sensors

        if self.__bulk_species_link_concentration_raw is None and \
                other.bulk_species_link_concentration_raw is not None:
            self.__bulk_species_link_concentration_raw = other.bulk_species_link_concentration_raw
            self.__sensor_config.bulk_species_link_sensors = \
                other.sensor_config.bulk_species_link_sensors

        if self.__surface_species_concentration_raw is None and \
                other.surface_species_concentration_raw is not None:
            self.__surface_species_concentration_raw = other.surface_species_concentration_raw
            self.__sensor_config.surface_species_sensors = \
                other.sensor_config.surface_species_sensors

        if self.__pumps_energy_usage_data_raw is None and \
                other.pumps_energyconsumption_data_raw is not None:
            self.__pumps_energy_usage_data_raw = other.pumps_energyconsumption_data_raw

        if self.__pumps_efficiency_data_raw is None and \
                other.pumps_efficiency_data_raw is not None:
            self.__pumps_efficiency_data_raw = other.pumps_efficiency_data_raw

        self.__init()

    def concatenate(self, other) -> None:
        """
        Concatenates two :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances
        -- i.e. add SCADA data from another given
        :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instance to this one.

        Note that the two :class:`~epyt_flow.simulation.scada.scada_data.ScadaData` instances
        must be the same in all other attributs (e.g. sensor configuration, etc.).

        Parameters
        ----------
        other : :class:`~epyt_flow.simulation.scada.scada_data.ScadaData`
            Other scada data to be concatenated to this data.
        """
        if not isinstance(other, ScadaData):
            raise TypeError(f"'other' must be an instance of 'ScadaData' but not of {type(other)}")
        if self.__sensor_config != other.sensor_config:
            raise ValueError("Sensor configurations must be the same!")
        if self.__frozen_sensor_config != other.frozen_sensor_config:
            raise ValueError("Sensor configurations of both instances must be " +
                             "either frozen or not frozen")
        if len(self.__sensor_reading_events) != len(other.sensor_reading_events):
            raise ValueError("'other' must have the same sensor reading events as this instance!")
        if any(e1 != e2 for e1, e2 in zip(self.__sensor_reading_events,
                                          other.sensor_reading_events)):
            raise ValueError("'other' must have the same sensor reading events as this instance!")

        self.__sensor_readings = None

        self.__sensor_readings_time = np.concatenate(
            (self.__sensor_readings_time, other.sensor_readings_time), axis=0)

        if self.__pressure_data_raw is not None:
            self.__pressure_data_raw = np.concatenate(
                (self.__pressure_data_raw, other.pressure_data_raw), axis=0)

        if self.__flow_data_raw is not None:
            self.__flow_data_raw = np.concatenate(
                (self.__flow_data_raw, other.flow_data_raw), axis=0)

        if self.__demand_data_raw is not None:
            self.__demand_data_raw = np.concatenate(
                (self.__demand_data_raw, other.demand_data_raw), axis=0)

        if self.__node_quality_data_raw is not None:
            self.__node_quality_data_raw = np.concatenate(
                (self.__node_quality_data_raw, other.node_quality_data_raw), axis=0)

        if self.__link_quality_data_raw is not None:
            self.__link_quality_data_raw = np.concatenate(
                (self.__link_quality_data_raw, other.link_quality_data_raw), axis=0)

        if self.__pumps_state_data_raw is not None:
            self.__pumps_state_data_raw = np.concatenate(
                (self.__pumps_state_data_raw, other.pumps_state_data_raw), axis=0)

        if self.__valves_state_data_raw is not None:
            self.__valves_state_data_raw = np.concatenate(
                (self.__valves_state_data_raw, other.valves_state_data_raw), axis=0)

        if self.__tanks_volume_data_raw is not None:
            self.__tanks_volume_data_raw = np.concatenate(
                (self.__tanks_volume_data_raw, other.tanks_volume_data_raw), axis=0)

        if self.__surface_species_concentration_raw is not None:
            self.__surface_species_concentration_raw = np.concatenate(
                (self.__surface_species_concentration_raw,
                 other.surface_species_concentration_raw),
                axis=0)

        if self.__bulk_species_node_concentration_raw is not None:
            self.__bulk_species_node_concentration_raw = np.concatenate(
                (self.__bulk_species_node_concentration_raw,
                 other.bulk_species_node_concentration_raw),
                axis=0)

        if self.__bulk_species_link_concentration_raw is not None:
            self.__bulk_species_link_concentration_raw = np.concatenate(
                (self.__bulk_species_link_concentration_raw,
                 other.bulk_species_link_concentration_raw),
                axis=0)

        if self.__pumps_energy_usage_data_raw is not None:
            self.__pumps_energy_usage_data_raw = np.concatenate(
                (self.__pumps_energy_usage_data_raw, other.pumps_energy_usage_data_raw),
                axis=0)

        if self.__pumps_efficiency_data_raw is not None:
            self.__pumps_efficiency_data_raw = np.concatenate(
                (self.__pumps_efficiency_data_raw, other.pumps_efficiency_data_raw),
                axis=0)

    def get_data(self) -> np.ndarray:
        """
        Computes the final sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Returns
        -------
        `numpy.ndarray`
            Final sensor readings.
        """
        # Comute clean sensor readings
        if self.__frozen_sensor_config is False:
            args = {"pressures": self.__pressure_data_raw,
                    "flows": self.__flow_data_raw,
                    "demands": self.__demand_data_raw,
                    "nodes_quality": self.__node_quality_data_raw,
                    "links_quality": self.__link_quality_data_raw,
                    "pumps_state": self.__pumps_state_data_raw,
                    "pumps_efficiency": self.__pumps_efficiency_data_raw,
                    "pumps_energyconsumption": self.__pumps_energy_usage_data_raw,
                    "valves_state": self.__valves_state_data_raw,
                    "tanks_volume": self.__tanks_volume_data_raw,
                    "bulk_species_node_concentrations": self.__bulk_species_node_concentration_raw,
                    "bulk_species_link_concentrations": self.__bulk_species_link_concentration_raw,
                    "surface_species_concentrations": self.__surface_species_concentration_raw}
            sensor_readings = self.__sensor_config.compute_readings(**args)
        else:
            data = []

            if self.__pressure_data_raw is not None:
                data.append(self.__pressure_data_raw)
            if self.__flow_data_raw is not None:
                data.append(self.__flow_data_raw)
            if self.__demand_data_raw is not None:
                data.append(self.__demand_data_raw)
            if self.__node_quality_data_raw is not None:
                data.append(self.__node_quality_data_raw)
            if self.__link_quality_data_raw is not None:
                data.append(self.__link_quality_data_raw)
            if self.__valves_state_data_raw is not None:
                data.append(self.__valves_state_data_raw)
            if self.__pumps_state_data_raw is not None:
                data.append(self.__pumps_state_data_raw)
            if self.__pumps_efficiency_data_raw is not None:
                data.append(self.__pumps_efficiency_data_raw)
            if self.__pumps_energy_usage_data_raw is not None:
                data.append(self.__pumps_energy_usage_data_raw)
            if self.__tanks_volume_data_raw is not None:
                data.append(self.__tanks_volume_data_raw)
            if self.__surface_species_concentration_raw is not None:
                data.append(self.__surface_species_concentration_raw)
            if self.__bulk_species_node_concentration_raw is not None:
                data.append(self.__bulk_species_node_concentration_raw)
            if self.__bulk_species_link_concentration_raw is not None:
                data.append(self.__bulk_species_link_concentration_raw)

            sensor_readings = np.concatenate(data, axis=1)

        # Apply sensor uncertainties
        state_sensors_idx = []   # Pump states and valve states are NOT affected!
        for link_id in self.sensor_config.pump_state_sensors:
            state_sensors_idx.append(
                self.__sensor_config.get_index_of_reading(pump_state_sensor=link_id))
        for link_id in self.sensor_config.valve_state_sensors:
            state_sensors_idx.append(
                self.__sensor_config.get_index_of_reading(valve_state_sensor=link_id))

        mask = np.ones(sensor_readings.shape[1], dtype=bool)
        mask[state_sensors_idx] = False

        sensor_readings[:, mask] = self.__apply_sensor_noise(sensor_readings[:, mask])

        # Apply sensor faults
        for idx, f in self.__apply_sensor_reading_events:
            sensor_readings[:, idx] = f(sensor_readings[:, idx], self.__sensor_readings_time)

        self.__sensor_readings = deepcopy(sensor_readings)

        return sensor_readings

    def __get_x_axis_label(self) -> str:
        if len(self.__sensor_readings_time) > 1:
            time_step = self.__sensor_readings_time[1] - self.__sensor_readings_time[0]
            if time_step > 60:
                time_steps_desc = f"{int(time_step / 60)}min"
                if time_step > 60*60:
                    time_steps_desc = f"{int(time_step / 60)}hr"
            else:
                time_steps_desc = f"{time_step}s"
            return f"Time ({time_steps_desc} steps)"
        else:
            return "Time"

    def get_data_pressures(self, sensor_locations: list[str] = None) -> np.ndarray:
        """
        Gets the final pressure sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing pressure sensor locations for which the sensor readings are requested.
            If None, the readings from all pressure sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Pressure sensor readings.
        """
        if self.__sensor_config.pressure_sensors == []:
            raise ValueError("No pressure sensors set")
        if sensor_locations is not None:
            if not isinstance(sensor_locations, list):
                raise TypeError("'sensor_locations' must be an instance of 'list[str]' " +
                                f"but not of '{type(sensor_locations)}'")
            if any(s_id not in self.__sensor_config.pressure_sensors for s_id in sensor_locations):
                raise ValueError("Invalid sensor ID in 'sensor_locations' -- note that all " +
                                 "sensors in 'sensor_locations' must be set in the current " +
                                 "pressure sensor configuration")
        else:
            sensor_locations = self.__sensor_config.pressure_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(pressure_sensor=s_id)
               for s_id in sensor_locations]
        return self.__sensor_readings[:, idx]

    def plot_pressures(self, sensor_locations: list[str] = None, show: bool = True,
                       save_to_file: str = None, ax: matplotlib.axes.Axes = None
                       ) -> matplotlib.axes.Axes:
        """
        Plots the final pressure sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing pressure sensor locations for which the sensor readings have to be plotted.
            If None, the readings from all pressure sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_pressures(sensor_locations)
        pressure_sensors = sensor_locations if sensor_locations is not None else \
            self.__sensor_config.pressure_sensors

        pressure_unit = "m" if is_flowunit_simetric(self.__sensor_config.flow_unit) else "psi"
        y_axis_label = f"Pressure in ${pressure_unit}$"

        return plot_timeseries_data(data.T, labels=[f"Node {n_id}" for n_id in pressure_sensors],
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label=y_axis_label,
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_flows(self, sensor_locations: list[str] = None) -> np.ndarray:
        """
        Gets the final flow sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing flow sensor locations for which the sensor readings are requested.
            If None, the readings from all flow sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Flow sensor readings.
        """
        if self.__sensor_config.flow_sensors == []:
            raise ValueError("No flow sensors set")
        if sensor_locations is not None:
            if not isinstance(sensor_locations, list):
                raise TypeError("'sensor_locations' must be an instance of 'list[str]' " +
                                f"but not of '{type(sensor_locations)}'")
            if any(s_id not in self.__sensor_config.flow_sensors for s_id in sensor_locations):
                raise ValueError("Invalid sensor ID in 'sensor_locations' -- note that all " +
                                 "sensors in 'sensor_locations' must be set in the current " +
                                 "flow sensor configuration")
        else:
            sensor_locations = self.__sensor_config.flow_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(flow_sensor=s_id)
               for s_id in sensor_locations]
        return self.__sensor_readings[:, idx]

    def plot_flows(self, sensor_locations: list[str] = None, show: bool = True,
                   save_to_file: str = None, ax: matplotlib.axes.Axes = None
                   ) -> matplotlib.axes.Axes:
        """
        Plots the final flow sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing flow sensor locations for which the sensor readings have to be plotted.
            If None, the readings from all flow sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_flows(sensor_locations)
        flow_sensors = sensor_locations if sensor_locations is not None else \
            self.__sensor_config.flow_sensors

        y_axis_label = f"Flow rate in ${flowunit_to_str(self.__sensor_config.flow_unit)}$"

        return plot_timeseries_data(data.T, labels=[f"Link {n_id}" for n_id in flow_sensors],
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label=y_axis_label,
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_demands(self, sensor_locations: list[str] = None) -> np.ndarray:
        """
        Gets the final demand sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing demand sensor locations for which the sensor readings are requested.
            If None, the readings from all demand sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Demand sensor readings.
        """
        if self.__sensor_config.demand_sensors == []:
            raise ValueError("No demand sensors set")
        if sensor_locations is not None:
            if not isinstance(sensor_locations, list):
                raise TypeError("'sensor_locations' must be an instance of 'list[str]' " +
                                f"but not of '{type(sensor_locations)}'")
            if any(s_id not in self.__sensor_config.demand_sensors for s_id in sensor_locations):
                raise ValueError("Invalid sensor ID in 'sensor_locations' -- note that all " +
                                 "sensors in 'sensor_locations' must be set in the current " +
                                 "demand sensor configuration")
        else:
            sensor_locations = self.__sensor_config.demand_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(demand_sensor=s_id)
               for s_id in sensor_locations]
        return self.__sensor_readings[:, idx]

    def plot_demands(self, sensor_locations: list[str] = None, show: bool = True,
                     save_to_file: str = None, ax: matplotlib.axes.Axes = None
                     ) -> matplotlib.axes.Axes:
        """
        Plots the final demand sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing demand sensor locations for which the sensor readings have to be plotted.
            If None, the readings from all demand sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_demands(sensor_locations)
        demand_sensors = sensor_locations if sensor_locations is not None else \
            self.__sensor_config.demand_sensors

        y_axis_label = f"Demand in ${flowunit_to_str(self.__sensor_config.flow_unit)}$"

        return plot_timeseries_data(data.T, labels=[f"Node {n_id}" for n_id in demand_sensors],
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label=y_axis_label,
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_nodes_quality(self, sensor_locations: list[str] = None) -> np.ndarray:
        """
        Gets the final node quality sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing node quality sensor locations for which the sensor readings are requested.
            If None, the readings from all node quality sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Node quality sensor readings.
        """
        if self.__sensor_config.quality_node_sensors == []:
            raise ValueError("No node quality sensors set")
        if sensor_locations is not None:
            if not isinstance(sensor_locations, list):
                raise TypeError("'sensor_locations' must be an instance of 'list[str]' " +
                                f"but not of '{type(sensor_locations)}'")
            if any(s_id not in self.__sensor_config.quality_node_sensors
                   for s_id in sensor_locations):
                raise ValueError("Invalid sensor ID in 'sensor_locations' -- note that all " +
                                 "sensors in 'sensor_locations' must be set in the current " +
                                 "node quality sensor configuration")
        else:
            sensor_locations = self.__sensor_config.quality_node_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(node_quality_sensor=s_id)
               for s_id in sensor_locations]
        return self.__sensor_readings[:, idx]

    def plot_nodes_quality(self, sensor_locations: list[str] = None, show: bool = True,
                           save_to_file: str = None, ax: matplotlib.axes.Axes = None
                           ) -> matplotlib.axes.Axes:
        """
        Plots the final node quality sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing node quality sensor locations for which the sensor readings
            have to be plotted.
            If None, the readings from all node quality sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_nodes_quality(sensor_locations)
        nodes_quality_sensors = sensor_locations if sensor_locations is not None else \
            self.__sensor_config.quality_node_sensors

        y_axis_label = f"${qualityunit_to_str(self.__sensor_config.quality_unit)}$"

        return plot_timeseries_data(data.T, labels=[f"Node {n_id}"
                                                    for n_id in nodes_quality_sensors],
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label=y_axis_label,
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_links_quality(self, sensor_locations: list[str] = None) -> np.ndarray:
        """
        Gets the final link quality sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing link quality sensor locations for which the sensor readings are requested.
            If None, the readings from all link quality sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Link quality sensor readings.
        """
        if self.__sensor_config.quality_link_sensors == []:
            raise ValueError("No link quality sensors set")
        if sensor_locations is not None:
            if not isinstance(sensor_locations, list):
                raise TypeError("'sensor_locations' must be an instance of 'list[str]' " +
                                f"but not of '{type(sensor_locations)}'")
            if any(s_id not in self.__sensor_config.quality_link_sensors
                   for s_id in sensor_locations):
                raise ValueError("Invalid sensor ID in 'sensor_locations' -- note that all " +
                                 "sensors in 'sensor_locations' must be set in the current " +
                                 "link quality sensor configuration")
        else:
            sensor_locations = self.__sensor_config.quality_link_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(link_quality_sensor=s_id)
               for s_id in sensor_locations]
        return self.__sensor_readings[:, idx]

    def plot_links_quality(self, sensor_locations: list[str] = None, show: bool = True,
                           save_to_file: str = None, ax: matplotlib.axes.Axes = None
                           ) -> matplotlib.axes.Axes:
        """
        Plots the final link/pipe quality sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing link quality sensor locations for which the sensor readings
            have to be plotted.
            If None, the readings from all link quality sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_links_quality(sensor_locations)
        links_quality_sensors = sensor_locations if sensor_locations is not None else \
            self.__sensor_config.quality_link_sensors

        y_axis_label = f"${qualityunit_to_str(self.__sensor_config.quality_unit)}$"

        return plot_timeseries_data(data.T, labels=[f"Link {n_id}"
                                                    for n_id in links_quality_sensors],
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label=y_axis_label,
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_pumps_state(self, sensor_locations: list[str] = None) -> np.ndarray:
        """
        Gets the final pump state sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing pump state sensor locations for which the sensor readings are requested.
            If None, the readings from all pump state sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Pump state sensor readings.
        """
        if self.__sensor_config.pump_state_sensors == []:
            raise ValueError("No pump state sensors set")
        if sensor_locations is not None:
            if not isinstance(sensor_locations, list):
                raise TypeError("'sensor_locations' must be an instance of 'list[str]' " +
                                f"but not of '{type(sensor_locations)}'")
            if any(s_id not in self.__sensor_config.pump_state_sensors
                   for s_id in sensor_locations):
                raise ValueError("Invalid sensor ID in 'sensor_locations' -- note that all " +
                                 "sensors in 'sensor_locations' must be set in the current " +
                                 "pump state sensor configuration")
        else:
            sensor_locations = self.__sensor_config.pump_state_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(pump_state_sensor=s_id)
               for s_id in sensor_locations]
        return self.__sensor_readings[:, idx]

    def plot_pumps_state(self, sensor_locations: list[str] = None, show: bool = True,
                         save_to_file: str = None, ax: matplotlib.axes.Axes = None
                         ) -> matplotlib.axes.Axes:
        """
        Plots the final pump state sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing pump state sensor locations for which the sensor readings have to be plotted.
            If None, the readings from all pump state sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_pumps_state(sensor_locations)
        pump_state_sensors = sensor_locations if sensor_locations is not None else \
            self.__sensor_config.pump_state_sensors

        return plot_timeseries_data(data.T, labels=[f"Pump {n_id}"
                                                    for n_id in pump_state_sensors],
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label="Pump state",
                                    y_ticks=([2.0, 3.0], ["Off", "On"]),
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_pumps_efficiency(self, sensor_locations: list[str] = None) -> np.ndarray:
        """
        Gets the final pump efficiency sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing pump efficiency sensor locations for which the sensor readings are requested.
            If None, the readings from all pump efficiency sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Pump efficiency sensor readings.
        """
        if self.__sensor_config.pump_efficiency_sensors == []:
            raise ValueError("No pump efficiency sensors set")
        if sensor_locations is not None:
            if not isinstance(sensor_locations, list):
                raise TypeError("'sensor_locations' must be an instance of 'list[str]' " +
                                f"but not of '{type(sensor_locations)}'")
            if any(s_id not in self.__sensor_config.pump_efficiency_sensors
                   for s_id in sensor_locations):
                raise ValueError("Invalid sensor ID in 'sensor_locations' -- note that all " +
                                 "sensors in 'sensor_locations' must be set in the current " +
                                 "pump efficiency sensor configuration")
        else:
            sensor_locations = self.__sensor_config.pump_efficiency_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(pump_efficiency_sensor=s_id)
               for s_id in sensor_locations]
        return self.__sensor_readings[:, idx]

    def plot_pumps_efficiency(self, sensor_locations: list[str] = None, show: bool = True,
                              save_to_file: str = None, ax: matplotlib.axes.Axes = None
                              ) -> matplotlib.axes.Axes:
        """
        Plots the final pump efficiency sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing pump efficiency sensor locations for which the sensor readings
            have to be plotted.
            If None, the readings from all pump efficiency sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_pumps_efficiency(sensor_locations)
        pump_efficiency_sensors = sensor_locations if sensor_locations is not None else \
            self.__sensor_config.pump_efficiency_sensors

        return plot_timeseries_data(data.T, labels=[f"Pump {n_id}"
                                                    for n_id in pump_efficiency_sensors],
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label="Efficiency in $\%$",
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_pumps_energyconsumption(self, sensor_locations: list[str] = None) -> np.ndarray:
        """
        Gets the final pump energy consumption sensor readings -- note that those might be subject
        to given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing pump energy consumption sensor locations for which
            the sensor readings are requested.
            If None, the readings from all pump energy consumption sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Pump energy consumption sensor readings.
        """
        if self.__sensor_config.pump_energyconsumption_sensors == []:
            raise ValueError("No pump energy consumption sensors set")
        if sensor_locations is not None:
            if not isinstance(sensor_locations, list):
                raise TypeError("'sensor_locations' must be an instance of 'list[str]' " +
                                f"but not of '{type(sensor_locations)}'")
            if any(s_id not in self.__sensor_config.pump_energyconsumption_sensors
                   for s_id in sensor_locations):
                raise ValueError("Invalid sensor ID in 'sensor_locations' -- note that all " +
                                 "sensors in 'sensor_locations' must be set in the current " +
                                 "pump efficiency sensor configuration")
        else:
            sensor_locations = self.__sensor_config.pump_energyconsumption_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(pump_energyconsumption_sensor=s_id)
               for s_id in sensor_locations]
        return self.__sensor_readings[:, idx]

    def plot_pumps_energyconsumption(self, sensor_locations: list[str] = None, show: bool = True,
                                     save_to_file: str = None, ax: matplotlib.axes.Axes = None
                                     ) -> matplotlib.axes.Axes:
        """
        Plots the final pump energy consumption sensor readings -- note that those might be
        subject to given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing pump energy consumption sensor locations for which the sensor readings
            have to be plotted.
            If None, the readings from all pump energy consumption sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_pumps_energyconsumption(sensor_locations)
        pump_energyconsumption_sensors = sensor_locations if sensor_locations is not None else \
            self.__sensor_config.pump_energyconsumption_sensors

        return plot_timeseries_data(data.T, labels=[f"Pump {n_id}"
                                                    for n_id in pump_energyconsumption_sensors],
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label="Energy consumption in $kilowatt - hour$",
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_valves_state(self, sensor_locations: list[str] = None) -> np.ndarray:
        """
        Gets the final valve state sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing valve state sensor locations for which the sensor readings are requested.
            If None, the readings from all valve state sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Valve state sensor readings.
        """
        if self.__sensor_config.valve_state_sensors == []:
            raise ValueError("No valve state sensors set")
        if sensor_locations is not None:
            if not isinstance(sensor_locations, list):
                raise TypeError("'sensor_locations' must be an instance of 'list[str]' " +
                                f"but not of '{type(sensor_locations)}'")
            if any(s_id not in self.__sensor_config.valve_state_sensors
                   for s_id in sensor_locations):
                raise ValueError("Invalid sensor ID in 'sensor_locations' -- note that all " +
                                 "sensors in 'sensor_locations' must be set in the current " +
                                 "valve state sensor configuration")
        else:
            sensor_locations = self.__sensor_config.valve_state_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(valve_state_sensor=s_id)
               for s_id in sensor_locations]
        return self.__sensor_readings[:, idx]

    def plot_valves_state(self, sensor_locations: list[str] = None, show: bool = True,
                          save_to_file: str = None, ax: matplotlib.axes.Axes = None
                          ) -> matplotlib.axes.Axes:
        """
        Plots the final valve state sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing valve state sensor locations for which the sensor readings have to be plotted.
            If None, the readings from all valve state sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_valves_state(sensor_locations)
        valve_state_sensors = sensor_locations if sensor_locations is not None else \
            self.__sensor_config.valve_state_sensors

        return plot_timeseries_data(data.T, labels=[f"Valve {n_id}"
                                                    for n_id in valve_state_sensors],
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label="Valve state",
                                    y_ticks=([2.0, 3.0], ["Closed", "Open"]),
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_tanks_water_volume(self, sensor_locations: list[str] = None) -> np.ndarray:
        """
        Gets the final water tanks volume sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing flow sensor locations for which the sensor readings are requested.
            If None, the readings from all water tanks volume sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Water tanks volume sensor readings.
        """
        if self.__sensor_config.tank_volume_sensors == []:
            raise ValueError("No tank volume sensors set")
        if sensor_locations is not None:
            if not isinstance(sensor_locations, list):
                raise TypeError("'sensor_locations' must be an instance of 'list[str]' " +
                                f"but not of '{type(sensor_locations)}'")
            if any(s_id not in self.__sensor_config.tank_volume_sensors
                   for s_id in sensor_locations):
                raise ValueError("Invalid sensor ID in 'sensor_locations' -- note that all " +
                                 "sensors in 'sensor_locations' must be set in the current " +
                                 "water tanks volume sensor configuration")
        else:
            sensor_locations = self.__sensor_config.tank_volume_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(tank_volume_sensor=s_id)
               for s_id in sensor_locations]
        return self.__sensor_readings[:, idx]

    def plot_tanks_water_volume(self, sensor_locations: list[str] = None, show: bool = True,
                                save_to_file: str = None, ax: matplotlib.axes.Axes = None
                                ) -> matplotlib.axes.Axes:
        """
        Plots the final water tanks volume sensor readings -- note that those might be subject to
        given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        sensor_locations : `list[str]`, optional
            Existing flow sensor locations for which the sensor readings have to be plotted.
            If None, the readings from all water tanks volume sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_tanks_water_volume(sensor_locations)
        tank_volume_sensors = sensor_locations if sensor_locations is not None else \
            self.__sensor_config.tank_volume_sensors

        volume_unit = "m^3" if is_flowunit_simetric(self.__sensor_config.flow_unit) else "feet^3"
        y_axis_label = f"Water volume in ${volume_unit}$"

        return plot_timeseries_data(data.T, labels=[f"Tank {n_id}"
                                                    for n_id in tank_volume_sensors],
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label=y_axis_label,
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_surface_species_concentration(self,
                                               surface_species_sensor_locations: dict = None
                                               ) -> np.ndarray:
        """
        Gets the final surface species concentration sensor readings --
        note that those might be subject to given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        surface_species_sensor_locations : `dict`, optional
            Existing surface species concentration sensors (species ID and link/pipe IDs) for which
            the sensor readings are requested.
            If None, the readings from all surface species concentration sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Surface species concentration sensor readings.
        """
        if self.__sensor_config.surface_species_sensors == {}:
            raise ValueError("No surface species sensors set")
        if surface_species_sensor_locations is not None:
            if not isinstance(surface_species_sensor_locations, dict):
                raise TypeError("'surface_species_sensor_locations' must be an instance of 'dict'" +
                                f" but not of '{type(surface_species_sensor_locations)}'")
            for species_id in surface_species_sensor_locations:
                if species_id not in self.__sensor_config.surface_species_sensors:
                    raise ValueError(f"Species '{species_id}' is not included in the " +
                                     "sensor configuration")

                my_surface_species_sensor_locations = \
                    self.__sensor_config.surface_species_sensors[species_id]
                for sensor_id in surface_species_sensor_locations[species_id]:
                    if sensor_id not in my_surface_species_sensor_locations:
                        raise ValueError(f"Link '{sensor_id}' is not included in the " +
                                         f"sensor configuration for species '{species_id}'")
        else:
            surface_species_sensor_locations = self.__sensor_config.surface_species_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(
            surface_species_sensor=(species_id, link_id))
                for species_id in surface_species_sensor_locations
                for link_id in surface_species_sensor_locations[species_id]]
        return self.__sensor_readings[:, idx]

    def plot_surface_species_concentration(self, surface_species_sensor_locations: dict = None,
                                           show: bool = True, save_to_file: str = None,
                                           ax: matplotlib.axes.Axes = None
                                           ) -> matplotlib.axes.Axes:
        """
        Plots the final surface species concentration sensor readings -- note that those might be
        subject to given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        surface_species_sensor_locations : `dict`, optional
            Existing surface species concentration sensors (species ID and link/pipe IDs) for which
            the sensor readings have to be plotted.
            If None, the readings from all surface species concentration sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_surface_species_concentration(surface_species_sensor_locations)
        if surface_species_sensor_locations is None:
            surface_species_sensor_locations = self.__sensor_config.surface_species_sensors

        area_unit = self.__sensor_config.surface_species_area_unit
        concentration_unit = None
        labels = []
        for species_id in surface_species_sensor_locations:
            mass_unit = self.__sensor_config.get_surface_species_mass_unit_id(species_id)
            if concentration_unit is not None:
                if concentration_unit != mass_unit:
                    raise ValueError("Can not plot species with different mass units")
                concentration_unit = mass_unit
            else:
                concentration_unit = mass_unit

            for link_id in surface_species_sensor_locations[species_id]:
                labels.append(f"{species_id} @ link {link_id}")

        y_axis_label = f"Concentration in ${massunit_to_str(concentration_unit)}/" +\
            f"{areaunit_to_str(area_unit)}$"

        return plot_timeseries_data(data.T, labels=labels,
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label=y_axis_label,
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_bulk_species_node_concentration(self,
                                                 bulk_species_sensor_locations: dict = None
                                                 ) -> np.ndarray:
        """
        Gets the final bulk species node concentration sensor readings --
        note that those might be subject to given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        bulk_species_sensor_locations : `dict`, optional
            Existing bulk species concentration sensors (species ID and node IDs) for which
            the sensor readings are requested.
            If None, the readings from all bulk species node concentration sensors are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Bulk species concentration sensor readings.
        """
        if self.__sensor_config.bulk_species_node_sensors == {}:
            raise ValueError("No bulk species node sensors set")
        if bulk_species_sensor_locations is not None:
            if not isinstance(bulk_species_sensor_locations, dict):
                raise TypeError("'bulk_species_sensor_locations' must be an instance of 'dict'" +
                                f" but not of '{type(bulk_species_sensor_locations)}'")
            for species_id in bulk_species_sensor_locations:
                if species_id not in self.__sensor_config.bulk_species_node_sensors:
                    raise ValueError(f"Species '{species_id}' is not included in the " +
                                     "sensor configuration")

                my_bulk_species_sensor_locations = \
                    self.__sensor_config.bulk_species_node_sensors[species_id]
                for sensor_id in bulk_species_sensor_locations[species_id]:
                    if sensor_id not in my_bulk_species_sensor_locations:
                        raise ValueError(f"Link '{sensor_id}' is not included in the " +
                                         f"sensor configuration for species '{species_id}'")
        else:
            bulk_species_sensor_locations = self.__sensor_config.bulk_species_node_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(
            bulk_species_node_sensor=(species_id, node_id))
                for species_id in bulk_species_sensor_locations
                for node_id in bulk_species_sensor_locations[species_id]]
        return self.__sensor_readings[:, idx]

    def plot_bulk_species_node_concentration(self, bulk_species_node_sensors: dict = None,
                                             show: bool = True, save_to_file: str = None,
                                             ax: matplotlib.axes.Axes = None
                                             ) -> matplotlib.axes.Axes:
        """
        Plots the final bulk species node concentration sensor readings --
        note that those might be subject to given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        bulk_species_node_sensors : `dict`, optional
            Existing bulk species concentration sensors (species ID and node IDs) for which
            the sensor readings are requested.
            If None, the readings from all bulk species node concentration sensors are returned.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_bulk_species_node_concentration(bulk_species_node_sensors)
        if bulk_species_node_sensors is None:
            bulk_species_node_sensors = self.__sensor_config.bulk_species_node_sensors

        concentration_unit = None
        labels = []
        for species_id in bulk_species_node_sensors:
            mass_unit = self.__sensor_config.get_bulk_species_mass_unit_id(species_id)
            if concentration_unit is not None:
                if concentration_unit != mass_unit:
                    raise ValueError("Can not plot species with different mass units")
                concentration_unit = mass_unit
            else:
                concentration_unit = mass_unit

            for node_id in bulk_species_node_sensors[species_id]:
                labels.append(f"{species_id} @ node {node_id}")

        y_axis_label = f"Concentration in ${massunit_to_str(concentration_unit)}/L$"

        return plot_timeseries_data(data.T, labels=labels,
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label=y_axis_label,
                                    show=show, save_to_file=save_to_file, ax=ax)

    def get_data_bulk_species_link_concentration(self,
                                                 bulk_species_sensor_locations: dict = None
                                                 ) -> np.ndarray:
        """
        Gets the final bulk species link/pipe concentration sensor readings --
        note that those might be subject to given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        bulk_species_sensor_locations : `dict`, optional
            Existing bulk species concentration sensors (species ID and link/pipe IDs) for which
            the sensor readings are requested.
            If None, the readings from all bulk species concentration link/pipe sensors
            are returned.

            The default is None.

        Returns
        -------
        `numpy.ndarray`
            Bulk species concentration sensor readings.
        """
        if self.__sensor_config.bulk_species_link_sensors == {}:
            raise ValueError("No bulk species link/pipe sensors set")
        if bulk_species_sensor_locations is not None:
            if not isinstance(bulk_species_sensor_locations, dict):
                raise TypeError("'bulk_species_sensor_locations' must be an instance of 'dict'" +
                                f" but not of '{type(bulk_species_sensor_locations)}'")
            for species_id in bulk_species_sensor_locations:
                if species_id not in self.__sensor_config.bulk_species_link_sensors:
                    raise ValueError(f"Species '{species_id}' is not included in the " +
                                     "sensor configuration")

                my_bulk_species_sensor_locations = \
                    self.__sensor_config.bulk_species_link_sensors[species_id]
                for sensor_id in bulk_species_sensor_locations[species_id]:
                    if sensor_id not in my_bulk_species_sensor_locations:
                        raise ValueError(f"Link '{sensor_id}' is not included in the " +
                                         f"sensor configuration for species '{species_id}'")
        else:
            bulk_species_sensor_locations = self.__sensor_config.bulk_species_link_sensors

        if self.__sensor_readings is None:
            self.get_data()

        idx = [self.__sensor_config.get_index_of_reading(
            bulk_species_link_sensor=(species_id, node_id))
                for species_id in bulk_species_sensor_locations
                for node_id in bulk_species_sensor_locations[species_id]]
        return self.__sensor_readings[:, idx]

    def plot_bulk_species_link_concentration(self, bulk_species_link_sensors: dict = None,
                                             show: bool = True, save_to_file: str = None,
                                             ax: matplotlib.axes.Axes = None
                                             ) -> matplotlib.axes.Axes:
        """
        Plots the final bulk species link concentration sensor readings -- note that those might be
        subject to given sensor faults and sensor noise/uncertainty.

        Parameters
        ----------
        bulk_species_link_sensors : `dict`, optional
            Existing bulk species link concentration sensors (species ID and link/pipe IDs) for which
            the sensor readings have to be plotted.
            If None, the readings from all bulk species link concentration sensors are plotted.

            The default is None.
        show : `bool`, optional
            If True, the plot/figure is shown in a window.

            Only considered when 'ax' is None.

            The default is True.
        save_to_file : `str`, optional
            File to which the plot is saved.

            If specified, 'show' must be set to False --
            i.e. a plot can not be shown and saved to a file at the same time!

            The default is None.
        ax : `matplotlib.axes.Axes`, optional
            If not None, 'ax' is used for plotting.

            The default is None.

        Returns
        -------
        `matplotlib.axes.Axes`
            Plot.
        """
        data = self.get_data_bulk_species_link_concentration(bulk_species_link_sensors)
        if bulk_species_link_sensors is None:
            bulk_species_link_sensors = self.__sensor_config.bulk_species_link_sensors

        area_unit = self.__sensor_config.surface_species_area_unit
        concentration_unit = None
        labels = []
        for species_id in bulk_species_link_sensors:
            mass_unit = self.__sensor_config.get_bulk_species_mass_unit_id(species_id)
            if concentration_unit is not None:
                if concentration_unit != mass_unit:
                    raise ValueError("Can not plot species with different mass units")
                concentration_unit = mass_unit
            else:
                concentration_unit = mass_unit

            for link_id in bulk_species_link_sensors[species_id]:
                labels.append(f"{species_id} @ link {link_id}")

        y_axis_label = f"Concentration in ${massunit_to_str(concentration_unit)}/" +\
            f"{areaunit_to_str(area_unit)}$"

        return plot_timeseries_data(data.T, labels=labels,
                                    x_axis_label=self.__get_x_axis_label(),
                                    y_axis_label=y_axis_label,
                                    show=show, save_to_file=save_to_file, ax=ax)
