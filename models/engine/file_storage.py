#!/usr/bin/python3

""" FileStorage module """

import datetime
import os
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.place import Place
from models.user import User
from models.state import State


class FileStorage:

    """ Serializtion and deserialization for base class """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Returns __objects dictionary """
        return FileStorage.__objects

    def new(self, obj):
        """ Creates new obj in __objects dictionary """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """ Serialzes __objects to JSON file """
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            d = {n: v.to_dict() for n, v in FileStorage.__objects.items()}
            json.dump(d, f)

    def reload(self):
        """ Deserializes JSON file into __objects """
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            obj_dict = {n: self.classes()[v["__class__"]](**v)
                        for n, v in obj_dict.items()}
            FileStorage.__objects = obj_dict

    def attributes(self):
        """ Returns the valid attributes """

        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes
