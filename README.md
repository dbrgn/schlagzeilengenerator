# schlagzeilengenerator.ch

![Screenshot](https://github.com/dbrgn/schlagzeilengenerator/raw/master/screenshot.png)

The headlines are tweeted daily by [@schlagzeilenbot](http://twitter.com/schlagzeilenbot).

## JSON API

To get JSON data from the website, just set the `Accept` header of a GET request
to `application/json`.

    curl -H "accept: application/json" http://www.schlagzeilengenerator.ch/

## Setup (Local)

Prerequisites: Python 3, [uv](https://docs.astral.sh/uv/)

1. Clone repository

2. Enter app directory

    cd app/

3. Install dependencies (automatically creates and manages virtual environment):

    uv sync

4. Export some environment variables:

    source env/dev

5. Run development server:

    uv run python app.py

## Setup (Docker)

Start containers:

    docker-compose build
    docker-compose up -d

To see the logs:

    docker-compose logs

## License

3-clause BSD, see `LICENSE` file for more information.

## Authors

* Danilo Bargen (Github: [@dbrgn](https://github.com/dbrgn/), Twitter: [@dbrgn](https://twitter.com/dbrgn))
* Simon Aebersold (Github: [@aebersold](https://github.com/aebersold/), Twitter: [@saebersold](https://twitter.com/saebersold))
