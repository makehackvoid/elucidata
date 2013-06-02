import pandas
import json
import requests
from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
import dateutil.parser
import time

api_url = 'http://opendata.linkdigital.com.au/api/3/'
    
get_resources = 'http://opendata.linkdigital.com.au/api/3/action/current_package_list_with_resources'

live = False

if live:
    r = requests.get(get_resources)
    with open('data.json', 'w') as f:
        f.write(r.content)
        f.close()
    raw_data = r.content
else:
    with open('data.json', 'r') as f:
        raw_data = f.read()
        f.close()
    
    data = json.loads(raw_data)

# print data.keys()

data_sets = pandas.DataFrame(data['result'])

#for name in df.columns:
#    print '\t\'' + name + '\','
    
data_sets = data_sets[[
    # 'author',
    # 'author_email',
    # 'extras',
    'groups',
    'id',
    # 'isopen',
    # 'license_id',
    # 'license_title',
    # 'license_url',
    # 'maintainer',
    # 'maintainer_email',
    # 'metadata_created',
    # 'metadata_modified',
    'name',
    # 'notes',
    'num_resources',
    'num_tags',
    'organization',
    # 'owner_org',
    # 'private',
    # 'relationships_as_object',
    # 'relationships_as_subject',
    'resources',
    'revision_id',
    'revision_timestamp',
    # 'state',
    'tags',
    'title',
    # 'tracking_summary',
    'type',
    # 'url',
    # 'version'
    ]]

#SQLAlchemy
# change when making .py file

user = 'postgres'
password = ''
server = 'localhost'
port = '5432'
database = 'mhv-govhack'
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

def usable_format(resources):
    # All formats in data_sets = set([u'XML', u'xlsx', u'ZIP', u'plain', u'KML', u'PDF', u'CSV', u'XLS', u'shp'])
    # just start with these, add more if we have time
    # if there are no valid formats in the data_set, we don't want to create the dataset record
    for resource in resources:
        if resource['format'].lower() in ['csv','kml']:
            return True
        else:
            return False

def text_format(resource):
    if resource['format'].lower() in ['xml','csv']:
        return True
    else:
        return False
        
for key, data_set in data_sets.iterrows():
    if usable_format(data_set['resources']):
        session.begin()
        
        # fill the dataset table
        dataset = DataSet()  
        dataset.id = data_set['id']
        dataset.api_url = api_url
        dataset.name = data_set['title']
        dataset.url_name = data_set['name']
        dataset.provider = data_set['organization']['title']
        dataset.revision_date = time.mktime(dateutil.parser.parse(data_set['revision_timestamp']).timetuple())
        dataset.revision_id = data_set['revision_id']
        session.add(dataset)
        # TODO: add field to database
        # dataset.description = data_set['notes'] up to the second new line

        try:
            session.commit()
        except SQLAlchemyError: # already exists (hopefully)
            # TODO: compare existing DataSet record's revision date && id to see if we need to replace it
            # code not working
            # q = session.query(DataSet).filter(DataSet.revision_id == dataset.revision_id)
            # if session.query(q.exists()):
            #    print 'it exists!', data_set['revision_id']
            #    continue
            # else:
            #    session.delete(dataset)
            #    session.add(dataset)
            #    session.commit()
            session.close()
            break # continue
        
        session.begin()
        # fill the group table
        for a_group in data_set['groups']:
            group = Group()
            # TODO: not sure if we can set the dataset_id outside the loop?
            group.dataset_id = data_set['id']
            group.group = a_group['title']
            session.add(group)
            
        # fill the tag table
        for a_tag in data_set['tags']:
            tag = Tag()
            # TODO: not sure if we can set the dataset_id outside the loop?
            tag.dataset_id = data_set['id']
            tag.tag = a_tag
            session.add(tag)
        
        # fill the resource_text or resource_map table 
        for resource in data_set['resources']:
            if text_format(resource):
                resource_text = ResourceText()
                resource_text.id = resource['id']
                resource_text.dataset_id = data_set['id']
                resource_text.name = resource['name']
                resource_text.resource_url = resource['url']
                resource_text.type = resource['format']
                session.add(resource_text)
                if resource['format'].lower() == 'csv':
                    df = pandas.DataFrame.from_csv(resource['url'])
                    resource_text.column_headers = ', '.join([str(x) for x in df.columns.tolist()])
                    resource_text.row_headers = ', '.join([str(x) for x in df.index.tolist()])
                    # TODO: parsed wordcount
                elif resource['format'].lower() == 'xml':
                    # TODO
                    None
                else:
                    print 'unexpected text format:', resource['format']
                # TODO: have to get the actual resources here from it's url and then parse it based on type
                # TODO: store the parsed data in the other data tables 
            else:
                resource_map = ResourceMap()
                resource_map.id = resource['id']
                resource_map.dataset_id = data_set['id']
                resource_map.name = resource['name']
                resource_map.resource_url = resource['url']
                resource_map.type = resource['format']
                session.add(resource_map)
                # TODO: have to get the actual resources here from it's url and then parse it based on type
                # TODO: store the parsed data in the other data tables 
            
        session.commit()

        break
