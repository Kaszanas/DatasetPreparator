import logging
import os
from pathlib import Path

import click

from datasetpreparator.settings import LOGGING_FORMAT


def file_renamer(input_path: Path) -> None:
    """
    Provides logic for renaming files with .zip and .json files
    that are contained within a directory.
    Contains hardcoded rules: if the file is of .zip extension
    it adds "_data" prefix to the filename.
    And if the file is of .json extension
    it adds "_summary" prefix to the filename.

    Parameters
    ----------
    input_path : Path
        Specifies the input directory where the files will be renamed.
    """

    if not input_path.exists():
        raise FileNotFoundError(f"Input path {input_path.as_posix()} does not exist.")

    if not input_path.is_dir():
        raise NotADirectoryError(
            f"Input path {input_path.as_posix()} is not a directory."
        )

    if not len(list(input_path.iterdir())) > 0:
        raise ValueError(f"Input path {input_path.as_posix()} is empty.")

    # TODO: This can be done with iterdir:
    for directory, _, file_list in os.walk(input_path.as_posix()):
        for file in file_list:
            # REVIEW: Can this be done better? Match case statement?
            if file.endswith(".zip"):
                os.rename(
                    os.path.join(directory, file),
                    os.path.join(directory, os.path.basename(directory) + "_data.zip"),
                )
            if file.startswith("package_summary"):
                os.rename(
                    os.path.join(directory, file),
                    os.path.join(
                        directory, os.path.basename(directory) + "_summary.json"
                    ),
                )
            if file.startswith("processed_mapping"):
                os.rename(
                    os.path.join(directory, file),
                    os.path.join(
                        directory,
                        os.path.basename(directory) + "_processed_mapping.json",
                    ),
                )
            if file.startswith("processed_failed"):
                os.rename(
                    os.path.join(directory, file),
                    os.path.join(
                        directory,
                        os.path.basename(directory) + "_processed_failed.log",
                    ),
                )
            if file.startswith("main_log"):
                os.rename(
                    os.path.join(directory, file),
                    os.path.join(
                        directory,
                        os.path.basename(directory) + "_main_log.log",
                    ),
                )


@click.command(
    help="Tool used for renaming auxilliary files (log files) that are produced when creating StarCraft 2 (SC2) datasets with https://github.com/Kaszanas/SC2InfoExtractorGo"
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
def main(input_path: Path, log: str) -> None:
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    file_renamer(input_path=input_path)


if __name__ == "__main__":
    main()
