FROM mongo:3.0
MAINTAINER Danilo Bargen <mail@dbrgn.ch>

COPY data /data
COPY init.sh /init.sh

RUN /bin/bash /init.sh
