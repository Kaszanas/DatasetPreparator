import unittest

from datasetpreparator.sc2.sc2egset_replaypack_processor.sc2egset_replaypack_processor import (
    sc2egset_replaypack_processor,
)

from datasetpreparator.sc2.sc2egset_replaypack_processor.utils.replaypack_processor_args import (
    ReplaypackProcessorArguments,
)
from tests.test_settings import (
    DELETE_SCRIPT_TEST_DIR,
    DELETE_SCRIPT_TEST_OUTPUT_DIR,
    DELETE_SCRIPT_TEST_INPUT_DIR,
)


from tests.test_utils import (
    create_script_test_input_dir,
    create_script_test_output_dir,
    dir_test_cleanup,
)


# TODO: sc2_replaypack_processor by default uses another piece of software for parsing SC2 replays.
# So it will be downloading the data from another repository.


class SC2ReplaypackProcessorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.SCRIPT_NAME = "sc2egset_replaypack_processor"
        # Create and get test input and output directories:
        cls.input_path = create_script_test_input_dir(script_name=cls.SCRIPT_NAME)
        cls.output_path = create_script_test_output_dir(script_name=cls.SCRIPT_NAME)
        cls.maps_directory = cls.input_path / "maps"

        # TODO: Verify that SC2InfoExtractorGo is available in path.
        # If not available download from GitHub release page.
        # It is probably best for this test to be ran from the docker container.

        # TODO: Set up a test directory with at least
        # two replaypacks with at least one SC2Replay file within.

    def test_sc2_replaypack_processor(self):
        # REVIEW: Unfortunately this script depends on SC2InfoExtractorGo. This means that
        # the dockerfile dev environment should be built with access to this executable.
        # There should be a way to exclude this test somehow.
        # This could be done either with another boolean set in the environment variables,
        # Maybe a pytest marker to skip this test?
        # Should this even be tested given that the SC2InfoExtractorGo will have its own tests?
        # This script is only providing a multiprocessing wrapper for the SC2InfoExtractorGo.

        arguments = ReplaypackProcessorArguments(
            input_path=self.input_path,
            output_path=self.output_path,
            maps_directory=self.maps_directory,
            n_processes=1,
        )

        sc2egset_replaypack_processor(arguments=arguments, force_overwrite=True)
        # TODO: Check if output contains the same directories as for input.
        # TODO: Check if outputs contain extracted JSON files with valid fields.

    @classmethod
    def tearDownClass(cls) -> None:
        dir_test_cleanup(
            script_name=cls.SCRIPT_NAME,
            delete_script_test_dir_bool=DELETE_SCRIPT_TEST_DIR,
            delete_script_test_input_bool=DELETE_SCRIPT_TEST_INPUT_DIR,
            delete_script_test_output_bool=DELETE_SCRIPT_TEST_OUTPUT_DIR,
        )
