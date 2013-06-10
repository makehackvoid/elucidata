import pandas
import json
import requests
from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
import dateutil.parser
import time

# TODO: move database details into config file not held in repository
user = 'postgres'
password = ''
server = 'localhost'
port = '5432'
database = 'mhv-govhack'
databaseurl = 'postgresql://' + user + ':' + password + '@' + server + ':' + port + '/' + database
engine = create_engine('postgresql://' + user + ':' + password + '@' + server + ':' + port + '/' + database)
session = create_session(bind=engine)
Base = declarative_base()
metadata = MetaData(bind=engine)


class DataSet(Base):
    __table__ = Table('dataset', metadata, autoload=True)


class Coordinate(Base):
    __table__ = Table('coordinate', metadata, autoload=True)


class DataPoint(Base):
    __table__ = Table('datapoint', metadata, autoload=True)


class ResourceMap(Base):
    __table__ = Table('resource_map', metadata, autoload=True)


class ResourceText(Base):
    __table__ = Table('resource_text', metadata, autoload=True)


class Word(Base):
    __table__ = Table('word', metadata, autoload=True)


class Tag(Base):
    __table__ = Table('tag', metadata, autoload=True)


class Group(Base):
    __table__ = Table('group', metadata, autoload=True)

session.begin()
session.execute('DELETE FROM "coordinate";')
session.execute('DELETE FROM "datapoint";')
session.execute('DELETE FROM "group";')
session.execute('DELETE FROM "resource_map";')
session.execute('DELETE FROM "word";')
session.execute('DELETE FROM "resource_text";')
session.execute('DELETE FROM "tag";')
session.execute('DELETE FROM "dataset";')

session.commit();
session.close();

print "[ARNI] Data has been terminated!"
