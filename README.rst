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

    curl -H "accept: application/json" http://www.schlagzeilengenerator.ch/


Setup (Local)
=============

Prerequisites: Python 3, Pip

1. Clone repository

2. If desired, create and activate a virtualenv::

    virtualenv -p /usr/bin/python3 VIRTUAL
    source VIRTUAL/bin/activate

3. Install requirements::

    pip install -r app/requirements.txt

4. Export some environment variables::

    source env/dev

5. Run development server::

    DEBUG=true python app/app.py


Setup (Docker)
==============

Start containers::

    docker-compose build
    docker-compose up -d

To see the logs::

    docker-compose logs


License
=======

3-clause BSD, see `LICENSE` file for more information.


Authors
=======

* Danilo Bargen (Github: `@dbrgn <https://github.com/dbrgn/>`_, Twitter: `@dbrgn <https://twitter.com/dbrgn>`_)
* Simon Aebersold (Github: `@aebersold <https://github.com/aebersold/>`_, Twitter: `@saebersold <https://twitter.com/saebersold>`_)
