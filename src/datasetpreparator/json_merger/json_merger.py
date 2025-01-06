import json
import logging
from pathlib import Path
from typing import Dict

import click

from datasetpreparator.settings import LOGGING_FORMAT
from datasetpreparator.utils.user_prompt import user_prompt_overwrite_ok


def merge_files(path_to_json_one: Path, path_to_json_two: Path) -> Dict[str, str]:
    """
    Exposes the logic to merge two json files by loading their contents from supplied paths.

    Parameters
    ----------
    path_to_json_one : Path
        Specifies the filepath of a .json file that is going to be merged.
    path_to_json_two : Path
        Specifies the filepath of a .json file that is going to be merged.

    Returns
    -------
    Dict[str, str]
        Returns a merged dictionary.
    """

    # Loading the supplied .json files and deserializing them:
    json_one_file = path_to_json_one.open(encoding="utf-8")
    loaded_json_one = json.loads(json_one_file.read())
    json_one_file.close()

    json_two_file = path_to_json_two.open(encoding="utf-8")
    loaded_json_two = json.loads(json_two_file.read())
    json_two_file.close()

    # Merging the loaded dictionaries:
    result_dict = loaded_json_one | loaded_json_two

    return result_dict


def save_output(output_filepath: Path, output_dict: Dict[str, str]) -> Path:
    """
    Exposes the logic for saving a dict to a .json file.

    Parameters
    ----------
    output_filepath : Path
        Speciifies the full output filepath which will be used, \
        this includes the filename.
    output_dict : Dict[str, str]
        Specifies the Python dictionary which will be serialized into a JSON.

    Returns
    -------
    Path
        Returns a path to the saved file.
    """

    with output_filepath.open(mode="w", encoding="utf-8") as output_file:
        json.dump(output_dict, output_file, indent=4)

    return output_filepath


def json_merger(
    path_to_json_one: Path,
    path_to_json_two: Path,
    output_filepath: Path,
    force_overwrite: bool,
) -> Path:
    """
    Merges two JSON files into one.

    Parameters
    ----------
    path_to_json_one : Path
        Path to first JSON file.
    path_to_json_two : Path
        Path to second JSON file.
    output_filepath : Path
        Filepath which will contain the final output of the merging.

    Returns
    -------
    Path
        Returns a path to the saved merged file.
    """

    # Checking early if the output file can be overwritten:
    # at this stage no merging of JSON files has been done yet.
    # User won't have to wait for the files to be merged to be prompted.
    if not user_prompt_overwrite_ok(output_filepath, force_overwrite):
        logging.error("User did not confirm possible overwrite. Exiting...")
        return Path("")

    output_dict = merge_files(
        path_to_json_one=path_to_json_one, path_to_json_two=path_to_json_two
    )

    final_out_filepath = save_output(
        output_filepath=output_filepath, output_dict=output_dict
    )

    return final_out_filepath


@click.command(
    help="Tool used for merging two .json files. Originally used to merge two json files created by https://github.com/Kaszanas/SC2MapLocaleExtractor"
)
@click.option(
    "--json_one",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True,
    help="Path to the first .json file that is going to be merged.",
)
@click.option(
    "--json_two",
    type=click.Path(writable=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True,
    help="Path to the second .json file that is going to be merged.",
)
@click.option(
    "--output_filepath",
    type=click.Path(dir_okay=False, file_okay=True, resolve_path=True),
    required=True,
    help="Filepath to which the result JSON file will be saved, note that any existing file of the same name will be overwriten.",
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
    path_to_json_one: Path,
    path_to_json_two: Path,
    output_filepath: Path,
    log: str,
    force_overwrite: bool,
) -> None:
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    json_merger(
        path_to_json_one=path_to_json_one,
        path_to_json_two=path_to_json_two,
        output_filepath=output_filepath,
        force_overwrite=force_overwrite,
    )


if __name__ == "__main__":
    main()
