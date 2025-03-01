# Directory Packager

Utility script for compressing a directory into a `.zip` archive. This script iterates over all of the directories in the input directory and compresses them into `.zip` archives.

# CLI Usage

Please keep in mind that the  ```src/dir_packager.py``` contains required argument values and can be customized with the following command line interaface:
```
Usage: directory_packager.py [OPTIONS]

  Tool that packages directories into .zip archives. Each directory in the
  input path is packaged into a separate .zip archive.

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
