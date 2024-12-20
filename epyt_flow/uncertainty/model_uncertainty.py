"""
Module provides a class for implementing model uncertainty.
"""
from copy import deepcopy
import warnings
import epyt
from epyt.epanet import ToolkitConstants
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
    """
    def __init__(self, pipe_length_uncertainty: Uncertainty = None,
                 pipe_roughness_uncertainty: Uncertainty = None,
                 pipe_diameter_uncertainty: Uncertainty = None,
                 base_demand_uncertainty: Uncertainty = None,
                 demand_pattern_uncertainty: Uncertainty = None,
                 elevation_uncertainty: Uncertainty = None,
                 constants_uncertainty: Uncertainty = None,
                 parameters_uncertainty: Uncertainty = None,
                 global_pipe_length_uncertainty: Uncertainty = None,
                 global_pipe_roughness_uncertainty: Uncertainty = None,
                 global_pipe_diameter_uncertainty: Uncertainty = None,
                 global_base_demand_uncertainty: Uncertainty = None,
                 global_demand_pattern_uncertainty: Uncertainty = None,
                 global_elevation_uncertainty: Uncertainty = None,
                 global_constants_uncertainty: Uncertainty = None,
                 global_parameters_uncertainty: Uncertainty = None,
                 local_pipe_length_uncertainty: dict[str, Uncertainty] = None,
                 local_pipe_roughness_uncertainty: dict[str, Uncertainty] = None,
                 local_pipe_diameter_uncertainty: dict[str, Uncertainty] = None,
                 local_base_demand_uncertainty: dict[str, Uncertainty] = None,
                 local_demand_pattern_uncertainty: dict[str, Uncertainty] = None,
                 local_elevation_uncertainty: dict[str, Uncertainty] = None,
                 local_constants_uncertainty: dict[str, Uncertainty] = None,
                 local_parameters_uncertainty: dict[str, int, Uncertainty] = None,
                 local_patterns_uncertainty: dict[str, Uncertainty] = None,
                 local_msx_patterns_uncertainty: dict[str, Uncertainty] = None,
                 **kwds):
        if pipe_length_uncertainty is not None:
            global_pipe_diameter_uncertainty = pipe_length_uncertainty
            warnings.warn("'pipe_length_uncertainty' is deprecated and " +
                          "will be removed in future releases")
        if pipe_roughness_uncertainty is not None:
            global_pipe_roughness_uncertainty = pipe_roughness_uncertainty
            warnings.warn("'pipe_roughness_uncertainty' is deprecated and " +
                          "will be removed in future releases")
        if pipe_diameter_uncertainty is not None:
            global_pipe_diameter_uncertainty = pipe_diameter_uncertainty
            warnings.warn("'pipe_diameter_uncertainty' is deprecated and " +
                          "will be removed in future releases")
        if base_demand_uncertainty is not None:
            global_base_demand_uncertainty = base_demand_uncertainty
            warnings.warn("'base_demand_uncertainty' is deprecated and " +
                          "will be removed in future releases")
        if demand_pattern_uncertainty is not None:
            global_demand_pattern_uncertainty = demand_pattern_uncertainty
            warnings.warn("'demand_pattern_uncertainty' is deprecated and " +
                          "will be removed in future releases")
        if elevation_uncertainty is not None:
            global_elevation_uncertainty = elevation_uncertainty
            warnings.warn("'elevation_uncertainty' is deprecated and " +
                          "will be removed in future releases")
        if constants_uncertainty is not None:
            global_constants_uncertainty = constants_uncertainty
            warnings.warn("'constants_uncertainty' is deprecated and " +
                          "will be removed in future releases")
        if parameters_uncertainty is not None:
            global_parameters_uncertainty = parameters_uncertainty
            warnings.warn("'parameters_uncertainty' is deprecated and " +
                          "will be removed in future releases")

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

        self.__global_pipe_length = global_pipe_length_uncertainty
        self.__global_pipe_roughness = global_pipe_roughness_uncertainty
        self.__global_pipe_diameter = global_pipe_diameter_uncertainty
        self.__global_base_demand = global_base_demand_uncertainty
        self.__global_demand_pattern = global_demand_pattern_uncertainty
        self.__global_elevation = global_elevation_uncertainty
        self.__global_constants = global_constants_uncertainty
        self.__global_parameters = global_parameters_uncertainty
        self.__local_pipe_length = local_pipe_length_uncertainty
        self.__local_pipe_roughness = local_pipe_roughness_uncertainty
        self.__local_pipe_diameter = local_pipe_diameter_uncertainty
        self.__local_base_demand = local_base_demand_uncertainty
        self.__local_demand_pattern = local_demand_pattern_uncertainty
        self.__local_elevation = local_elevation_uncertainty
        self.__local_constants = local_constants_uncertainty
        self.__local_parameters = local_parameters_uncertainty
        self.__local_patterns = local_patterns_uncertainty
        self.__local_msx_patterns = local_msx_patterns_uncertainty

        super().__init__(**kwds)

    @property
    def global_pipe_length(self) -> Uncertainty:
        """
        Returns the global pipe length uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global pipe length uncertainty.
        """
        return deepcopy(self.__global_pipe_length)

    @property
    def global_pipe_roughness(self) -> Uncertainty:
        """
        Returns the global pipe roughness uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global pipe roughness uncertainty.
        """
        return deepcopy(self.__global_pipe_roughness)

    @property
    def global_pipe_diameter(self) -> Uncertainty:
        """
        Returns the global pipe diameter uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global pipe diameter uncertainty.
        """
        return deepcopy(self.__global_pipe_diameter)

    @property
    def global_base_demand(self) -> Uncertainty:
        """
        Returns the global base demand uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global base demand uncertainty.
        """
        return deepcopy(self.__global_base_demand)

    @property
    def global_demand_pattern(self) -> Uncertainty:
        """
        Returns the global demand pattern uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global demand pattern uncertainty.
        """
        return deepcopy(self.__global_demand_pattern)

    @property
    def global_elevation(self) -> Uncertainty:
        """
        Returns the global node elevation uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global node elevation uncertainty.
        """
        return deepcopy(self.__global_elevation)

    @property
    def global_constants(self) -> Uncertainty:
        """
        Returns the global MSX constant uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global MSX constant uncertainty.
        """
        return deepcopy(self.__global_constants)

    @property
    def global_parameters(self) -> Uncertainty:
        """
        Returns the global MSX parameter uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Global MSX parameter uncertainty.
        """
        return deepcopy(self.__global_parameters)

    @property
    def local_pipe_length(self) -> dict[str, Uncertainty]:
        """
        Returns the local pipe length uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local pipe length uncertainty.
        """
        return deepcopy(self.__local_pipe_length)

    @property
    def local_pipe_roughness(self) -> dict[str, Uncertainty]:
        """
        Returns the local pipe roughness uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local pipe roughness uncertainty.
        """
        return deepcopy(self.__local_pipe_roughness)

    @property
    def local_pipe_diameter(self) -> dict[str, Uncertainty]:
        """
        Returns the local pipe diameter uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local pipe diameter uncertainty.
        """
        return deepcopy(self.__local_pipe_diameter)

    @property
    def local_base_demand(self) -> dict[str, Uncertainty]:
        """
        Returns the local base demand uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local base demand uncertainty.
        """
        return deepcopy(self.__local_base_demand)

    @property
    def local_demand_pattern(self) -> dict[str, Uncertainty]:
        """
        Returns the local demand pattern uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local demand pattern uncertainty.
        """
        return deepcopy(self.__local_demand_pattern)

    @property
    def local_elevation(self) -> dict[str, Uncertainty]:
        """
        Returns the local node elevation uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local node elevation uncertainty.
        """
        return deepcopy(self.__local_elevation)

    @property
    def local_constants(self) -> dict[str, Uncertainty]:
        """
        Returns the local MSX constant uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local MSX constant uncertainty.
        """
        return deepcopy(self.__local_constants)

    @property
    def local_parameters(self) -> dict[tuple[str, int, str], Uncertainty]:
        """
        Returns the local MSX parameter uncertainty.

        Returns
        -------
        dict[tuple[str, int, str], :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local MSX parameter uncertainty.
        """
        return deepcopy(self.__local_parameters)

    @property
    def local_patterns(self) -> dict[str, Uncertainty]:
        """
        Returns the local EPANET patterns uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local EPANET patterns uncertainty.
        """
        return deepcopy(self.__local_patterns)

    @property
    def local_msx_patterns(self) -> dict[str, Uncertainty]:
        """
        Returns the local EPANET-MSX patterns uncertainty.

        Returns
        -------
        dict[str, :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`]
            Local EPANET-MSX patterns uncertainty.
        """
        return deepcopy(self.__local_msx_patterns)

    def get_attributes(self) -> dict:
        attribs = {"global_pipe_length_uncertainty": self.__global_pipe_length,
                   "global_pipe_roughness_uncertainty": self.__global_pipe_roughness,
                   "global_pipe_diameter_uncertainty": self.__global_pipe_diameter,
                   "global_base_demand_uncertainty": self.__global_base_demand,
                   "global_demand_pattern_uncertainty": self.__global_demand_pattern,
                   "global_elevation_uncertainty": self.__global_elevation,
                   "global_constants_uncertainty": self.__global_constants,
                   "global_parameters_uncertainty": self.__global_parameters,
                   "local_pipe_length_uncertainty": self.__local_pipe_length,
                   "local_pipe_roughness_uncertainty": self.__local_pipe_roughness,
                   "local_pipe_diameter_uncertainty": self.__local_pipe_diameter,
                   "local_base_demand_uncertainty": self.__local_base_demand,
                   "local_demand_pattern_uncertainty": self.__local_demand_pattern,
                   "local_elevation_uncertainty": self.__local_elevation,
                   "local_constants_uncertainty": self.__local_constants,
                   "local_parameters_uncertainty": self.__local_parameters,
                   "local_patterns_uncertainty": self.__local_patterns,
                   "local_msx_patterns_uncertainty": self.__local_msx_patterns}

        return super().get_attributes() | attribs

    def __eq__(self, other) -> bool:
        if not isinstance(other, ModelUncertainty):
            raise TypeError("Can not compare 'ModelUncertainty' instance " +
                            f"with '{type(other)}' instance")

        return self.__global_pipe_length == other.global_pipe_length \
            and self.__global_pipe_roughness == other.global_pipe_roughness \
            and self.__global_pipe_diameter == other.global_pipe_diameter \
            and self.__global_base_demand == other.global_base_demand \
            and self.__global_demand_pattern == other.global_demand_pattern \
            and self.__global_elevation == other.global_elevation \
            and self.__global_parameters == other.global_parameters \
            and self.__global_constants == other.global_constants \
            and self.__local_pipe_length == other.local_pipe_length \
            and self.__local_pipe_roughness == other.local_pipe_roughness \
            and self.__local_pipe_diameter == other.local_pipe_diameter \
            and self.__local_base_demand == other.local_base_demand \
            and self.__local_demand_pattern == other.local_demand_pattern \
            and self.__local_elevation == other.local_elevation \
            and self.__local_parameters == other.local_parameters \
            and self.__local_constants == other.local_constants \
            and self.__local_patterns == other.local_patterns \
            and self.__local_msx_patterns == other.local_msx_patterns

    def __str__(self) -> str:
        return f"global_pipe_length: {self.__global_pipe_length} " +\
            f"global_pipe_roughness: {self.__global_pipe_roughness} " + \
            f"global_pipe_diameter: {self.__global_pipe_diameter} " + \
            f"global_demand_base: {self.__global_base_demand} " + \
            f"global_demand_pattern: {self.__global_demand_pattern} " + \
            f"global_elevation: {self.__global_elevation} " + \
            f"global_constants: {self.__global_constants} " + \
            f"global_parameters: {self.__global_parameters}" + \
            f"local_pipe_length: {self.__local_pipe_length} " +\
            f"local_pipe_roughness: {self.__local_pipe_roughness} " + \
            f"local_pipe_diameter: {self.__local_pipe_diameter} " + \
            f"local_demand_base: {self.__local_base_demand} " + \
            f"local_demand_pattern: {self.__local_demand_pattern} " + \
            f"local_elevation: {self.__local_elevation} " + \
            f"local_constants: {self.__local_constants} " + \
            f"local_parameters: {self.__local_parameters} " + \
            f"local_patterns: {self.__local_patterns} " + \
            f"local_msx_patterns: {self.__local_msx_patterns}"

    def apply(self, epanet_api: epyt.epanet) -> None:
        """
        Applies the specified model uncertainties to the scenario.

        Parameters
        ----------
        epanet_api : `epyt.epanet <https://epanet-python-toolkit-epyt.readthedocs.io/en/stable/api.html#epyt.epanet.epanet>`_
            Interface to EPANET and EPANET-MSX.
        """
        if self.__global_pipe_length is not None:
            link_length = epanet_api.getLinkLength()
            link_length = self.__global_pipe_length.apply_batch(link_length)
            epanet_api.setLinkLength(link_length)

        if self.__local_pipe_length is not None:
            for pipe_id, uncertainty in self.__local_pipe_length.items():
                link_idx = epanet_api.getLinkIndex(pipe_id)
                link_length = epanet_api.getLinkLength(link_idx)
                link_length = uncertainty.apply(link_length)
                epanet_api.setLinkLength(link_idx, link_length)

        if self.__global_pipe_diameter is not None:
            link_diameters = epanet_api.getLinkDiameter()
            link_diameters = self.__global_pipe_diameter.apply_batch(link_diameters)
            epanet_api.setLinkDiameter(link_diameters)

        if self.__local_pipe_diameter is not None:
            for pipe_id, uncertainty in self.__local_pipe_diameter.items():
                link_idx = epanet_api.getLinkIndex(pipe_id)
                link_diameter = epanet_api.getLinkDiameter(link_idx)
                link_diameter = uncertainty.apply(link_diameter)
                epanet_api.setLinkDiameter(link_idx, link_diameter)

        if self.__global_pipe_roughness is not None:
            coeffs = epanet_api.getLinkRoughnessCoeff()
            coeffs = self.__global_pipe_roughness.apply_batch(coeffs)
            epanet_api.setLinkRoughnessCoeff(coeffs)

        if self.__local_pipe_roughness is not None:
            for pipe_id, uncertainty in self.__local_pipe_roughness.items():
                link_idx = epanet_api.getLinkIndex(pipe_id)
                link_roughness_coeff = epanet_api.getLinkRoughnessCoeff(link_idx)
                link_roughness_coeff = uncertainty.apply(link_roughness_coeff)
                epanet_api.setLinkRoughnessCoeff(link_idx, link_roughness_coeff)

        if self.__global_base_demand is not None:
            all_nodes_idx = epanet_api.getNodeIndex()
            for node_idx in all_nodes_idx:
                n_demand_categories = epanet_api.getNodeDemandCategoriesNumber(node_idx)
                for demand_category in range(n_demand_categories):
                    base_demand = epanet_api.getNodeBaseDemands(node_idx)[demand_category + 1]
                    base_demand = self.__global_base_demand.apply(base_demand)
                    epanet_api.setNodeBaseDemands(node_idx, demand_category + 1, base_demand)

        if self.__local_base_demand is not None:
            for node_id, uncertainty in self.__local_base_demand.items():
                node_idx = epanet_api.getNodeIndex(node_id)
                n_demand_categories = epanet_api.getNodeDemandCategoriesNumber(node_idx)
                for demand_category in range(n_demand_categories):
                    base_demand = epanet_api.getNodeBaseDemands(node_idx)[demand_category + 1]
                    base_demand = uncertainty.apply(base_demand)
                    epanet_api.setNodeBaseDemands(node_idx, demand_category + 1, base_demand)

        if self.__global_demand_pattern is not None:
            demand_patterns_idx = epanet_api.getNodeDemandPatternIndex()
            demand_patterns_id = np.unique([demand_patterns_idx[k]
                                            for k in demand_patterns_idx.keys()])
            for pattern_id in demand_patterns_id:
                if pattern_id == 0:
                    continue
                pattern_length = epanet_api.getPatternLengths(pattern_id)
                for t in range(pattern_length):
                    v = epanet_api.getPatternValue(pattern_id, t+1)
                    v_ = self.__global_demand_pattern.apply(v)
                    epanet_api.setPatternValue(pattern_id, t+1, v_)

        if self.__local_demand_pattern is not None:
            patterns_id = epanet_api.getPatternNameID()
            paterns_idx = epanet_api.getPatternIndex()

            for pattern_id, uncertainty in self.__local_demand_pattern.items():
                pattern_idx = paterns_idx[patterns_id.index(pattern_id)]
                pattern_length, = epanet_api.getPatternLengths(pattern_id)
                for t in range(pattern_length):
                    v = epanet_api.getPatternValue(pattern_idx, t+1)
                    v_ = uncertainty.apply(v)
                    epanet_api.setPatternValue(pattern_idx, t+1, v_)

        if self.__global_elevation is not None:
            elevations = epanet_api.getNodeElevations()
            elevations = self.__global_elevation.apply_batch(elevations)
            epanet_api.setNodeElevations(elevations)

        if self.__local_elevation is not None:
            for node_id, uncertainty in self.__local_elevation.items():
                node_idx = epanet_api.getNodeIndex(node_id)
                elevation = epanet_api.getNodeElevations(node_idx)
                elevation = uncertainty.apply(elevation)
                epanet_api.setNodeElevations(node_idx, elevation)

        if self.__local_patterns is not None:
            for pattern_id, uncertainty in self.__local_patterns.items():
                pattern_idx = epanet_api.getPatternIndex(pattern_id)
                pattern_length = epanet_api.getPatternLengths(pattern_idx)
                pattern = np.array([epanet_api.getPatternValue(pattern_idx, t+1)
                                    for t in range(pattern_length)])
                pattern = uncertainty.apply_batch(pattern)
                epanet_api.setPattern(pattern_idx, pattern)

        if epanet_api.MSXFile is not None:
            if self.__global_constants is not None:
                constants = np.array(epanet_api.getMSXConstantsValue())
                constants = self.__global_constants.apply_batch(constants)
                epanet_api.setMSXConstantsValue(constants)

            if self.__local_constants:
                for constant_id, uncertainty in self.__local_constants.items():
                    idx = epanet_api.MSXgetindex(ToolkitConstants.MSX_CONSTANT, constant_id)
                    constant = epanet_api.msx.MSXgetconstant(idx)
                    constant = uncertainty.apply(constant)
                    epanet_api.msx.MSXsetconstant(idx, constant)

            if self.__global_parameters is not None:
                parameters_pipes = epanet_api.getMSXParametersPipesValue()
                for i, pipe_idx in enumerate(epanet_api.getLinkPipeIndex()):
                    if len(parameters_pipes[i]) == 0:
                        continue

                    parameters_pipes_val = self.__global_parameters.apply_batch(
                        np.array(parameters_pipes[i]))
                    epanet_api.setMSXParametersPipesValue(pipe_idx, parameters_pipes_val)

                parameters_tanks = epanet_api.getMSXParametersTanksValue()
                for i, tank_idx in enumerate(epanet_api.getNodeTankIndex()):
                    if parameters_tanks[i] is None or len(parameters_tanks[i]) == 0:
                        continue

                    parameters_tanks_val = self.__global_parameters.apply_batch(
                        np.array(parameters_tanks[i]))
                    epanet_api.setMSXParametersTanksValue(tank_idx, parameters_tanks_val)

            if self.__local_parameters is not None:
                for (param_id, item_type, item_id), uncertainty in self.__local_parameters.items():
                    idx, = epanet_api.getMSXParametersIndex([param_id])

                    if item_type == ToolkitConstants.MSX_NODE:
                        item_idx = epanet_api.getNodeIndex(item_id)
                    elif item_type == ToolkitConstants.MSX_LINK:
                        item_idx = epanet_api.getLinkIndex(item_id)
                    else:
                        raise ValueError(f"Unknown item type '{item_type}' must be either " +
                                         "ToolkitConstants.MSX_NODE or ToolkitConstants.MSX_LINK")

                    parameter = epanet_api.msx.MSXgetparameter(item_type, item_idx, idx)
                    parameter = uncertainty.apply(parameter)
                    epanet_api.msx.MSXsetparameter(item_type, item_idx, idx, parameter)

            if self.__local_msx_patterns is not None:
                for pattern_id, uncertainty in self.__local_msx_patterns.items():
                    pattern_idx, = epanet_api.getMSXPatternsIndex([pattern_id])
                    pattern = epanet_api.getMSXConstantsValue([pattern_idx])
                    pattern = uncertainty.apply_batch(pattern)
                    epanet_api.setMSXPattern(pattern_idx, pattern)
        else:
            if self.__local_msx_patterns is not None or self.__local_parameters is not None or \
                    self.__local_constants is not None or self.__global_constants is not None or \
                    self.__global_parameters is not None:
                warnings.warn("Ignoring EPANET-MSX uncertainties because not .msx file was loaded")
