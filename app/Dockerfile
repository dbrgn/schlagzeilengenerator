FROM docker.io/alpine:3.16

# Env vars
ENV PYTHONUNBUFFERED=1

# Dependencies
RUN apk add --update \
    python3 python3-dev py-pip \
    uwsgi uwsgi-python3 \
    git \
    gcc libc-dev

ADD . /code

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
EXPOSE 8000
CMD ["uwsgi", \
     "--plugins-dir", "/usr/lib/uwsgi", \
     "--plugin", "python3", \
     "--socket", "0.0.0.0:8000", \
     "-w", "app:app", \
     "--master", \
     "--processes", "2", \
     "--threads", "2", \
     "--max-requests", "20", \
     "--reload-mercy", "10", \
     "--worker-reload-mercy", "10"]
