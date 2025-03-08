# JSON Merger

Utility script that is merging two JSON files into an output JSON file.

# CLI Usage

Please keep in mind that the  ```src/json_merger.py``` contains required argument values and can be customized with the following command line interaface:
```
Usage: json_merger.py [OPTIONS]

  Tool used for merging two .json files. Originally used to merge two json
  files created by https://github.com/Kaszanas/SC2MapLocaleExtractor

Options:
  --json_one FILE                Path to the first .json file that is going to
                                 be merged.  [required]
  --json_two FILE                Path to the second .json file that is going
                                 to be merged.  [required]
  --output_filepath FILE         Filepath to which the result JSON file will
                                 be saved, note that any existing file of the
                                 same name will be overwriten.  [required]
  --force_overwrite BOOLEAN      Flag that specifies if the user wants to
                                 overwrite files or directories without being
                                 prompted.  [required]
  --log [INFO|DEBUG|ERROR|WARN]  Log level. Default is WARN.
  --help                         Show this message and exit.
```

# Execute With Docker

## Repository Docker Image

Please refer to the main [README](../../README.md) for the instructions.
