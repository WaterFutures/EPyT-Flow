"""
Module provides a class for implementing species injection (e.g. contamination) events.
"""
from copy import deepcopy
import warnings
import math
import numpy as np
import epyt
from epyt.epanet import ToolkitConstants

from .system_event import SystemEvent
from ...serialization import serializable, JsonSerializable, \
    SPECIESINJECTION_EVENT_ID


@serializable(SPECIESINJECTION_EVENT_ID, ".epytflow_speciesinjection_event")
class SpeciesInjectionEvent(SystemEvent, JsonSerializable):
    """
    Class implementing a (bulk) species injection event -- e.g. modeling a contamination event.

    Parameters
    ----------
    species_id : `str`
        ID of the bulk species that is going to be injected.
    node_id : `str`
        ID of the node at which the injection is palced.
    profile : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_
        Injection strength profile -- i.e. every entry corresponds to the strength of the injection
        at a point in time. Pattern will repeat if it is shorter than the total injection time.
    source_type : `int`
        Type of the bulk species injection source -- must be one of
        the following EPANET toolkit constants:

            - EN_CONCEN     = 0
            - EN_MASS       = 1
            - EN_SETPOINT   = 2
            - EN_FLOWPACED  = 3

        Description:

            - E_CONCEN Sets the concentration of external inflow entering a node
            - EN_MASS Injects a given mass/minute into a node
            - EN_SETPOINT Sets the concentration leaving a node to a given value
            - EN_FLOWPACED Adds a given value to the concentration leaving a node
    """
    def __init__(self, species_id: str, node_id: str, profile: np.ndarray, source_type: int,
                 **kwds):
        if not isinstance(species_id, str):
            raise TypeError("'species_id' must be an instance of 'str' but not of " +
                            f"'{type(species_id)}'")
        if not isinstance(node_id, str):
            raise TypeError("'node_id' must be an instance of 'str' but not of " +
                            f"'{type(node_id)}'")
        if not isinstance(profile, np.ndarray):
            raise TypeError("'profile' must be an instance of 'numpy.ndarray' but not of " +
                            f"'{type(profile)}'")
        if not isinstance(source_type, int):
            raise TypeError("'source_type' must be an instance of 'int' but not of " +
                            f"'{type(source_type)}'")
        if not 0 <= source_type <= 3:
            raise ValueError("'source_tye' must be in [0, 3]")

        self.__species_id = species_id
        self.__node_id = node_id
        self.__profile = profile
        self.__source_type = source_type

        super().__init__(**kwds)

    @property
    def species_id(self) -> str:
        """
        Gets the ID of the bulk species that is going to be injected.

        Returns
        -------
        `str`
            Bulk species ID.
        """
        return self.__species_id

    @property
    def node_id(self) -> str:
        """
        Gets the ID of the node at which the injection is palced.

        Returns
        -------
        `str`
            Node ID.
        """
        return self.__node_id

    @property
    def profile(self) -> np.ndarray:
        """
        Gets the injection strength profile.

        Returns
        -------
        `numpy.ndarray`
            Pattern of the injection.
        """
        return deepcopy(self.__profile)

    @property
    def source_type(self) -> int:
        """
        Type of the bulk species injection source -- will be one of
        the following EPANET toolkit constants:

            - EN_CONCEN     = 0
            - EN_MASS       = 1
            - EN_SETPOINT   = 2
            - EN_FLOWPACED  = 3

        Returns
        -------
        `int`
            Type of the injection source.
        """
        return self.__source_type

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"species_id": self.__species_id,
                                           "node_id": self.__node_id, "profile": self.__profile,
                                           "source_type": self.__source_type}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__species_id == other.species_id and \
            self.__node_id == other.node_id and np.all(self.__profile == other.profile) and \
            self.__source_type == other.source_type

    def __str__(self) -> str:
        return f"{super().__str__()} species_id: {self.__species_id} " +\
            f"node_id: {self.__node_id} profile: {self.__profile} source_type: {self.__source_type}"

    def _get_pattern_id(self) -> str:
        return f"{self.__species_id}_{self.__node_id}"

    def init(self, epanet_api: epyt.epanet) -> None:
        super().init(epanet_api)

        # Check parameters
        if self.__species_id not in self._epanet_api.getMSXSpeciesNameID():
            raise ValueError(f"Unknown species '{self.__species_id}'")
        if self.__node_id not in self._epanet_api.getNodeNameID():
            raise ValueError(f"Unknown node '{self.__node_id}'")

        # Create final injection strength pattern
        total_sim_duration = self._epanet_api.getTimeSimulationDuration()
        time_step = self._epanet_api.getTimeHydraulicStep()

        pattern = np.zeros(math.ceil(total_sim_duration / time_step))

        end_time = self.end_time if self.end_time is not None else total_sim_duration
        injection_pattern_length = math.ceil((end_time - self.start_time) / time_step)
        injection_time_start_idx = int(self.start_time / time_step)

        injection_pattern = None
        if len(self.__profile) == injection_pattern_length:
            injection_pattern = self.profile
        else:
            injection_pattern = np.tile(self.profile,
                                        math.ceil(injection_pattern_length / len(self.profile)))

        pattern[injection_time_start_idx:
                injection_time_start_idx + injection_pattern_length] = injection_pattern

        # Create injection
        source_type_ = "None"
        if self.__source_type == ToolkitConstants.EN_CONCEN:
            source_type_ = "CONCEN"
        elif self.__source_type == ToolkitConstants.EN_MASS:
            source_type_ = "MASS"
        elif self.__source_type == ToolkitConstants.EN_SETPOINT:
            source_type_ = "SETPOINT"
        elif self.__source_type == ToolkitConstants.EN_FLOWPACED:
            source_type_ = "FLOWPACED"

        pattern_id = self._get_pattern_id()
        if pattern_id in self._epanet_api.getMSXPatternsNameID():
            node_idx = self._epanet_api.getNodeIndex(self.__node_id)
            species_idx, = self._epanet_api.getMSXSpeciesIndex([self.__species_id])
            cur_source_type = self._epanet_api.msx.MSXgetsource(node_idx, species_idx)
            if cur_source_type[0] != source_type_:
                raise ValueError("Source type does not match existing source type")

            # Add new injection amount to existing injection --
            # i.e. two injection events at the same node
            pattern_idx, = self._epanet_api.getMSXPatternsIndex([pattern_id])
            cur_pattern = self._epanet_api.getMSXPattern()[pattern_idx - 1]
            cur_pattern += pattern
            self._epanet_api.setMSXPattern(pattern_idx, cur_pattern)
        else:
            self._epanet_api.addMSXPattern(pattern_id, pattern)
        self._epanet_api.setMSXSources(self.__node_id, self.__species_id, source_type_, 1,
                                       pattern_id)

    def cleanup(self) -> None:
        warnings.warn("Can not undo SpeciedInjectionEvent -- " +
                      "EPANET-MSX does not support removing patterns")

    def apply(self, cur_time: int) -> None:
        pass
