FROM docker.io/alpine:3.16

# Env vars
ENV PYTHONUNBUFFERED=1

# Dependencies
RUN apk add --update \
    python3 python3-dev \
    uwsgi uwsgi-python3 \
    git \
    gcc libc-dev \
    curl

# Install uv with pinned version using binary for better security
ARG UV_VERSION=0.4.18
RUN curl -LsSf https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-${UV_VERSION}-x86_64-unknown-linux-musl.tar.gz \
    | tar -xzC /usr/local/bin --strip-components=1 \
    && chmod +x /usr/local/bin/uv

ADD . /code

# Install dependencies using uv project management
RUN uv sync

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
CMD ["uv", "run", "uwsgi", \
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
