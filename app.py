import os

from flask import Flask
from flask_heroku import Heroku
from  pymongo import Connection


app = Flask(__name__)
heroku = Heroku(app)

app.debug = True

connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
db = connection[app.config['MONGODB_DB']]


### Views ###

@app.route('/')
def hello():
    return 'Hello World!'


### Dev Server ###

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
