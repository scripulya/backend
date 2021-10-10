from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

Base = declarative_base()


class RentalProperty(Base):
    __tablename__ = 'real_estates'
    id = Column(Integer, primary_key=True)
    address = Column(String)
    price = Column(String)
    coords = Column(Geometry('POINT'))
    resource_link = Column(String)


class Municipality(Base):
    __tablename__ = 'municipality'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry('POLYGON'))
