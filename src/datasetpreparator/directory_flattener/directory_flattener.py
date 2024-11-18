import os
from pathlib import Path
from typing import Dict, List, Tuple
import json
import shutil
import logging
import hashlib


import click
from tqdm import tqdm

from datasetpreparator.settings import LOGGING_FORMAT


def save_dir_mapping(output_path: str, dir_mapping: dict) -> None:
    """
    Saves a JSON file containing the mapping of the
    directory structure before it was "flattened".

    Parameters
    ----------
    output_path : str
        Specifies the path where the mapping will be saved.
    dir_mapping : dict
        Specifies the directory mapping dict.
    """
    with open(os.path.join(output_path, "processed_mapping.json"), "w") as json_file:
        json.dump(dir_mapping, json_file)


def calculate_file_hash(file_path: Path) -> str:
    """
    Calculates the file hash using the selected algorithm.

    Parameters
    ----------
    file_path : Path
        Path to the file which will be hashed.

    Returns
    -------
    str
        Returns the hash of the file.
    """

    # Open the file, read it in binary mode and calculate the hash:
    path_str = file_path.as_posix().encode("utf-8")

    path_hash = hashlib.md5(path_str).hexdigest()

    return path_hash


def directory_flatten(
    root_directory: Path,
    list_of_files: List[Path],
    dir_output_path: Path,
) -> Dict[str, str]:
    """
    Flattens a single directory and copies the contents
    to the specified output directory.

    Parameters
    ----------
    list_of_files : List[Path]
        List of files which were detected to be moved.
    dir_output_path : Path
        Path to the output directory where the files will be copied.

    Returns
    -------
    Dict[str, str]
        Returns a directory mapping from the current unique filename
        to the previous path relative to the root of the not-flattened directory.
    """

    # Walk over the directory
    dir_structure_mapping = {}
    for file in tqdm(
        list_of_files,
        desc=f"Flattening directory {root_directory.name}",
        unit="files",
    ):
        # Getting the ReplayPack/directory/structure/file.SC2Replay path,
        # this is needed to calculate the hash of the filepath:
        root_dir_name_and_file = root_directory.name / file.relative_to(root_directory)

        # Get unique filename:
        unique_filename = calculate_file_hash(root_dir_name_and_file)
        original_extension = file.suffix
        new_path_and_filename = Path(dir_output_path, unique_filename).with_suffix(
            original_extension
        )
        logging.debug(f"New path and filename! {new_path_and_filename.as_posix()}")

        current_file = Path(root_directory, file).resolve()
        logging.debug(f"Current file: {current_file.as_posix()}")

        # Copying files:
        if not current_file.exists():
            logging.error(f"File does not exist. Path len: {len(current_file)}")
            continue

        shutil.copy(current_file, new_path_and_filename)
        logging.debug(f"File copied to {new_path_and_filename.as_posix()}")

        # Finding the relative path from the root directory to the file:
        dir_structure_mapping[new_path_and_filename.name] = root_dir_name_and_file

    return dir_structure_mapping


def multiple_directory_flattener(
    input_path: Path, output_path: Path, file_extension: str
) -> Tuple[bool, List[Path]]:
    """
    Provides the main logic for "directory flattening".
    Iterates all of the directories found in the input path, and
    detects files that end with a specific extension,
    moves the files to a new output path at the top of the directory
    named after the original input directory.
    This function returns a file mapping for all of the files that were moved.
    This file mapping represents the relative
    directory structure before the processing occured.

    Parameters
    ----------
    input_path : Path
        Specifies the path that will be searched for files.
    output_path : Path
        Specifies the path where directories will be created and files will \
        be copied in a flat directory structure.
    file_extension : str
        Specifies extension for which the detected files will be brought \
        up to the top level of the "flattened" directory

    Returns
    -------
    Tuple[bool, List[Path]]
        Returns a tuple where the first element signifies if the processing was ok,
        and a list of paths to the output directories which were flattened.
    """

    # input must be a directory:
    if not input_path.is_dir():
        logging.error(
            f"Input path must be a directory! {input_path.resolve().as_posix()}"
        )
        return (False, [Path()])

    # Input must exist:
    if not input_path.exists():
        logging.error(f"Input path must exist! {input_path.resolve().as_posix()}")
        return (False, [Path()])

    # Output path must be a directory:
    if not output_path.is_dir():
        logging.error(
            f"Output path must be a directory! {output_path.resolve().as_posix()}"
        )
        return (False, [Path()])

    output_directories = []
    # Iterate over directories:
    for item in os.listdir(input_path):
        maybe_dir = Path(input_path, item).resolve()
        if not maybe_dir.is_dir():
            logging.debug(f"Skipping {str(maybe_dir)}, not a directory.")
            continue

        files_with_extension = list(maybe_dir.glob(f"**/*{file_extension}"))
        if not files_with_extension:
            logging.debug(
                f"Skipping {str(maybe_dir)}, no files with selected extension."
            )
            continue

        dir_output_path = Path(output_path, item).resolve()
        if not dir_output_path.exists():
            logging.debug(f"Creating directory {str(dir_output_path)}, didn't exist.")
            dir_output_path.mkdir()

        dir_structure_mapping = directory_flatten(
            root_directory=maybe_dir,
            list_of_files=files_with_extension,
            dir_output_path=dir_output_path,
        )

        save_dir_mapping(
            output_path=dir_output_path,
            dir_mapping=dir_structure_mapping,
        )

        output_directories.append(dir_output_path)

    return (True, output_directories)


@click.command(
    help="Directory restructuring tool used in order to flatten the structure, map the old structure to a separate file, and for later processing with other tools. Created primarily to define StarCraft 2 (SC2) datasets."
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
    help="Please provide output path where the tool will put files after processing.",
)
@click.option(
    "--file_extension",
    type=str,
    default=".SC2Replay",
    required=True,
    help="Specify file extension for the files that will be put to the top level directory.",
)
@click.option(
    "--log",
    type=click.Choice(["INFO", "DEBUG", "ERROR", "WARN"], case_sensitive=False),
    default="WARN",
    help="Log level (INFO, DEBUG, ERROR)",
)
def main(input_path: Path, output_path: Path, file_extension: str, log: str) -> None:
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    multiple_directory_flattener(
        input_path=input_path, output_path=output_path, file_extension=file_extension
    )


if __name__ == "__main__":
    main()
