
ARG PYTHON_VERSION=3.11

# Built .exe replay parsing tool is required to run sc2_replaypack_processor
# https://github.com/Kaszanas/SC2InfoExtractorGo
FROM kaszanas/sc2infoextractorgo:latest AS extractor

FROM python:${PYTHON_VERSION}-alpine AS build

WORKDIR /app

# Copying the replay parsing tool:
# sc2egset_replaypack_processor requires the .exe file to be in the same directory as the script:
COPY --from=extractor /app/SC2InfoExtractorGo /app/SC2InfoExtractorGo
COPY --from=extractor /app/maps/ /app/maps/

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

# Copy test files:
COPY /src/ /app/src/
COPY /tests/__init__.py /app/tests/__init__.py
COPY /tests/conftest.py /app/tests/conftest.py
COPY /tests/test_utils.py /app/tests/test_utils.py
COPY /tests/test_settings.py /app/tests/test_settings.py
COPY /tests/test_main.py /app/tests/test_main.py
COPY /tests/test_cases/ /app/tests/test_cases/

# Copy docs files:
COPY /docs/ /app/docs/
COPY mkdocs.yml /app/mkdocs.yml
COPY README.md /app/README.md
COPY CONTRIBUTING.md /app/CONTRIBUTING.md

# Bring the scripts to the top level.
# They import parts of the project but as long as the project is installed
# in the same environment, they can run from anywhere as long as the environment
# is activated.
COPY /src/datasetpreparator/directory_flattener/directory_flattener.py \
    /src/datasetpreparator/directory_packager/directory_packager.py \
    /src/datasetpreparator/file_renamer/file_renamer.py \
    /src/datasetpreparator/json_merger/json_merger.py \
    /src/datasetpreparator/processed_mapping_copier/processed_mapping_copier.py \
    /src/datasetpreparator/sc2/sc2_map_downloader/sc2_map_downloader.py \
    /src/datasetpreparator/sc2/sc2egset_replaypack_processor/sc2egset_replaypack_processor.py \
    /src/datasetpreparator/sc2/sc2reset_replaypack_downloader/sc2reset_replaypack_downloader.py \
    /app/


# Install current project:
RUN $POETRY_HOME/bin/poetry install --all-extras
