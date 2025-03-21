# Directory Flattener

Utility script for entering each of the supplied replaypacks and flattening its structure. Please note that in the process of flattening the structure, the script will also rename the files using their hash values. Hashing of filenames is done to alleviate the potential files with the same name in different directories.

# CLI Usage

Please keep in mind that ```src/directory_flattener.py``` contains required argument values and can be customized with the following command line interaface:

```
Usage: directory_flattener.py [OPTIONS]

  Directory restructuring tool used in order to flatten the structure.
  Saves the mapping of the old directory structure to a separate file. Used to ease
  processing with other tools. Can be used to extract additional meaning from
  the directory structure in case of tournament replaypacks. Created primarily
  to define StarCraft 2 (SC2) datasets.

Options:
  --input_path DIRECTORY         Input path to the dataset that is going to be
                                 processed.  [required]
  --output_path DIRECTORY        Output path where the tool will put files
                                 after processing.  [required]
  --file_extension TEXT          File extension for the files that will be put
                                 to the top level directory. Example
                                 ('.SC2Replay').  [required]
  --force_overwrite BOOLEAN      Flag that specifies if the user wants to
                                 overwrite files or directories without being
                                 prompted.  [required]
  --log [INFO|DEBUG|ERROR|WARN]  Log level. Default is WARN.
  --help                         Show this message and exit.
```

# Execute With Docker

Please refer to the main [README](../../README.md) for the instructions.
