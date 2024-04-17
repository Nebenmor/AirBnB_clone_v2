#!/usr/bin/python3
""" This is a city Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os

class City(BaseModel, Base):
    """ The is a city class and contains state ID and name """

    __tablename__ = "cities"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', backref="cities",
                              cascade="all, delete-orphan")

    else:
        name = ""
        state_id = ""
