__author__ = 'David'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantcatalog.db')

### code to make the script run ###
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()