[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5296664.svg)](https://doi.org/10.5281/zenodo.5296664)

# SC2DatasetPreparator

Tools in this repository were used to create the **[SC2ReSet: StarCraft II Esport Replaypack Set](https://doi.org/10.5281/zenodo.5575796)**, and finally **[SC2EGSet: StarCraft II Esport Game State Dataset](https://doi.org/10.5281/zenodo.5503997)**.

# Installation

To install current version of the toolset as separate CLI tools run the following command:
```
pip install sc2datasetpreparator[all]
```

## Dataset Preparation Steps

To reproduce our experience with defining a dataset and to be able to compare your results with our work we describe how to perform the processing below.

### Using Docker

1. Build the docker image from: https://github.com/Kaszanas/SC2InfoExtractorGo
2. Run the commands as described in the ```Makefile```. But first make sure that all of the script parameters are set according to your needs.

### Using Python

0. Obtain replays to process. This can be a replaypack or your own replay folder.
1. Download latest version of [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo), or build it from source.
2. **Optional** If the replays that you have are held in nested directories it is best to use  ```src/directory_flattener.py```. This will copy the directory and place all of the files to the top directory where it can be further processed. In order to preserve the old directory structure, a .json file is created. The file contains the old directory tree to a mapping: ```{"replayUniqueHash": "whereItWasInOldStructure"}```. This step is is required in order to properly use [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo) as it only lists the files immediately available on the top level of the input directory. [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo).
3. **Optional** Use the map downloader ```src/sc2_map_downloader.py``` to download maps that were used in the replays that you obtained. This is required for the next step.
4. **Optional** Use the [SC2MapLocaleExtractor](https://github.com/Kaszanas/SC2MapLocaleExtractor) to obtain the mapping of ```{"foreign_map_name": "english_map_name"}``` which is required for the [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo) to translate the map names in the output .json files.
5. Perform replaypack processing using ```src/sc2_replaypack_processor.py``` with the [SC2InfoExtractorGo](https://github.com/Kaszanas/SC2InfoExtractorGo) placed in PATH, or next to the script.
6. **Optional** Using the ```src/file_renamer.py```, rename the files that were generated in the previous step. This is not required and is done to increase the readibility of the directory structure for the output.
7. Using the ```src/file_packager.py```, create .zip archives containing the datasets and the supplementary files. By finishing this stage, your dataset should be ready to upload.

#### Customization

In order to specify different processing flags for https://github.com/Kaszanas/SC2InfoExtractorGo please modify the ```src/sc2_replaypack_processor``` file directly

## Scripts Command Line Arguments Usage

Before using this software please install Python >= 3.10 and ```requirements.txt```.

Each of the scripts has its usage described in their respective `README.md` files.

# Citations

## Software
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

## [Dataset Description Pre-print](https://arxiv.org/abs/2207.03428)

```
@misc{https://doi.org/10.48550/arxiv.2207.03428,
  doi       = {10.48550/ARXIV.2207.03428},
  url       = {https://arxiv.org/abs/2207.03428},
  author    = {Białecki, Andrzej and Jakubowska, Natalia and Dobrowolski, Paweł and Białecki, Piotr and Krupiński, Leszek and Szczap, Andrzej and Białecki, Robert and Gajewski, Jan},
  keywords  = {Machine Learning (cs.LG), Artificial Intelligence (cs.AI), Machine Learning (stat.ML), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title     = {SC2EGSet: StarCraft II Esport Replay and Game-state Dataset},
  publisher = {arXiv},
  year      = {2022},
  copyright = {Creative Commons Attribution 4.0 International}
}

```

## [SC2ReSet: StarCraft II Esport Replaypack Set](https://doi.org/10.5281/zenodo.5575796)

```
@dataset{bialecki_andrzej_2022_5575797,
  author       = {Białecki, Andrzej},
  title        = {SC2ReSet: StarCraft II Esport Replaypack Set},
  month        = jun,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.5575797},
  url          = {https://doi.org/10.5281/zenodo.5575797}
}
```

## [SC2EGSet: StarCraft II Esport Game State Dataset](https://doi.org/10.5281/zenodo.5503997)

```
@dataset{bialecki_andrzej_2022_6629349,
  author       = {Białecki, Andrzej and
                  Jakubowska, Natalia and
                  Dobrowolski, Paweł and
                  Szczap, Andrzej and
                  Białecki, Robert and
                  Gajewski, Jan},
  title        = {SC2EGSet: StarCraft II Esport Game State Dataset},
  month        = jun,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.6629349},
  url          = {https://doi.org/10.5281/zenodo.6629349}
}
```
