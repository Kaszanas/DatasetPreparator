# SC2 Map Downloader

Utility script that opens each of the provided replays and downloads the map from the Blizzard servers. This is required to later create the localization mapping for map translation with [SC2MapLocaleExtractor](https://github.com/Kaszanas/SC2MapLocaleExtractor).

# CLI Usage

Please keep in mind that the  ```src/sc2_map_downloader.py``` does not contain default flag values and can be customized with the following command line flags:
```
Usage: sc2_map_downloader.py [OPTIONS]

Tool for downloading StarCraft 2 (SC2) maps based on the data that is
available within .SC2Replay file.

Options:
  --input_path DIRECTORY         Please provide input path to the dataset that
                                 is going to be processed.  [required]
  --output_path DIRECTORY        Please provide output path where StarCraft 2
                                 (SC2) map files will be downloaded.
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
docker build --tag=datasetpreparator:sc2_map_downloader .
```

Run the docker image (please replace `<paths>`):
```bash
docker run \
    -v "<./input>:/app/input" \
    -v "<./output>:/app/output" \
    datasetpreparator:sc2_map_downloader \
    python3 sc2_map_downloader.py \
    --input_dir /app/input \
    --output_dir /app/output
```
