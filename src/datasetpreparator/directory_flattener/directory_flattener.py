import hashlib
import json
import logging
import shutil
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import freeze_support
from pathlib import Path
from typing import Dict, List, Tuple

import click
from tqdm import tqdm

from datasetpreparator.utils.logging import initialize_logging
from datasetpreparator.utils.user_prompt import user_prompt_overwrite_ok


class MultiprocessFlattenArguments:
    def __init__(
        self,
        dir_output_path: Path,
        maybe_dir: Path,
        files_with_extension: List[Path],
    ):
        self.dir_output_path = dir_output_path
        self.maybe_dir = maybe_dir
        self.files_with_extension = files_with_extension


class DirectoryCreationArguments:
    def __init__(
        self,
        dir_output_path: Path,
        maybe_dir: Path,
        files_with_extension: List[Path],
        force_overwrite: bool,
    ):
        self.dir_output_path = dir_output_path
        self.maybe_dir = maybe_dir
        self.files_with_extension = files_with_extension
        self.force_overwrite = force_overwrite


def save_dir_mapping(output_path: Path, dir_mapping: dict) -> None:
    """
    Saves a JSON file containing the mapping of the
    directory structure before it was "flattened".

    Parameters
    ----------
    output_path : Path
        Specifies the path where the mapping will be saved.
    dir_mapping : dict
        Specifies the directory mapping dict.
    """

    path_to_mapping = Path(output_path, "processed_mapping.json").resolve()

    with path_to_mapping.open("w") as json_file:
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
    path_str = str(file_path).encode("utf-8")

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
        desc=f"Flattening {root_directory.name:<35}",
        unit="file",
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
        dir_structure_mapping[new_path_and_filename.name] = (
            root_dir_name_and_file.as_posix()
        )

    return dir_structure_mapping


def multiprocess_directory_flattener(
    directories_to_process: List[MultiprocessFlattenArguments],
    n_processes: int,
) -> List[Path]:
    """
    Multiprocesses the directory flattening.

    Parameters
    ----------
    directories_to_process : List[MultiprocessFlattenArguments]
        List of the arguments corresponding to the directories that will be processed.
    n_processes : int
        Number of processes that will be spawned.

    Returns
    -------
    List[Path]
        Returns a list of paths to the output directories.
    """

    with ThreadPoolExecutor(
        max_workers=n_processes,
        initializer=tqdm.set_lock,
        initargs=(tqdm.get_lock(),),
    ) as executor:
        results = list(executor.map(flatten_save_dir_mapping, directories_to_process))

    return list(results)


def flatten_save_dir_mapping(
    arguments: MultiprocessFlattenArguments,
) -> Path:
    """
    Flattens the directory and saves the mapping.

    Parameters
    ----------
    arguments : MultiprocessFlattenArguments
        Specifies the arguments as per the MultiprocessFlattenArguments class fields.

    Returns
    -------
    Path
        Returns the path to the output directory.
    """

    dir_structure_mapping = directory_flatten(
        root_directory=arguments.maybe_dir,
        list_of_files=arguments.files_with_extension,
        dir_output_path=arguments.dir_output_path,
    )

    save_dir_mapping(
        output_path=arguments.dir_output_path,
        dir_mapping=dir_structure_mapping,
    )

    return arguments.dir_output_path


def create_output_directory(
    arguments: DirectoryCreationArguments,
) -> MultiprocessFlattenArguments:
    """
    Creates the output directory if it doesn't exist.
    Returns the arguments for the directory flattening.

    Parameters
    ----------
    arguments : DirectoryCreationArguments
        Specifies the arguments as per the DirectoryCreationArguments class fields.
        These arguments are used to create the output directory.

    Returns
    -------
    MultiprocessFlattenArguments
        Returns the arguments for the directory flattening.
    """

    if user_prompt_overwrite_ok(
        path=arguments.dir_output_path,
        force_overwrite=arguments.force_overwrite,
    ):
        logging.debug(
            f"Creating directory {str(arguments.dir_output_path)}, didn't exist."
        )
        arguments.dir_output_path.mkdir(exist_ok=True)

    return MultiprocessFlattenArguments(
        dir_output_path=arguments.dir_output_path,
        maybe_dir=arguments.maybe_dir,
        files_with_extension=arguments.files_with_extension,
    )


def multiple_directory_flattener(
    input_path: Path,
    output_path: Path,
    file_extension: str,
    n_threads: int,
    force_overwrite: bool,
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
    n_processes : int
        Specifies the number of processes that will be spawned.
    force : bool
        Specifies if the user wants to overwrite the output directory without \
        being prompted.

    Returns
    -------
    Tuple[bool, List[Path]]
        Returns a tuple where the first element signifies if the processing was ok,
        and a list of paths to the output directories which were flattened.
    """

    # input must be a directory:
    if not input_path.is_dir():
        logging.error(f"Input path must be a directory! {str(input_path.resolve())}")
        return (False, [Path()])

    # Input must exist:
    if not input_path.exists():
        logging.error(f"Input path must exist! {str(input_path.resolve())}")
        return (False, [Path()])

    # Output path must be an existing directory:
    if user_prompt_overwrite_ok(path=output_path, force_overwrite=force_overwrite):
        output_path.mkdir(exist_ok=True)

    directories_to_create = []

    # Iterate over directories:
    # TODO: this can be sped up:
    directory_contants = list(input_path.iterdir())
    for item in tqdm(
        directory_contants,
        desc="Creating output directories",
        unit="dir",
    ):
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

        dir_output_path = Path(output_path, item.name).resolve()
        directories_to_create.append(
            DirectoryCreationArguments(
                dir_output_path=dir_output_path,
                maybe_dir=maybe_dir,
                files_with_extension=files_with_extension,
                force_overwrite=force_overwrite,
            )
        )

    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        multiprocess_flatten_arguments = list(
            executor.map(create_output_directory, directories_to_create)
        )

    output_directories = multiprocess_directory_flattener(
        directories_to_process=multiprocess_flatten_arguments,
        n_processes=n_threads,
    )

    return (True, output_directories)


@click.command(
    help="Directory restructuring tool used in order to flatten the structure. Saves the mapping of the old directory structure to a separate file. Used to ease processing with other tools. Can be used to extract additional meaning from the directory structure in case of tournament replaypacks. Created primarily to define StarCraft 2 (SC2) datasets."
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
    help="Input path to the dataset that is going to be processed.",
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
    help="Output path where the tool will put files after processing.",
)
@click.option(
    "--file_extension",
    type=str,
    default=".SC2Replay",
    required=True,
    help="File extension for the files that will be put to the top level directory. Example ('.SC2Replay').",
)
@click.option(
    "--n_threads",
    type=int,
    default=1,
    required=False,
    help="Number of threads to use for directory flattening.",
)
@click.option(
    "--force_overwrite",
    type=bool,
    default=False,
    required=True,
    help="Flag that specifies if the user wants to overwrite files or directories without being prompted.",
)
@click.option(
    "--log",
    type=click.Choice(["INFO", "DEBUG", "ERROR", "WARN"], case_sensitive=False),
    default="WARN",
    help="Log level. Default is WARN.",
)
def main(
    input_path: Path,
    output_path: Path,
    file_extension: str,
    n_threads: int,
    log: str,
    force_overwrite: bool,
) -> None:
    initialize_logging(log=log)

    multiple_directory_flattener(
        input_path=input_path,
        output_path=output_path,
        file_extension=file_extension,
        n_threads=n_threads,
        force_overwrite=force_overwrite,
    )


if __name__ == "__main__":
    freeze_support()  # For Windows support of parallel tqdm
    main()
