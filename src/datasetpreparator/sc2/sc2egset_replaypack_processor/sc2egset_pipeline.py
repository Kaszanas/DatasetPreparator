import logging
from pathlib import Path

import click

from datasetpreparator.directory_flattener.directory_flattener import (
    multiple_directory_flattener,
)
from datasetpreparator.directory_packager.directory_packager import (
    multiple_dir_packager,
)
from datasetpreparator.file_renamer.file_renamer import file_renamer
from datasetpreparator.processed_mapping_copier.processed_mapping_copier import (
    processed_mapping_copier,
)
from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.download_maps import (
    sc2infoextractorgo_map_download,
)
from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.file_copier import (
    move_files,
)
from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.multiprocess import (
    sc2egset_replaypack_processor,
)
from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.replaypack_processor_args import (
    ReplaypackProcessorArguments,
)
from datasetpreparator.settings import LOGGING_FORMAT
from datasetpreparator.utils.user_prompt import user_prompt_overwrite_ok


def prepare_sc2reset(
    output_path: Path,
    replaypacks_input_path: Path,
    n_processes: int,
    force_overwrite: bool,
    maps_output_path: Path,
    directory_flattener_output_path: Path,
) -> None:
    # Directory flattener:

    if user_prompt_overwrite_ok(
        path=directory_flattener_output_path, force_overwrite=force_overwrite
    ):
        directory_flattener_output_path.mkdir(exist_ok=True)

    logging.info("Flattening directories...")
    multiple_directory_flattener(
        input_path=replaypacks_input_path,
        output_path=directory_flattener_output_path,
        file_extension=".SC2Replay",
    )

    # Separate arguments for map downloading are required because the maps directory should be placed
    # ready for the SC2ReSet to be zipped and moved to the output directory:
    map_downloader_args = ReplaypackProcessorArguments(
        input_path=replaypacks_input_path,
        output_path=directory_flattener_output_path,
        n_processes=n_processes,
        maps_directory=maps_output_path,
    )

    # NOTE: Chinese maps need to be pre-seeded so that they can be
    # hosted later on. They are also needed for the SC2EGSet to reproduce the results.
    # Download all maps for multiprocess, map files are used as a source of truth for
    # SC2InfoExtractorGo downloading mechanism:
    logging.info("Downloading all maps using SC2InfoExtractorGo...")
    sc2infoextractorgo_map_download(arguments=map_downloader_args)

    # Package SC2ReSet and the downloaded maps, move to the output directory:
    logging.info("Packaging SC2ReSet and the downloaded maps...")
    multiple_dir_packager(input_path=directory_flattener_output_path)

    sc2reset_output_path = Path(output_path, "SC2ReSet").resolve()
    logging.info("Moving SC2ReSet to the output directory...")
    move_files(
        input_path=directory_flattener_output_path,
        output_path=sc2reset_output_path,
        force_overwrite=force_overwrite,
    )


def prepare_sc2egset(
    replaypacks_input_path: Path,
    output_path: Path,
    n_processes: int,
    maps_output_path: Path,
    directory_flattener_output_path: Path,
    force_overwrite: bool,
) -> None:
    # SC2EGSet Processor:
    sc2egset_processor_args = ReplaypackProcessorArguments(
        input_path=replaypacks_input_path,
        output_path=output_path,
        n_processes=n_processes,
        maps_directory=maps_output_path,
    )

    # Process SC2EGSet, this will use the same map directory as the previous step:
    logging.info("Processing SC2EGSet using SC2InfoExtractorGo...")
    sc2egset_replaypack_processor(
        arguments=sc2egset_processor_args, force_overwrite=force_overwrite
    )

    # Processed Mapping Copier:
    logging.info("Copying processed_mapping.json files...")
    processed_mapping_copier(
        input_path=directory_flattener_output_path, output_path=output_path
    )

    # File Renamer:
    logging.info("Renaming auxilliary (log) files...")
    file_renamer(input_path=output_path)

    logging.info("Packaging SC2EGSet...")
    multiple_dir_packager(input_path=output_path, force_overwrite=force_overwrite)

    # SC2EGSet should be ready, move it to the final output directory:
    sc2egset_output_path = Path(output_path, "SC2EGSet").resolve()
    logging.info("Moving SC2EGSet to the output directory...")
    move_files(
        input_path=output_path,
        output_path=sc2egset_output_path,
        force_overwrite=force_overwrite,
    )


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
    input_path: Path,
    output_path: Path,
    n_processes: int,
    force_overwrite: bool,
    log: str,
) -> None:
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    # Create output directory if it does not exist:
    if user_prompt_overwrite_ok(path=output_path, force_overwrite=force_overwrite):
        output_path.mkdir(exist_ok=True)

    # This input will be flattened:
    replaypacks_input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()

    maps_output_path = Path(output_path, "maps").resolve()
    directory_flattener_output_path = Path(
        output_path, "directory_flattener_output"
    ).resolve()

    # TODO: Recreate the entire pipeline for SC2ReSet and SC2EGSet:
    prepare_sc2reset(
        output_path=output_path,
        replaypacks_input_path=replaypacks_input_path,
        n_processes=n_processes,
        force_overwrite=force_overwrite,
        maps_output_path=maps_output_path,
        directory_flattener_output_path=directory_flattener_output_path,
    )

    prepare_sc2egset(
        replaypacks_input_path=replaypacks_input_path,
        output_path=output_path,
        n_processes=n_processes,
        maps_output_path=maps_output_path,
        directory_flattener_output_path=directory_flattener_output_path,
    )


if __name__ == "__main__":
    main()
