# SC2 Map Downloader

Utility script that opens each of the provided replays and downloads the map from the Blizzard servers. This is required to later create the localization mapping for map translation with [SC2MapLocaleExtractor](https://github.com/Kaszanas/SC2MapLocaleExtractor).

# CLI Usage

Please keep in mind that the  ```src/sc2_map_downloader.py``` contains required argument values and can be customized with the following command line interaface:
```
Usage: sc2_map_downloader.py [OPTIONS]

  Tool for downloading StarCraft 2 (SC2) maps based on the data that available
  within .SC2Replay files.

Options:
  --input_path DIRECTORY         Input path to the dataset that is going to be
                                 processed. The script will find all
                                 .SC2Replay files in the directory.
                                 [required]
  --output_path DIRECTORY        Output path where StarCraft 2 (SC2) map files
                                 will be downloaded.  [required]
  --log [INFO|DEBUG|ERROR|WARN]  Log level. Default is WARN.
  --help                         Show this message and exit.
```

# Execute With Docker

## Repository Docker Image

Please refer to the main [README](../../README.md) for the instructions.
