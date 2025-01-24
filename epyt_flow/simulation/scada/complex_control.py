"""
Module contains a class for representing complex control rules as implemented in EPANET.
"""
from copy import deepcopy
from typing import Any
import numpy as np
from epyt.epanet import ToolkitConstants

from ...serialization import JsonSerializable, COMPLEX_CONTROL_ID, COMPLEX_CONTROL_CONDITION_ID, \
    COMPLEX_CONTROL_ACTION_ID, serializable


EN_R_AND = 2
EN_R_OR  = 3

EN_R_DEMAND    = 1
EN_R_HEAD      = 2
EN_R_LEVEL     = 3
EN_R_PRESSURE  = 4
EN_R_FLOW      = 5
EN_R_STATUS    = 6
EN_R_SETTING   = 7
EN_R_POWER     = 8
EN_R_TIME      = 9
EN_R_CLOCKTIME = 10
EN_R_FILLTIME  = 11
EN_R_DRAINTIME = 12

EN_R_EQ      = 0
EN_R_NEQ     = 1
EN_R_LEQ     = 2
EN_R_GEQ     = 3
EN_R_LESS    = 4
EN_R_GREATER = 5
EN_R_IS      = 6
EN_R_NOT     = 7
EN_R_BELOW   = 8
EN_R_ABOVE   = 9

EN_R_ACTION_SETTING       = -1
EN_R_ACTION_STATUS_OPEN   = 1
EN_R_ACTION_STATUS_CLOSED = 2
EN_R_ACTION_STATUS_ACTIVE = 3


