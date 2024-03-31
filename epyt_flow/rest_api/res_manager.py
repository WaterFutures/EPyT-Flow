"""
This module contains a class for managing recourses such as scenarios or SCADA data.
"""
from typing import Any
import uuid


class ResourceManager():
    """
    Class implementing a simple resource manager where resources are associated with UUIDs.
    """
    def __init__(self):
        self.__resources = {}

    def __create_uuid(self) -> str:
        return str(uuid.uuid4())

    def validate_uuid(self, item_uuid: str) -> bool:
        """
        Validates a given UUID -- i.e. checks if there is a resource associated with the given UUID.

        Parameters
        ----------
        item_uuid : `str`
            UUID of the item.

        Returns
        -------
        `bool`
            True if the given UUID is valid, False otherwise.
        """
        return item_uuid in self.__resources

    def create_new_item(self, item: Any) -> str:
        """
        Adds a new item to the resource manager.

        Parameters
        ----------
        item : `Any`
            Item to be added.

        Returns
        -------
        `str`
            UUID of the new item.
        """
        new_item_uuid = self.__create_uuid()
        self.__resources[new_item_uuid] = item

        return new_item_uuid

    def get(self, item_uuid: str) -> Any:
        """
        Gets the item associated with a given UUID.

        Parameters
        ----------
        item_uuid : `str`
            UUID of the item.

        Returns
        -------
        `Any`
            Resource item.
        """
        if item_uuid not in self.__resources:
            raise ValueError(f"Invalid UUID '{item_uuid}'")

        return self.__resources[item_uuid]

    def close_item(self, item: Any):
        """
        Closes a given resource item -- i.e. all clean-up logic for an item should be called here.

        Parameters
        ----------
        item : `Any`
            Resource item.
        """

    def remove(self, item_uuid: str) -> None:
        """
        Removes the scenario associated with a given UUID

        Parameters
        ----------
        item_uuid : `str`
            UUID of the item.
        """
        if item_uuid not in self.__resources:
            raise ValueError(f"Invalid UUID '{item_uuid}'")

        self.close_item(self.__resources[item_uuid])
        del self.__resources[item_uuid]
