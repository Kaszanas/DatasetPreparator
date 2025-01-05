import os
from pathlib import Path
import logging
import click
from tqdm import tqdm

from datasetpreparator.settings import LOGGING_FORMAT
from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.replaypack_processor_args import (
    ReplaypackProcessorArguments,
    SC2InfoExtractorGoArguments,
)
from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.multiprocess import (
    multiprocessing_scheduler,
    pre_process_download_maps,
)

from datasetpreparator.directory_flattener.directory_flattener import (
    multiple_directory_flattener,
)

from datasetpreparator.directory_packager.directory_packager import (
    multiple_dir_packager,
)

from datasetpreparator.processed_mapping_copier.processed_mapping_copier import (
    processed_mapping_copier,
)

from datasetpreparator.file_renamer.file_renamer import file_renamer


def define_sc2egset_args(
    input_path: Path,
    output_path: Path,
    arguments: ReplaypackProcessorArguments,
    maybe_dir: Path,
) -> ReplaypackProcessorArguments | None:
    logging.debug(f"Processing entry: {maybe_dir}")
    processing_input_dir = Path(input_path, maybe_dir).resolve()
    if not processing_input_dir.is_dir():
        logging.debug("Entry is not a directory, skipping!")
        return None

    logging.debug(f"Output dir: {output_path}")
    # Create the main output directory:
    if not output_path.exists():
        output_path.mkdir()

    # TODO: use pathlib:
    path, output_directory_name = os.path.split(maybe_dir)
    logging.debug(f"Output dir name: {output_directory_name}")
    if output_directory_name == "input":
        return None

    output_directory_with_name = Path(output_path, output_directory_name).resolve()
    logging.debug(f"Output filepath: {output_directory_with_name}")

    # Create the output subdirectories:
    if not output_directory_with_name.exists():
        output_directory_with_name.mkdir()

    sc2_info_extractor_go_args = (
        SC2InfoExtractorGoArguments.get_sc2egset_processing_args(
            processing_input=processing_input_dir,
            output=output_directory_with_name,
            perform_chat_anonymization=arguments.perform_chat_anonymization,
        )
    )

    return sc2_info_extractor_go_args


def sc2info_extractor_go_map_download(arguments: ReplaypackProcessorArguments):
    # Pre-process, download all maps:
    logging.info("Downloading all maps...")
    map_download_arguments = SC2InfoExtractorGoArguments.get_download_maps_args(
        processing_input=arguments.input_path, output=arguments.output_path
    )
    pre_process_download_maps(arguments=map_download_arguments)
    pass


def sc2egset_replaypack_processor(
    arguments: ReplaypackProcessorArguments,
):
    """
    Processes multiple StarCraft II replaypacks
    by using https://github.com/Kaszanas/SC2InfoExtractorGo

    Parameters
    ----------
    arguments : ReplaypackProcessorArguments
        Specifies the arguments as per the ReplaypackProcessorArguments class fields.
    """

    input_path = arguments.input_path
    output_path = arguments.output_path
    n_processes = arguments.n_processes

    multiprocessing_list = []
    for maybe_dir in tqdm(list(input_path.iterdir())):
        sc2_info_extractor_go_args = define_sc2egset_args(
            input_path=input_path,
            output_path=output_path,
            arguments=arguments,
            maybe_dir=maybe_dir,
        )
        if sc2_info_extractor_go_args is not None:
            multiprocessing_list.append(sc2_info_extractor_go_args)

    # Run processing with multiple SC2InfoExtractorGo instances:
    multiprocessing_scheduler(multiprocessing_list, int(n_processes))


@click.command(
    help="Tool used to recreate SC2ReSet and SC2EGSet Dataset. Depends on SC2InfoExtractorGo (https://github.com/Kaszanas/SC2InfoExtractorGo) which is executed on multiple replaypack directories in the process. Entire pipeline for replay processing runs with the command line arguments used to create SC2EGSet. Assists in processing StarCraft 2 (SC2) datasets."
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
    help="Input directory containing multiple StarCraft 2 replaypacks. These files will be processed exactly the same as SC2ReSet and SC2EGSet datasets.",
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
    help="Output path where the tool will place the processed files for SC2ReSet and SC2EGSet dataset as children directories.",
)
@click.option(
    "--n_processes",
    type=int,
    default=4,
    required=True,
    help="Number of processes to be spawned for the dataset processing with SC2InfoExtractorGo.",
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
    n_processes: int,
    log: str,
) -> None:
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    # Create output directory if it does not exist:
    if not output_path.exists():
        output_path.mkdir(exist_ok=True)

    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()

    maps_output_path = Path(output_path, "maps").resolve()

    arguments = ReplaypackProcessorArguments(
        input_path=input_path,
        output_path=output_path,
        n_processes=n_processes,
        maps_directory=maps_output_path,
    )

    # TODO: Recreate the entire pipeline for SC2ReSet and SC2EGSet:
    # REVIEW: Note that the Chinese maps need to be pre-seeded so that they can be
    # hosted later on.

    # Directory flattener:
    directory_flattener_output_path = Path(
        output_path, "directory_flattener_output"
    ).resolve()
    # REVIEW: Should it be ok if the directory exists?
    # it may contain some files that should not be overwritten:
    # --force as a flag in CLI
    # input command waiting for user input to confirm potential overwrite:
    #

    if not directory_flattener_output_path.exists():
        directory_flattener_output_path.mkdir(exist_ok=True)

    # TODO: Check if the output directory is not empty, if it is you can proceed
    # if the directory is not empty issue a warning with confirmation prompt.

    # if not empty and not force:
    #   prompt user to confirm overwrite

    logging.info("Flattening directories...")
    multiple_directory_flattener(
        input_path=input_path,
        output_path=directory_flattener_output_path,
        file_extension=".SC2Replay",
    )

    # Download all maps for multiprocess, map files are used as a source of truth for
    # SC2InfoExtractorGo downloading mechanism:
    logging.info("Downloading all maps using SC2InfoExtractorGo...")
    sc2info_extractor_go_map_download(arguments=arguments)

    # Package SC2ReSet and the downloaded maps, move to the output directory:
    logging.info("Packaging SC2ReSet and the downloaded maps...")
    multiple_dir_packager(input_path="")

    # Process SC2EGSet, this will use the same map directory as the previous step:
    logging.info("Processing SC2EGSet using SC2InfoExtractorGo...")
    sc2egset_replaypack_processor(arguments=arguments)

    # Processed Mapping Copier:
    logging.info("Copying processed_mapping.json files...")
    processed_mapping_copier(input_path="", output_path="")

    # File Renamer:
    logging.info("Renaming auxilliary (log) files...")
    file_renamer(input_path="")


if __name__ == "__main__":
    main()
