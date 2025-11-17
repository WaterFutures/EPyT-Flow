"""
Module provides a class for implementing model uncertainty.
"""
from typing import Optional
from copy import deepcopy
import warnings
from epanet_plus import EPyT, EpanetConstants
import numpy as np

from ..serialization import serializable, JsonSerializable, MODEL_UNCERTAINTY_ID
from .uncertainties import Uncertainty


@serializable(MODEL_UNCERTAINTY_ID, ".epytflow_uncertainty_model_uncertainty")
class ModelUncertainty(JsonSerializable):
    """
    Class implementing model uncertainty -- i.e. uncertainties in pipe length, pipe roughness,
    base demand, etc.

    Parameters
    ----------
    global_pipe_length_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Global uncertainty of pipe lengths. None, in the case of no uncertainty.

        The default is None.
    global_pipe_roughness_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Global uncertainty of pipe roughness coefficients. None, in the case of no uncertainty.

        The default is None.
    global_pipe_diameter_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Global uncertainty of pipe diameters. None, in the case of no uncertainty.

        The default is None.
    global_base_demand_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Global uncertainty of base demands. None, in the case of no uncertainty.

        The default is None.
    global_demand_pattern_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Global uncertainty of demand patterns. None, in the case of no uncertainty.

        The default is None.
    global_elevation_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Global uncertainty of elevations. None, in the case of no uncertainty.

        The default is None.
    global_constants_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Global uncertainty of MSX constants. None, in the case of no uncertainty.

        The default is None.
    global_parameters_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Global uncertainty of MSX parameters. None, in the case of no uncertaint.

        The default is None.
    local_pipe_length_uncertainty : dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`], optional
        Local uncertainty of pipe lengths -- i.e. a dictionary of pipe IDs and uncertainties.

        None, in the case of no uncertainty.

        The default is None.
    local_pipe_roughness_uncertainty : dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`], optional
        Local uncertainty of pipe roughness coefficients -- i.e. a dictionary of pipe IDs and uncertainties.

        None, in the case of no uncertainty.

        The default is None.
    local_pipe_diameter_uncertainty : dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`], optional
        Local uncertainty of pipe diameters -- i.e. a dictionary of pipe IDs and uncertainties.

        None, in the case of no uncertainty.

        The default is None.
    local_base_demand_uncertainty : dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`], optional
        Local uncertainty of base demands -- i.e. a dictionary of node IDs and uncertainties.

        None, in the case of no uncertainty.

        The default is None.
    local_demand_pattern_uncertainty : dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`], optional
        Local uncertainty of demand patterns --
        i.e. a dictionary of demand pattern IDs and uncertainties.

        None, in the case of no uncertainty.

        The default is None.
    local_elevation_uncertainty : dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`], optional
        Local uncertainty of elevations -- i.e. a dictionary of node IDs and uncertainties.

        None, in the case of no uncertainty.

        The default is None.
    local_constants_uncertainty : dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`], optional
        Local uncertainty of MSX constants -- i.e. a dictionary of constant IDs and uncertainties.

        None, in the case of no uncertainty.

        The default is None.
    local_parameters_uncertainty : dict[tuple[str, int, str] :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`], optional
        Local uncertainty of MSX parameters -- i.e. a dictionary of
        (parameter ID, item type, item ID) and uncertainties.

        None, in the case of no uncertainty.

        The default is None.
    local_patterns_uncertainty : dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`], optional
        Local uncertainty of EPANET patterns -- i.e. a dictionary of pattern IDs and uncertainties.

        None, in the case of no uncertainty.

        The default is None.
    local_msx_patterns_uncertainty : dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`], optional
        Local uncertainty of EPANET-MSX patterns -- i.e. a dictionary of MSX pattern IDs
        and uncertainties.

        None, in the case of no uncertainty.

        The default is None.
    seed : `int`, optional
        Seed for the random number generator.

        Thed default is None.
    cache_original : `bool`, optional
        If True, all original properties are cached before the uncertainties are applied.
        This is necessary if you have multiple simulation runs and you want to reset/re-apply
        the uncertainties before each run.

        You can set it to False if you do not and want to re-apply the uncertainties and
        save some working memory.

        The default is True.
    """
    def __init__(self, global_pipe_length_uncertainty: Optional[Uncertainty] = None,
                 global_pipe_roughness_uncertainty: Optional[Uncertainty] = None,
                 global_pipe_diameter_uncertainty: Optional[Uncertainty] = None,
                 global_base_demand_uncertainty: Optional[Uncertainty] = None,
                 global_demand_pattern_uncertainty: Optional[Uncertainty] = None,
                 global_elevation_uncertainty: Optional[Uncertainty] = None,
                 global_constants_uncertainty: Optional[Uncertainty] = None,
                 global_parameters_uncertainty: Optional[Uncertainty] = None,
                 local_pipe_length_uncertainty: Optional[dict[str, Uncertainty]] = None,
                 local_pipe_roughness_uncertainty: Optional[dict[str, Uncertainty]] = None,
                 local_pipe_diameter_uncertainty: Optional[dict[str, Uncertainty]] = None,
                 local_base_demand_uncertainty: Optional[dict[str, Uncertainty]] = None,
                 local_demand_pattern_uncertainty: Optional[dict[str, Uncertainty]] = None,
                 local_elevation_uncertainty: Optional[dict[str, Uncertainty]] = None,
                 local_constants_uncertainty: Optional[dict[str, Uncertainty]] = None,
                 local_parameters_uncertainty: Optional[dict[str, int, Uncertainty]] = None,
                 local_patterns_uncertainty: Optional[dict[str, Uncertainty]] = None,
                 local_msx_patterns_uncertainty: Optional[dict[str, Uncertainty]] = None,
                 seed: Optional[int] = None, cache_original: Optional[bool] = True,
                 **kwds):
        if global_pipe_length_uncertainty is not None:
            if not isinstance(global_pipe_length_uncertainty, Uncertainty):
                raise TypeError("'global_pipe_length_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(global_pipe_length_uncertainty)}'")
        if global_pipe_roughness_uncertainty is not None:
            if not isinstance(global_pipe_roughness_uncertainty, Uncertainty):
                raise TypeError("'global_pipe_roughness_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(global_pipe_roughness_uncertainty)}'")
        if global_pipe_diameter_uncertainty is not None:
            if not isinstance(global_pipe_diameter_uncertainty, Uncertainty):
                raise TypeError("'global_pipe_diameter_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(global_pipe_diameter_uncertainty)}'")
        if global_base_demand_uncertainty is not None:
            if not isinstance(global_base_demand_uncertainty, Uncertainty):
                raise TypeError("'global_base_demand_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(global_base_demand_uncertainty)}'")
        if global_demand_pattern_uncertainty is not None:
            if not isinstance(global_demand_pattern_uncertainty, Uncertainty):
                raise TypeError("'global_demand_pattern_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(global_demand_pattern_uncertainty)}'")
        if global_elevation_uncertainty is not None:
            if not isinstance(global_elevation_uncertainty, Uncertainty):
                raise TypeError("'global_elevation_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(global_elevation_uncertainty)}'")
        if global_constants_uncertainty is not None:
            if not isinstance(global_constants_uncertainty, Uncertainty):
                raise TypeError("'global_constants_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(global_constants_uncertainty)}'")
        if global_parameters_uncertainty is not None:
            if not isinstance(global_parameters_uncertainty, Uncertainty):
                raise TypeError("'global_parameters_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(global_parameters_uncertainty)}'")

        if local_pipe_length_uncertainty is not None:
            if not isinstance(local_pipe_length_uncertainty, dict):
                raise TypeError("'local_pipe_length_uncertainty' must be an instance of " +
                                "'dict[str, epyt_flow.uncertainty.Uncertainty]' but not of " +
                                f"'{type(local_pipe_length_uncertainty)}'")
            if any(not isinstance(key, str) or not isinstance(val, Uncertainty)
                   for key, val in local_pipe_length_uncertainty.items()):
                raise TypeError("'local_pipe_length_uncertainty': " +
                                "All keys must be instances of 'str' and all values must be " +
                                "instances of 'epyt_flow.uncertainty.Uncertainty'")
        if local_pipe_roughness_uncertainty is not None:
            if not isinstance(local_pipe_roughness_uncertainty, dict):
                raise TypeError("'local_pipe_roughness_uncertainty' must be an instance of " +
                                "'dict[str, epyt_flow.uncertainty.Uncertainty]' but not of " +
                                f"'{type(local_pipe_roughness_uncertainty)}'")
            if any(not isinstance(key, str) or not isinstance(val, Uncertainty)
                   for key, val in local_pipe_roughness_uncertainty.items()):
                raise TypeError("'local_pipe_roughness_uncertainty': " +
                                "All keys must be instances of 'str' and all values must be " +
                                "instances of 'epyt_flow.uncertainty.Uncertainty'")
        if local_pipe_diameter_uncertainty is not None:
            if not isinstance(local_pipe_diameter_uncertainty, dict):
                raise TypeError("'local_pipe_diameter_uncertainty' must be an instance of " +
                                "'dict[str, epyt_flow.uncertainty.Uncertainty]' but not of " +
                                f"'{type(local_pipe_diameter_uncertainty)}'")
            if any(not isinstance(key, str) or not isinstance(val, Uncertainty)
                   for key, val in local_pipe_diameter_uncertainty.items()):
                raise TypeError("'local_pipe_diameter_uncertainty': " +
                                "All keys must be instances of 'str' and all values must be " +
                                "instances of 'epyt_flow.uncertainty.Uncertainty'")
        if local_base_demand_uncertainty is not None:
            if not isinstance(local_base_demand_uncertainty, dict):
                raise TypeError("'local_base_demand_uncertainty' must be an instance of " +
                                "'dict[str, epyt_flow.uncertainty.Uncertainty]' but not of " +
                                f"'{type(local_base_demand_uncertainty)}'")
            if any(not isinstance(key, str) or not isinstance(val, Uncertainty)
                   for key, val in local_base_demand_uncertainty.items()):
                raise TypeError("'local_base_demand_uncertainty': " +
                                "All keys must be instances of 'str' and all values must be " +
                                "instances of 'epyt_flow.uncertainty.Uncertainty'")
        if local_demand_pattern_uncertainty is not None:
            if not isinstance(local_demand_pattern_uncertainty, dict):
                raise TypeError("'local_demand_pattern_uncertainty' must be an instance of " +
                                "'dict[str, epyt_flow.uncertainty.Uncertainty]' but not of " +
                                f"'{type(local_demand_pattern_uncertainty)}'")
            if any(not isinstance(key, str) or not isinstance(val, Uncertainty)
                   for key, val in local_demand_pattern_uncertainty.items()):
                raise TypeError("'local_demand_pattern_uncertainty': " +
                                "All keys must be instances of 'str' and all values must be " +
                                "instances of 'epyt_flow.uncertainty.Uncertainty'")
        if local_elevation_uncertainty is not None:
            if not isinstance(local_elevation_uncertainty, dict):
                raise TypeError("'local_elevation_uncertainty' must be an instance of " +
                                "'dict[str, epyt_flow.uncertainty.Uncertainty]' but not of " +
                                f"'{type(local_elevation_uncertainty)}'")
            if any(not isinstance(key, str) or not isinstance(val, Uncertainty)
                   for key, val in local_elevation_uncertainty.items()):
                raise TypeError("'local_elevation_uncertainty': " +
                                "All keys must be instances of 'str' and all values must be " +
                                "instances of 'epyt_flow.uncertainty.Uncertainty'")
        if local_constants_uncertainty is not None:
            if not isinstance(local_constants_uncertainty, dict):
                raise TypeError("'local_constants_uncertainty' must be an instance of " +
                                "'dict[str, epyt_flow.uncertainty.Uncertainty]' but not of " +
                                f"'{type(local_constants_uncertainty)}'")
            if any(not isinstance(key, str) or not isinstance(val, Uncertainty)
                   for key, val in local_constants_uncertainty.items()):
                raise TypeError("'local_constants_uncertainty': " +
                                "All keys must be instances of 'str' and all values must be " +
                                "instances of 'epyt_flow.uncertainty.Uncertainty'")
        if local_parameters_uncertainty is not None:
            if not isinstance(local_parameters_uncertainty, dict):
                raise TypeError("'local_parameters_uncertainty' must be an instance of " +
                                "'dict[str, epyt_flow.uncertainty.Uncertainty]' but not of " +
                                f"'{type(local_parameters_uncertainty)}'")
            if any(not isinstance(key, tuple) or not isinstance(key[0], str) or
                   not isinstance(key[1], int) or not isinstance(key[2], str) or
                   not isinstance(local_parameters_uncertainty[key], Uncertainty)
                   for key in local_parameters_uncertainty.keys()):
                raise TypeError("'local_parameters_uncertainty': " +
                                "All keys must be instances of 'tuple[str, int, str]' and all " +
                                "values must be instances of 'epyt_flow.uncertainty.Uncertainty'")
        if local_patterns_uncertainty is not None:
            if not isinstance(local_patterns_uncertainty, dict):
                raise TypeError("'local_patterns_uncertainty' must be an instance of " +
                                "'dict[str, epyt_flow.uncertainty.Uncertainty]' but not of " +
                                f"'{type(local_patterns_uncertainty)}'")
            if any(not isinstance(key, str) or not isinstance(val, Uncertainty)
                   for key, val in local_patterns_uncertainty.items()):
                raise TypeError("'local_patterns_uncertainty': " +
                                "All keys must be instances of 'str' and all values must be " +
                                "instances of 'epyt_flow.uncertainty.Uncertainty'")
        if local_msx_patterns_uncertainty is not None:
            if not isinstance(local_msx_patterns_uncertainty, dict):
                raise TypeError("'local_msx_patterns_uncertainty' must be an instance of " +
                                "'dict[str, epyt_flow.uncertainty.Uncertainty]' but not of " +
                                f"'{type(local_msx_patterns_uncertainty)}'")
            if any(not isinstance(key, str) or not isinstance(val, Uncertainty)
                   for key, val in local_msx_patterns_uncertainty.items()):
                raise TypeError("'local_msx_patterns_uncertainty': " +
                                "All keys must be instances of 'str' and all values must be " +
                                "instances of 'epyt_flow.uncertainty.Uncertainty'")
        if not isinstance(cache_original, bool):
            raise TypeError("'cache_original' must be an instance of 'bool' " +
                            f"but not of '{type(cache_original)}'")

        self._global_pipe_length = global_pipe_length_uncertainty
        self._global_pipe_roughness = global_pipe_roughness_uncertainty
        self._global_pipe_diameter = global_pipe_diameter_uncertainty
        self._global_base_demand = global_base_demand_uncertainty
        self._global_demand_pattern = global_demand_pattern_uncertainty
        self._global_elevation = global_elevation_uncertainty
        self._global_constants = global_constants_uncertainty
        self._global_parameters = global_parameters_uncertainty
        self._local_pipe_length = local_pipe_length_uncertainty
        self._local_pipe_roughness = local_pipe_roughness_uncertainty
        self._local_pipe_diameter = local_pipe_diameter_uncertainty
        self._local_base_demand = local_base_demand_uncertainty
        self._local_demand_pattern = local_demand_pattern_uncertainty
        self._local_elevation = local_elevation_uncertainty
        self._local_constants = local_constants_uncertainty
        self._local_parameters = local_parameters_uncertainty
        self._local_patterns = local_patterns_uncertainty
        self._local_msx_patterns = local_msx_patterns_uncertainty
        self.__seed = seed
        self.__cache_original = cache_original

        self._cache_links_length = None
        self._cache_links_diameter = None
        self._cache_links_roughness_coeff = None
        self._cache_nodes_base_demand = None
        self._cache_nodes_demand_pattern = None
        self._cache_nodes_elevation = None
        self._cache_patterns = None
        self._cache_msx_constants = None
        self._cache_msx_links_parameters = None
        self._cache_msx_tanks_parameters = None
        self._cache_msx_patterns = None

        super().__init__(**kwds)

    @property
    def seed(self) -> int:
        """
        Returns the seed used for the random number generator.

        Returns
        -------
        `int`
            Seed for the random number generator.
        """
        return self.__seed

    @property
    def global_pipe_length(self) -> Uncertainty:
        """
        Returns the global pipe length uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global pipe length uncertainty.
        """
        return deepcopy(self._global_pipe_length)

    @property
    def global_pipe_roughness(self) -> Uncertainty:
        """
        Returns the global pipe roughness uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global pipe roughness uncertainty.
        """
        return deepcopy(self._global_pipe_roughness)

    @property
    def global_pipe_diameter(self) -> Uncertainty:
        """
        Returns the global pipe diameter uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global pipe diameter uncertainty.
        """
        return deepcopy(self._global_pipe_diameter)

    @property
    def global_base_demand(self) -> Uncertainty:
        """
        Returns the global base demand uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global base demand uncertainty.
        """
        return deepcopy(self._global_base_demand)

    @property
    def global_demand_pattern(self) -> Uncertainty:
        """
        Returns the global demand pattern uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global demand pattern uncertainty.
        """
        return deepcopy(self._global_demand_pattern)

    @property
    def global_elevation(self) -> Uncertainty:
        """
        Returns the global node elevation uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global node elevation uncertainty.
        """
        return deepcopy(self._global_elevation)

    @property
    def global_constants(self) -> Uncertainty:
        """
        Returns the global MSX constant uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global MSX constant uncertainty.
        """
        return deepcopy(self._global_constants)

    @property
    def global_parameters(self) -> Uncertainty:
        """
        Returns the global MSX parameter uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global MSX parameter uncertainty.
        """
        return deepcopy(self._global_parameters)

    @property
    def local_pipe_length(self) -> dict[str, Uncertainty]:
        """
        Returns the local pipe length uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local pipe length uncertainty.
        """
        return deepcopy(self._local_pipe_length)

    @property
    def local_pipe_roughness(self) -> dict[str, Uncertainty]:
        """
        Returns the local pipe roughness uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local pipe roughness uncertainty.
        """
        return deepcopy(self._local_pipe_roughness)

    @property
    def local_pipe_diameter(self) -> dict[str, Uncertainty]:
        """
        Returns the local pipe diameter uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local pipe diameter uncertainty.
        """
        return deepcopy(self._local_pipe_diameter)

    @property
    def local_base_demand(self) -> dict[str, Uncertainty]:
        """
        Returns the local base demand uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local base demand uncertainty.
        """
        return deepcopy(self._local_base_demand)

    @property
    def local_demand_pattern(self) -> dict[str, Uncertainty]:
        """
        Returns the local demand pattern uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local demand pattern uncertainty.
        """
        return deepcopy(self._local_demand_pattern)

    @property
    def local_elevation(self) -> dict[str, Uncertainty]:
        """
        Returns the local node elevation uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local node elevation uncertainty.
        """
        return deepcopy(self._local_elevation)

    @property
    def local_constants(self) -> dict[str, Uncertainty]:
        """
        Returns the local MSX constant uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local MSX constant uncertainty.
        """
        return deepcopy(self._local_constants)

    @property
    def local_parameters(self) -> dict[tuple[str, int, str], Uncertainty]:
        """
        Returns the local MSX parameter uncertainty.

        Returns
        -------
        dict[tuple[str, int, str], :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local MSX parameter uncertainty.
        """
        return deepcopy(self._local_parameters)

    @property
    def local_patterns(self) -> dict[str, Uncertainty]:
        """
        Returns the local EPANET patterns uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local EPANET patterns uncertainty.
        """
        return deepcopy(self._local_patterns)

    @property
    def local_msx_patterns(self) -> dict[str, Uncertainty]:
        """
        Returns the local EPANET-MSX patterns uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local EPANET-MSX patterns uncertainty.
        """
        return deepcopy(self._local_msx_patterns)

    def get_attributes(self) -> dict:
        attribs = {"global_pipe_length_uncertainty": self._global_pipe_length,
                   "global_pipe_roughness_uncertainty": self._global_pipe_roughness,
                   "global_pipe_diameter_uncertainty": self._global_pipe_diameter,
                   "global_base_demand_uncertainty": self._global_base_demand,
                   "global_demand_pattern_uncertainty": self._global_demand_pattern,
                   "global_elevation_uncertainty": self._global_elevation,
                   "global_constants_uncertainty": self._global_constants,
                   "global_parameters_uncertainty": self._global_parameters,
                   "local_pipe_length_uncertainty": self._local_pipe_length,
                   "local_pipe_roughness_uncertainty": self._local_pipe_roughness,
                   "local_pipe_diameter_uncertainty": self._local_pipe_diameter,
                   "local_base_demand_uncertainty": self._local_base_demand,
                   "local_demand_pattern_uncertainty": self._local_demand_pattern,
                   "local_elevation_uncertainty": self._local_elevation,
                   "local_constants_uncertainty": self._local_constants,
                   "local_parameters_uncertainty": self._local_parameters,
                   "local_patterns_uncertainty": self._local_patterns,
                   "local_msx_patterns_uncertainty": self._local_msx_patterns,
                   "seed": self.__seed}

        return super().get_attributes() | attribs

    def __eq__(self, other) -> bool:
        if not isinstance(other, ModelUncertainty):
            raise TypeError("Can not compare 'ModelUncertainty' instance " +
                            f"with '{type(other)}' instance")

        return self._global_pipe_length == other.global_pipe_length \
            and self._global_pipe_roughness == other.global_pipe_roughness \
            and self._global_pipe_diameter == other.global_pipe_diameter \
            and self._global_base_demand == other.global_base_demand \
            and self._global_demand_pattern == other.global_demand_pattern \
            and self._global_elevation == other.global_elevation \
            and self._global_parameters == other.global_parameters \
            and self._global_constants == other.global_constants \
            and self._local_pipe_length == other.local_pipe_length \
            and self._local_pipe_roughness == other.local_pipe_roughness \
            and self._local_pipe_diameter == other.local_pipe_diameter \
            and self._local_base_demand == other.local_base_demand \
            and self._local_demand_pattern == other.local_demand_pattern \
            and self._local_elevation == other.local_elevation \
            and self._local_parameters == other.local_parameters \
            and self._local_constants == other.local_constants \
            and self._local_patterns == other.local_patterns \
            and self._local_msx_patterns == other.local_msx_patterns \
            and self.__seed == other.seed

    def __str__(self) -> str:
        return f"global_pipe_length: {self._global_pipe_length} " +\
            f"global_pipe_roughness: {self._global_pipe_roughness} " + \
            f"global_pipe_diameter: {self._global_pipe_diameter} " + \
            f"global_demand_base: {self._global_base_demand} " + \
            f"global_demand_pattern: {self._global_demand_pattern} " + \
            f"global_elevation: {self._global_elevation} " + \
            f"global_constants: {self._global_constants} " + \
            f"global_parameters: {self._global_parameters}" + \
            f"local_pipe_length: {self._local_pipe_length} " +\
            f"local_pipe_roughness: {self._local_pipe_roughness} " + \
            f"local_pipe_diameter: {self._local_pipe_diameter} " + \
            f"local_demand_base: {self._local_base_demand} " + \
            f"local_demand_pattern: {self._local_demand_pattern} " + \
            f"local_elevation: {self._local_elevation} " + \
            f"local_constants: {self._local_constants} " + \
            f"local_parameters: {self._local_parameters} " + \
            f"local_patterns: {self._local_patterns} " + \
            f"local_msx_patterns: {self._local_msx_patterns} + seed: {self.__seed}"

    def undo(self, epanet_api: EPyT) -> None:
        """
        Undo all applied uncertainties -- i.e, resets the properties to their original value.

        Note that this function can only be used if `cache_original` (of the constructor)
        was set to True (default).

        Parameters
        ----------
        epanet_api : `epanet_plus.EPyT <https://epanet-plus.readthedocs.io/en/stable/api.html#epanet_plus.epanet_toolkit.EPyT>`_
            Interface to EPANET and EPANET-MSX
        """
        if self.__cache_original is False:
            raise ValueError("Caching was disabled by the user")

        if self._cache_links_length is not None:
            for link_idx, link_len in zip(epanet_api.get_all_links_idx(),
                                          self._cache_links_length):
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_LENGTH, link_len)

        if self._cache_links_diameter is not None:
            for link_idx, link_diam in zip(epanet_api.get_all_links_idx(),
                                           self._cache_links_diameter):
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_DIAMETER, link_diam)

        if self._cache_links_roughness_coeff is not None:
            for link_idx, link_roughness in zip(epanet_api.get_all_links_idx(),
                                                self._cache_links_roughness_coeff):
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_ROUGHNESS, link_roughness)

        if self._cache_nodes_base_demand is not None:
            for node_idx in self._cache_nodes_base_demand.keys():
                for demand_category, base_demand in self._cache_nodes_base_demand[node_idx].items():
                    epanet_api.setbasedemand(node_idx, demand_category + 1, base_demand)

        if self._cache_nodes_demand_pattern is not None:
            for pattern_idx, demand_pattern in self._cache_nodes_demand_pattern.items():
                epanet_api.set_pattern(pattern_idx, demand_pattern.tolist())

        if self._cache_nodes_elevation is not None:
            for node_idx, node_elev in zip(epanet_api.get_all_nodes_idx(),
                                           self._cache_nodes_elevation):
                epanet_api.setnodevalue(node_idx, EpanetConstants.EN_ELEVATION, node_elev)

        if self._cache_patterns is not None:
            for pattern_idx, pattern in self._cache_patterns.items():
                epanet_api.set_pattern(pattern_idx, pattern.tolist())

        if self._cache_msx_constants is not None:
            for constant_idx, constant_value in enumerate(self._cache_msx_constants):
                epanet_api.MSXsetconstant(constant_idx + 1, constant_value)

        if self._cache_msx_links_parameters is not None:
            for pipe_idx, parameters_pipes_val in self._cache_msx_links_parameters.items():
                for param_idx, param_value in enumerate(parameters_pipes_val):
                    epanet_api.MSXsetparameter(EpanetConstants.MSX_LINK, pipe_idx,
                                               param_idx + 1, param_value)

        if self._cache_msx_tanks_parameters is not None:
            for tank_idx, parameters_tanks_val in self._cache_msx_tanks_parameters.items():
                for param_idx, param_value in enumerate(parameters_tanks_val):
                    epanet_api.MSXsetparameter(EpanetConstants.MSX_NODE, tank_idx,
                                               param_idx + 1, param_value)

        if self._cache_msx_patterns is not None:
            for pattern_idx, pattern in self._cache_msx_patterns:
                epanet_api.MSXsetpattern(pattern_idx, pattern.tolist(), len(pattern))

    def apply(self, epanet_api: EPyT) -> None:
        """
        Applies the specified model uncertainties to the scenario.

        Parameters
        ----------
        epanet_api : `epanet_plus.EPyT <https://epanet-plus.readthedocs.io/en/stable/api.html#epanet_plus.epanet_toolkit.EPyT>`_
            Interface to EPANET and EPANET-MSX.
        """
        np_rand_gen = np.random.default_rng(seed=self.__seed)

        all_links_idx = epanet_api.get_all_links_idx()
        all_nodes_idx = epanet_api.get_all_nodes_idx()

        if self._global_pipe_length is not None:
            self._global_pipe_length.set_random_generator(np_rand_gen)

            link_length = np.array([epanet_api.getlinkvalue(link_idx, EpanetConstants.EN_LENGTH)
                                    for link_idx in all_links_idx])
            self._cache_links_length = np.copy(link_length)

            link_length = self._global_pipe_length.apply_batch(link_length)
            for link_idx, link_value in zip(all_links_idx, link_length):
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_LENGTH, link_value)

        if self._local_pipe_length is not None:
            self._local_pipe_length.set_random_generator(np_rand_gen)
            self._cache_links_length = np.array([epanet_api.getlinkvalue(link_idx, EpanetConstants.EN_LENGTH)
                                                 for link_idx in all_links_idx])

            for pipe_id, uncertainty in self._local_pipe_length.items():
                link_idx = epanet_api.get_link_idx(pipe_id)
                link_length = epanet_api.getlinkvalue(link_idx, EpanetConstants.EN_LENGTH)

                link_length = uncertainty.apply(link_length)
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_LENGTH, link_length)

        if self._global_pipe_diameter is not None:
            self._global_pipe_diameter.set_random_generator(np_rand_gen)

            link_diameters = np.array([epanet_api.getlinkvalue(link_idx, EpanetConstants.EN_DIAMETER)
                                       for link_idx in all_links_idx])
            self._cache_links_diameter = np.copy(link_diameters)

            link_diameters = self._global_pipe_diameter.apply_batch(link_diameters)
            for link_idx, link_value in zip(all_links_idx, link_diameters):
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_DIAMETER, link_value)

        if self._local_pipe_diameter is not None:
            self._local_pipe_diameter.set_random_generator(np_rand_gen)
            self._cache_links_diameter = np.array([epanet_api.getlinkvalue(link_idx,
                                                                           EpanetConstants.EN_DIAMETER)
                                                   for link_idx in all_links_idx])

            for pipe_id, uncertainty in self._local_pipe_diameter.items():
                link_idx = epanet_api.get_link_idx(pipe_id)
                link_diameter = epanet_api.getlinkvalue(link_idx, EpanetConstants.EN_DIAMETER)

                link_diameter = uncertainty.apply(link_diameter)
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_DIAMETER, link_diameter)

        if self._global_pipe_roughness is not None:
            self._global_pipe_roughness.set_random_generator(np_rand_gen)

            coeffs = np.array([epanet_api.getlinkvalue(link_idx, EpanetConstants.EN_ROUGHNESS)
                               for link_idx in all_links_idx])
            self._cache_links_roughness_coeff = np.copy(coeffs)

            coeffs = self._global_pipe_roughness.apply_batch(coeffs)
            for link_idx, link_value in zip(all_links_idx, coeffs):
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_ROUGHNESS, link_value)

        if self._local_pipe_roughness is not None:
            self._local_pipe_roughness.set_random_generator(np_rand_gen)
            self._cache_links_roughness_coeff = \
                np.array([epanet_api.getlinkvalue(link_idx, EpanetConstants.EN_ROUGHNESS)
                          for link_idx in all_links_idx])

            for pipe_id, uncertainty in self._local_pipe_roughness.items():
                link_idx = epanet_api.get_link_idx(pipe_id)
                link_roughness_coeff = epanet_api.getlinkvalue(link_idx,
                                                               EpanetConstants.EN_ROUGHNESS)

                link_roughness_coeff = uncertainty.apply(link_roughness_coeff)
                epanet_api.setlinkvalue(link_idx, EpanetConstants.EN_ROUGHNESS,
                                        link_roughness_coeff)

        if self._global_base_demand is not None:
            self._global_base_demand.set_random_generator(np_rand_gen)

            self._cache_nodes_base_demand = {}
            for node_idx in all_nodes_idx:
                self._cache_nodes_base_demand[node_idx] = {}
                n_demand_categories = epanet_api.getnumdemands(node_idx)
                for demand_idx in range(n_demand_categories):
                    base_demand = epanet_api.getbasedemand(node_idx, demand_idx + 1)
                    self._cache_nodes_base_demand[node_idx][demand_idx] = base_demand

                    base_demand = self._global_base_demand.apply(base_demand)
                    epanet_api.setbasedemand(node_idx, demand_idx + 1, base_demand)

        if self._local_base_demand is not None:
            self._local_base_demand.set_random_generator(np_rand_gen)

            self._cache_nodes_base_demand = {}
            for node_id, uncertainty in self._local_base_demand.items():
                node_idx = epanet_api.get_node_idx(node_id)
                self._cache_nodes_base_demand[node_idx] = {}
                n_demand_categories = epanet_api.getnumdemands(node_idx)
                for demand_idx in range(n_demand_categories):
                    base_demand = epanet_api.getbasedemand(node_idx, demand_idx + 1)
                    self._cache_nodes_base_demand[node_idx][demand_idx] = base_demand

                    base_demand = uncertainty.apply(base_demand)
                    epanet_api.setbasedemand(node_idx, demand_idx + 1, base_demand)

        if self._global_demand_pattern is not None:
            self._global_demand_pattern.set_random_generator(np_rand_gen)

            self._cache_nodes_demand_pattern = {}
            demand_patterns_idx = np.array([epanet_api.getdemandpattern(node_idx, demand_idx + 1)
                                            for node_idx in epanet_api.get_all_nodes_idx()
                                            for demand_idx in range(epanet_api.getnumdemands(node_idx))])

            for pattern_idx in list(set(demand_patterns_idx)):
                demand_pattern = np.array(epanet_api.get_pattern(pattern_idx))
                self._cache_nodes_demand_pattern[pattern_idx] = np.copy(demand_pattern)

                demand_pattern = self._global_demand_pattern.apply_batch(demand_pattern)
                epanet_api.set_pattern(pattern_idx, demand_pattern.tolist())

        if self._local_demand_pattern is not None:
            self._local_demand_pattern.set_random_generator(np_rand_gen)

            self._cache_nodes_demand_pattern = {}

            for pattern_id, uncertainty in self._local_demand_pattern.items():
                pattern_idx = epanet_api.getpatternindex(pattern_id)
                demand_pattern = np.array(epanet_api.get_pattern(pattern_idx))
                self._cache_nodes_demand_pattern[pattern_id] = np.copy(demand_pattern)

                demand_pattern = uncertainty.apply_batch(demand_pattern)
                epanet_api.set_pattern(pattern_idx, demand_pattern.tolist())

        if self._global_elevation is not None:
            self._global_elevation.set_random_generator(np_rand_gen)

            elevations = np.array([epanet_api.get_node_elevation(node_idx)
                                   for node_idx in epanet_api.get_all_nodes_idx()])
            self._cache_nodes_elevation = np.copy(elevations)

            elevations = self._global_elevation.apply_batch(elevations)
            for node_idx, node_elev in enumerate(elevations):
                epanet_api.setnodevalue(node_idx + 1, EpanetConstants.EN_ELEVATION, node_elev)

        if self._local_elevation is not None:
            self._local_elevation.set_random_generator(np_rand_gen)
            self._cache_nodes_elevation = np.array([epanet_api.get_node_elevation(node_idx)
                                                    for node_idx in epanet_api.get_all_nodes_idx()])

            for node_id, uncertainty in self._local_elevation.items():
                node_idx = epanet_api.get_node_idx(node_id)
                elevation = epanet_api.get_node_elevation(node_idx)

                elevation = uncertainty.apply(elevation)
                epanet_api.setnodevalue(node_idx, EpanetConstants.EN_ELEVATION, elevation)

        if self._local_patterns is not None:
            self._local_patterns.set_random_generator(np_rand_gen)
            self._cache_patterns = {}

            for pattern_id, uncertainty in self._local_patterns.items():
                pattern_idx = epanet_api.getpatternindex(pattern_id)
                pattern = np.array(epanet_api.get_pattern(pattern_idx))
                self._cache_patterns[pattern_idx] = np.copy(pattern)

                pattern = uncertainty.apply_batch(pattern)
                epanet_api.set_pattern(pattern_idx, pattern.tolist())

        if epanet_api.msx_file is not None:
            if self._global_constants is not None:
                self._global_constants.set_random_generator(np_rand_gen)

                constants = np.array([epanet_api.MSXgetconstant(const_idx + 1)
                                      for const_idx in range(epanet_api.MSXgetcount(EpanetConstants.MSX_CONSTANT))])
                self._cache_msx_patterns = np.copy(constants)

                constants = self._global_constants.apply_batch(constants)
                for const_idx, const_value in enumerate(constants):
                    epanet_api.MSXsetconstant(const_idx + 1, const_value)

            if self._local_constants:
                self._local_constants.set_random_generator(np_rand_gen)

                self._cache_msx_patterns = np.array([epanet_api.MSXgetconstant(const_idx + 1)
                                                     for const_idx in range(epanet_api.MSXgetcount(EpanetConstants.MSX_CONSTANT))])

                for constant_id, uncertainty in self._local_constants.items():
                    idx = epanet_api.MSXgetindex(EpanetConstants.MSX_CONSTANT, constant_id)
                    constant = epanet_api.MSXgetconstant(idx)

                    constant = uncertainty.apply(constant)
                    epanet_api.MSXsetconstant(idx, constant)

            if self._global_parameters is not None:
                self._global_parameters.set_random_generator(np_rand_gen)

                self._cache_msx_links_parameters = {}
                num_params = epanet_api.MSXgetcount(EpanetConstants.MSX_PARAMETER)
                parameters_pipes = [np.array([epanet_api.MSXgetparameter(EpanetConstants.MSX_LINK,
                                                                         pipe_idx,
                                                                         param_idx + 1)
                                              for param_idx in range(num_params)])
                                     for pipe_idx in epanet_api.get_all_pipes_idx()]
                for i, pipe_idx in enumerate(epanet_api.get_all_pipes_idx()):
                    if len(parameters_pipes[i]) == 0:
                        continue

                    self._cache_msx_links_parameters[pipe_idx] = parameters_pipes[i]
                    parameters_pipes_val = self._global_parameters.apply_batch(parameters_pipes[i])
                    for param_idx, param_value in enumerate(parameters_pipes_val):
                        epanet_api.MSXsetparameter(EpanetConstants.MSX_LINK, pipe_idx,
                                                   param_idx + 1, param_value)

                self._cache_msx_tanks_parameters = {}
                num_params = epanet_api.MSXgetcount(EpanetConstants.MSX_PARAMETER)
                parameters_tanks = [np.array([epanet_api.MSXgetparameter(EpanetConstants.MSX_NODE,
                                                                         tank_idx + 1, param_idx + 1)
                                              for param_idx in range(num_params)])
                                     for tank_idx in range(epanet_api.get_num_tanks())]
                for i, tank_idx in enumerate(epanet_api.get_all_tanks_idx()):
                    if parameters_tanks[i] is None or len(parameters_tanks[i]) == 0:
                        continue

                    self._cache_msx_tanks_parameters[tank_idx] = parameters_tanks[i]
                    parameters_tanks_val = self._global_parameters.apply_batch(parameters_tanks[i])
                    for idx, val in enumerate(parameters_tanks_val):
                        epanet_api.MSXsetparameter(EpanetConstants.MSX_NODE, tank_idx, idx + 1, val)

            if self._local_parameters is not None:
                self._local_parameters.set_random_generator(np_rand_gen)
                self._cache_msx_links_parameters = {}
                self._cache_msx_tanks_parameters = {}

                for (param_id, item_type, item_id), uncertainty in self._local_parameters.items():
                    idx, = epanet_api.MSXgetindex(EpanetConstants.MSX_PARAMETER, param_id)

                    if item_type == EpanetConstants.MSX_NODE:
                        item_idx = epanet_api.get_node_idx(item_id)
                    elif item_type == EpanetConstants.MSX_LINK:
                        item_idx = epanet_api.get_link_idx(item_id)
                    else:
                        raise ValueError(f"Unknown item type '{item_type}' must be either " +
                                         "EpanetConstants.MSX_NODE or EpanetConstants.MSX_LINK")

                    parameter = epanet_api.MSXgetparameter(item_type, item_idx, idx)
                    if item_type == EpanetConstants.MSX_NODE:
                        self._cache_msx_tanks_parameters[item_idx] = parameter
                    elif item_type == EpanetConstants.MSX_LINK:
                        self._cache_msx_links_parameters[item_idx] = parameter

                    parameter = uncertainty.apply(parameter)
                    epanet_api.MSXsetparameter(item_type, item_idx, idx, parameter)

            if self._local_msx_patterns is not None:
                self._local_msx_patterns.set_random_generator(np_rand_gen)
                self._cache_msx_patterns = {}

                for pattern_id, uncertainty in self._local_msx_patterns.items():
                    pattern_idx = epanet_api.MSXgetindex(EpanetConstants.MSX_PATTERN, pattern_id)
                    pattern = np.array(epanet_api.get_msx_pattern(pattern_idx))
                    self._cache_msx_patterns[pattern_idx] = np.copy(pattern)

                    pattern = uncertainty.apply_batch(pattern)
                    epanet_api.MSXsetpattern(pattern_idx, pattern.tolist(), len(pattern))
        else:
            if self._local_msx_patterns is not None or self._local_parameters is not None or \
                    self._local_constants is not None or self._global_constants is not None or \
                    self._global_parameters is not None:
                warnings.warn("Ignoring EPANET-MSX uncertainties because not .msx file was loaded")
