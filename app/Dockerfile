FROM alpine:3.2
MAINTAINER Danilo Bargen <mail@dbrgn.ch>

# Env vars
ENV PYTHONUNBUFFERED=1

# Dependencies
RUN apk add --update \
    python3 python3-dev py-pip \
    uwsgi uwsgi-python3 \
    git \
    gcc libc-dev

# Add code
#RUN git clone https://github.com/dbrgn/schlagzeilengenerator /git \
#    && mv /git/app /code \
#    && rm -r /git /code/Dockerfile
ADD . /code
RUN rm /code/Dockerfile

# Install pypi dependencies
RUN pip3 install -r /code/requirements.txt

# Server directory
RUN adduser -D generator \
    && chown -R generator:generator /code

# Expose volume
VOLUME ["/code/static"]

# Change to unprivileged user
USER generator

# Entry point
WORKDIR /code
EXPOSE 5000
CMD ["uwsgi", \
     "--plugin", "/usr/lib/uwsgi/python3", \
     "--socket", "0.0.0.0:5000", \
     "-w", "app:app", \
     "--master", \
     "--processes", "2", \
     "--threads", "2", \
     "--max-requests", "20"]
