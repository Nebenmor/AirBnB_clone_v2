#!/usr/bin/python3
"""A module that defines a class for hbnb that manages file storage"""
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import json


class FileStorage:
    """This class helps manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    classes = {
                'BaseModel': BaseModel, 'User': User, 'Place': Place,
                'State': State, 'City': City, 'Amenity': Amenity,
                'Review': Review
                }

    def all(self, cls=None):
        """This returns a dictionary of models currently in storage"""
        if cls is not None:
            objs = {}
            for key, value in FileStorage.__objects.items():
                if eval(key.split('.')[0]) == cls:
                    objs[key] = value
            return objs
        return FileStorage.__objects

    def new(self, obj):
        """This helps to add new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """This helps to save storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """This helpst to load storage dictionary from file"""

        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = FileStorage.classes[val['__class__\
']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        This helps to delete an object of the class
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]
                self.save()

    def close(self):
        """It helps to call the reload method."""
        self.reload()
