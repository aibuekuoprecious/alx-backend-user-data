#!/usr/bin/env python3
""" 
Base module
"""

from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}
Base = TypeVar('Base')


class Base():
    """ 
    The Base class is the parent class for all other classes in the project.
    It provides common functionality and attributes.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ 
        Initialize a Base instance with optional arguments.

        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.

        Attributes:
            id (str): The unique identifier for the instance.
            created_at (datetime): The timestamp of when the instance was created.
            updated_at (datetime): The timestamp of when the instance was last updated.
        """
        class_name = str(self.__class__.__name__)
        if DATA.get(class_name) is None:
            DATA[class_name] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs.get('created_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: Base) -> bool:
        """ 
        Compare two instances for equality.

        Args:
            other (Base): The other instance to compare with.

        Returns:
            bool: True if the instances are equal, False otherwise.
        """
        if type(self) != type(other):
            return False
        if not isinstance(self, Base):
            return False
        return (self.id == other.id)

    def to_json(self, for_serialization: bool = False) -> dict:
        """ 
        Convert the object to a JSON dictionary.

        Args:
            for_serialization (bool): Flag indicating whether to include private attributes in the JSON dictionary.

        Returns:
            dict: The JSON dictionary representation of the object.
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if type(value) is datetime:
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        """ 
        Load all objects from file.
        """
        class_name = cls.__name__
        file_path = ".db_{}.json".format(class_name)
        DATA[class_name] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[class_name][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """ 
        Save all objects to file.
        """
        class_name = cls.__name__
        file_path = ".db_{}.json".format(class_name)
        objs_json = {}
        for obj_id, obj in DATA[class_name].items():
            objs_json[obj_id] = obj.to_json(True)

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """ 
        Save current object.
        """
        class_name = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[class_name][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """ 
        Remove object.
        """
        class_name = self.__class__.__name__
        if DATA[class_name].get(self.id) is not None:
            del DATA[class_name][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """ 
        Count all objects.

        Returns:
            int: The number of objects.
        """
        class_name = cls.__name__
        return len(DATA[class_name].keys())

    @classmethod
    def all(cls) -> Iterable[Base]:
        """ 
        Return all objects.

        Returns:
            Iterable[Base]: An iterable containing all objects.
        """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> Base:
        """ 
        Return one object by ID.

        Args:
            id (str): The ID of the object to retrieve.

        Returns:
            Base: The object with the specified ID, or None if not found.
        """
        class_name = cls.__name__
        return DATA[class_name].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[Base]:
        """ 
        Search all objects with matching attributes.

        Args:
            attributes (dict): The attributes to search for.

        Returns:
            List[Base]: A list of objects that match the specified attributes.
        """
        class_name = cls.__name__

        def _search(obj):
            if len(attributes) == 0:
                return True
            for k, v in attributes.items():
                if (getattr(obj, k) != v):
                    return False
            return True

        return list(filter(_search, DATA[class_name].values()))
