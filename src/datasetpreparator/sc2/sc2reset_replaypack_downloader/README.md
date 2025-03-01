# SC2ReSet Replaypack Downloader

Utility script, downloads the contents of SC2ReSet replaypack from a Zenodo repository (https://doi.org/10.5281/zenodo.5575796).

# CLI Usage

Please keep in mind that the ```sc2reset_replaypack_downloader.py``` contains required argument values and can be customized with the following command line interaface:
```
Usage: sc2reset_replaypack_downloader.py [OPTIONS]

  Tool used for downloading SC2ReSet: StarCraft II Esport Replaypack Set
  (https://zenodo.org/doi/10.5281/zenodo.5575796).

Options:
  --download_path DIRECTORY      Path to which the archives will be
                                 downloaded.  [required]
  --unpack_path DIRECTORY        Path to which the archives will be unpacked.
                                 [required]
  --n_workers INTEGER            Number of workers used for extracting the
                                 .zip archives.  [required]
  --log [INFO|DEBUG|ERROR|WARN]  Log level. Default is WARN.
  --help                         Show this message and exit.
```

# Execute With Docker

## Repository Docker Image

Please refer to the main [README](../../README.md) for the instructions.

# Citation

SC2ReSet replaypack collection was formally introduced in:

```bibtex
@article{Białecki2023,
  author  = {Bia{\l}ecki, Andrzej
             and Jakubowska, Natalia
             and Dobrowolski, Pawe{\l}
             and Bia{\l}ecki, Piotr
             and Krupi{\'{n}}ski, Leszek
             and Szczap, Andrzej
             and Bia{\l}ecki, Robert
             and Gajewski, Jan},
  title   = {SC2EGSet: StarCraft II Esport Replay and Game-state Dataset},
  journal = {Scientific Data},
  year    = {2023},
  month   = {Sep},
  day     = {08},
  volume  = {10},
  number  = {1},
  pages   = {600},
  issn    = {2052-4463},
  doi     = {10.1038/s41597-023-02510-7},
  url     = {https://doi.org/10.1038/s41597-023-02510-7}
}
```
