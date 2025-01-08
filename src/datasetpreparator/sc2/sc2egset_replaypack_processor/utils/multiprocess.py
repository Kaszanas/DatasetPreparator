import logging
import subprocess
import os
import shutil
from multiprocessing import Pool

from typing import List

from tqdm import tqdm

from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.replaypack_processor_args import (
    ReplaypackProcessorArguments,
    SC2InfoExtractorGoArguments,
    define_sc2egset_args,
)

from datasetpreparator.settings import PATH_TO_SC2INFOEXTRACTORGO


def multiprocessing_scheduler(
    processing_arguments: List[SC2InfoExtractorGoArguments], number_of_processes: int
) -> None:
    """
    Responsible for spawning the multiprocessing_client functions.

    Parameters
    ----------
    processing_arguments : List[Tuple[str, str]]
        Processing arguments holds a list of input and output directories \
        for the https://github.com/Kaszanas/SC2InfoExtractorGo
    number_of_processes : int
        Specifies how many processes will be spawned.
    """

    with Pool(processes=number_of_processes) as pool:
        pool.imap_unordered(process_single_replaypack, processing_arguments)
        pool.close()
        pool.join()


def process_single_replaypack(arguments: SC2InfoExtractorGoArguments) -> None:
    """
    Responsible for running a single process that will
    extract data from a replaypack.

    Parameters
    ----------
    arguments : SC2InfoExtractorGoArguments
        Specifies all of the arguments required to run SC2InfoExtractorGo.
    """

    # TODO: This will be refactored to use only the arguments object:
    directory = arguments.processing_input
    output_directory_filepath = arguments.output

    # TODO: This needs to be verified, should use Pathlib:
    # Copying the mapping file that contains directory tree information:
    directory_contents = os.listdir(directory)
    if "processed_mapping.json" in directory_contents:
        logging.debug("Found mapping json in %s", directory)
        mapping_filepath = os.path.join(directory, "processed_mapping.json")
        output_mapping_filepath = os.path.join(
            output_directory_filepath, "processed_mapping.json"
        )
        shutil.copy(mapping_filepath, output_mapping_filepath)

    logging.debug(
        "Running subprocess for %s with output to %s",
        directory,
        output_directory_filepath,
    )

    # TODO: Check if I can do a pipe from the subprocess to get multiple progress bars:
    subprocess.run(
        [
            # FIXME hardcoded binary name
            str(PATH_TO_SC2INFOEXTRACTORGO),
            f"-input={arguments.processing_input}/",
            f"-output={arguments.output}/",
            f"-perform_integrity_checks={arguments.perform_integrity_checks}",
            f"-perform_validity_checks={arguments.perform_validity_checks}",
            f"-perform_cleanup={arguments.perform_cleanup}",
            f"-perform_chat_anonymization={arguments.perform_chat_anonymization}",
            f"-number_of_packages={arguments.number_of_packages}",
            f"-max_procs={arguments.max_procs}",
            f"-log_level={arguments.log_level}",
            f"-log_dir={output_directory_filepath}/",
        ]
    )


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

    multiprocessing_list = []
    for maybe_dir in tqdm(list(arguments.input_path.iterdir())):
        sc2_info_extractor_go_args = define_sc2egset_args(
            arguments=arguments,
            maybe_dir=maybe_dir,
        )
        if sc2_info_extractor_go_args is not None:
            multiprocessing_list.append(sc2_info_extractor_go_args)

    # Run processing with multiple SC2InfoExtractorGo instances:
    multiprocessing_scheduler(multiprocessing_list, int(arguments.n_processes))


def pre_process_download_maps(arguments: SC2InfoExtractorGoArguments) -> None:
    """
    Acts as a pre-process step, executes SC2InfoExtractorGo with the
    -only_map_download flag. Maps are required in the future steps of the
    processing due to the fact that multiple SC2InfoExtractorGo instances will
    be running in parallel. This means that the maps cannot be downloaded and processed
    at the same time.

    Parameters
    ----------
    arguments : SC2InfoExtractorGoArguments
        Specifies all of the arguments required to run SC2InfoExtractorGo.
    """

    output_directory_filepath = arguments.output

    subprocess.run(
        [
            str(PATH_TO_SC2INFOEXTRACTORGO),
            f"-input={arguments.processing_input}/",
            f"-output={arguments.output}/",
            "-only_map_download=true",
            f"-max_procs={arguments.max_procs}",
            f"-log_level={arguments.log_level}",
            f"-log_dir={output_directory_filepath}/",
        ]
    )
