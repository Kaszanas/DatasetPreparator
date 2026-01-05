[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5296664.svg)](https://doi.org/10.5281/zenodo.5296664)

# DatasetPreparator

This project contains various scripts that can assist in the process of preparing datasets. To have a broad overview of the tools please refer to the **[Detailed Tools Description](#detailed-tools-description)**.

Tools in this repository were used to create the **[SC2ReSet: StarCraft II Esport Replaypack Set](https://doi.org/10.5281/zenodo.5575796)**, and finally **[SC2EGSet: StarCraft II Esport Game State Dataset](https://doi.org/10.5281/zenodo.5503997)**, citation information **[Cite Us!](#cite-us)**.

## Installation

> [!NOTE]
> To run this project there are some prerequisites that you need to have installed on your system:
> - Docker
> - **Optional** make (if you do not wish to use make, please refer to the commands defined in the `makefile` and run them manually)

Our prefered way of distributing the toolset is through DockerHub. We use the Docker Image to provide a fully reproducible environment for our scripts.

To pull the image from DockerHub, run the following command:

```bash
docker pull kaszanas/datasetpreparator:latest
```

If you wish to clone the repository and build the Docker image yourself, run the following command:

```bash
make docker_build
```

After building the image, please refer to the **[Command Line Arguments Usage](#command-line-arguments-usage)** section for the usage of the scripts and for a full description for each of the scripts refer to **[Detailed Tools Description](#detailed-tools-description)**.


## Command Line Arguments Usage

When using Docker, you will have to pass the arguments through the `docker run` command and mount the input/output directory. Below is an example of how to run the `directory_flattener` script using Docker. For ease of use we have prepared example directory structure in the `processing` directory. The command below uses that to issue a command to flatten the directory structure:

```bash
docker run -rm \
  -v ".\processing:/app/processing" \
  datasetpreparator:latest \
  python3 directory_flattener.py \
  --input_path ./processing/input/directory_flattener \
  --output_path ./processing/output/directory_flattener \
  --n_processes 8 \
  --force_overwrite True \
```

## SC2EGSet Dataset Reproduction Steps

> [!NOTE]
> Instructions below are for reproducing the result of the SC2EGSet dataset. If you wish to use the tools in this repository separately for your own dataset, please refer to the **[Detailed Tools Description](#detailed-tools-description)**.

### Using Docker

We provide a release image containing all of the scripts. To see the usage of these scripts please refer to their respective ``README.md`` files as described in [Detailed Tools Description](#detailed-tools-description).

The following steps were used to prepare the SC2ReSet and SC2EGSet datasets:
1. Build the docker image for the DatasetPreparator using the provided ```makefile``` target: ```make docker_build```. This will load all of the dependencies such as the [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo).
2. Place the input replaypacks into `./processing/input/directory_flattener` directory.
3. Run the command ```make sc2reset_sc2egset_pipeline``` to process the replaypacks and create the datasets. The output will be placed in `./processing/output/SC2ReSet` and `./processing/output/SC2EGSet` directories.


### Detailed Tools Description

Each of the scripts has its usage described in their respective `README.md` files, you can find the detailed description of the available tools below.

#### CLI Usage; Generic scripts
1. [Directory Packager (dir_packager): README](src/datasetpreparator/directory_packager/README.md)
2. [Directory Flattener (directory_flattener): README](src/datasetpreparator/directory_flattener/README.md)
3. [File Renamer (file_renamer): README](src/datasetpreparator/file_renamer/README.md)
4. [JSON Merger (json_merger): README](src/datasetpreparator/json_merger/README.md)
5. [Processed Mapping Copier (processed_mapping_copier): README](src/datasetpreparator/processed_mapping_copier/README.md)

#### CLI Usage; StarCraft 2 Specific Scripts
1. [SC2 Map Downloader (sc2_map_downloader): README](src/datasetpreparator/sc2/sc2_map_downloader/README.md)
2. [SC2EGSet Pipeline (sc2egset_pipeline): README](src/datasetpreparator/sc2/sc2egset_replaypack_processor/README.md)
3. [SC2EGSet Replaypack Processor (sc2egset_replaypack_processor): README](src/datasetpreparator/sc2/sc2egset_replaypack_processor/README.md)
4. [SC2ReSet Replaypack Downloader (sc2reset_replaypack_downloader): README](src/datasetpreparator/sc2/sc2reset_replaypack_downloader/README.md)


<!-- ### Using Python

1. Obtain replays to process. This can be a replaypack or your own replay folder.
2. Download latest version of [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo), or build it from source.
3. **Optional** If the replays that you have are held in nested directories it is best to use  ```src/directory_flattener.py```. This will copy the directory and place all of the files to the top directory where it can be further processed. In order to preserve the old directory structure, a .json file is created. The file contains the old directory tree to a mapping: ```{"replayUniqueHash": "whereItWasInOldStructure"}```. This step is is required in order to properly use [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo) as it only lists the files immediately available on the top level of the input directory. [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo).
4. **Optional** Use the map downloader ```src/sc2_map_downloader.py``` to download maps that were used in the replays that you obtained. This is required for the next step.
5. **Optional** Use the [SC2MapLocaleExtractor](https://github.com/Kaszanas/SC2MapLocaleExtractor) to obtain the mapping of ```{"foreign_map_name": "english_map_name"}``` which is required for the [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo) to translate the map names in the output .json files.
6. Perform replaypack processing using ```src/sc2_replaypack_processor.py``` with the [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo) placed in PATH, or next to the script.
7. **Optional** Using the ```src/file_renamer.py```, rename the files that were generated in the previous step. This is not required and is done to increase the readibility of the directory structure for the output.
8. Using the ```src/file_packager.py```, create .zip archives containing the datasets and the supplementary files. By finishing this stage, your dataset should be ready to upload. -->


## Contributing and Reporting Issues

If you want to report a bug, request a feature, or open any other issue, please do so in the **[issue tracker](https://github.com/Kaszanas/SC2DatasetPreparator/issues/new/choose)**.

Please see **[CONTRIBUTING.md](https://github.com/Kaszanas/SC2DatasetPreparator/blob/main/CONTRIBUTING.md)** for detailed development instructions and contribution guidelines.

## Cite Us!

### This Repository

### [SC2EGSet: Dataset Description](https://www.researchgate.net/publication/373767449_SC2EGSet_StarCraft_II_Esport_Replay_and_Game-state_Dataset)

```
@article{Bialecki2023_SC2EGSet,
  author   = {Bia{\l}ecki, Andrzej
              and Jakubowska, Natalia
              and Dobrowolski, Pawe{\l}
              and Bia{\l}ecki, Piotr
              and Krupi{\'{n}}ski, Leszek
              and Szczap, Andrzej
              and Bia{\l}ecki, Robert
              and Gajewski, Jan},
  title    = {SC2EGSet: StarCraft II Esport Replay and Game-state Dataset},
  journal  = {Scientific Data},
  year     = {2023},
  month    = {Sep},
  day      = {08},
  volume   = {10},
  number   = {1},
  pages    = {600},
  issn     = {2052-4463},
  doi      = {10.1038/s41597-023-02510-7},
  url      = {https://doi.org/10.1038/s41597-023-02510-7}
}
```

```
@software{Białecki_2022_6366039,
  author    = {Białecki, Andrzej and
               Białecki, Piotr and
               Krupiński, Leszek},
  title     = {{Kaszanas/SC2DatasetPreparator: 1.2.0
               SC2DatasetPreparator Release}},
  month     = {jun},
  year      = {2022},
  publisher = {Zenodo},
  version   = {1.2.0},
  doi       = {10.5281/zenodo.5296664},
  url       = {https://doi.org/10.5281/zenodo.5296664}
}
```
