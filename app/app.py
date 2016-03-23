"""
    Schlagzeilengenerator
    ~~~~~~~~~~~~~~~~~~~~~

    A small web application to generate tabloid press headlines.

    :copyright: (c) 2012 by Danilo Bargen, Simon Aebersold.
    :license: BSD 3-clause, see LICENSE for more details.
"""

import os
import sys
from random import randrange
from urllib.parse import urlparse, urlunparse, quote_plus
from base64 import b64encode, b64decode

from flask import Flask, request, redirect
from flask import render_template, jsonify
from pymongo import MongoClient


app = Flask(__name__)


# Environment variables
env = os.environ.get
true_values = ['1', 'true', 'y', 'yes', 1, True]
def require_env(name):
    value = env(name)
    assert value, 'Missing {} env variable'.format(name)
    return value


# MongoDB connection
def get_mongo_client(host, port):
    print('[schlagzeilengenerator] Connecting to mongodb at %s:%s...' % (host, port))
    client = MongoClient(mongo_host, mongo_port,
                         connect=False,
                         serverSelectionTimeoutMS=6000,
                         connectTimeoutMS=2000,
                         socketTimeoutMS=1000)
    db = client[env('MONGODB_DB', 'schlagzeilengenerator')]
    if env('MONGODB_USER'):
        print('[schlagzeilengenerator] Authenticating against mongodb...')
        db.authenticate(require_env('MONGODB_USER'), require_env('MONGODB_PASSWORD'))
    return db

# Connect to MongoDB
mongo_host = env('MONGODB_HOST', '127.0.0.1')
mongo_port = int(env('MONGODB_PORT', '27017'))
app.db = get_mongo_client(mongo_host, mongo_port)


### Helper functions ###

def request_wants_json():
    # Taken from http://flask.pocoo.org/snippets/45/
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > request.accept_mimetypes['text/html']


def mongo_get_random(collection_name):
    collection = app.db[collection_name]
    count = collection.count()
    if count == 0:
        print('[schlagzeilengenerator] No data in the database.', file=sys.stderr)
        sys.exit(2)
    elif count == 1:
        offset = 0
    else:
        offset = randrange(1, count)
    return collection.find().skip(offset).limit(1)[0]


def mongo_get_by_id(collection_name, item_id):
    collection = app.db[collection_name]
    cursor = collection.find({'id': item_id}).limit(1)
    if cursor.count() == 0:
        errmsg = '[schlagzeilengenerator] %s item with ID %d not found.'
        print(errmsg % (collection_name, item_id), file=sys.stderr)
        raise ValueError(errmsg)
    return cursor[0]


### Headline generation ###

def generate_headline(ids=None):
    """Generate and return an awesome headline.

    Args:
        ids:
            Iterable of five IDs (intro, adjective, prefix, suffix, action).
            Optional. If this is ``None``, random values are fetched from the
            database.

    Returns:
        Tuple of parts and permalink (intro, adjective, prefix, suffix, action,
        permalink)

    """
    print('[schlagzeilengenerator] Generating a headline...')

    # Correct endings
    adjective_endings = {
        'm': 'r',
        'w': '',
        's': 's',
        'p': '',
    }

    # Get random database entries
    if ids is not None:
        d_intro = mongo_get_by_id('intro', ids[0])
        d_adjective = mongo_get_by_id('adjective', ids[1])
        d_prefix = mongo_get_by_id('prefix', ids[2])
        d_suffix = mongo_get_by_id('suffix', ids[3])
        d_action = mongo_get_by_id('action', ids[4])
    else:
        d_intro = mongo_get_random('intro')
        d_adjective = mongo_get_random('adjective')
        d_prefix = mongo_get_random('prefix')
        d_suffix = mongo_get_random('suffix')
        d_action = mongo_get_random('action')
        ids = (d_intro['id'], d_adjective['id'], d_prefix['id'], d_suffix['id'], d_action['id'])

    # Get data from mongo dictionaries
    case = d_suffix['case']
    intro = d_intro['text']
    adjective = d_adjective['text'] + adjective_endings[case]
    prefix = d_prefix['text']
    suffix = d_suffix['text']
    if case == 'p':
        action = '%s %s' % (d_action['action_p'], d_action['text'])
    else:
        action = '%s %s' % (d_action['action_s'], d_action['text'])

    # Build permalink
    permalink = b64encode(b','.join(str(i).encode('ascii') for i in ids))

    return intro, adjective, prefix, suffix, action.strip(), permalink


### Views ###

@app.context_processor
def inject_url():
    """Inject the website-URL into the context."""
    return dict(app_url=os.environ.get('APP_URL', 'http://www.schlagzeilengenerator.ch/'))


@app.route('/', methods=['GET'])
@app.route('/<permalink>', methods=['GET'])
def headline(permalink=None):
    # Prepare variables
    error = ''
    status_code = 200

    # Fetch parts
    if permalink is None:
        intro, adjective, prefix, suffix, action, link = generate_headline()
    else:
        try:
            ids = [int(i) for i in b64decode(permalink).decode('ascii').split(',')]
            assert len(ids) == 5, 'There must be 5 IDs in permalink'
            intro, adjective, prefix, suffix, action, link = generate_headline(ids)
        except (ValueError, AssertionError, TypeError):
            error = 'Invalid permalink.'

    # Prepare and return output
    if error == '':
        context = {
            'intro': intro,
            'adjective': adjective,
            'subject': '%s-%s' % (prefix, suffix),
            'action': action,
            'headline': '%s: %s %s-%s %s' % (intro, adjective, prefix, suffix, action),
            'permalink': quote_plus(link),
        }
    else:
        context = {'error': 'Invalid permalink.'}
        status_code = 400
    if request_wants_json():
        return jsonify(context), status_code
    return render_template('headline.html', **context), status_code


if env('DEBUG', 'False').lower() in true_values:
    app.config['DEBUG'] = True


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = env('DEBUG', 'False').lower() in true_values
    app.run(host='0.0.0.0', port=port, debug=debug)