#!/usr/bin/python3
""" This is Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import os

place_amenity = Table('place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id')),
    Column('amenity_id', String(60), ForeignKey('amenities.id'))
)


class Place(BaseModel, Base):
    """ IS a place to stay """
    __tablename__ = "places"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)

        reviews = relationship('Review', backref="place",
                              cascade="all, delete-orphan")
        amenities = relationship('Amenity',
                                back_populates='place_amenities',
                                secondary= place_amenity,
                                viewonly=False)

    else:

        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def amenities(self):
            from models import storage
            listen = []
            for amenity_id in self.amenity_ids:
                dict_ = storage.all(storage.classes['Amenity'])\
                    .get("Amenity.{}".format(amenity_id))
                if dict_:
                    listen.append(dict_)
            return listen
            # dict_ = storage.all(storage.classes['Amenity'])
            # for key in dict_:
            #     if key.split('.')[1] in self.amenity_ids:
            #         listen.append(dict_[key])
            # return listen

        @property
        def reviews(self):
            from models import storage
            file_reviews = storage.all(storage.classes['Review']).values()
            return [review  for review in file_reviews if review.place_id == self.id]

        @amenities.setter
        def amenities(self, obj):
            if obj.__class__.__name__ == 'Amenity':
                self.amenity_ids.append(obj.id)
