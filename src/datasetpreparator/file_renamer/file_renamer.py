import logging
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
        logging.error(
            f"Input path {str(input_path)} does not exist. No files will be renamed."
        )
        return
    if not input_path.is_dir():
        logging.error(f"Input path {str(input_path)} is not a directory.")
        return

    if not len(list(input_path.iterdir())) > 0:
        logging.error(f"Input path {str(input_path)} is empty. No files to rename.")
        return

    all_files = input_path.glob("**/*")
    for file in all_files:
        directory = file.parent

        if file.name.endswith(".zip"):
            new_name = file.stem + "_data.zip"
            new_path = directory / new_name
            file.rename(new_path)

        if file.name.startswith("package_summary"):
            new_name = file.stem + "_summary.json"
            new_path = directory / new_name
            file.rename(new_path)

        if file.name.startswith("processed_mapping"):
            new_name = file.stem + "_processed_mapping.json"
            new_path = directory / new_name
            file.rename(new_path)

        if file.name.startswith("processed_failed"):
            new_name = file.stem + "_processed_failed.log"
            new_path = directory / new_name
            file.rename(new_path)

        if file.name.startswith("main_log"):
            new_name = file.stem + "_main_log.log"
            new_path = directory / new_name
            file.rename(new_path)


@click.command(
    help="Tool used for renaming auxilliary files (log files) that are produced when creating StarCraft 2 (SC2) datasets with https://github.com/Kaszanas/SC2InfoExtractorGo. Additionally, this tool renames the .zip files so that they carry the original directory name with an added '_data' suffix."
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
