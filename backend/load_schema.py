from sqlalchemy import *

metadata = MetaData()

coordinate = Table('coordinate', metadata,
    Column('id', Integer, primary_key = True),
    Column('lat', Float, nullable = False),
    Column('long', Float, nullable = False)
)

datapoint = Table('datapoint', metadata,
    Column('map_id', String, ForeignKey('resource_map.id'), primary_key = True, autoincrement = False),
    Column('coordinate_id', Integer, ForeignKey('coordinate.id'), primary_key = True, autoincrement = False),
    Column('weight', Integer, nullable = False)
)

resource_map = Table('resource_map', metadata,
    Column('id', String, primary_key = True, autoincrement = False),
    Column('dataset_id', String, ForeignKey('dataset.id'), nullable = False),
    Column('type', String),
    Column('name', String),
    Column('resource_url', String),
    Column('parsed', Boolean)
)

dataset = Table('dataset', metadata,
    Column('id', String, primary_key = True, autoincrement = False),
    Column('api_url', String),
    Column('revision_date', Integer),
    Column('revision_id', String),
    Column('name', String),
    Column('description', String),
    Column('url_name', String),
    Column('provider', String)
)

resource_text = Table('resource_text', metadata,
    Column('id', String, primary_key = True, autoincrement = False),
    Column('dataset_id', String, ForeignKey('dataset.id'), nullable = False),
    Column('column_headers', String),
    Column('row_headers', String),
    Column('type', String),
    Column('name', String),
    Column('resource_url', String),
    Column('wordcount', Integer),
    Column('parsed', Boolean)
)

resource_word = Table('word', metadata,
    Column('text_id', String, ForeignKey('resource_text.id'), primary_key = True, autoincrement = False),
    Column('word', String, primary_key = True, autoincrement = False),
    Column('frequency', Float)
)

tag = Table('tag', metadata,
    Column('dataset_id', String, ForeignKey('dataset.id'), primary_key = True, autoincrement = False),
    Column('tag', String, primary_key = True, autoincrement = False)
)

group = Table('group', metadata,
    Column('dataset_id', String, ForeignKey('dataset.id'), primary_key = True, autoincrement = False),
    Column('group', String, primary_key = True, autoincrement = False)
)

# TODO: move database details into config file not held in repository
user = 'postgres'
password = ''
server = 'localhost'
port = '5432'
database = 'mhv-govhack'
databaseurl = 'postgresql://' + user + ':' + password + '@' + server + ':' + port + '/' + database
engine = create_engine(databaseurl, client_encoding='utf8')

metadata.create_all(engine)
