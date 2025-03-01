import logging
from pathlib import Path

import click

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
    sc2egset_replaypack_processor(arguments=sc2egset_processor_args)

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
    help="Tool used to recreate SC2EGSet Dataset. Executes SC2InfoExtractorGo (https://github.com/Kaszanas/SC2InfoExtractorGo) on multiple replaypack directories with hardcoded CLI arguments. Assists in processing StarCraft 2 (SC2) datasets."
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
        exists=False,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Output path where the tool will place the processed files for SC2ReSet and SC2EGSet dataset as children directories.",
)
@click.option(
    "--maps_path",
    type=click.Path(
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to the StarCraft 2 maps that will be used in replay processing. If there are no maps, they will be downloaded.",
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
    maps_path: Path,
    n_processes: int,
    force_overwrite: bool,
    log: str,
) -> None:
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    output_path = output_path.resolve()

    replaypacks_input_path = input_path.resolve()
    maps_path = maps_path.resolve()
    if user_prompt_overwrite_ok(path=maps_path, force_overwrite=force_overwrite):
        maps_path.mkdir(exist_ok=True)

    # Create output directory if it does not exist:
    if user_prompt_overwrite_ok(path=output_path, force_overwrite=force_overwrite):
        output_path.mkdir(exist_ok=True)

    # Pre-processing, downloading maps and flattening directories:
    map_downloader_args = ReplaypackProcessorArguments(
        input_path=replaypacks_input_path,
        output_path=output_path,
        maps_directory=maps_path,
        n_processes=n_processes,
    )
    sc2infoextractorgo_map_download(arguments=map_downloader_args)

    # Main processing
    sc2egset_processor_args = ReplaypackProcessorArguments(
        input_path=replaypacks_input_path,
        output_path=output_path,
        maps_directory=maps_path,
        n_processes=n_processes,
    )
    sc2egset_replaypack_processor(
        arguments=sc2egset_processor_args, force_overwrite=force_overwrite
    )


if __name__ == "__main__":
    main()
