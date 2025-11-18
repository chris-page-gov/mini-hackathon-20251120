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

# Pre-install Python dependencies defined in the workspace requirements file.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Clean up temporary files.
RUN rm /tmp/requirements.txt
