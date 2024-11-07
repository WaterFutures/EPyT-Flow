"""
Module provides a class for implementing model uncertainty.
"""
from copy import deepcopy
import warnings
import epyt
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
    pipe_length_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Uncertainty of pipe lengths. None, in the case of no uncertainty.

        The default is None.
    pipe_roughness_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Uncertainty of pipe roughness coefficients. None, in the case of no uncertainty.

        The default is None.
    pipe_diameter_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Uncertainty of pipe diameters. None, in the case of no uncertainty.

        The default is None.
    base_demand_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Uncertainty of base demands. None, in the case of no uncertainty.

        The default is None.
    demand_pattern_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Uncertainty of demand patterns. None, in the case of no uncertainty.

        The default is None.
    elevation_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Uncertainty of elevations. None, in the case of no uncertainty.

        The default is None.
    constants_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Uncertainty of MSX constants. None, in the case of no uncertainty.

        The default is None.
    parameters_uncertainty : :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`, optional
        Uncertainty of MSX parameters. None, in the case of no uncertainty.

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
                 demand_base_uncertainty: Uncertainty = None, **kwds):
        if demand_base_uncertainty is not None:
            warnings.warn("Loading a file that was created with an outdated version of EPyT-Flow" +
                          " -- support of such old files will be removed in the next release!",
                          DeprecationWarning)

        if pipe_length_uncertainty is not None:
            if not isinstance(pipe_length_uncertainty, Uncertainty):
                raise TypeError("'pipe_length_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(pipe_length_uncertainty)}'")
        if pipe_roughness_uncertainty is not None:
            if not isinstance(pipe_roughness_uncertainty, Uncertainty):
                raise TypeError("'pipe_roughness_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(pipe_roughness_uncertainty)}'")
        if pipe_diameter_uncertainty is not None:
            if not isinstance(pipe_diameter_uncertainty, Uncertainty):
                raise TypeError("'pipe_diameter_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(pipe_diameter_uncertainty)}'")
        if base_demand_uncertainty is not None:
            if not isinstance(base_demand_uncertainty, Uncertainty):
                raise TypeError("'base_demand_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(base_demand_uncertainty)}'")
        if demand_pattern_uncertainty is not None:
            if not isinstance(demand_pattern_uncertainty, Uncertainty):
                raise TypeError("'demand_pattern_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(demand_pattern_uncertainty)}'")
        if elevation_uncertainty is not None:
            if not isinstance(elevation_uncertainty, Uncertainty):
                raise TypeError("'elevation_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(elevation_uncertainty)}'")
        if constants_uncertainty is not None:
            if not isinstance(constants_uncertainty, Uncertainty):
                raise TypeError("'constants_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(constants_uncertainty)}'")
        if parameters_uncertainty is not None:
            if not isinstance(parameters_uncertainty, Uncertainty):
                raise TypeError("'parameters_uncertainty' must be an instance of " +
                                "'epyt_flow.uncertainty.Uncertainty' but not of " +
                                f"'{type(parameters_uncertainty)}'")

        self.__pipe_length = pipe_length_uncertainty
        self.__pipe_roughness = pipe_roughness_uncertainty
        self.__pipe_diameter = pipe_diameter_uncertainty
        self.__base_demand = base_demand_uncertainty
        self.__demand_pattern = demand_pattern_uncertainty
        self.__elevation = elevation_uncertainty
        self.__constants = constants_uncertainty
        self.__parameters = parameters_uncertainty

        super().__init__(**kwds)

    @property
    def pipe_length(self) -> Uncertainty:
        """
        Gets the pipe length uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Pipe length uncertainty.
        """
        return deepcopy(self.__pipe_length)

    @property
    def pipe_roughness(self) -> Uncertainty:
        """
        Gets the pipe roughness uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Pipe roughness uncertainty.
        """
        return deepcopy(self.__pipe_roughness)

    @property
    def pipe_diameter(self) -> Uncertainty:
        """
        Gets the pipe diameter uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Pipe diameter uncertainty.
        """
        return deepcopy(self.__pipe_diameter)

    @property
    def base_demand(self) -> Uncertainty:
        """
        Gets the base demand uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Demand base uncertainty.
        """
        return deepcopy(self.__base_demand)

    @property
    def demand_pattern(self) -> Uncertainty:
        """
        Gets the demand pattern uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Demand pattern uncertainty.
        """
        return deepcopy(self.__demand_pattern)

    @property
    def elevation(self) -> Uncertainty:
        """
        Gets the node elevation uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            Node elevation uncertainty.
        """
        return deepcopy(self.__elevation)

    @property
    def constants(self) -> Uncertainty:
        """
        Gets the MSX constant uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            MSX constant uncertainty.
        """
        return deepcopy(self.__constants)

    @property
    def parameters(self) -> Uncertainty:
        """
        Gets the MSX parameter uncertainty.

        Returns
        -------
        :class:`~epyt_flow.uncertainty.uncertainties.Uncertainty`
            MSX parameter uncertainty.
        """
        return deepcopy(self.__parameters)

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"pipe_length_uncertainty": self.__pipe_length,
                                           "pipe_roughness_uncertainty": self.__pipe_roughness,
                                           "pipe_diameter_uncertainty": self.__pipe_diameter,
                                           "base_demand_uncertainty": self.__base_demand,
                                           "demand_pattern_uncertainty": self.__demand_pattern,
                                           "elevation_uncertainty": self.__elevation,
                                           "constants_uncertainty": self.__constants,
                                           "parameters_uncertainty": self.__parameters}

    def __eq__(self, other) -> bool:
        if not isinstance(other, ModelUncertainty):
            raise TypeError("Can not compare 'ModelUncertainty' instance " +
                            f"with '{type(other)}' instance")

        return self.__pipe_length == other.pipe_length \
            and self.__pipe_roughness == other.pipe_roughness \
            and self.__pipe_diameter == other.pipe_diameter \
            and self.__base_demand == other.base_demand \
            and self.__demand_pattern == other.demand_pattern \
            and self.__elevation == other.elevation \
            and self.__parameters == other.parameters and self.__constants == other.constants

    def __str__(self) -> str:
        return f"pipe_length: {self.__pipe_length} pipe_roughness: {self.__pipe_roughness} " + \
            f"pipe_diameter: {self.__pipe_diameter} demand_base: {self.__base_demand} " + \
            f"demand_pattern: {self.__demand_pattern} elevation: {self.__elevation} " + \
            f"constants: {self.__constants} parameters: {self.__parameters}"

    def apply(self, epanet_api: epyt.epanet) -> None:
        """
        Applies the specified model uncertainties to the scenario.

        Parameters
        ----------
        epanet_api : `epyt.epanet`
            Interface to EPANET and EPANET-MSX.
        """
        if self.__pipe_length is not None:
            link_length = epanet_api.getLinkLength()
            link_length = self.__pipe_length.apply_batch(link_length)
            epanet_api.setLinkLength(link_length)

        if self.__pipe_diameter is not None:
            link_diameters = epanet_api.getLinkDiameter()
            link_diameters = self.__pipe_diameter.apply_batch(link_diameters)
            epanet_api.setLinkDiameter(link_diameters)

        if self.__pipe_roughness is not None:
            coeffs = epanet_api.getLinkRoughnessCoeff()
            coeffs = self.__pipe_roughness.apply_batch(coeffs)
            epanet_api.setLinkRoughnessCoeff(coeffs)

        if self.__base_demand is not None:
            all_nodes_idx = epanet_api.getNodeIndex()
            for node_idx in all_nodes_idx:
                n_demand_categories = epanet_api.getNodeDemandCategoriesNumber(node_idx)
                for demand_category in range(n_demand_categories):
                    base_demand = epanet_api.getNodeBaseDemands(node_idx)[demand_category + 1]
                    base_demand = self.__base_demand.apply(base_demand)
                    epanet_api.setNodeBaseDemands(node_idx, demand_category + 1, base_demand)

        if self.__demand_pattern is not None:
            demand_patterns_idx = epanet_api.getNodeDemandPatternIndex()
            demand_patterns_id = np.unique([demand_patterns_idx[k]
                                            for k in demand_patterns_idx.keys()])
            for pattern_id in demand_patterns_id:
                if pattern_id == 0:
                    continue
                pattern_length = epanet_api.getPatternLengths(pattern_id)
                for t in range(pattern_length):
                    v = epanet_api.getPatternValue(pattern_id, t+1)
                    epanet_api.setPatternValue(pattern_id, t+1, self.__demand_pattern.apply(v))

        if self.__elevation is not None:
            elevations = epanet_api.getNodeElevations()
            elevations = self.__elevation.apply_batch(elevations)
            epanet_api.setNodeElevations(elevations)

        if self.__constants is not None:
            constants = np.array(epanet_api.getMSXConstantsValue())
            constants = self.__constants.apply_batch(constants)
            epanet_api.setMSXConstantsValue(constants)

        if self.__parameters is not None:
            parameters_pipes = epanet_api.getMSXParametersPipesValue()
            for i, pipe_idx in enumerate(epanet_api.getLinkPipeIndex()):
                if len(parameters_pipes[i]) == 0:
                    continue

                parameters_pipes_val = self.__parameters.apply_batch(np.array(parameters_pipes[i]))
                epanet_api.setMSXParametersPipesValue(pipe_idx, parameters_pipes_val)

            parameters_tanks = epanet_api.getMSXParametersTanksValue()
            for i, tank_idx in enumerate(epanet_api.getNodeTankIndex()):
                if parameters_tanks[i] is None or len(parameters_tanks[i]) == 0:
                    continue

                parameters_tanks_val = self.__parameters.apply_batch(np.array(parameters_tanks[i]))
                epanet_api.setMSXParametersTanksValue(tank_idx, parameters_tanks_val)
