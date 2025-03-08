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
    n_processes: int,
) -> None:
    """
    Downloads all maps contained in the .SC2Replay files in the input directory.
    Maps are placed in the maps_directory.

    Parameters
    ----------
    input_path : Path
        Specifies the input directory where the .SC2Replay files are held.
        SC2InfoExtractorGo will recursively search for .SC2Replay files in this directory.
    maps_directory : Path
        Specifies the directory where the maps are stored and will be downloaded to.
    n_processes : int
        Specifies the number of processes to use for downloading the maps.
    """

    # Pre-process, download all maps:
    logging.info("Downloading all maps...")
    map_download_arguments = SC2InfoExtractorGoArguments.get_download_maps_args(
        processing_input=input_path,
        maps_directory=maps_directory,
        n_processes=n_processes,
    )
    pre_process_download_maps(arguments=map_download_arguments)
