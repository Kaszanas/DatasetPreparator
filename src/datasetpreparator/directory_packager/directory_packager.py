import logging
import os
from pathlib import Path
from typing import List
from zipfile import ZipFile, ZIP_BZIP2

import click

from datasetpreparator.settings import LOGGING_FORMAT
from datasetpreparator.utils.user_prompt import user_prompt_overwrite_ok


def multiple_dir_packager(input_path: str) -> List[Path]:
    """
    Packages the specified directory into a .zip archive.

    Parameters
    ----------
    input_path : str
        Specifies the path which will be turned into a .zip archive.

    Returns
    -------
    List[Path]
        Returns a list of Paths to packaged archives.
    """

    output_archives = []
    for directory in os.listdir(path=input_path):
        directory_path = Path(input_path, directory).resolve()
        if not directory_path.is_dir():
            continue

        output_archives.append(dir_packager(directory_path=directory_path))

    return output_archives


def dir_packager(directory_path: Path) -> Path:
    """
    Archives a single input directory.
    Archive is stored in the same directory as the input.

    Parameters
    ----------
    directory_path : Path
        Specifies the path to the directory that will be archived.

    Returns
    -------
    Path
        Returns a Path to the archive.
    """

    final_archive_path = directory_path.with_suffix(".zip")

    if user_prompt_overwrite_ok(final_archive_path):
        logging.info(f"Set final archive name to: {str(final_archive_path)}")
        with ZipFile(str(final_archive_path), "w") as zip_file:
            for file in directory_path.iterdir():
                abs_filepath = os.path.join(directory_path, file)
                zip_file.write(
                    filename=abs_filepath, arcname=file, compress_type=ZIP_BZIP2
                )

    return final_archive_path


@click.command(
    help="Tool that packages directories into .zip archives. Each directory in the input path is packaged into a separate .zip archive."
)
@click.option(
    "--input_path",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
    required=True,
    help="Input path to the directory containing the dataset that is going to be processed by packaging into .zip archives.",
)
@click.option(
    "--log",
    type=click.Choice(["INFO", "DEBUG", "ERROR", "WARN"], case_sensitive=False),
    default="WARN",
    help="Log level. Default is WARN.",
)
def main(input_path: Path, log: str):
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    multiple_dir_packager(input_path=input_path)


if __name__ == "__main__":
    main()
