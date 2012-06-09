########################
schlagzeilengenerator.ch
########################

Coming soon.


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

    $ heroku apps:create --stack cedar [appname]
    $ heroku addons:add mongolab:starter
    $ git push heroku master
