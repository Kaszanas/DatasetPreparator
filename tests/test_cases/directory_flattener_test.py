import logging
import unittest
from datasetpreparator.directory_flattener.directory_flattener import (
    multiple_directory_flattener,
)

from tests.test_settings import (
    DELETE_SCRIPT_TEST_DIR,
    DELETE_SCRIPT_TEST_OUTPUT_DIR,
    DELETE_SCRIPT_TEST_INPUT_DIR,
)

from tests.test_utils import (
    create_script_test_input_dir,
    create_script_test_output_dir,
    create_test_text_files,
    create_nested_test_directories,
    dir_test_cleanup,
)


class DirectoryFlattenerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.SCRIPT_NAME = "directory_flattener"
        # Create and get test input and output directories:
        cls.input_path = create_script_test_input_dir(script_name=cls.SCRIPT_NAME)
        cls.output_path = create_script_test_output_dir(script_name=cls.SCRIPT_NAME)
        cls.n_threads = 1
        cls.file_extension = ".SC2Replay"

        # Create nested directory structure mimicking how real replaypacks look like:
        cls.n_dirs = 2
        nested_dirs = create_nested_test_directories(
            input_path=cls.input_path, n_dirs=cls.n_dirs
        )
        cls.n_nested_files = 4
        cls.n_out_of_distribution_files = 1
        for directory in nested_dirs:
            # Create multiple test files with the selected extension:
            create_test_text_files(
                input_path=directory,
                n_files=cls.n_nested_files,
                filenames=[],
                extension=cls.file_extension,
            )
            # Create additional files that should not be present in the output:
            create_test_text_files(
                input_path=directory,
                n_files=cls.n_out_of_distribution_files,
                filenames=[],
                extension=".txt",
            )

        # TODO: There could also be empty input directories to test or directorie
        # with all files that are not of the selected extension.
        # In that case to get a proper assertion each of the input directories should
        # be remembered and the number of files in the output should be known
        # before the assertions are made.
        # cls.list_of_input_dirs = list(cls.input_path.iterdir())

    def test_directory_flattener(self) -> None:
        ok, list_of_output_dirs = multiple_directory_flattener(
            input_path=self.input_path,
            output_path=self.output_path,
            file_extension=self.file_extension,
            n_threads=self.n_threads,
            force_overwrite=True,
        )

        # Check if the input data was correct for processing:
        self.assertTrue(ok)

        # Check the number of output directories:
        self.assertEqual(self.n_dirs, len(list_of_output_dirs))
        logging.info(f"Number of output directories: {len(list_of_output_dirs)}")
        logging.info(f"Output directories: {list_of_output_dirs}")

        for output_dir in list_of_output_dirs:
            logging.info(f"Checking output directory: {output_dir}")
            # Assert the final directory have the same number of
            # files with the selected extension.
            out_files = list(output_dir.glob(f"*{self.file_extension}"))

            logging.info(
                f"Number of files with extension {self.file_extension}: {len(out_files)}"
            )
            logging.info(f"{self.n_nested_files=}")

            # Check only the number of files with the selected extension:
            self.assertEqual(self.n_nested_files, len(out_files))

            # Check with the processed mapping file created:
            self.assertEqual(self.n_nested_files + 1, len(list(output_dir.iterdir())))

            # Assert the final flattened directory to
            # have one .json file with the mapping
            json_files = list(output_dir.glob("*.json"))
            self.assertEqual(1, len(json_files))

            # There should be no nested directories in the output:
            for file in output_dir.iterdir():
                self.assertFalse(file.is_dir())

            # TODO: Check the contents of the json mapping?

    @classmethod
    def tearDownClass(cls) -> None:
        dir_test_cleanup(
            script_name=cls.SCRIPT_NAME,
            delete_script_test_dir_bool=DELETE_SCRIPT_TEST_DIR,
            delete_script_test_input_bool=DELETE_SCRIPT_TEST_INPUT_DIR,
            delete_script_test_output_bool=DELETE_SCRIPT_TEST_OUTPUT_DIR,
        )
