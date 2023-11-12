#!/usr/bin/python3
""" BaseClass model for the AirBnB clone project """

import uuid
import models
from datetime import datetime

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:

    """ Class for base model """

    def __init__(self, *args, **kwargs):
        """ Initialization of the BaseClass Model """

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key != "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
            models.storage.save()

    def __str__(self):
        """ Returns a human readable string representation  """

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """ Shows the updated_at attribute
        with the new datetime """

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ Returns a dictionary representation of ann instance."""

        curr_dict = self.__dict__.copy()
        curr_dict["__class__"] = type(self).__name__
        curr_dict["created_at"] = curr_dict["created_at"].isoformat()
        curr_dict["updated_at"] = curr_dict["updated_at"].isoformat()
        return my_dict
