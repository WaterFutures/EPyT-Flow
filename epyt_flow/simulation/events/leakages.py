"""
Module provides classes for implementing leakages.
"""
from copy import deepcopy
import math
import numpy as np
import epyt

from .system_event import SystemEvent
from ...serialization import serializable, JsonSerializable, \
    LEAKAGE_ID, ABRUPT_LEAKAGE_ID, INCIPIENT_LEAKAGE_ID


@serializable(LEAKAGE_ID, ".epytflow_leakage")
class Leakage(SystemEvent, JsonSerializable):
    """
    Base class for a leakage.

    Parameters
    ----------
    link_id : `str`
        ID of the link at which the leak is placed.
        Note that if the leak is placed at a node, then 'link_id' must be None and the
        ID of the node must be set in 'node_id'
    diameter : `float`
        Diameter of this leak.
    profile : `numpy.ndarray`
        Pattern of this leak.
    node_id : `str`, optional
        ID of the node at which the leak is placed.
        This parameter must only be set if the leak is placed at a node instead of a link.
        In this case, 'link_id' must be None.

        The default is None.
    """
    def __init__(self, link_id: str, diameter: float, profile: np.ndarray, node_id: str = None,
                 **kwds):
        if link_id is not None and node_id is not None:
            raise ValueError("Leak can not be placed at a link and node at the same time")
        if link_id is None and node_id is None:
            raise ValueError("Leak must be placed at either a link or a node -- " +
                             "expecting either 'link_id' or 'node_id' but both are None")
        if link_id is not None:
            if not isinstance(link_id, str):
                raise TypeError("'link_id' must be an instance of 'str' " +
                                f"but not of '{type(link_id)}'")
        if not isinstance(diameter, float):
            raise TypeError("'diameter must be an instance of 'float' but " +
                            f"not of '{type(diameter)}'")
        if diameter <= 0:
            raise ValueError("'diameter' must be greater than zero")
        if profile is not None:
            if not isinstance(profile, np.ndarray):
                raise TypeError("'profile' must be an instance of 'numpy.ndarray' but " +
                                f"not of '{type(profile)}'")
            if len(profile.shape) > 1:
                raise ValueError("'profile' must be a one-dimensional array " +
                                 f"but not of shape '{profile.shape}'")
        if node_id is not None:
            if not isinstance(node_id, str):
                raise TypeError("'node_id' must be an instance of 'str' " +
                                f"but not of '{type(node_id)}'")

        self.__link_id = link_id
        self.__node_id = node_id
        self.__diameter = diameter
        self.__profile = profile

        self.__leaky_node_id = None
        self.__leak_emitter_coef = None
        self.__time_pattern_idx = 0

        super().__init__(**kwds)

    @property
    def link_id(self) -> str:
        """
        Gets the ID of the link at which the leak is placed.

        Returns
        -------
        `str`
            ID of the link at which the leak is placed.
        """
        return self.__link_id

    @property
    def node_id(self) -> str:
        """
        Gets the ID of the node at which the leak is placed.

        Returns
        -------
        `str`
            ID of the node at which the leak is placed.
        """
        return self.__node_id

    @property
    def diameter(self) -> float:
        """
        Gets the diameter of the leak.

        Returns
        -------
        `float`
            Diameter of the leak.
        """
        return self.__diameter

    @property
    def profile(self) -> np.ndarray:
        """
        Gets the pattern of the leak.

        Returns
        -------
        `numpy.ndarray`
            Pattern of the leak.
        """
        return deepcopy(self.__profile)

    @profile.setter
    def profile(self, pattern: np.ndarray):
        if not isinstance(pattern, np.ndarray):
            raise TypeError("'profile' must be an instance of 'numpy.ndarray' but " +
                            f"not of '{type(pattern)}'")
        if len(pattern.shape) > 1:
            raise ValueError("'profile' must be a one-dimensional array " +
                             f"but not of shape '{pattern.shape}'")

        self.__profile = pattern

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"link_id": self.link_id, "diameter": self.diameter,
                                           "profile": self.profile,
                                           "node_id": self.__leaky_node_id
                                           if self.link_id is None else None}

    def __eq__(self, other) -> bool:
        if not isinstance(other, Leakage):
            raise TypeError(f"Can not compare 'Leakage' instance with '{type(other)}' instance")

        return super().__eq__(other) and self.__link_id == other.link_id \
            and self.__diameter == other.diameter and self.__profile == other.profile \
            and self.__node_id == other.node_id

    def __str__(self) -> str:
        return f"{super().__str__()} link_id: {self.link_id} diameter: {self.diameter} " +\
            f"profile: {self.profile} node_id: {self.__node_id}"

    def compute_leak_area(self, diameter: float, factor_units: float = 100.) -> float:
        """
        Computes the leak area given the diameter.

        Parameters
        ----------
        diameter : `float`
            Diameter of the leak.
        factor_units : `float`, optional
            Factor for converting units.

            The default is 100 to change the units to EPANET default units.

        Returns
        -------
        `float`
            Leak area.
        """
        return (np.pi * (diameter / 2) ** 2) * factor_units

    def compute_leak_emitter_coefficient(self, area: float, discharg_coef: float = .75,
                                         g: float = 9.8) -> float:
        """
        Computes the leak emitter coefficient.

        emitter_coef = discharg_coef * area * sqrt(2*g)   where g = 9.8, discharg_coef = .75

        leak_demand = emitter_coef * pressure^alpha       where alpha = .5

        Parameters
        ----------
        area : `float`
            Leak area as computed in
            :func:`epyt_flow.simulation.events.leakages.Leakage.compute_leak_area`.
        discharg_coef : `float`, optional
            Discharg coefficient.

            The default is set to 0.75
        g : `float`, optional
            Gravitational constant. Do not change this!

            The default is 9.8

        Returns
        -------
        `float`
            Leak emitter coefficient.
        """
        return discharg_coef * area * np.sqrt(2. * g)

    def init(self, epanet_api: epyt.epanet) -> None:
        super().init(epanet_api)

        # Split pipe if leak is placed at a link/pipe
        if self.__link_id is not None:
            if self.__link_id not in self._epanet_api.getLinkNameID():
                raise ValueError(f"Unknown link/pipe '{self.__link_id}'")

            new_link_id = f"leak_pipe_{self.link_id}"
            new_node_id = f"leak_node_{self.link_id}"

            all_nodes_id = self._epanet_api.getNodeNameID()
            if new_node_id in all_nodes_id:
                raise ValueError(f"There is already a leak at pipe {self.link_id}")

            self._epanet_api.splitPipe(self.link_id, new_link_id, new_node_id)
            self.__leaky_node_id = self._epanet_api.getNodeIndex(new_node_id)
        else:
            if self.__node_id not in self._epanet_api.getNodeNameID():
                raise ValueError(f"Unknown node '{self.__node_id}'")

            self.__leaky_node_id = self._epanet_api.getNodeIndex(self.__node_id)

        self._epanet_api.setNodeEmitterCoeff(self.__leaky_node_id, 0.)

        # Compute leak emitter coefficient
        self.__leak_emitter_coef = self.compute_leak_emitter_coefficient(
            self.compute_leak_area(self.__diameter))

    def reset(self) -> None:
        self.__time_pattern_idx = 0

    def exit(self, cur_time) -> None:
        self._epanet_api.setNodeEmitterCoeff(self.__leaky_node_id, 0.)

    def apply(self, cur_time: int) -> None:
        self._epanet_api.setNodeEmitterCoeff(self.__leaky_node_id,
                                             self.__leak_emitter_coef *
                                             self.__profile[self.__time_pattern_idx])
        self.__time_pattern_idx += 1


