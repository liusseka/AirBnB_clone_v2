#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.place import Place


class State(BaseModel, Base):
    """ Defines a State class """

    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship('City',
        cascade='all, delete, delete-orphan',
        backref='state')

    @property
    def cities(self):
        data = models.storage.all()
        data_list = []
        result = []
        for key in data:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if (city[0] == 'City'):
                data_list.append(data[key])
        for item in data_list:
            if (item.state_id == self.id):
                result.append(item)
        return (result)


