########################
schlagzeilengenerator.ch
########################

.. image:: https://github.com/dbrgn/schlagzeilengenerator/raw/master/screenshot.png

The headlines are tweeted daily by `@schlagzeilenbot <http://twitter.com/schlagzeilenbot>`_.


JSON API
========

To get JSON data from the website, just set the `Accept` header of a GET request
to `application/json`.

::

    $ curl -H "accept: application/json" http://www.schlagzeilengenerator.ch/


Setup (Local)
=============

Prerequisites: Python 2, Pip, MongoDB

1. Clone repository

2. If desired, create and activate a virtualenv::

    $ virtualenv --no-site-packages VIRTUAL
    $ source VIRTUAL/bin/activate

3. Install requirements::

    $ pip install -r requirements.txt

4. Import testdata into a MongoDB database called "schlagzeilengenerator"::

    $ mongoimport --drop -d schlagzeilengenerator -c intro --file data/intro.json
    $ mongoimport --drop -d schlagzeilengenerator -c adjective --file data/adjective.json
    $ mongoimport --drop -d schlagzeilengenerator -c prefix --file data/prefix.json
    $ mongoimport --drop -d schlagzeilengenerator -c suffix --file data/suffix.json
    $ mongoimport --drop -d schlagzeilengenerator -c action --file data/action.json

5. Export some environment variables::

    $ source env/dev

6. Run development server::

    $ python app.py


Setup (Heroku)
==============

::

    $ heroku apps:create --region eu [appname]
    $ heroku addons:add mongolab:sandbox
    $ heroku addons:add newrelic:standard
    $ heroku addons:open newrelic:standard
    $ git push heroku master


License
=======

3-clause BSD, see `LICENSE` file for more information.


Authors
=======

* Danilo Bargen (Github: `@dbrgn <https://github.com/dbrgn/>`_, Twitter: `@dbrgn <https://twitter.com/dbrgn>`_)
* Simon Aebersold (Github: `@aebersold <https://github.com/aebersold/>`_, Twitter: `@saebersold <https://twitter.com/saebersold>`_)
