FROM mongo:3.0
MAINTAINER Danilo Bargen <mail@dbrgn.ch>

# Copy data and init script
COPY data /tmp/data
COPY init.sh /init.sh

# Create a new data directory, as we can't add data to the existing volume.
RUN mkdir -p /srv/mongodb && chown -R mongodb:mongodb /srv/mongodb

# Seed database with data
RUN /bin/bash /init.sh

# Cleanup
RUN rm -r /init.sh /tmp/data

# Create volume
VOLUME /srv/mongodb

CMD ["mongod", "--smallfiles", "--storageEngine", "wiredTiger", "--dbpath", "/srv/mongodb"]
