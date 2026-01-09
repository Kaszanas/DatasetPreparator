import logging
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import freeze_support
from pathlib import Path
from zipfile import ZIP_BZIP2, ZipFile

import click
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from datasetpreparator.utils.logging import initialize_logging
from datasetpreparator.utils.user_prompt import (
    create_directory,
    user_prompt_overwrite_ok,
)


class DirectoryPackagerArguments:
    def __init__(self, directory_path: Path, force_overwrite: bool):
        self.directory_path = directory_path
        self.force_overwrite = force_overwrite


def multiple_dir_packager(
    input_path: Path,
    n_threads: int,
    force_overwrite: bool,
) -> list[Path]:
    """
    Packages the specified directory into a .zip archive.

    Parameters
    ----------
    input_path : Path
        Specifies the path to a directoryu for which each of its directories
        will be turned into a .zip archive.
    n_threads : int
        Specifies the number of threads to use for packaging.
    force_overwrite : bool
        Specifies if the user wants to overwrite files or directories without being prompted

    Returns
    -------
    list[Path]
        Returns a list of Paths to packaged archives.
    """

    dirs_to_package = []

    directory_contents = list(input_path.iterdir())
    if not directory_contents:
        logging.error(f"The input path {str(input_path)} is empty!")
        return []

    for directory in directory_contents:
        logging.debug(f"Processing directory: {str(directory)}")

        directory_path = Path(input_path, directory.name).resolve()
        if not directory_path.is_dir():
            continue

        dirs_to_package.append(
            DirectoryPackagerArguments(
                directory_path=directory_path,
                force_overwrite=force_overwrite,
            )
        )

    with ThreadPoolExecutor(
        max_workers=n_threads,
        initializer=tqdm.set_lock,
        initargs=(tqdm.get_lock(),),
    ) as executor:
        output_archives = list(executor.map(dir_packager, dirs_to_package))

    return output_archives


def dir_packager(arguments: DirectoryPackagerArguments) -> Path:
    """
    Archives a single input directory.
    Archive is stored in the same directory as the input.

    Parameters
    ----------
    arguments : DirectoryPackagerArguments
        Specifies the arguments as per the DirectoryPackagerArguments class fields.

    Returns
    -------
    Path
        Returns a Path to the archive.
    """

    final_archive_path = arguments.directory_path.with_suffix(".zip")

    if user_prompt_overwrite_ok(
        path=final_archive_path, force_overwrite=arguments.force_overwrite
    ):
        logging.info(f"Set final archive name to: {str(final_archive_path)}")
        with ZipFile(str(final_archive_path), "w") as zip_file:
            with logging_redirect_tqdm():
                for file in tqdm(
                    list(arguments.directory_path.rglob("*")),
                    desc=f"Packaging {final_archive_path.name:<30}",
                    unit="files",
                ):
                    abs_filepath = str(file.resolve())

                    logging.debug(f"Adding file: {abs_filepath}")
                    zip_file.write(
                        filename=abs_filepath,
                        arcname=file.relative_to(arguments.directory_path),
                        compress_type=ZIP_BZIP2,
                    )

    return final_archive_path


@click.command(
    help="Tool that packages directories into .zip archives. Each directory in the input path is packaged into a separate .zip archive."
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
    help="Input path to the directory containing the dataset that is going to be processed by packaging into .zip archives.",
)
@click.option(
    "--n_threads",
    type=int,
    default=1,
    required=False,
    help="Number of threads to use for packaging. Default is 1.",
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
def main(input_path: Path, log: str, n_threads: int, force_overwrite: bool):
    initialize_logging(log=log)

    if create_directory(directory=input_path):
        logging.error(
            f"Input path {str(input_path)} was just created. You should fill it with files before proceeding."
        )
        return

    multiple_dir_packager(
        input_path=input_path,
        n_threads=n_threads,
        force_overwrite=force_overwrite,
    )


if __name__ == "__main__":
    freeze_support()  # For Windows support of parallel tqdm
    main()