@serializable(COMPLEX_CONTROL_CONDITION_ID, ".epytflow_complex_control_condition")
class RuleCondition(JsonSerializable):
    """
    Class representing a rule condition.

    Parameters
    ----------
    object_type_id : `int`
        ID of the object type.

        Must be one of the following EPANET constants:

            - EN_R_NODE   = 6
            - EN_R_LINK   = 7
            - EN_R_SYSTEM = 8
    object_id : `str`
        ID of the object (i.e. junction, pipe, link, tank, etc.).
    attribute_id : `int`
        Type ID of the object's attribute that is checked.

        Must be on of the following constants:

            - EN_R_DEMAND    = 1
            - EN_R_HEAD      = 2
            - EN_R_LEVEL     = 3
            - EN_R_PRESSURE  = 4
            - EN_R_FLOW      = 5
            - EN_R_STATUS    = 6
            - EN_R_SETTING   = 7
            - EN_R_TIME      = 9
            - EN_R_CLOCKTIME = 10
            - EN_R_FILLTIME  = 11
            - EN_R_DRAINTIME = 12
    relation_type_id : `int`
        ID of the type of comparison.

        Must be one of the following constants:

            - EN_R_EQ      = 0
            - EN_R_NEQ     = 1
            - EN_R_LEQ     = 2
            - EN_R_GEQ     = 3
            - EN_R_LESS    = 4
            - EN_R_GREATER = 5
            - EN_R_IS      = 6
            - EN_R_NOT     = 7
            - EN_R_BELOW   = 8
            - EN_R_ABOVE   = 9
    value : `Any`
        Value that is compared against.
    """
    def __init__(self, object_type_id: int, object_id: str, attribute_id: int,
                 relation_type_id: int, value: Any, **kwds):
        if not isinstance(object_type_id, int):
            raise TypeError("'object_type_id' must be an instance of 'int' " +
                            f"but not of '{type(object_type_id)}'")
        if object_type_id not in [ToolkitConstants.EN_R_NODE, ToolkitConstants.EN_R_LINK,
                                  ToolkitConstants.EN_R_SYSTEM]:
            raise ValueError(f"Invalid value '{object_type_id}' for 'object_type_id'")
        if not isinstance(object_id, str):
            raise TypeError("'object_id' must be an instance of 'str' " +
                            f"but not of '{type(object_id)}'")
        if not isinstance(attribute_id, int):
            raise TypeError("'attribute_id' must be an instance of 'int' " +
                            f"but not of '{type(attribute_id)}'")
        if attribute_id not in [EN_R_DEMAND, EN_R_HEAD, EN_R_LEVEL, EN_R_PRESSURE,
                                EN_R_FLOW, EN_R_STATUS, EN_R_SETTING, EN_R_POWER, EN_R_TIME,
                                EN_R_CLOCKTIME, EN_R_FILLTIME, EN_R_DRAINTIME]:
            raise ValueError(f"Invalid value '{attribute_id}' for 'attribute_id'")
        if not isinstance(relation_type_id, int):
            raise TypeError("'relation_type_id' must be an instance of 'int' " +
                            f"but not of '{type(relation_type_id)}'")
        if relation_type_id not in [EN_R_EQ, EN_R_NEQ, EN_R_LEQ, EN_R_GEQ, EN_R_LESS, EN_R_GREATER,
                                    EN_R_IS, EN_R_NOT, EN_R_BELOW, EN_R_ABOVE]:
            raise ValueError(f"Invalid value '{relation_type_id}' for 'relation_type_id'")

        self.__object_type_id = object_type_id
        self.__object_id = object_id
        self.__attribute_id = attribute_id
        self.__relation_type_id = relation_type_id
        self.__value = value

        super().__init__(**kwds)

    @property
    def object_type_id(self) -> int:
        """
        Returns the ID of the object type.

        Will be one of the following EPANET constants:

            - EN_R_NODE   = 6
            - EN_R_LINK   = 7
            - EN_R_SYSTEM = 8

        Returns
        -------
        `int`
            ID of the object type..
        """
        return self.__object_type_id

    @property
    def object_id(self) -> str:
        """
        Returns the ID of the object (i.e. junction, pipe, link, tank, etc.).

        Returns
        -------
        `str`
            ID of the object.
        """
        return self.__object_id

    @property
    def attribute_id(self) -> int:
        """
        Returns the type ID of the object's attribute that is checked.

        Will be one of the following constants:

            - EN_R_DEMAND    = 1
            - EN_R_HEAD      = 2
            - EN_R_LEVEL     = 3
            - EN_R_PRESSURE  = 4
            - EN_R_FLOW      = 5
            - EN_R_STATUS    = 6
            - EN_R_SETTING   = 7
            - EN_R_TIME      = 9
            - EN_R_CLOCKTIME = 10
            - EN_R_FILLTIME  = 11
            - EN_R_DRAINTIME = 12

        Returns
        -------
        `int`
            Type ID of the object's attribute that is checked.
        """
        return self.__attribute_id

    @property
    def relation_type_id(self) -> int:
        """
        Returns the ID of the type of comparison.

        Will be one of the following constants:

            - EN_R_EQ      = 0
            - EN_R_NEQ     = 1
            - EN_R_LEQ     = 2
            - EN_R_GEQ     = 3
            - EN_R_LESS    = 4
            - EN_R_GREATER = 5
            - EN_R_IS      = 6
            - EN_R_NOT     = 7
            - EN_R_BELOW   = 8
            - EN_R_ABOVE   = 9

        Returns
        -------
        `int`
            ID of the type of comparison.
        """
        return self.__relation_type_id

    @property
    def value(self) -> Any:
        """
        Returns the value that is compared against.

        Returns
        -------
        `Any`
            Value that is compared against.
        """
        return self.__value

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"object_type_id": self.__object_type_id,
                                           "object_id": self.__object_id,
                                           "attribute_id": self.__attribute_id,
                                           "relation_type_id": self.__relation_type_id,
                                           "value": self.__value}

    def __eq__(self, other) -> bool:
        return self.__object_type_id == other.object_type_id and \
            self.__object_id == other.object_id and self.__attribute_id == other.attribute_id and \
            self.__relation_type_id == other.relation_type_id and self.__value == other.value

    def __str__(self) -> str:
        desc = ""

        if self.__attribute_id == EN_R_DEMAND:
            if self.__object_type_id == ToolkitConstants.EN_R_NODE:
                desc += f"JUNCTION {self.__object_id} DEMAND "
            elif self.__object_type_id == ToolkitConstants.EN_R_SYSTEM:
                desc += "SYSTEM DEMAND "
        elif self.__attribute_id == EN_R_HEAD:
            desc += f"JUNCTION {self.__object_id} HEAD "
        elif self.__attribute_id == EN_R_LEVEL:
            desc += f"TANK {self.__object_id} LEVEL "
        elif self.__attribute_id == EN_R_PRESSURE:
            desc += f"JUNCTION {self.__object_id} PRESSURE "
        elif self.__attribute_id == EN_R_FLOW:
            desc += f"LINK {self.__object_id} FLOW "
        elif self.__attribute_id == EN_R_STATUS:
            desc += f"LINK {self.__object_id} STATUS "
        elif self.__attribute_id == EN_R_SETTING:
            desc += f"LINK {self.__object_id} SETTING "
        elif self.__attribute_id == EN_R_TIME:
            desc += "SYSTEM TIME "
        elif self.__attribute_id == EN_R_CLOCKTIME:
            desc += "SYSTEM CLOCKTIME "
        elif self.__attribute_id == EN_R_FILLTIME:
            desc += f"TANK {self.__object_id} FILLTIME "
        elif self.__attribute_id == EN_R_DRAINTIME:
            desc += f"TANK {self.__object_id} DRAINTIME "

        if self.__relation_type_id == EN_R_EQ:
            desc += "= "
        elif self.__relation_type_id == EN_R_IS:
            desc += "IS "
        elif self.__relation_type_id == EN_R_NOT:
            desc += "IS NOT "
        elif self.__relation_type_id == EN_R_LEQ:
            desc += "<= "
        elif self.__relation_type_id == EN_R_GEQ:
            desc += ">= "
        elif self.__relation_type_id == EN_R_ABOVE:
            desc += "ABOVE "
        elif self.__relation_type_id == EN_R_BELOW:
            desc += "BELOW "
        elif self.__relation_type_id == EN_R_LESS:
            desc += "< "
        elif self.__relation_type_id == EN_R_GREATER:
            desc += "> "

        desc += str(self.__value)

        return desc


