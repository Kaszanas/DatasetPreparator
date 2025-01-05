# File Renamer

# CLI Usage

Please keep in mind that the  ```src/file_renamer.py``` contains required argument values and can be customized with the following command line interaface:
```
Usage: file_renamer.py [OPTIONS]

  Tool used for renaming auxilliary files (log files) that are produced when
  creating StarCraft 2 (SC2) datasets with
  https://github.com/Kaszanas/SC2InfoExtractorGo

Options:
  --input_path DIRECTORY         Input path to the directory containing the
                                 dataset that is going to be processed by
                                 packaging into .zip archives.  [required]
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
docker run -v "<./input>:/app/input" \
    datasetpreparator:latest \
    python3 file_renamer.py --input_dir /app/input
```
