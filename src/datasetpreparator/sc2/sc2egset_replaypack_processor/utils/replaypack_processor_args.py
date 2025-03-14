import logging
from pathlib import Path
import os

from datasetpreparator.utils.user_prompt import user_prompt_overwrite_ok


class SC2InfoExtractorGoArguments:
    """
    Arguments for the SC2InfoExtractorGo binary.

    Parameters
    ----------
    processing_input : Path, optional
        Input directory where .SC2Replay files are held.
    output : Path, optional
        Output directory where compressed zip packages will be saved
    game_mode_filter : int, optional
        Specifies which game mode should be included from the processed files
        in a format of a binary flag: AllGameModes: 0b11111111.
    log_dir : Path, optional
        Specifies directory which will hold the logging information
    log_level : int, optional
        Specifies a log level from 1-7:
        Panic - 1, Fatal - 2,
        Error - 3, Warn - 4,
        Info - 5, Debug - 6,
        Trace - 7.
    number_of_packages : int, optional
        Provide a number of zip packages to be created and compressed
        into a zip archive. Please remember that this number needs to be lower
        than the number of processed files. If set to 0, will ommit the
        zip packaging and output .json directly to drive
    only_map_download : bool, optional
        Specifies if the tool is supposed to only download
        the maps and not process the replays
    perform_chat_anonymization : bool, optional
        Specifies if the chat anonymization should be performed
    perform_cleanup: bool, optional
        Provide if the tool is supposed to perform the cleaning
        functions within the processing pipeline
    perform_filtering : bool, optional
        Specifies if the pipeline ought to verify different hard coded game modes.
        If set to false completely bypasses the filtering
    perform_integrity_checks : bool, optional
        If the software is supposed to check the hardcoded
        integrity checks for the provided replays
    perform_player_anonymization : bool, optional
        Specifies if the tool is supposed to perform player anonymization
        functions within the processing pipeline.
        If set to true please remember to download and run
        an anonymization server: https://doi.org/10.5281/zenodo.5138313.
    perform_validity_checks : bool, optional
        Provide if the tool is supposed to use hardcoded validity checks
        and verify if the replay file variables
        are within 'common sense' ranges.
    max_procs : int, optional
        Specifies the number of logic cores of a processor
        that will be used for processing, by default os.cpu_count()
    """

    def __init__(
        self,
        processing_input: Path = Path("./replays/input"),
        output: Path = Path("./replays/output"),
        game_mode_filter: int = 0b11111111,
        log_dir: Path = Path("./logs"),
        log_level: int = 4,
        number_of_packages: int = 1,
        only_map_download: bool = False,
        maps_directory: Path = Path("./maps/"),
        perform_chat_anonymization: bool = False,
        perform_cleanup: bool = True,
        perform_filtering: bool = False,
        perform_integrity_checks: bool = False,
        perform_player_anonymization: bool = False,
        perform_validity_checks: bool = False,
        max_procs: int = os.cpu_count(),
    ):
        self.processing_input = processing_input.resolve()
        self.output = output.resolve()
        self.log_dir = log_dir.resolve()
        self.maps_directory = maps_directory.resolve()

        self.game_mode_filter = game_mode_filter
        self.log_level = log_level
        self.max_procs = max_procs
        self.number_of_packages = number_of_packages
        self.only_map_download = "true" if only_map_download else "false"
        self.perform_chat_anonymization = (
            "true" if perform_chat_anonymization else "false"
        )
        self.perform_cleanup = "true" if perform_cleanup else "false"
        self.perform_filtering = "true" if perform_filtering else "false"
        self.perform_integrity_checks = "true" if perform_integrity_checks else "false"
        self.perform_player_anonymization = (
            "true" if perform_player_anonymization else "false"
        )
        self.perform_validity_checks = "true" if perform_validity_checks else "false"

    @staticmethod
    def get_download_maps_args(
        processing_input: Path,
        maps_directory: Path,
        n_processes: int,
    ) -> "SC2InfoExtractorGoArguments":
        """
        Creates arguments for downloading the maps using the SC2InfoExtractorGo binary.

        Parameters
        ----------
        processing_input : Path
            Specifies the input directory where the .SC2Replay files are held.
            SC2InfoExtractorGo will recursively search for .SC2Replay files in this directory.
        maps_directory : Path
            Specifies the directory where the maps are stored and will be downloaded to.
        n_processes : int
            Number of SC2InfoExtractorGo processes that will be spawned.

        Returns
        -------
        SC2InfoExtractorGoArguments
            Arguments for the SC2InfoExtractorGo binary.
        """

        arguments = SC2InfoExtractorGoArguments(
            processing_input=processing_input,
            maps_directory=maps_directory,
            only_map_download=True,
            max_procs=n_processes,
        )

        return arguments

    @staticmethod
    def get_sc2egset_processing_args(
        processing_input: Path,
        output: Path,
        maps_directory: Path,
        perform_chat_anonymization: bool,
    ) -> "SC2InfoExtractorGoArguments":
        """
        Creates arguments for the processing of the SC2EGSet dataset.

        Parameters
        ----------
        processing_input : Path
            Specifies the input directory where the flattened replaypacks are held.
        output : Path
            Specifies the output directory where the processed replaypacks will be saved.
        maps_directory : Path
            Specifies the directory where the maps are stored.
        perform_chat_anonymization : bool
            Specifies if the chat anonymization should be performed.

        Returns
        -------
        SC2InfoExtractorGoArguments
            Arguments for the SC2InfoExtractorGo binary.
        """

        arguments = SC2InfoExtractorGoArguments(
            processing_input=processing_input,
            output=output,
            maps_directory=maps_directory,
            perform_integrity_checks=True,
            perform_validity_checks=False,
            perform_cleanup=True,
            perform_chat_anonymization=perform_chat_anonymization,
            number_of_packages=1,
            max_procs=1,
            log_level=3,
            log_dir=output,
        )

        return arguments


