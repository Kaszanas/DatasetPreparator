import logging
from pathlib import Path
from typing import List, Set, Tuple

import click
import sc2reader
import requests

from datasetpreparator.settings import LOGGING_FORMAT


def list_maps_to_download(replay_files: List[Path]) -> Set[Tuple[str, str]]:
    """
    Opens replay files and keeps only unique maps.

    Parameters
    ----------
    replay_files : List[Path]
        Specifies a list of the paths to replays for which
        the unique maps will be detected.

    Returns
    -------
    Set[Tuple[str, str]]
        Returns a set that holds tuples with (map_hash, map_url) for all of
        the unique maps.
    """

    replay_map_archive_hashes = set()
    for replay_filepath in replay_files:
        replay = sc2reader.load_replay(str(replay_filepath), load_map=True)
        replay_map_url = replay.map_file.url
        logging.info(f"Replay map url is: {replay_map_url}")
        replay_map_hash = replay.map_hash

        # Only download map if not previously donwloaded:
        if (replay_map_hash, replay_map_url) not in replay_map_archive_hashes:
            replay_map_archive_hashes.add((replay_map_hash, replay_map_url))

    return replay_map_archive_hashes


def download_maps(
    output_path: Path,
    hash_set: Set[Tuple[str, str]],
) -> Path:
    """
    Contains logic to try to read and download a map based on the
    information that is held within .SC2Replay file.

    Parameters
    ----------
    output_path : Path
        Specifies where the final map file will be downloaded.
    hash_set : Set[Tuple[str, str]]
        Specifies a set that holds tuples with (map_hash, map_url) for all of
        the maps that should be downloaded.

    Returns
    -------
    Path
        Returns a Path to the output directory.
    """

    for map_hash, map_url in hash_set:
        try:
            response = requests.get(map_url, allow_redirects=True)
            output_filepath = Path(output_path, f"{map_hash}.SC2Map").resolve()
            with output_filepath.open(mode="wb") as output_map_file:
                output_map_file.write(response.content)
        except:  # noqa: E722
            logging.error(
                f"Error detected! Cannot process map: hash: {map_hash} url: {map_url}"
            )
            continue

    return output_path


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

    glob_pattern = "**/*.SC2Replay"

    replay_files = input_path.glob(glob_pattern)
    maps_to_download = list_maps_to_download(replay_files=replay_files)

    output_directory = download_maps(
        output_path=output_path,
        hash_set=maps_to_download,
    )

    return output_directory


@click.command(
    help="Tool for downloading StarCraft 2 (SC2) maps based on the data that is available within .SC2Replay file."
)
@click.option(
    "--input_path",
    type=click.Path(
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Please provide input path to the dataset that is going to be processed.",
)
@click.option(
    "--output_path",
    type=click.Path(
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Please provide output path where StarCraft 2 (SC2) map files will be downloaded.",
)
@click.option(
    "--log",
    type=click.Choice(["INFO", "DEBUG", "ERROR", "WARN"], case_sensitive=False),
    default="WARN",
    help="Log level",
)
def main(input_path: Path, output_path: Path, log: str) -> None:
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()

    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    output_dir = sc2_map_downloader(
        input_path=input_path, output_path=output_path.resolve()
    )

    logging.info(f"Finished donwloading maps to: {output_dir.as_posix()}")


if __name__ == "__main__":
    main()
