import logging
import shutil
import subprocess
from multiprocessing import Pool
from pathlib import Path
from typing import List

from tqdm import tqdm

from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.replaypack_processor_args import (
    ReplaypackProcessorArguments,
    SC2InfoExtractorGoArguments,
    define_sc2egset_args,
)
from datasetpreparator.settings import PATH_TO_SC2INFOEXTRACTORGO


def multiprocessing_scheduler(
    processing_arguments: List[SC2InfoExtractorGoArguments],
    number_of_processes: int,
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

    # TODO: This needs to be verified, should use Pathlib:
    # Copying the mapping file that contains directory tree information:

    copy_processed_mapping_file(arguments=arguments)

    logging.debug(
        f"Running subprocess for {arguments.processing_input} with output to {arguments.output}",
    )

    # TODO: Check if I can do a pipe from the subprocess to get multiple progress bars:
    command = [
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
        f"-log_dir={arguments.output}/",
        f"-maps_directory={arguments.maps_directory}/",
        "-skip_map_download",
    ]

    subprocess.run(command)


def copy_processed_mapping_file(arguments: SC2InfoExtractorGoArguments) -> None:
    """
    Copies the processed_mapping.json file from the input directory to the output directory.

    Parameters
    ----------
    arguments : SC2InfoExtractorGoArguments
        Specifies all of the arguments required to run SC2InfoExtractorGo.
        In this case, the input and output directories are used.
    """

    input_mapping_filepath = Path(
        arguments.processing_input, "processed_mapping.json"
    ).resolve()

    if input_mapping_filepath.exists():
        logging.debug(f"Found mapping json in {arguments.processing_input}")

        if not arguments.output.exists():
            arguments.output.mkdir(parents=True, exist_ok=True)

        output_mapping_filepath = Path(
            arguments.output, "processed_mapping.json"
        ).resolve()

        logging.debug(
            f"Copying {str(input_mapping_filepath)} to {str(output_mapping_filepath)}"
        )
        shutil.copy(input_mapping_filepath, output_mapping_filepath)


def sc2egset_replaypack_processor(
    arguments: ReplaypackProcessorArguments,
    force_overwrite: bool,
):
    """
    Processes multiple StarCraft II replaypacks
    by using https://github.com/Kaszanas/SC2InfoExtractorGo

    Parameters
    ----------
    arguments : ReplaypackProcessorArguments
        Specifies the arguments as per the ReplaypackProcessorArguments class fields.
    force_overwrite : bool
        Specifies whether the output directory should be overwritten.
    """

    multiprocessing_list = []
    for maybe_dir in tqdm(
        list(arguments.input_path.iterdir()), desc="Defining multiprocessing list"
    ):
        sc2_info_extractor_go_args = define_sc2egset_args(
            arguments=arguments,
            maybe_dir=maybe_dir,
            force_overwrite=force_overwrite,
        )
        if sc2_info_extractor_go_args is not None:
            logging.debug(
                f"Appending {sc2_info_extractor_go_args} to multiprocessing_list"
            )
            multiprocessing_list.append(sc2_info_extractor_go_args)

    # Run processing with multiple SC2InfoExtractorGo instances:
    logging.debug("Running multiprocessing_scheduler")
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

    command = [
        str(PATH_TO_SC2INFOEXTRACTORGO),
        f"-input={arguments.processing_input}/",
        f"-maps_directory={arguments.maps_directory}/",
        "-only_map_download=true",
        f"-max_procs={2*arguments.max_procs}",
        f"-log_level={arguments.log_level}",
        "-log_dir=logs/",
    ]

    subprocess.run(command)
