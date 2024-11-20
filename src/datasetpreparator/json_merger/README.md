# JSON Merger

Utility script that is merging two JSON files into an output JSON file.

# CLI Usage

Please keep in mind that the  ```src/json_merger.py``` contains default flag values and can be customized with the following command line flags:
```
Usage: json_merger.py [OPTIONS]

Tool used for merging two .json files. Created in order to merge two
mappings created by https://github.com/Kaszanas/SC2MapLocaleExtractor

Options:
  --json_one FILE                Please provide the path to the first .json
                                 file that is going to be merged.  [required]
  --json_two FILE                Please provide the path to the second .json
                                 file that is going to be merged.  [required]
  --output_filepath FILE         Please provide a filepath to which the result
                                 JSON file will be saved, note that any
                                 existing file of the same name will be
                                 overwriten.  [required]
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
docker build --tag=datasetpreparator:json_merger .
```

Run the docker image (please replace `<paths>`):
```bash
docker run -v "<./input>:/app/input" \
    datasetpreparator:file_packager \
    python3 json_merger.py \
    --json_one /app/input/json1.json \
    --json_two /app/input/json2.json \
    --output_filepath /app/input/merged.json
```
