from copy import deepcopy
import numpy
import numpy as np
import epyt

from .system_event import SystemEvent
from ...serialization import serializable, Serializable,\
    LEAKAGE_ID, ABRUPT_LEAKAGE_ID, INCIPIENT_LEAKAGE_ID


@serializable(LEAKAGE_ID)
class Leakage(SystemEvent, Serializable):
    """
    Base class for a leakage.

    Parameters
    ----------
    link_id : `str`
        ID of the link at which the leak is placed.
    diameter : `float`
        Diameter of this leak.
    profile : `numpy.ndarray`
        Pattern of this leak.

    Attributes
    ----------
    link_id : `str`
        ID of the link at which the leak is placed.
    diameter : `float`
        Diameter of this leak.
    profile : `numpy.ndarray`
        Pattern of this leak.
    """
    def __init__(self, link_id:str, diameter:float, profile:numpy.ndarray, **kwds):
        self.__link_id = link_id
        self.__diameter = diameter
        self._profile = profile

        self.__leaky_node_id = None
        self.__leak_emitter_coef = None
        self.__time_pattern_idx = 0

        super().__init__(**kwds)

    @property
    def link_id(self) -> str:
        return self.__link_id

    @property
    def diameter(self) -> float:
        return self.__diameter

    @property
    def profile(self) -> numpy.ndarray:
        return deepcopy(self._profile)

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"link_id": self.link_id, "diameter": self.diameter,
                                           "profile": self.profile}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.link_id == other.link_id \
            and self.diameter == other.diameter and self.profile == other.profile

    def __str__(self) -> str:
        return f"{super().__str__()} link_id: {self.link_id} diameter: {self.diameter} "+\
            f"profile: {self.profile}"

    def compute_leak_area(self, diameter:float, factor_units:float=100.) -> float:
        # factor_units=100 changes the units to EPANET default units
        return (np.pi * (diameter / 2) ** 2) * factor_units

    def compute_leak_emitter_coefficient(self, area:float, discharg_coef:float=.75,
                                         g:float=9.8) -> float:
        # leak_demand = emitter_coef * pressure^alpha    with alpha = .5
        # emitter_coef = discharg_coef * area * sqrt(2*g)   with g = 9.8, discharg_coef = .75
        return discharg_coef * area * np.sqrt(2. * g)

    def init(self, epanet_api:epyt.epanet) -> None:
        super().init(epanet_api)

        # Split pipe
        new_link_id = f"leak_pipe_{self.link_id}"
        new_node_id = f"leak_node_{self.link_id}"

        all_nodes_id = self._epanet_api.getNodeNameID()
        if new_node_id in all_nodes_id:
            raise ValueError(f"There is already a leak at pipe {self.link_id}")

        self._epanet_api.splitPipe(self.link_id, new_link_id, new_node_id)
        self.__leaky_node_id = self._epanet_api.getNodeIndex(new_node_id)
        self.__leak_emitter_coef = self.compute_leak_emitter_coefficient(
            self.compute_leak_area(self.__diameter))
        self._epanet_api.setNodeEmitterCoeff(self.__leaky_node_id, 0.)

    def apply(self, cur_time:int) -> None:
        if self.start_time <= cur_time < self.end_time:
            self._epanet_api.setNodeEmitterCoeff(self.__leaky_node_id,
                                                 self.__leak_emitter_coef \
                                                    * self._profile[self.__time_pattern_idx])
            self.__time_pattern_idx += 1
        elif cur_time >= self.end_time:
            self._epanet_api.setNodeEmitterCoeff(self.__leaky_node_id, 0.)


@serializable(ABRUPT_LEAKAGE_ID)
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
    def __init__(self, link_id:str, diameter:float, **kwds):
        super().__init__(link_id=link_id, diameter=diameter, profile=None, **kwds)

    def init(self, epanet_api:epyt.epanet) -> None:
        super().init(epanet_api)

        # Set pattern
        total_sim_duration = self._epanet_api.getTimeSimulationDuration()
        time_step = self._epanet_api.getTimeHydraulicStep()

        if self.end_time is not None:
            n_leaky_time_points = int((self.end_time - self.start_time) / time_step)
        else:
            n_leaky_time_points = int((total_sim_duration - self.start_time) / time_step)

        self._profile = np.ones(n_leaky_time_points)


@serializable(INCIPIENT_LEAKAGE_ID)
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
    def __init__(self, link_id:str, diameter:float, peak_time:int, **kwds):
        if peak_time < kwds["start_time"] or \
            (kwds["end_time"] is not None and peak_time > kwds["end_time"]):
            raise ValueError("'peak_time' must be greater than 'start_time' and "\
                             "smaller than 'end_time'")

        self.__peak_time = peak_time

        super().__init__(link_id=link_id, diameter=diameter, profile=None, **kwds)

    @property
    def peak_time(self) -> int:
        return self.__peak_time

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"peak_time": self.peak_time}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.peak_time == other.peak_time

    def __str__(self) -> str:
        return f"{super().__str__()} peak_time: {self.peak_time}"

    def init(self, epanet_api:epyt.epanet) -> None:
        super().init(epanet_api)

        # Set pattern
        total_sim_duration = self._epanet_api.getTimeSimulationDuration()
        time_step = self._epanet_api.getTimeHydraulicStep()

        if self.end_time is not None:
            n_leaky_time_points = int((self.end_time - self.start_time) / time_step)
        else:
            n_leaky_time_points = int((total_sim_duration - self.start_time) / time_step)

        self._profile = np.ones(n_leaky_time_points)

        coeff = int((self.peak_time - self.start_time) / time_step)
        for t in range(coeff):
            self._profile[t] = (1. / coeff) + ((1. / coeff) * t)    # Linear interpolation!
