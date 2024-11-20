
ARG PYTHON_VERSION=3.11

# Built .exe replay parsing tool is required to run sc2_replaypack_processor
# https://github.com/Kaszanas/SC2InfoExtractorGo
FROM kaszanas/sc2infoextractorgo:latest AS extractor

FROM python:${PYTHON_VERSION}-alpine AS build

WORKDIR /app

# Copying the replay parsing tool:
# sc2egset_replaypack_processor requires the .exe file to be in the same directory as the script:
COPY --from=extractor /app/SC2InfoExtractorGo /app/SC2InfoExtractorGo
# Ensure the executable has the right permissions
RUN chmod +x /app/SC2InfoExtractorGo

# Copy only what is required to install the project:
COPY pyproject.toml poetry.lock ci/install_poetry.py /app/

# Install poetry
# TODO: this is rather ugly, we are installing poetry into the release Docker build. Use multi-stage builds instead.
ENV POETRY_HOME=/opt/poetry
RUN python3 install_poetry.py --version 1.8.4 && \
    $POETRY_HOME/bin/poetry --version

# Install only dependencies without installing current project:
RUN $POETRY_HOME/bin/poetry \
    config virtualenvs.create false \
    && $POETRY_HOME/bin/poetry install --no-root

# Copy entire repository contents
COPY . .

# Install current project:
RUN $POETRY_HOME/bin/poetry install --all-extras
