#################################################
# CI stage exists to gurantee that no release   #
# image is ever built without testing           #
#################################################

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
ENV  PYTHONPATH="${PYTHONPATH}:/intensive-brew"

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

# Copy the content of the `README` file needed for packaging
COPY README.md/ .

# Copy the content of the `src` directory to the working directory
COPY src/ ./src

# Copy the content of the `test` directory to the working directory
COPY tests/ ./tests

# Add all files to trigger commit checks
RUN git add .

# `Poe the Poet` doesn't need to activate the Python environment.
ENV POETRY_ACTIVE 1

RUN : \
    # Lint project & check for safety
    && poe lint \
    # Run tests and check coverage
    && poe test \
    # Package the project
    && poetry build --format=wheel


# Release stage
FROM python:3.10-slim AS app

# Configure Python to print tracebacks on crash
ENV PYTHONFAULTHANDLER=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /intensive-brew

# Set python path
ENV  PYTHONPATH=/intensive-brew

# Get destribution package from `ci` stage
COPY --from=ci /intensive-brew/dist ./dist

# Install package and depednancies
RUN pip3 install dist/*

# Enable container to be used as a binary that accepts input
ENTRYPOINT ["intensive-brew"]