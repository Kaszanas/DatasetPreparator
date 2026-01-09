import logging
import os
from multiprocessing import freeze_support
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
from datasetpreparator.utils.logging import initialize_logging
from datasetpreparator.utils.user_prompt import (
    create_directory,
    user_prompt_overwrite_ok,
)


def prepare_sc2reset(
    replaypacks_input_path: Path,
    output_path: Path,
    n_processes: int,
    force_overwrite: bool,
    maps_output_path: Path,
    directory_flattener_output_path: Path,
) -> None:
    """
    Function that runs all of the necessary steps to prepare SC2ReSet dataset.

    Parameters
    ----------
    replaypacks_input_path : Path
        Input directory containing multiple replaypacks.
    output_path : Path
        Output path where the tool will place the processed files for SC2ReSet.
    n_processes : int
        Number of goroutines to be spawned for reading the replay files,
        this will multiplied by two.
    force_overwrite : bool
        Flag that specifies if the user wants to overwrite files or directories without being prompted.
    maps_output_path : Path
        Path where the maps will be downloaded.
    directory_flattener_output_path : Path
        Path where the directory flattener output will be placed
    """

    # Directory flattener:
    if user_prompt_overwrite_ok(
        path=directory_flattener_output_path,
        force_overwrite=force_overwrite,
    ):
        directory_flattener_output_path.mkdir(exist_ok=True)

    logging.info("Flattening directories...")
    multiple_directory_flattener(
        input_path=replaypacks_input_path,
        output_path=directory_flattener_output_path,
        file_extension=".SC2Replay",
        n_threads=n_processes,
        force_overwrite=force_overwrite,
    )

    # NOTE: Chinese maps need to be pre-seeded so that they can be
    # hosted later on. They are also needed for the SC2EGSet to reproduce the results.
    # Download all maps for multiprocess, map files are used as a source of truth for
    # SC2InfoExtractorGo downloading mechanism:
    logging.info("Downloading all maps using SC2InfoExtractorGo...")
    sc2infoextractorgo_map_download(
        input_path=directory_flattener_output_path,
        maps_directory=maps_output_path,
        n_processes=n_processes,
    )

    # Package SC2ReSet and the downloaded maps, move to the output directory:
    logging.info("Packaging SC2ReSet and the downloaded maps...")
    multiple_dir_packager(
        input_path=directory_flattener_output_path,
        n_threads=n_processes,
        force_overwrite=force_overwrite,
    )

    sc2reset_output_path = Path(output_path, "SC2ReSet").resolve()
    logging.info("Moving SC2ReSet to the output directory...")
    move_files(
        input_path=directory_flattener_output_path,
        output_path=sc2reset_output_path,
        force_overwrite=force_overwrite,
        extension=".zip",
        recursive=True,
    )


def prepare_sc2egset(
    replaypacks_input_path: Path,
    output_path: Path,
    sc2egset_replaypack_processor_output: Path,
    n_processes: int,
    maps_output_path: Path,
    directory_flattener_output_path: Path,
    force_overwrite: bool,
) -> None:
    """
    Function that runs all of the necessary steps to prepare SC2EGSet dataset.

    Parameters
    ----------
    replaypacks_input_path : Path
        Input directory containing multiple replaypacks.
        Should be the same as the output of directory flattener.
    output_path : Path
        Output path where the tool will place the processed files for SC2EGSet.
    n_processes : int
        Number of Python processes to be spawned for the dataset processing with SC2InfoExtractorGo.
    maps_output_path : Path
        Path where the maps are stored.
    directory_flattener_output_path : Path
        Path where the directory flattener output is placed.
    force_overwrite : bool
        Flag that specifies if the user wants to overwrite files or directories without being prompted.
    """

    # SC2EGSet Processor:
    sc2egset_processor_args = ReplaypackProcessorArguments(
        input_path=replaypacks_input_path,
        output_path=sc2egset_replaypack_processor_output,
        n_processes=n_processes,
        maps_directory=maps_output_path,
    )

    # Process SC2EGSet, this will use the same map directory as the previous step:
    logging.info("Processing SC2EGSet using SC2InfoExtractorGo...")
    sc2egset_replaypack_processor(
        arguments=sc2egset_processor_args,
        force_overwrite=force_overwrite,
    )

    # Processed Mapping Copier:
    logging.info("Copying processed_mapping.json files...")
    processed_mapping_copier(
        input_path=directory_flattener_output_path,
        output_path=sc2egset_replaypack_processor_output,
    )

    # File Renamer:
    logging.info(
        f"Renaming auxilliary (log) files in {str(sc2egset_replaypack_processor_output)}"
    )
    file_renamer(input_path=sc2egset_replaypack_processor_output)

    logging.info("Packaging SC2EGSet...")
    multiple_dir_packager(
        input_path=sc2egset_replaypack_processor_output,
        n_threads=n_processes,
        force_overwrite=force_overwrite,
    )

    # SC2EGSet should be ready, move it to the final output directory:
    sc2egset_output = Path(output_path, "SC2EGSet").resolve()
    logging.info("Moving SC2EGSet to the output directory...")
    move_files(
        input_path=sc2egset_replaypack_processor_output,
        output_path=sc2egset_output,
        force_overwrite=force_overwrite,
        extension=".zip",
        recursive=False,
    )


@click.command(
    help="Tool used to recreate SC2ReSet and SC2EGSet Dataset. Depends on SC2InfoExtractorGo (https://github.com/Kaszanas/SC2InfoExtractorGo) which is executed on multiple replaypack directories in the process. Entire pipeline for replay processing runs with the command line arguments used to create SC2EGSet. Assists in processing StarCraft 2 (SC2) datasets."
)
@click.option(
    "--input_path",
    type=click.Path(
        exists=False,
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
        exists=False,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path where the maps will be downloaded.",
)
@click.option(
    "--n_processes",
    type=int,
    default=os.cpu_count(),
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
    initialize_logging(log=log)
    # This input will be flattened:
    replaypacks_input_path = Path(input_path).resolve()
    if create_directory(directory=replaypacks_input_path):
        logging.error(
            f"Input path {str(replaypacks_input_path)} was just created. You should fill it with files before proceeding."
        )
        return

    # Create output directory if it does not exist:
    output_path = Path(output_path).resolve()
    create_directory(directory=output_path)

    maps_output_path = Path(maps_path).resolve()
    create_directory(directory=maps_output_path)
    directory_flattener_output_path = Path(output_path, "directory_flattener").resolve()

    # TODO: Recreate the entire pipeline for SC2ReSet and SC2EGSet:
    prepare_sc2reset(
        replaypacks_input_path=replaypacks_input_path,
        output_path=output_path,
        n_processes=n_processes,
        force_overwrite=force_overwrite,
        maps_output_path=maps_output_path,
        directory_flattener_output_path=directory_flattener_output_path,
    )

    sc2egset_replaypack_processor_output_path = Path(
        output_path, "sc2egset_replaypack_processor"
    ).resolve()

    prepare_sc2egset(
        replaypacks_input_path=directory_flattener_output_path,
        output_path=output_path,
        sc2egset_replaypack_processor_output=sc2egset_replaypack_processor_output_path,
        n_processes=n_processes,
        maps_output_path=maps_output_path,
        directory_flattener_output_path=directory_flattener_output_path,
        force_overwrite=force_overwrite,
    )


if __name__ == "__main__":
    freeze_support()  # For Windows support of parallel tqdm
    main()
