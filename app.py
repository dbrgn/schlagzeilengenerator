import os
import sys

from flask import Flask
from flask_heroku import Heroku
from mongokit import Connection

import models


app = Flask(__name__)
heroku = Heroku(app)

app.debug = True

connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
connection.register(models.BasePart.__subclasses__())
db = connection[app.config['MONGODB_DB']]


### Views ###

@app.route('/')
def hello():
    return 'Hello World!'


### Management functions ###

def load_fixture_data(clear=False):
    import fixtures
    for collection, data in fixtures.collections:
        if clear:
            print 'Dropping collection %s' % collection
            db[collection].drop()
        print 'Loading collection %s' % collection
        db[collection].insert(data)


### Dev Server ###

if __name__ == '__main__':
    if sys.argv[1] == 'loaddata':
        clear = len(sys.argv) > 2 and sys.argv[2] == '--clear'
        load_fixture_data(clear=clear)
    else:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
