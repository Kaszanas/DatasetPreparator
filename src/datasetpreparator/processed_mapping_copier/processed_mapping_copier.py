import shutil
from pathlib import Path

import click

from datasetpreparator.utils.logging import initialize_logging
from datasetpreparator.utils.user_prompt import create_directory


def processed_mapping_copier(input_path: Path, output_path: Path) -> None:
    """
    Exposes logic for copying a specific file from all of the immediate subdirectories
    of the input path to the matching immediate subdirectories in the output path.

    Parameters
    ----------
    input_path : Path
        Specifies the input path that contains subdirectories with the \
        desired file to be copied.
    output_path : Path
        Specifies the output path that contains matching subdirectories which \
        will be the destination of the copied file.
    """

    # Iterating over the input path to find all of the immediate directories:

    for maybe_dir in input_path.iterdir():
        if maybe_dir.is_dir():
            # if the output directory does not exist the copying is ommited:
            dir_name = maybe_dir.name
            dir_output_path = (output_path / dir_name).resolve()
            if not dir_output_path.exists():
                continue

            # The mapping was detected within the input directory
            # So the path is created and the file is copied:
            dir_files = maybe_dir.iterdir()
            if "processed_mapping.json" in list(dir_files):
                mapping_filepath = (maybe_dir / "processed_mapping.json").resolve()
                mapping_out_filepath = (
                    dir_output_path / "processed_mapping.json"
                ).resolve()
                shutil.copy(mapping_filepath, mapping_out_filepath)


@click.command(
    help="Tool for copying the auxilliary file of processed_mapping.json to the matching directory after processing the replaypack into a JSON dataset with sc2egset_replaypack_processor.py. This script is required to reproduce SC2EGSet Dataset."
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
    help="Input path to the flattened replaypacks that contain procesed_mapping.json files.",
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
    help="Output path where processed_mapping.json will be copied.",
)
@click.option(
    "--log",
    type=click.Choice(["INFO", "DEBUG", "ERROR", "WARN"], case_sensitive=False),
    default="WARN",
    help="Log level. Default is WARN.",
)
def main(input_path: Path, output_path: Path, log: str) -> None:
    initialize_logging(log=log)

    create_directory(directory=output_path, created_warning=True)

    processed_mapping_copier(input_path=input_path, output_path=output_path)


if __name__ == "__main__":
    main()
