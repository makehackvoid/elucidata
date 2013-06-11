from flask import *
from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)

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

def get_words(root_word = None, limit = 30):
    sql = "SELECT SUM(frequency) AS total, word FROM word "
    if root_word != None:
        sql += "INNER JOIN resource_text ON word.text_id = resource_text.id "
        sql += "WHERE (SELECT word1.text_id FROM word AS word1 "
        sql += "WHERE resource_text.id = word1.text_id AND word1.word = '" + root_word + "') = word.text_id "
    sql += "GROUP BY word ORDER BY total DESC LIMIT " + str(limit)
    result = session.query("total", "word").from_statement(sql).all()
    max_freq = 0
    for r in result:
        if r.total > max_freq: max_freq = r.total

    array_string = "["
    for r in result:
        array_string += "{text: '" + r.word + "', size: " + str(10 + (1.0* r.total / max_freq * 70)) + "},"
    if len(result) != 0:
        array_string = array_string[:-1]
    array_string += "]"
    return array_string

def get_dataset_words(dataset): 
    results = session.query(Word).filter(Word.text_id == ResourceText.id).filter(ResourceText.dataset_id == dataset.id).all()
    max_freq = 0
    for r in results:
        if r.frequency > max_freq: max_freq = r.frequency

    array_string = "["
    for r in results:
        array_string += "{text: '" + r.word + "', size: " + str(10 + (1.0* r.frequency / max_freq * 70)) + "},"
    if len(results) != 0:
        array_string = array_string[:-1]
    array_string += "]"
    return array_string

def get_datasets_for_word(word):
    results = session.query(DataSet).filter(DataSet.id == ResourceText.dataset_id).filter(ResourceText.id == Word.text_id).filter(Word.word == word).all()
    return results;

def get_words_for_datasets(datasets):
    r = {}
    for dataset in datasets:
        r[dataset] = get_dataset_words(dataset)
    return r

@app.route('/')
def index_handler():
    print session.query(DataSet).count()
    return render_template("index.html", map_data=session.query(Coordinate).all(), cloud_data=get_words())

@app.route('/cloud')
def cloud_handler():
    return render_template("cloud.html", cloud_data=get_words(limit = 100))

@app.route('/cloud/<word>')
def word_handler(word):
    datasets = get_datasets_for_word(word)
    word_clouds = get_words_for_datasets(datasets)
    return render_template("word.html", word=word, cloud_data = get_words(word), datasets = datasets, dataset_clouds = word_clouds)

@app.route('/map')
def map_handler():
    return render_template("map.html", map_data=session.query(Coordinate).all())


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=80)