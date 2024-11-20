import logging
import os
from pathlib import Path
import shutil

import click

from datasetpreparator.settings import LOGGING_FORMAT


def processed_mapping_copier(input_path: str, output_path: str) -> None:
    """
    Exposes logic for copying a specific file from all of the immediate subdirectories
    of the input path to the matching immediate subdirectories in the output path.

    Parameters
    ----------
    input_path : str
        Specifies the input path that contains subdirectories with the \
        desired file to be copied.
    output_path : str
        Specifies the output path that contains matching subdirectories which \
        will be the destination of the copied file.
    """

    # Iterating over the input path to find all of the immediate directories:
    for item in os.listdir(input_path):
        maybe_dir = os.path.join(input_path, item)
        if os.path.isdir(maybe_dir):
            # if the output directory does not exist the copying is ommited:
            dir_output_path = os.path.join(os.path.abspath(output_path), item)
            if not os.path.exists(dir_output_path):
                continue

            # The mapping was detected within the input directory
            # So the path is created and the file is copied:
            if "processed_mapping.json" in os.listdir(maybe_dir):
                mapping_filepath = os.path.join(maybe_dir, "processed_mapping.json")
                mapping_out_filepath = os.path.join(
                    dir_output_path, "processed_mapping.json"
                )
                shutil.copy(mapping_filepath, mapping_out_filepath)


@click.command(
    help="Tool for copying the processed_mapping.json files to the matching directory after processing the replaypack into a JSON dataset. This step is required to define the StarCraft 2 (SC2) dataset."
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
    help="Please provide input path to the flattened replaypacks that contain procesed_mapping.json files.",
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
    help="Please provide output path where processed_mapping.json will be copied.",
)
@click.option(
    "--log",
    type=click.Choice(["INFO", "DEBUG", "ERROR", "WARN"], case_sensitive=False),
    default="WARN",
    help="Log level",
)
def main(input_path: Path, output_path: Path, log: str) -> None:
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    processed_mapping_copier(input_path=input_path, output_path=output_path)


if __name__ == "__main__":
    main()