@serializable(COMPLEX_CONTROL_ACTION_ID, ".epytflow_complex_control_action")
class RuleAction(JsonSerializable):
    """
    Class representing a rule action.

    Parameters
    ----------
    link_type_id : `int`
        Link type ID.

        Must be one of following EPANET constants:

            - EN_CVPIPE = 0
            - EN_PIPE = 1
            - EN_PUMP = 2
            - EN_PRV = 3
            - EN_PSV = 4
            - EN_PBV = 5
            - EN_FCV = 6
            - EN_TCV = 7
            - EN_GPV = 8
    link_id : `str`
        Link ID.
    action_type_id : `int`
        Type ID of the action.

        Must be one of the following constants:

            - EN_R_ACTION_SETTING       = -1
            - EN_R_ACTION_STATUS_OPEN   = 1
            - EN_R_ACTION_STATUS_CLOSED = 2
            - EN_R_ACTION_STATUS_ACTIVE = 3
    action_value : `Any`
        Value of the acton (e.g. pump speed).
        Only relevant if action_type_id = EN_R_SETTING, will be ignored in all other cases.
    """
    def __init__(self, link_type_id: int, link_id: str, action_type_id: int, action_value: Any,
                 **kwds):
        if not isinstance(link_type_id, int):
            raise TypeError("'link_type_id' must be an istanace of 'int' " +
                            f"but not of '{type(link_type_id)}'")
        if link_type_id not in [ToolkitConstants.EN_CVPIPE, ToolkitConstants.EN_PIPE,
                                ToolkitConstants.EN_PUMP, ToolkitConstants.EN_PRV,
                                ToolkitConstants.EN_PSV, ToolkitConstants.EN_PBV,
                                ToolkitConstants.EN_FCV, ToolkitConstants.EN_TCV,
                                ToolkitConstants.EN_GPV]:
            raise ValueError(f"Invalid value '{link_type_id}' for 'link_type_id'")
        if not isinstance(link_id, str):
            raise TypeError("'link_id' must be an instance of 'str' " +
                            f"but not of '{type(link_id)}'")
        if not isinstance(action_type_id, int):
            raise TypeError("'action_type_id' must be an instance of 'int' " +
                            f"but not of '{type(action_type_id)}'")
        if action_type_id not in [EN_R_ACTION_SETTING, EN_R_ACTION_STATUS_OPEN,
                                  EN_R_ACTION_STATUS_CLOSED, EN_R_ACTION_STATUS_ACTIVE]:
            raise ValueError(f"Invalid value '{action_type_id}' for 'action_type_id'")

        self.__link_type_id = link_type_id
        self.__link_id = link_id
        self.__action_type_id = action_type_id
        self.__action_value = action_value

        super().__init__(**kwds)

    @property
    def link_type_id(self) -> int:
        """
        Returns the link type ID.

        Will be one of the following EPANET constants:

            - EN_CVPIPE = 0
            - EN_PIPE = 1
            - EN_PUMP = 2
            - EN_PRV = 3
            - EN_PSV = 4
            - EN_PBV = 5
            - EN_FCV = 6
            - EN_TCV = 7
            - EN_GPV = 8

        Returns
        -------
        `int`
            Link type ID.
        """
        return self.__link_type_id

    @property
    def link_id(self) -> str:
        """
        Returns the link ID.

        Returns
        -------
        `str`
            Link ID.
        """
        return self.__link_id

    @property
    def action_type_id(self) -> int:
        """
        Returns the type ID of the action.

        Will be one of the following constants:

            - EN_R_ACTION_SETTING       = -1
            - EN_R_ACTION_STATUS_OPEN   = 1
            - EN_R_ACTION_STATUS_CLOSED = 2
            - EN_R_ACTION_STATUS_ACTIVE = 3

        Returns
        -------
        `int`
            Type ID of the action.
        """
        return self.__action_type_id

    @property
    def action_value(self) -> Any:
        """
        Returns the value of the acton (e.g. pump speed).
        Only relevant if action_type_id = EN_R_SETTING.

        Returns
        -------
        `Any`
            Value of the action.
        """
        return self.__action_value

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"link_type_id": self.__link_type_id,
                                           "link_id": self.__link_id,
                                           "action_type_id": self.__action_type_id,
                                           "action_value": self.__action_value}

    def __eq__(self, other) -> bool:
        return self.__link_type_id == other.link_type_id and \
            self.__link_id == other.link_id and \
            self.__action_type_id == other.action_type_id and \
            self.__action_value == other.action_value

    def __str__(self) -> str:
        desc = ""

        if self.__link_type_id in [ToolkitConstants.EN_CVPIPE, ToolkitConstants.EN_PIPE]:
            desc += "PIPE "
        elif self.__link_type_id == ToolkitConstants.EN_PUMP:
            desc += "PUMP "
        else:
            desc += "VALVE "

        desc += f"{self.__link_id} "

        if self.__action_type_id == EN_R_ACTION_SETTING:
            desc += f"SETTING IS {self.__action_value}"
        elif self.__action_type_id == EN_R_ACTION_STATUS_OPEN:
            desc += "STATUS IS OPEN"
        elif self.__action_type_id == EN_R_ACTION_STATUS_CLOSED:
            desc += "STATUS IS CLOSED"
        elif self.action_type_id == EN_R_ACTION_STATUS_ACTIVE:
            desc += "STATUS IS ACTIVE"

        return desc


