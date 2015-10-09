#!/bin/bash
set -e

# Start mongodb in background
/bin/bash /entrypoint.sh mongod --smallfiles &
MONGO_PID=$!

# Sleep a bit
echo "Waiting 25s for mongod to start..."
sleep 25

# Import data
mongoimport --drop -d schlagzeilengenerator -c intro --file /data/intro.json
mongoimport --drop -d schlagzeilengenerator -c adjective --file /data/adjective.json
mongoimport --drop -d schlagzeilengenerator -c prefix --file /data/prefix.json
mongoimport --drop -d schlagzeilengenerator -c suffix --file /data/suffix.json
mongoimport --drop -d schlagzeilengenerator -c action --file /data/action.json

# Stop mongodb
kill -INT $MONGO_PID
