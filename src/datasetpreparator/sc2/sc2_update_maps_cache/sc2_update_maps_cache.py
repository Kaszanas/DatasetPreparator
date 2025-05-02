import logging
import os
from pathlib import Path
import click

from datasetpreparator.settings import LOGGING_FORMAT

import shutil

from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.download_maps import (
    sc2infoextractorgo_map_download,
)


class BnetPathNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class BnetCacheNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def place_dependency_in_cache(
    bnet_base_dir: Path,
    map_filepath: Path,
) -> Path:
    """
    Function responsible for copying a matched StarCraft 2 path to its expected
    cache directory within the StarCraft 2 game files.

    Parameters
    ----------
    battle_net_cache_directory : Path
        Path to the battle.net cache directory, where the file will be copied.
    map_filepath : Path
        Path to the map that will be copied.

    Returns
    -------
    Path
        Returns the path to the copied map in the Cache directory.
    """

    # SC2InfoExtractor saves maps filenames given by their hash:
    map_hash = map_filepath.stem
    file_extension = map_filepath.suffix

    cache_map_filepath = (
        Path(
            bnet_base_dir,
            "Cache",
            map_hash[0:2],
            map_hash[2:4],
            f"{map_hash}",
        )
        .with_suffix(file_extension)
        .resolve()
    )

    if cache_map_filepath.exists():
        logging.info(
            f"The cache entry already exists, skipping: {str(cache_map_filepath)}"
        )
        return cache_map_filepath

    logging.info(f"No cache entry existed prior, copying {str(cache_map_filepath)}")
    shutil.copy(map_filepath, cache_map_filepath)

    return cache_map_filepath


# NOTE: This is Windows only:
def read_execute_info(path: Path = Path("~/Documents")) -> Path | None:
    """
    Helper function reading the 'StarCraft II/ExecuteInfo.txt' file and acquiring the
    relevant information for the location of Battle.net Cache directory.

    Parameters
    ----------
    path : Path
        Path where to look for the 'StarCraft II/ExecuteInfo.txt'.

    Returns
    -------
    Path | None
        Returns path to the direcotry of bnet or None.
    """

    user_path = path.expanduser()

    path_to_execute_info = (user_path / "StarCraft II/ExecuteInfo.txt").resolve()
    if not path_to_execute_info.exists():
        return None

    with path_to_execute_info.open(
        "rb"
    ) as f:  # Binary because the game appends a '\0' :(.
        for line in f:
            parts = [p.strip() for p in line.decode("utf-8").split("=")]
            if len(parts) != 2:
                continue
            if not parts[0] == "executable":
                continue

            exec_path = Path(parts[1]).resolve()

            exec_path_parents_list = list(exec_path.parents)
            if len(exec_path_parents_list) < 3:
                logging.warning(
                    "Could not find the Battle.net cache based on ExecuteInfo.txt, parent list too short"
                )
                return None

            return_exec_path = exec_path_parents_list[2]

            return return_exec_path


def test_looks_like_battle_net(bnet_path: Path):
    if bnet_path.name != "Battle.net":
        raise BnetPathNotFound(f"Doesn't look like a Battle.net cache: {bnet_path}")
    cache_path = (bnet_path / Path("Cache")).resolve()
    if not cache_path.is_dir():
        raise BnetCacheNotFound("Missing a Cache subdirectory:", bnet_path)


def check_windows_default_path() -> Path | None:
    maybe_default_windows_path = Path("C:/Program Files (x86)/StarCraft II")
    default_windows_path = None
    if maybe_default_windows_path.exists():
        default_windows_path = maybe_default_windows_path

    return default_windows_path


def get_bnet_path(bnet_base_dir: Path | None) -> Path:
    sc2_environment_val = os.environ.get("SC2PATH")
    sc2_environment_bnet_path = None
    if sc2_environment_val:
        sc2_environment_bnet_path = Path(sc2_environment_val).resolve()

    user_directory_bnet_path = read_execute_info(path=Path("~/Documents"))
    default_windows_bnet_path = check_windows_default_path()

    # There are multiple ways of acquiring the battle.net base directory.
    # The user does not need to provide it, there are some seemingly sane defaults in place.
    # For the sake of automation there is also a way of providing this path through an
    # environment variable.
    # In no path exists at all the program will throw an exception and the user
    # will be forced to evaluate that the correct path can be passed.
    some_bnet_path = (
        sc2_environment_bnet_path
        or user_directory_bnet_path
        or default_windows_bnet_path
        or bnet_base_dir
    )
    if not some_bnet_path:
        raise BnetPathNotFound(
            "Cannot run without having the path to a directory where the Cache lives."
        )

    test_looks_like_battle_net(some_bnet_path)

    return some_bnet_path


@click.command(
    help="WINDOWS SPECIFIC! Updates the maps cache directory for StarCraft 2. This is a helper script that makes sure that the game engine has access to the maps in case of processing replays using the game engiine."
)
@click.option(
    "--replays_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Path to the directory containing the replays for which the maps should be downloaded and placed in the Battle.net cache.",
    required=True,
)
@click.option(
    "--maps_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Path to the directory where the StarCraft 2 maps will be downloaded. These files will be moved to the Battle.net cache.",
    required=True,
)
@click.option(
    "--bnet_base_dir",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=Path,
    ),
    help="Path to the directory in which the Battle.net cache exists. On Windows this directory is by default 'C:/ProgramData/Blizzard Entertainment/Battle.net'. If the -PrePopulateCache option is set in the Battle.net launcher as the execute option this will be the directory where the game is installed.",
)
@click.option(
    "--n_processes",
    type=int,
    help="Number of processes to use for reading replays and acquiring the map urls to download.",
    default=4,
    required=True,
)
@click.option(
    "--log",
    type=click.Choice(["INFO", "DEBUG", "ERROR", "WARN"], case_sensitive=False),
    default="WARN",
    required=4,
    help="Log level. Default is WARN.",
)
def sc2_update_maps_cache(
    replays_path: Path,
    maps_path: Path,
    bnet_base_dir: Path,
    n_processes: int,
    log: str,
) -> None:
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    # Step 0 Check if the Battle.net directory was passed, and if not try to detect it automatically:
    bnet_path = get_bnet_path(bnet_base_dir=bnet_base_dir)

    # Step 1 Download the maps using SC2ExtractorGo. This process omits downloading
    # any maps that already exist, in theory this should be efficient:
    sc2infoextractorgo_map_download(
        input_path=replays_path,
        maps_directory=maps_path,
        n_processes=n_processes,
    )

    # Populate all of the maps to the cache directory.
    all_map_files = list(maps_path.rglob("*.s2ma"))
    for map_filepath in all_map_files:
        place_dependency_in_cache(
            bnet_base_dir=bnet_path,
            map_filepath=map_filepath,
        )


if __name__ == "__main__":
    sc2_update_maps_cache()
