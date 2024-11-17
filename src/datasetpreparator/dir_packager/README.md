# File Packager

Utility script for compressing a directory into a `.zip` archive.

# CLI Usage

Please keep in mind that the  ```src/file_packager.py``` contains default flag values and can be customized with the following command line flags:
```
usage: file_packager.py [-h] [--input_dir INPUT_DIR]

Tool used for processing StarCraft 2 (SC2) datasets. with https://github.com/Kaszanas/SC2InfoExtractorGo

options:
  -h, --help            show this help message and exit
  --input_dir INPUT_DIR (default = ../../processing/sc2_replaypack_processor/output)
                        Please provide input path to the directory containing the dataset that is going to be processed by packaging into .zip archives.
```

# Execute With Docker

> [!NOTE]
> There are two ways of executing this script with Docker. One is to use the main repository Dockerfile (available in `docker` directory) and the other is to use the Dockerfile contained in this directory.

## Repository Docker Image

Please refer to the main [README](../../README.md) for the instructions.

## Script Docker Image

Buil the docker image:
```bash
docker build --tag=datasetpreparator:file_packager .
```

Run the docker image (please replace `<paths>`):
```bash
docker run -v "<./input>:/app/input" \
    datasetpreparator:file_packager \
    python3 dir_packager.py --input_dir /app/input
```
