from pathlib import Path
import unittest

from datasetpreparator.sc2.sc2reset_replaypack_downloader.utils.get_md5 import (
    get_md5,
)

from datasetpreparator.sc2.sc2reset_replaypack_downloader.sc2reset_replaypack_downloader import (
    sc2reset_replaypack_downloader,
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


class SC2ReSetDownloaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.SCRIPT_NAME = "sc2reset_replaypack_downloader"

        # Create and get test input and output directories:
        cls.input_path = create_script_test_input_dir(script_name=cls.SCRIPT_NAME)
        cls.output_path = create_script_test_output_dir(script_name=cls.SCRIPT_NAME)

        cls.test_replaypack_list = [
            (
                "2016_IEM_10_Taipei",
                "https://zenodo.org/record/5575797/files/2016_IEM_10_Taipei.zip?download=1",
                "f9150577d08216ce5ec5de954d8d536c",
            ),
        ]

    def test_sc2reset_replaypack_downloader(self):
        replaypack_name, replaypack_url, archive_md5 = self.test_replaypack_list[0]

        sc2reset_replaypack_downloader(
            download_path=self.input_path,
            unpack_path=self.output_path,
            n_workers=1,
            replaypack_list=self.test_replaypack_list,
        )

        # Check if the replaypack was downloaded:
        archive_name = f"{replaypack_name}.zip"
        self.assertTrue(
            Path(self.input_path, archive_name).exists(),
            msg="The replaypack was not downloaded.",
        )
        # Check the md5 of the downloaded archive:
        self.assertEqual(
            archive_md5,
            get_md5(Path(self.input_path, archive_name)),
            msg="The md5 of the downloaded archive is not correct.",
        )
        # Check if the replaypack was unpacked:
        self.assertTrue(
            Path(self.output_path, replaypack_name).exists(),
            msg="The replaypack was not unpacked.",
        )
        # Check if the replaypack was unpacked correctly:
        self.assertNotEqual(
            0, len(list(Path(self.output_path, replaypack_name).glob("*.SC2Replay")))
        )

    @classmethod
    def tearDownClass(cls) -> None:
        dir_test_cleanup(
            script_name=cls.SCRIPT_NAME,
            delete_script_test_dir_bool=DELETE_SCRIPT_TEST_DIR,
            delete_script_test_input_bool=DELETE_SCRIPT_TEST_INPUT_DIR,
            delete_script_test_output_bool=DELETE_SCRIPT_TEST_OUTPUT_DIR,
        )
