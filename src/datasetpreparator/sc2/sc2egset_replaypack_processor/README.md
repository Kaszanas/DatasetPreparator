# SC2 Replaypack Processor

Utility script that leverages the [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo) and runs the program within multiple processes to parallelize the StarCraft 2 replay processing.

# CLI Usage

Please keep in mind that the ```src/sc2_replaypack_processor.py```  contains default flag values and can be customized with the following command line flags:
```
Usage: sc2egset_replaypack_processor.py [OPTIONS]

Tool used to execute SC2InfoExtractorGo
(https://github.com/Kaszanas/SC2InfoExtractorGo) on multiple replaypack
directories. Assists in processing StarCraft 2 (SC2) datasets.

Options:
  --input_path DIRECTORY          Please provide an output directory for the
                                  resulting files.  [required]
  --output_path DIRECTORY         Please provide output path where StarCraft 2
                                  (SC2) map files will be downloaded.
                                  [required]
  --perform_chat_anonymization BOOLEAN
                                  Provide 'True' if chat should be anonymized,
                                  otherwise 'False'.  [required]
  --n_processes INTEGER           Please provide the number of processes to be
                                  spawned for the dataset processing.
                                  [required]
  --log [INFO|DEBUG|ERROR]        Log level (INFO, DEBUG, ERROR)
  --help                          Show this message and exit.
```

# Execute With Docker

> [!NOTE]
> There are two ways of executing this script with Docker. One is to use the main repository Dockerfile (available in `docker` directory) and the other is to use the Dockerfile contained in this directory.

## Repository Docker Image

Please refer to the main [README](../../README.md) for the instructions.

## Script Docker Image

Buil the docker image:
```bash
docker build --tag=datasetpreparator:sc2_replaypack_processor .
```

Run the docker image (please replace `<paths>`):
```bash
docker run -v "<./input>:/app/input" \
    datasetpreparator:sc2_replaypack_processor \
    python3 sc2_replaypack_processor.py --input_dir /app/input
```