class ReplaypackProcessorArguments:
    """
    Arguments for the ReplaypackProcessor.

    Parameters
    ----------
    input_path : Path
        Input path that contains multiple replaypacks.
    output_path : Path
        Output path where the processed replaypacks will be saved.
    n_processes : int
        Number of SC2InfoExtractorGo processes that will be spawned.
    """

    def __init__(
        self,
        input_path: Path,
        output_path: Path,
        maps_directory: Path,
        n_processes: int,
    ):
        self.input_path = input_path
        self.output_path = output_path
        self.n_processes = n_processes
        self.maps_directory = maps_directory


def define_sc2egset_args(
    arguments: ReplaypackProcessorArguments,
    maybe_dir: Path,
    force_overwrite: bool,
) -> ReplaypackProcessorArguments | None:
    """
    Creates final ReplaypackProcessorArguments for SC2InfoExtractorGo. These arguments
    are used to perform extraction of the data from a replaypack with the same arguments
    as SC2EGSetDataset.

    Parameters
    ----------
    arguments : ReplaypackProcessorArguments
        Arguments to the command line tool
    maybe_dir : Path
        Directory that is being processed
    force_overwrite : bool
        Specifies if the output directory should forcefully overwriten without asking the user.

    Returns
    -------
    ReplaypackProcessorArguments | None
        _description_
    """

    input_path = arguments.input_path
    output_path = arguments.output_path

    logging.debug(f"Processing entry: {maybe_dir}")
    processing_input_dir = Path(input_path, maybe_dir).resolve()
    if not processing_input_dir.is_dir():
        logging.debug("Entry is not a directory, skipping!")
        return None

    logging.debug(f"Output dir: {output_path}")
    # Create the main output directory:
    if not user_prompt_overwrite_ok(path=output_path, force_overwrite=force_overwrite):
        output_path.mkdir(exist_ok=True)

    # TODO: use pathlib:
    path, output_directory_name = os.path.split(maybe_dir)
    logging.debug(f"Output dir name: {output_directory_name}")
    if output_directory_name == "input":
        return None

    output_directory_with_name = Path(output_path, output_directory_name).resolve()
    logging.debug(f"Output filepath: {output_directory_with_name}")

    # Create the output subdirectories:
    if not user_prompt_overwrite_ok(
        path=output_directory_with_name, force_overwrite=force_overwrite
    ):
        output_directory_with_name.mkdir(exist_ok=True)

    sc2_info_extractor_go_args = (
        SC2InfoExtractorGoArguments.get_sc2egset_processing_args(
            processing_input=processing_input_dir,
            output=output_directory_with_name,
            perform_chat_anonymization=False,
            maps_directory=arguments.maps_directory,
        )
    )

    logging.debug(f"Finished creating args for {maybe_dir}")

    return sc2_info_extractor_go_args
