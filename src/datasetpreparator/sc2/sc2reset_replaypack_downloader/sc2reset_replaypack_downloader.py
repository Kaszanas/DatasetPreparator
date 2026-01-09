import logging
from pathlib import Path
from typing import List, Tuple

import click

from datasetpreparator.sc2.sc2reset_replaypack_downloader.available_replaypacks import (
    SC2RESET_REPLAYPACKS,
)
from datasetpreparator.sc2.sc2reset_replaypack_downloader.utils.download_replaypack import (
    download_replaypack,
)
from datasetpreparator.sc2.sc2reset_replaypack_downloader.utils.unpack_zipfile import (
    unpack_zipfile,
)
from datasetpreparator.utils.logging import initialize_logging


def sc2reset_replaypack_downloader(
    download_path: Path,
    unpack_path: Path,
    n_workers: int,
    replaypack_list: List[Tuple[str, str, str]] = SC2RESET_REPLAYPACKS,
) -> None:
    """
    Downloads and unpacks SC2ReSet: StarCraft II Esport Replaypack Set
    (https://zenodo.org/doi/10.5281/zenodo.5575796). If the md5 of the downloaded
    archive does not match the expected md5, the program will retry downloading the
    archive.

    Parameters
    ----------
    download_path : Path
        Specifies the path to which the archives will be downloaded.
    unpack_path : Path
        Specifies the path to which the archives will be unpacked.
    n_workers : int
        Specifies the number of workers used for extracting the .zip archives.
    replaypack_list : List[Tuple[str, str, str]]
        Specifies the list of replaypacks to be downloaded. By default each of
        the tuples is (replaypack_name, replaypack_url, archive_md5).
    """

    if replaypack_list is None:
        return

    if n_workers <= 0:
        return

    # Download replaypacks:
    downloaded_paths: List[Tuple[str, str]] = []
    for replaypack_name, replaypack_url, file_md5 in replaypack_list:
        downloaded_replaypack_path, ok = download_replaypack(
            destination_dir=download_path,
            replaypack_name=replaypack_name,
            replaypack_url=replaypack_url,
            replaypack_md5=file_md5,
        )
        # If the download was succesful, add the path to the list of downloaded paths:
        if ok:
            downloaded_paths.append((replaypack_name, downloaded_replaypack_path))
            continue
        logging.error(
            f"Replaypack {replaypack_name} could not be downloaded. Adding to retry list..."
        )

    # Unpack replaypacks:
    for replaypack_name, downloaded_replaypack_path in downloaded_paths:
        destination_subdir = Path(replaypack_name)
        unpack_zipfile(
            destination_dir=unpack_path,
            destination_subdir=destination_subdir,
            zip_path=downloaded_replaypack_path,
            n_workers=n_workers,
        )


@click.command(
    help="Tool used for downloading SC2ReSet: StarCraft II Esport Replaypack Set (https://zenodo.org/doi/10.5281/zenodo.5575796)."
)
@click.option(
    "--download_path",
    type=click.Path(
        exists=False,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to which the archives will be downloaded.",
)
@click.option(
    "--unpack_path",
    type=click.Path(
        exists=False,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to which the archives will be unpacked.",
)
@click.option(
    "--n_workers",
    type=int,
    default=4,
    required=True,
    help="Number of workers used for extracting the .zip archives.",
)
@click.option(
    "--log",
    type=click.Choice(["INFO", "DEBUG", "ERROR", "WARN"], case_sensitive=False),
    default="WARN",
    help="Log level. Default is WARN.",
)
def main(download_path: Path, unpack_path: Path, n_workers: int, log: str) -> None:
    initialize_logging(log=log)

    sc2reset_replaypack_downloader(
        download_path=download_path.resolve(),
        unpack_path=unpack_path.resolve(),
        n_workers=n_workers,
    )


if __name__ == "__main__":
    main()
