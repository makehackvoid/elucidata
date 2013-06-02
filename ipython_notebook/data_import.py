import pandas
import json
import requests
from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
import dateutil.parser
import time
import regex
from collections import Counter

stop_words = '''about,after,all,also,an,and,another,any,are,as,at,be,because,been,before
being,between,both,but,by,came,can,come,could,did,do,each,for,from,get
got,has,had,he,have,her,here,him,himself,his,how,if,in,into,is,it,like
make,many,me,might,more,most,much,must,my,never,now,of,on,only,or,other
our,out,over,said,same,see,should,since,some,still,such,take,than,that
the,their,them,then,there,these,they,this,those,through,to,too,under,up
very,was,way,we,well,were,what,where,which,while,who,with,would,you,your,a
b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,$,1,2,3,4,5,6,7,8,9,0,_
NaN,Inc'''
stop_words = stop_words.replace('\n',',')
stop_words = stop_words.split(',')

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
    
    raw_data = raw_data.decode('iso-8859-1').encode('ascii', 'ignore')
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
    'notes',
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
        note = data_set['notes']
        if note.startswith('    \n\n'):
            note = note.replace('    \n\n','')
            note = note[0:note.find('\n\n')]
        dataset.description = note
        session.add(dataset)
        
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
            continue
        
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
            tag.tag = a_tag['name']
            session.add(tag)
        
        session.commit()

        # fill the resource_text or resource_map table 
        for resource in data_set['resources']:
            session.begin()
            if text_format(resource):
                resource_text = ResourceText()
                resource_text.id = resource['id']
                resource_text.dataset_id = data_set['id']
                resource_text.name = resource['name']
                resource_text.resource_url = resource['url']
                resource_text.type = resource['format']
                if resource['format'].lower() == 'csv':
                    cnt = Counter()
                    
                    try:
                        df = pandas.DataFrame.from_csv(resource['url'])
                        resource_text.column_headers = ', '.join([str(x).decode('iso-8859-1').encode('ascii', 'ignore') for x in df.columns.tolist()])
                        resource_text.row_headers = ', '.join([str(x).decode('iso-8859-1').encode('ascii', 'ignore') for x in df.index.tolist()])
                        a_words = regex.sub('[^a-zA-Z ]+','', df.to_string())
                        a_words = a_words.decode('iso-8859-1').encode('ascii', 'ignore')
                        a_words = a_words.replace('NaN','')
                        for a_word in a_words.split():
                            if a_word not in stop_words:
                                cnt[a_word] += 1
                        resource_text.wordcount = len(a_words)
                        resource_text.parsed = True
                    
                        session.add(resource_text)
                        session.commit()
                        #if len(cnt.items()) > 0:
                        session.begin()
                        # get the top 30 words and put htem into word
                        for w in cnt.most_common(30):
                            word = Word()
                            word.word = w[0]
                            word.frequency = w[1]
                            word.text_id = resource['id']
                            session.add(word)
                        session.commit()
                        
                    except:
                        resource_text.parsed = False
                        session.add(resource_text)
                        session.commit()

                        continue
                # elif resource['format'].lower() == 'xml':
                    # TODO (later)
                    # None
                # else:
                    # print 'unexpected text format:', resource['format']
 
            else:
                resource_map = ResourceMap()
                resource_map.id = resource['id']
                resource_map.dataset_id = data_set['id']
                resource_map.name = resource['name']
                resource_map.resource_url = resource['url']
                resource_map.type = resource['format']
                # TODO: have to get the actual resources here from it's url and then parse it based on type
                if resource['format'].lower() == 'kml':
                    # TODO: parse kml data and fill datapoint and coordinate tables
                    # print resource['url']
                    None
                # else:
                    # print 'unexpected text format:', resource['format']
                session.add(resource_map)
                session.commit()
        session.close()
        
print "finished"