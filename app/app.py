# coding=utf-8
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
from urlparse import urlparse, urlunparse
from urllib import quote_plus
from base64 import b64encode, b64decode

from flask import Flask, request, redirect
from flask import render_template, jsonify
from flask_heroku import Heroku
from pymongo import Connection


app = Flask(__name__)
heroku = Heroku(app)


connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
db = connection[app.config['MONGODB_DB']]
if app.config['MONGODB_USER']:
    db.authenticate(app.config['MONGODB_USER'], app.config['MONGODB_PASSWORD'])


### Helper functions ###

def request_wants_json():
    # Taken from http://flask.pocoo.org/snippets/45/
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > request.accept_mimetypes['text/html']


def mongo_get_random(collection_name):
    collection = db[collection_name]
    count = collection.count()
    if count == 0:
        print >> sys.stderr, 'No data in the database.'
        sys.exit(2)
    elif count == 1:
        offset = 0
    else:
        offset = randrange(1, count)
    return collection.find().skip(offset).limit(1)[0]


def mongo_get_by_id(collection_name, item_id):
    collection = db[collection_name]
    cursor = collection.find({'id': item_id}).limit(1)
    if cursor.count() == 0:
        errmsg = '%s item with ID %d not found.' % (collection_name, item_id)
        print >> sys.stderr, errmsg
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
    permalink = b64encode(','.join(map(str, ids)))

    return intro, adjective, prefix, suffix, action.strip(), permalink


### Views ###

@app.before_request
def redirect_nonwww():
    """Redirect non-www requests to www."""
    urlparts = urlparse(request.url)
    if urlparts.netloc == 'schlagzeilengenerator.ch':
        urlparts_list = list(urlparts)
        urlparts_list[1] = 'www.schlagzeilengenerator.ch'
        return redirect(urlunparse(urlparts_list), code=301)


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
            ids = map(int, b64decode(permalink).split(','))
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG') in ['true', 'True', 'TRUE', 't', 'T', '1']
    app.run(host='0.0.0.0', port=port, debug=debug)
