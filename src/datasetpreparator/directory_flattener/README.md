# Directory Flattener

Utility script for entering each of the supplied replaypacks and flattening its structure. Please note that in the process of flattening the structure, the script will also rename the files using their hash values. Hashing of filenames is done to alleviate the potential files with the same name in different directories.

# CLI Usage

Please keep in mind that ```src/directory_flattener.py``` does not contain default flag values and can be customized with the following command line flags:

```
Usage: directory_flattener.py [OPTIONS]

Directory restructuring tool used in order to flatten the structure, map the
old structure to a separate file, and for later processing with other tools.
Created primarily to define StarCraft 2 (SC2) datasets.

Options:
  --input_path DIRECTORY         Please provide input path to the dataset that
                                 is going to be processed.  [required]
  --output_path DIRECTORY        Please provide output path where the tool
                                 will put files after processing.  [required]
  --file_extension TEXT          Specify file extension for the files that
                                 will be put to the top level directory.
                                 [required]
  --log [INFO|DEBUG|ERROR|WARN]  Log level
  --help                         Show this message and exit.
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
    datasetpreparator:directory_flattener \
    python3 directory_flattener.py \
    --input_dir /app/input \
    --output_dir /app/output \
    --file_extension .SC2Replay
```
