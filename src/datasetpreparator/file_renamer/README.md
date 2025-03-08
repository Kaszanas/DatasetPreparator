# File Renamer

# CLI Usage

Please keep in mind that the  ```src/file_renamer.py``` contains required argument values and can be customized with the following command line interaface:
```
Usage: file_renamer.py [OPTIONS]

  Tool used for renaming auxilliary files (log files) that are produced when
  creating StarCraft 2 (SC2) datasets with
  https://github.com/Kaszanas/SC2InfoExtractorGo. Additionally, this tool
  renames the .zip files so that they carry the original directory name with
  an added '_data' suffix.

Options:
  --input_path DIRECTORY         Input path to the directory containing the
                                 dataset that is going to be processed by
                                 packaging into .zip archives.  [required]
  --log [INFO|DEBUG|ERROR|WARN]  Log level. Default is WARN.
  --help                         Show this message and exit.
```

# Execute With Docker

## Repository Docker Image

Please refer to the main [README](../../README.md) for the instructions.
