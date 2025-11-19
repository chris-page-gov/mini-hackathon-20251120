# syntax=docker/dockerfile:1

FROM mcr.microsoft.com/devcontainers/python:3.11

# Install system packages required for geospatial and scientific Python libraries.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gdal-bin \
        libgdal-dev \
        libproj-dev \
        libspatialindex-dev \
        build-essential \
        curl \
        unzip \
    && rm -rf /var/lib/apt/lists/*

# Install uv globally so dependency installs can run without manual steps.
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && mv /root/.local/bin/uvx /usr/local/bin/uvx \
    && rm -rf /root/.local
