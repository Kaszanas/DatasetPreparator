import logging
from pathlib import Path
from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.multiprocess import (
    pre_process_download_maps,
)
from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.replaypack_processor_args import (
    SC2InfoExtractorGoArguments,
)


def sc2infoextractorgo_map_download(
    input_path: Path,
    maps_directory: Path,
) -> None:
    # Pre-process, download all maps:
    logging.info("Downloading all maps...")
    map_download_arguments = SC2InfoExtractorGoArguments.get_download_maps_args(
        processing_input=input_path,
        maps_directory=maps_directory,
    )
    pre_process_download_maps(arguments=map_download_arguments)
