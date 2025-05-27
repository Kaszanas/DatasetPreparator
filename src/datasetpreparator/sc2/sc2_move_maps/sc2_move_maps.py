import logging
import shutil
from pathlib import Path
from typing import List

import click

from datasetpreparator.settings import LOGGING_FORMAT

from tqdm import tqdm


def sc2_move_maps(
    maps_path: Path,
    maps_path_installation_directory: Path,
) -> List[Path]:
    all_map_files = list(maps_path.rglob("*.s2ma"))

    copied_files = []
    for map_file in tqdm(all_map_files, desc="Copying maps", unit="file"):
        destination_path = (
            (maps_path_installation_directory / map_file.stem)
            .with_suffix(".SC2Map")
            .resolve()
        )
        if destination_path.exists():
            logging.warning(
                f"The map {map_file.name} already exists in the destination directory. Skipping."
            )
            continue

        # Copy the original map name to the destination with .SC2Map extension
        try:
            shutil.copyfile(map_file, destination_path)
            copied_files.append(destination_path)
        except Exception as e:
            logging.error(
                f"Failed to copy {str(map_file)} to {str(destination_path)}: {str(e)}"
            )
            continue

    return copied_files


@click.command(
    help="Moves StarCraft 2 maps with .s2ma extension to the StarCraft 2 installation directory under /Maps."
)
@click.option(
    "--sc2_installation_directory",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=Path,
    ),
    help="Path to the StarCraft 2 installation directory. This is where the maps will be moved to under /Maps.",
    required=True,
)
@click.option(
    "--maps_path",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=Path,
    ),
    help="Path to the directory where the StarCraft 2 maps are stored. These files will be moved to the StarCraft 2 installation directory under /Maps.",
    required=True,
)
@click.option(
    "--log",
    type=click.Choice(["INFO", "DEBUG", "ERROR", "WARN"], case_sensitive=False),
    default="WARN",
    required=4,
    help="Log level. Default is WARN.",
)
def main(sc2_installation_directory: Path, maps_path: Path, log: str):
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    maps_path_installation_directory = (sc2_installation_directory / "Maps").resolve()
    if not maps_path_installation_directory.exists():
        logging.warning(
            f"The maps directory {str(maps_path_installation_directory)} does not exist. Creating it."
        )
        maps_path_installation_directory.mkdir(parents=True, exist_ok=True)

    sc2_move_maps(
        maps_path=maps_path,
        maps_path_installation_directory=maps_path_installation_directory,
    )


if __name__ == "__main__":
    main()
