FROM ghcr.io/astral-sh/uv:0.9-python3.13-trixie-slim

ARG UID=1000
ARG GID=1000

# Install development dependencies
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
    neovim \
    git \
    curl \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r dev -g $GID \
 && useradd -r -g dev -u $UID -d /home/dev -s /bin/bash dev \
 && mkdir /home/dev && chown dev:dev /home/dev

# Create workspace directory with default ownership
# Note: VS Code Dev Containers will automatically adjust UID/GID via updateRemoteUserUID
RUN mkdir -p /code && chown dev:dev /code

# Switch to non-root user
USER dev

# Create OpenCode directories with default ownership
RUN mkdir -p ~/.config/opencode/ \
 && mkdir -p ~/.local/share/opencode/

ENTRYPOINT ["/bin/bash"]
