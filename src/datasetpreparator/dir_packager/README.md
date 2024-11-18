# Directory Packager

Utility script for compressing a directory into a `.zip` archive. This script iterates over all of the directories in the input directory and compresses them into `.zip` archives.

# CLI Usage

Please keep in mind that the  ```src/dir_packager.py``` contains default flag values and can be customized with the following command line flags:
```
Usage: dir_packager.py [OPTIONS]

Tool used for processing StarCraft 2 (SC2) datasets.
with https://github.com/Kaszanas/SC2InfoExtractorGo

Options:
  --input_path DIRECTORY    Please provide input path to the directory
                            containing the dataset that is going to be
                            processed by packaging into .zip archives.
                            [required]
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
docker build --tag=datasetpreparator:dir_packager .
```

Run the docker image (please replace `<paths>`):
```bash
docker run -v "<./input>:/app/input" \
    datasetpreparator:dir_packager \
    python3 dir_packager.py --input_dir /app/input
```
