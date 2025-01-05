# Processed Mapping Copier

Utility script that enters each of the processed replaypack directories and copies the log files that are left after processing with `sc2_replaypack_processor`.

# CLI Usage

Please keep in mind that the  ```src/processed_mapping_copier.py``` contains required argument values and can be customized with the following command line interaface:
```
Usage: processed_mapping_copier.py [OPTIONS]

  Tool for copying the auxilliary file of processed_mapping.json to the
  matching directory after processing the replaypack into a JSON dataset with
  sc2egset_replaypack_processor.py. This script is required to reproduce
  SC2EGSet Dataset.

Options:
  --input_path DIRECTORY         Input path to the flattened replaypacks that
                                 contain procesed_mapping.json files.
                                 [required]
  --output_path DIRECTORY        Output path where processed_mapping.json will
                                 be copied.  [required]
  --log [INFO|DEBUG|ERROR|WARN]  Log level. Default is WARN.
  --help                         Show this message and exit.
```

# Execute With Docker

> [!NOTE]
> There are two ways of executing this script with Docker. One is to use the main repository Dockerfile (available in `docker` directory) and the other is to use the Dockerfile contained in this directory.

## Repository Docker Image

Please refer to the main [README](../../README.md) for the instructions.

## Script Docker Image

Build the docker image:
```bash
docker build --tag=datasetpreparator:latest .
```

Run the docker image (please replace `<paths>`):
```bash
docker run \
    -v "<./input>:/app/input" \
    -v "<./output>:/app/output" \
    datasetpreparator:latest \
    python3 processed_mapping_copier.py \
    --input_dir /app/input \
    --output_dir /app/output
```
