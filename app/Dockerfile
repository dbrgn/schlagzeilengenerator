FROM ghcr.io/astral-sh/uv:alpine3.21

# Env vars
ENV PYTHONUNBUFFERED=1

# Dependencies
RUN apk add --update \
    uwsgi uwsgi-python3

ADD . /code

# Install dependencies using uv project management
ENV UV_PROJECT=/code
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
     "--plugin", "python3", \
     "--socket", "0.0.0.0:8000", \
     "--venv", "/code/.venv/", \
     "-w", "app:app", \
     "--master", \
     "--processes", "2", \
     "--threads", "2", \
     "--max-requests", "20", \
     "--reload-mercy", "10", \
     "--worker-reload-mercy", "10"]