@serializable(ABRUPT_LEAKAGE_ID, ".epytflow_leakage_abrupt")
class AbruptLeakage(Leakage):
    """
    Class implementing an abrupt leakage event.

    Parameters
    ----------
    link_id : `str`
        ID of the link at which the leak is placed.
    diameter : `float`
        Maximum diameter of the leak -- i.e. small leak diameter in the beginning,
        growing over time until peak time is reached.
    """
    def __init__(self, link_id: str, diameter: float, **kwds):
        if "profile" not in kwds:
            super().__init__(link_id=link_id, diameter=diameter, profile=None, **kwds)
        else:
            super().__init__(link_id=link_id, diameter=diameter, **kwds)

    def init(self, epanet_api: epyt.epanet) -> None:
        super().init(epanet_api)

        # Set pattern
        total_sim_duration = self._epanet_api.getTimeSimulationDuration()
        time_step = self._epanet_api.getTimeHydraulicStep()

        if self.end_time is not None:
            n_leaky_time_points = math.ceil((self.end_time - self.start_time) / time_step)
        else:
            n_leaky_time_points = math.ceil((total_sim_duration - self.start_time) / time_step)

        self.profile = np.ones(n_leaky_time_points)


@serializable(INCIPIENT_LEAKAGE_ID, ".epytflow_leakage_incipient")
class IncipientLeakage(Leakage):
    """
    Class implementing an incipient leakage event.

    Parameters
    ----------
    link_id : `str`
        ID of the link at which the leak is placed.
    diameter : `float`
        Maximum diameter of the leak -- i.e. small leak diameter in the beginning,
        growing over time until peak time is reached.
    peak_time : `int`
        Time (seconds since the simulation start) when this leak reaches
        its larges size (leak diameter).
    """
    def __init__(self, link_id: str, diameter: float, peak_time: int, **kwds):
        if peak_time < kwds["start_time"] or (kwds["end_time"] is not None and
                                              peak_time > kwds["end_time"]):
            raise ValueError("'peak_time' must be greater than 'start_time' and " +
                             "smaller than 'end_time'")

        self.__peak_time = peak_time

        if "profile" not in kwds:
            super().__init__(link_id=link_id, diameter=diameter, profile=None, **kwds)
        else:
            super().__init__(link_id=link_id, diameter=diameter, **kwds)

    @property
    def peak_time(self) -> int:
        """
        Gets the peak time (seconds since the simulation start) of the leak.

        Returns
        -------
        `int`
            Peak time of the leak.
        """
        return self.__peak_time

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"peak_time": self.peak_time}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.peak_time == other.peak_time

    def __str__(self) -> str:
        return f"{super().__str__()} peak_time: {self.peak_time}"

    def init(self, epanet_api: epyt.epanet) -> None:
        super().init(epanet_api)

        # Set pattern
        total_sim_duration = self._epanet_api.getTimeSimulationDuration()
        time_step = self._epanet_api.getTimeHydraulicStep()

        if self.end_time is not None:
            n_leaky_time_points = math.ceil((self.end_time - self.start_time) / time_step)
        else:
            n_leaky_time_points = math.ceil((total_sim_duration - self.start_time) / time_step)

        profile = np.ones(n_leaky_time_points)

        coeff = int((self.peak_time - self.start_time) / time_step)
        for t in range(coeff):
            profile[t] = (1. / coeff) + ((1. / coeff) * t)    # Linear interpolation!

        self.profile = profile
