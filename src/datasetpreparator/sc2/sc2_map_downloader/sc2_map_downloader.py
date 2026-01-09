import logging
from pathlib import Path

import click

from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.download_maps import (
    sc2infoextractorgo_map_download,
)
from datasetpreparator.utils.logging import initialize_logging
from datasetpreparator.utils.user_prompt import create_directory


def sc2_map_downloader(input_path: Path, output_path: Path) -> Path:
    """
    Holds the main loop for asynchronous map downloading logic.

    Parameters
    ----------
    input_path : Path
        Specifies the input path that contains .SC2Replay files \
        which will be used for map detection.
    output_path : Path
        Specifies the output path where the downloaded maps will be placed.
    """

    sc2infoextractorgo_map_download(
        input_path=input_path,
        maps_directory=output_path,
        n_processes=8,
    )

    return output_path


@click.command(
    help="Tool for downloading StarCraft 2 (SC2) maps based on the data that available within .SC2Replay files."
)
@click.option(
    "--input_path",
    type=click.Path(
        exists=False,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Input path to the dataset that is going to be processed. The script will find all .SC2Replay files in the directory.",
)
@click.option(
    "--output_path",
    type=click.Path(
        exists=False,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Output path where StarCraft 2 (SC2) map files will be downloaded.",
)
@click.option(
    "--n_processes",
    type=click.INT,
    default=8,
    help="Number of processes to use for extracting the map URLs. Default is 8.",
)
@click.option(
    "--log",
    type=click.Choice(["INFO", "DEBUG", "ERROR", "WARN"], case_sensitive=False),
    default="WARN",
    help="Log level. Default is WARN.",
)
def main(input_path: Path, output_path: Path, log: str) -> None:
    input_path = Path(input_path).resolve()
    create_directory(directory=input_path, created_warning=True)
    output_path = Path(output_path).resolve()
    create_directory(directory=output_path)

    initialize_logging(log=log)

    output_dir = sc2_map_downloader(
        input_path=input_path,
        output_path=output_path,
    )

    logging.info(f"Finished downloading maps to: {str(output_dir)}")


if __name__ == "__main__":
    main()
