# SC2 Replaypack Processor

Utility script that leverages the [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo) and runs the program within multiple processes to parallelize the StarCraft 2 replay processing.

# CLI Usage

Please keep in mind that the ```sc2_replaypack_processor.py``` contains required argument values and can be customized with the following command line interaface:
```
Usage: sc2egset_replaypack_processor.py [OPTIONS]

  Tool used to recreate SC2ReSet and SC2EGSet Dataset. Executes the entire
  pipeline for replay processing. Depends on SC2InfoExtractorGo
  (https://github.com/Kaszanas/SC2InfoExtractorGo) which is executed on
  multiple replaypack directories in the process. Assists in processing
  StarCraft 2 (SC2) datasets.

Options:
  --input_path DIRECTORY         Input directory containing multiple StarCraft 2
                                 replaypacks. These files will be processed
                                 exactly the same as SC2ReSet and SC2EGSet
                                 datasets.  [required]
  --output_path DIRECTORY        Output path where the tool will place the
                                 processed files for SC2ReSet and SC2EGSet
                                 dataset as children directories.  [required]
  --n_processes INTEGER          Number of processes to be spawned for the
                                 dataset processing with SC2InfoExtractorGo.
                                 [required]
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
    python3 sc2_replaypack_processor.py --input_dir /app/input
```
