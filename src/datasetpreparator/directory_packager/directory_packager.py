import logging
from pathlib import Path
from typing import List
from zipfile import ZipFile, ZIP_BZIP2

import click
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from datasetpreparator.settings import LOGGING_FORMAT
from datasetpreparator.utils.user_prompt import user_prompt_overwrite_ok


def multiple_dir_packager(input_path: Path, force_overwrite: bool) -> List[Path]:
    """
    Packages the specified directory into a .zip archive.

    Parameters
    ----------
    input_path : Path
        Specifies the path to a directoryu for which each of its directories will be turned into a .zip archive.
    force_overwrite : bool
        Specifies if the user wants to overwrite files or directories without being prompted

    Returns
    -------
    List[Path]
        Returns a list of Paths to packaged archives.
    """

    output_archives = []
    for directory in input_path.iterdir():
        logging.debug(f"Processing directory: {str(directory)}")

        directory_path = Path(input_path, directory.name).resolve()
        if not directory_path.is_dir():
            continue

        logging.debug(f"Packaging directory: {str(directory_path)}")
        processed_path = dir_packager(
            directory_path=directory_path, force_overwrite=force_overwrite
        )
        output_archives.append(processed_path)

    return output_archives


def dir_packager(directory_path: Path, force_overwrite: bool) -> Path:
    """
    Archives a single input directory.
    Archive is stored in the same directory as the input.

    Parameters
    ----------
    directory_path : Path
        Specifies the path to the directory that will be archived.
    force_overwrite : bool
        Specifies if the user wants to overwrite files or directories without being prompted

    Returns
    -------
    Path
        Returns a Path to the archive.
    """

    final_archive_path = directory_path.with_suffix(".zip")

    if user_prompt_overwrite_ok(
        path=final_archive_path, force_overwrite=force_overwrite
    ):
        logging.info(f"Set final archive name to: {str(final_archive_path)}")
        with ZipFile(str(final_archive_path), "w") as zip_file:
            with logging_redirect_tqdm():
                for file in tqdm(
                    list(directory_path.rglob("*")),
                    desc=f"Packaging {final_archive_path.name}",
                    unit="files",
                ):
                    abs_filepath = str(file.resolve())

                    logging.debug(f"Adding file: {abs_filepath}")
                    zip_file.write(
                        filename=abs_filepath,
                        arcname=file.relative_to(directory_path),
                        compress_type=ZIP_BZIP2,
                    )

    return final_archive_path


@click.command(
    help="Tool that packages directories into .zip archives. Each directory in the input path is packaged into a separate .zip archive."
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
    help="Input path to the directory containing the dataset that is going to be processed by packaging into .zip archives.",
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
def main(input_path: Path, log: str, force_overwrite: bool):
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    multiple_dir_packager(input_path=input_path, force_overwrite=force_overwrite)


if __name__ == "__main__":
    main()
