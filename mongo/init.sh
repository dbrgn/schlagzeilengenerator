#!/bin/bash
set -e

# Start mongodb in background
/bin/bash /entrypoint.sh mongod \
    --smallfiles \
    --storageEngine wiredTiger \
    --dbpath /srv/mongodb &
MONGO_PID=$!

# Sleep a bit
echo "Waiting 30s for mongod to start..."
sleep 30

# Import data
mongoimport -d schlagzeilengenerator -c intro --file /tmp/data/intro.json
mongoimport -d schlagzeilengenerator -c adjective --file /tmp/data/adjective.json
mongoimport -d schlagzeilengenerator -c prefix --file /tmp/data/prefix.json
mongoimport -d schlagzeilengenerator -c suffix --file /tmp/data/suffix.json
mongoimport -d schlagzeilengenerator -c action --file /tmp/data/action.json

# Stop mongodb
kill -INT $MONGO_PID
