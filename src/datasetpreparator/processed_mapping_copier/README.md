# Processed Mapping Copier

Utility script that enters each of the processed replaypack directories and copies the log files that are left after processing with `sc2_replaypack_processor`.

# CLI Usage

Please keep in mind that the  ```src/processed_mapping_copier.py``` contains default flag values and can be customized with the following command line flags:
```
Usage: processed_mapping_copier.py [OPTIONS]

Tool for copying the processed_mapping.json files to the matching directory
after processing the replaypack into a JSON dataset. This step is required
to define the StarCraft 2 (SC2) dataset.

Options:
  --input_path DIRECTORY    Please provide input path to the flattened
                            replaypacks that contain procesed_mapping.json
                            files.  [required]
  --output_path DIRECTORY   Please provide output path where
                            processed_mapping.json will be copied.  [required]
  --log [INFO|DEBUG|ERROR]  Log level (INFO, DEBUG, ERROR)
  --help                    Show this message and exit.
```

# Execute With Docker

> [!NOTE]
> There are two ways of executing this script with Docker. One is to use the main repository Dockerfile (available in `docker` directory) and the other is to use the Dockerfile contained in this directory.

## Repository Docker Image

Please refer to the main [README](../../README.md) for the instructions.

## Script Docker Image

Buil the docker image:
```bash
docker build --tag=datasetpreparator:processed_mapping_copier .
```

Run the docker image (please replace `<paths>`):
```bash
docker run \
    -v "<./input>:/app/input" \
    -v "<./output>:/app/output" \
    datasetpreparator:file_packager \
    python3 processed_mapping_copier.py \
    --input_dir /app/input \
    --output_dir /app/output
```
