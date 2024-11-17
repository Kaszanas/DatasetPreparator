# Directory Flattener

Utility script for entering each of the supplied replaypacks and flattening its structure. Please note that in the process of flattening the structure, the script will also rename the files using their hash values. Hashing of filenames is done to alleviate the potential files with the same name in different directories.

# CLI Usage

Please keep in mind that ```src/directory_flattener.py``` does not contain default flag values and can be customized with the following command line flags:

```
usage: directory_flattener.py [-h] [--input_path INPUT_PATH] [--output_path OUTPUT_PATH]
                              [--file_extension FILE_EXTENSION]

Directory restructuring tool used in order to flatten the structure, map the old structure to a separate
file, and for later processing with other tools. Created primarily to define StarCraft 2 (SC2) datasets.

options:
  -h, --help            show this help message and exit
  --input_path INPUT_PATH (default = ../../processing/directory_flattener/input)
                        Please provide input path to the dataset that is going to be processed.
  --output_path OUTPUT_PATH (default = ../../processing/directory_flattener/output)
                        Please provide output path where sc2 map files will be downloaded.
  --file_extension FILE_EXTENSION (default = .SC2Replay)
                        Please provide a file extension for files that will be moved and renamed.
```

# Execute With Docker

> [!NOTE]
> There are two ways of executing this script with Docker. One is to use the main repository Dockerfile (available in `docker` directory) and the other is to use the Dockerfile contained in this directory.

## Repository Docker Image

Please refer to the main [README](../../README.md) for the instructions.

## Script Docker Image

Buil the docker image:
```bash
docker build --tag=datasetpreparator:directory_flattener .
```

Run the docker image (please replace `<paths>`):
```bash
docker run
    -v "<./input>:/app/input" \
    -v "<./output>:/app/output" \
    datasetpreparator:file_packager \
    python3 directory_flattener.py \
    --input_dir /app/input \
    --output_dir /app/output \
    --file_extension .SC2Replay
```
