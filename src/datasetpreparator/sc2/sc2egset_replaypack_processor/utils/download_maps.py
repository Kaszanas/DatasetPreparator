import logging
from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.multiprocess import (
    pre_process_download_maps,
)
from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.replaypack_processor_args import (
    ReplaypackProcessorArguments,
    SC2InfoExtractorGoArguments,
)


def sc2info_extractor_go_map_download(arguments: ReplaypackProcessorArguments):
    # Pre-process, download all maps:
    logging.info("Downloading all maps...")
    map_download_arguments = SC2InfoExtractorGoArguments.get_download_maps_args(
        processing_input=arguments.input_path, output=arguments.output_path
    )
    pre_process_download_maps(arguments=map_download_arguments)