@serializable(COMPLEX_CONTROL_ID, ".epytflow_complex_control")
class ComplexControlModule(JsonSerializable):
    """
    Class representing a complex control module (i.e. IF-THEN-ELSE rule) as implemented in EPANET.

    Parameters
    ----------
    rule_id : `str`
        ID of the rule.
    condition_1 : :class:`~epyt_flow.simulation.scada.complex_control.RuleCondition`
        First condition of this rule.
    additional_conditions : list[tuple[int, :class:`~epyt_flow.simulation.scada.complex_control.RuleCondition`]]
        List of (optional) additional conditions incl. their conjunction operator
        (must be either EN_R_AND = 2 or EN_R_OR  = 3).

        Empty list if there are no additional conditions.
    actions : list[:class:`~epyt_flow.simulation.scada.complex_control.RuleAction`]
        List of actions that are applied if the conditions are met.
        Must contain at least one action.
    else_actions : list[:class:`~epyt_flow.simulation.scada.complex_control.RuleAction`]
        List of actions that are applied if the conditions are NOT met.
    priority : `int`
        Priority of this control rule.
    """
    def __init__(self, rule_id: str, condition_1: RuleCondition,
                 additional_conditions: list[tuple[int, RuleCondition]], actions: list[RuleAction],
                 else_actions: list[RuleAction], priority: int, **kwds):
        if not isinstance(rule_id, str):
            raise TypeError(f"'rule_id' must be an instance of 'str' but not of '{type(rule_id)}'")
        if not isinstance(condition_1, RuleCondition):
            raise TypeError("'condition_1' must be an instance of " +
                            "'epyt_flow.simulation.scada.RuleCondition' " +
                            f"but not of '{type(condition_1)}'")
        if not isinstance(additional_conditions, list) or \
                any(not isinstance(condition, tuple) for condition in additional_conditions) or \
                any(not isinstance(condition[0], int) or condition[0] not in [EN_R_AND, EN_R_OR] or
                    not isinstance(condition[1], RuleCondition)
                    for condition in additional_conditions):
            raise TypeError("'additional_conditions' must be a list of " +
                            "'tuple[int, epyt_flow.simulation.scada.RuleCondition]' instances")
        if not isinstance(actions, list) or any(not isinstance(action, RuleAction)
                                                for action in actions):
            raise TypeError("'actions' must be a list of " +
                            "'epyt_flow.simulation.scada.RuleAction' instances")
        if len(actions) == 0:
            raise ValueError("'actions' must contain at least one action")
        if not isinstance(else_actions, list) or any(not isinstance(action, RuleAction)
                                                     for action in actions):
            raise TypeError("'else_actions' must be a list of " +
                            "'epyt_flow.simulation.scada.RuleAction' instances")
        if not isinstance(priority, int) or priority < 0:
            raise TypeError("'priority' must be a non-negative integer")

        self.__rule_id = rule_id
        self.__condition_1 = condition_1
        self.__additional_conditions = additional_conditions
        self.__actions = actions
        self.__else_actions = else_actions
        self.__priority = priority

        super().__init__(**kwds)

    @property
    def rule_id(self) -> str:
        """
        Returns the ID of this control rule.

        Returns
        -------
        `str`
            ID of this control rule.
        """
        return self.__rule_id

    @property
    def condition_1(self) -> RuleCondition:
        """
        Returns the first condition of this rule.

        Returns
        -------
        :class:`~epyt_flow.simulation.scada.complex_control.RuleCondition`
            First condition of this rule.
        """
        return deepcopy(self.__condition_1)

    @property
    def additional_conditions(self) -> list[tuple[int, RuleCondition]]:
        """
        Returns the list of (optional) additional conditions incl. their conjunction operator.
        Empty list if there are no additional conditions.

        Returns
        -------
        list[tuple[int, :class:`~epyt_flow.simulation.scada.complex_control.RuleCondition`]]
            List of (optional) additional conditions incl. their conjunction operator.
        """
        return deepcopy(self.__additional_conditions)

    @property
    def actions(self) -> list[RuleAction]:
        """
        Returns the list of actions that are applied if the conditions are met.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.scada.complex_control.RuleAction`]
            List of actions that are applied if the conditions are met.
        """
        return deepcopy(self.__actions)

    @property
    def else_actions(self) -> list[RuleAction]:
        """
        Returns the list of actions that are applied if the conditions are NOT met.

        Returns
        -------
        list[:class:`~epyt_flow.simulation.scada.complex_control.RuleAction`]
            List of actions that are applied if the conditions are NOT met.
        """
        return deepcopy(self.__else_actions)

    @property
    def priority(self) -> int:
        """
        Returns the priority of this control rule.

        Returns
        -------
        `int`
            Priority of this control rule.
        """
        return self.__priority

    def get_attributes(self) -> dict:
        return super().get_attributes() | {"rule_id": self.__rule_id,
                                           "condition_1": self.__condition_1,
                                           "additional_conditions": self.__additional_conditions,
                                           "actions": self.__actions,
                                           "else_actions": self.__else_actions,
                                           "priority": self.__priority}

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.__rule_id == other.rule_id and \
            self.__priority == other.priority and self.__condition_1 == other.condition_1 and \
            np.all(self.__additional_conditions == other.additional_conditions) and \
            np.all(self.__actions == other.actions) and \
            np.all(self.__else_actions == other.else_actions)

    def __str__(self) -> str:
        desc = ""

        desc += f"RULE {self.__rule_id}\n"
        desc += f"IF {self.__condition_1} "
        for op, action in self.__additional_conditions:
            if op == EN_R_AND:
                desc += "\nAND "
            elif op == EN_R_OR:
                desc += "\nOR "

            desc += f"{action} "
        desc += "\nTHEN "
        desc += "\nAND ".join(str(action) for action in self.__actions)
        if len(self.__else_actions) != 0:
            desc += "\nELSE " + "\nAND ".join(str(action) for action in self.__else_actions)

        desc += f"\nPRIORITY {self.__priority}"

        return desc
