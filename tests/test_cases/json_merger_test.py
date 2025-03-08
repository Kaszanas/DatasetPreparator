import unittest
import json

from datasetpreparator.json_merger.json_merger import json_merger

from tests.test_settings import (
    DELETE_SCRIPT_TEST_DIR,
    DELETE_SCRIPT_TEST_OUTPUT_DIR,
    DELETE_SCRIPT_TEST_INPUT_DIR,
)


from tests.test_utils import (
    create_script_test_input_dir,
    create_script_test_output_dir,
    create_test_json_files,
    dir_test_cleanup,
)


class JSONMergerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.SCRIPT_NAME = "json_merger"
        # Create and get test input and output directories:
        cls.input_path = create_script_test_input_dir(script_name=cls.SCRIPT_NAME)
        cls.output_path = create_script_test_output_dir(script_name=cls.SCRIPT_NAME)
        cls.output_filepath = cls.output_path / "merged.json"

        cls.test_key = "test_key"
        cls.test_key_other = "test_key_other"
        cls.test_key_content = "test_key_data"

        # Create two json files with some overlapping keys and values:
        json_file_paths = create_test_json_files(
            input_path=cls.input_path,
            test_key=cls.test_key,
            test_key_other=cls.test_key_other,
            test_key_content=cls.test_key_content,
        )

        cls.path_to_json_one = json_file_paths[0]
        cls.path_to_json_two = json_file_paths[1]

    def test_json_merger(self):
        merged_json_filepath = json_merger(
            path_to_json_one=self.path_to_json_one,
            path_to_json_two=self.path_to_json_two,
            output_filepath=self.output_filepath,
            force_overwrite=True,
        )

        # Read merged file:
        merged_json_file = merged_json_filepath.open()
        merged_json_content = json.load(merged_json_file)
        merged_json_file.close()

        # Test key should be in the merged data:
        self.assertIn(member=self.test_key, container=merged_json_content)
        self.assertIn(member=self.test_key_other, container=merged_json_content)

    @classmethod
    def tearDownClass(cls) -> None:
        dir_test_cleanup(
            script_name=cls.SCRIPT_NAME,
            delete_script_test_dir_bool=DELETE_SCRIPT_TEST_DIR,
            delete_script_test_input_bool=DELETE_SCRIPT_TEST_INPUT_DIR,
            delete_script_test_output_bool=DELETE_SCRIPT_TEST_OUTPUT_DIR,
        )
