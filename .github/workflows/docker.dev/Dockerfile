# Set base image (host OS)
ARG PYTHON_VERSION=3.10
FROM python:$PYTHON_VERSION-slim AS ci

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install needed utlities and compilers that may be required for certain packages or platforms.
RUN  : \
     && apt-get update \
     && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        curl \
        bash \
        vim \
        build-essential \
     && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /intensive-brew

# Set python path
ENV  PYTHONPATH=/intensive-brew

# Install & configure needed package
RUN : \
    && pip3 install poetry \
    && poetry config virtualenvs.create false

# Install requirements
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

# Init git repo
RUN git init -b ci

# Port commit checks config
COPY .pre-commit-config.yaml .

# Install & pre-load pre-commit enviroments
RUN : \
    && pre-commit install --install-hooks \
    && pre-commit run

# Copy the content of the `src` directory to the working directory
COPY src/ ./src

# Copy the content of the `test` directory to the working directory
COPY tests/ ./tests

# Add all files to trigger commit checks
RUN git add .

# Enable container to be used as a binary that accepts input
ENTRYPOINT ["/bin/bash", "-c"]
