from flask import *
app = Flask(__name__)

@app.route('/')
def index_handler():
    return render_template("index.html")

@app.route('/cloud')
def cloud_handler():
    return render_template("cloud.html")

@app.route('/cloud/<word>')
def word_handler(word):
    return render_template("word.html", word=word)

@app.route('/map')
def map_handler():
    return render_template("map.html")


if __name__ == '__main__':
    app.run(debug=True)