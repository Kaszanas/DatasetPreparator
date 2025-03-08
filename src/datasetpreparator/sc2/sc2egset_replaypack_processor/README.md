# SC2 Replaypack Processor

Utility script that leverages the [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo) and runs the program within multiple processes to parallelize the StarCraft 2 replay processing.

# CLI Usage

Please keep in mind that the ```sc2egset_pipeline.py``` contains required argument values and can be customized with the following command line interaface:

```
Usage: sc2egset_pipeline.py [OPTIONS]

  Tool used to recreate SC2ReSet and SC2EGSet Dataset. Depends on
  SC2InfoExtractorGo (https://github.com/Kaszanas/SC2InfoExtractorGo) which
  is executed on multiple replaypack directories in the process. Entire pipeline
  for replay processing runs with the command line arguments used to create
  SC2EGSet. Assists in processing StarCraft 2 (SC2) datasets.

Options:
  --input_path DIRECTORY         Input directory containing multiple StarCraft
                                 2 replaypacks. These files will be processed
                                 exactly the same as SC2ReSet and SC2EGSet
                                 datasets.  [required]
  --output_path DIRECTORY        Output path where the tool will place the
                                 processed files for SC2ReSet and SC2EGSet
                                 dataset as children directories.  [required]
  --n_processes INTEGER          Number of processes to be spawned for the
                                 dataset processing with SC2InfoExtractorGo.
                                 [required]
  --force_overwrite BOOLEAN      Flag that specifies if the user wants to
                                 overwrite files or directories without being
                                 prompted.  [required]
  --log [INFO|DEBUG|ERROR|WARN]  Log level. Default is WARN.
  --help                         Show this message and exit.
```

Please keep in mind that the ```sc2_replaypack_processor.py``` contains required argument values and can be customized with the following command line interaface:

```
Usage: sc2egset_replaypack_processor.py [OPTIONS]

  Tool used to recreate SC2EGSet Dataset. Executes SC2InfoExtractorGo
  (https://github.com/Kaszanas/SC2InfoExtractorGo) on multiple replaypack
  directories with hardcoded CLI arguments. Assists in processing StarCraft 2
  (SC2) datasets.

Options:
  --input_path DIRECTORY         Input directory containing multiple StarCraft
                                 2 replaypacks. These files will be processed
                                 exactly the same as SC2ReSet and SC2EGSet
                                 datasets.  [required]
  --output_path DIRECTORY        Output path where the tool will place the
                                 processed files for SC2ReSet and SC2EGSet
                                 dataset as children directories.  [required]
  --maps_path DIRECTORY          Path to the StarCraft 2 maps that will be
                                 used in replay processing. If there are no
                                 maps, they will be downloaded.  [required]
  --n_processes INTEGER          Number of processes to be spawned for the
                                 dataset processing with SC2InfoExtractorGo.
                                 [required]
  --force_overwrite BOOLEAN      Flag that specifies if the user wants to
                                 overwrite files or directories without being
                                 prompted.  [required]
  --log [INFO|DEBUG|ERROR|WARN]  Log level. Default is WARN.
  --help                         Show this message and exit.
```

# Execute With Docker

## Repository Docker Image

Please refer to the main [README](../../README.md) for the instructions.
