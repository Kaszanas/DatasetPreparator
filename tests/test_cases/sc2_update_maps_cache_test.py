import os
from pathlib import Path
import unittest

from datasetpreparator.sc2.sc2_update_maps_cache.sc2_update_maps_cache import (
    BnetPathNotFound,
    place_dependency_in_cache,
    get_bnet_path,
)
from tests.test_utils import (
    create_script_test_input_dir,
    create_script_test_output_dir,
    create_test_text_files,
    delete_script_test_dir,
)

# NOTE: This test can only be ran from within Docker!
# NOTE: Otherwise it is not guaranteed that an existing StarCraft 2 installation
# NOTE: won't mess with it due to the automated way of searching for the Battle.net
# NOTE: base directory.


class SC2UpdateMapsCacheTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.BNET_SC2_ENV_KEY = "SC2PATH"

        # Input dir requires that there are some maps placed in it:
        cls.SCRIPT_NAME = "sc2_update_maps_cache"
        cls.test_input_dir = create_script_test_input_dir(script_name=cls.SCRIPT_NAME)
        cls.example_map_filenames = [
            "6389a20d0d79432fc788a1fa9524ed0d7cf485f0484001400b674081e2c09ca1",
            "41538911b9079d111e33562d081ab60526b3e80e9a3dca2f1fe667a88b2e4696",
            "0d4787c6e9256c440ea7bca55ee5f81e2da706c6974c4184eef3368b933067f2",
            "02d4abb44229949dbb02dc5ac2a125b3e89bf0a23c50d61f2f3e59bdbef4e1ae",
        ]
        # Create example .s2ma files:
        create_test_text_files(
            input_path=cls.test_input_dir,
            filenames=cls.example_map_filenames,
            extension=".s2ma",
        )

        # Output dir for the test will be used as the bnet_base dir to which the
        # this base dir should contain a /Cache directory which will be filled in
        # with the sample data:
        cls.test_output_dir = create_script_test_output_dir(script_name=cls.SCRIPT_NAME)

        # Variables for tests that only acquire the Battle.net path:
        cls.SCRIPT_NAME_GET_BNET_MISSING_BNET = "sc2_update_maps_cache/get_bnet"
        cls.SCRIPT_NAME_GET_BNET_MISSING_CACHE = (
            "sc2_update_maps_cache/get_bnet/Battle.net"
        )
        cls.get_bnet_test_output_dir = create_script_test_output_dir(
            script_name=cls.SCRIPT_NAME_GET_BNET
        )

        cls.SCRIPT_NAME_GET_BNET_CORRECT = (
            "sc2_update_maps_cache/get_bnet/Battle.net/Cache"
        )

    # REVIEW: What more could be added here to see if the maps were copied correctly?
    # REVIEW: How deep to check the directory structure and proper copying?
    def test_copying_maps_correct(self):
        # List all s2ma files:
        map_files = list(self.test_input_dir.rglob("*.s2ma"))

        # Exact number of files which were created should be listed:
        self.assertEqual(len(map_files), len(self.example_map_filenames))

        for map_filepath in map_files:
            dependency_in_cache = place_dependency_in_cache(
                bnet_base_dir=self.test_output_dir,
                map_filepath=map_filepath,
            )
            self.assertTrue(dependency_in_cache.exists())
            # TODO: Check the directory structure:
            # TODO: Add more checks:

        # Recursive glob for the copied example maps:
        files_in_output = list(self.test_output_dir.rglob("*.s2ma"))
        self.assertEqual(len(self.example_map_filenames), len(files_in_output))

    # TODO: In theory if the map name will be too short the indexing for creating the
    # directory structure will fail and cause an IndexError.
    # I don't know if there are more ways to break this, but by default when downloading the
    # maps from the Battle.net servers they come with a proper filenames as given
    # by their hash.
    def test_copying_maps_incorrect(self):
        # dependency_in_cache = place_dependency_in_cache(
        #     bnet_base_dir="", map_filepath=""
        # )
        pass

    def test_get_bnet_path_user_missing_cache_dir(self):
        # By default any directory that is named "Battle.net" will be fine here.
        # The assumption is that the user can pass the right directory to the program.
        # Otherwise the automatically inferred path should be correct.
        # There is a hidden test abstracted out in the function below:
        with self.assertRaises(BnetPathNotFound):
            bnet_path = get_bnet_path(
                bnet_base_dir=self.SCRIPT_NAME_GET_BNET_MISSING_CACHE
            )
            self.assertIsInstance(bnet_path, Path)

    def test_get_bnet_path_user_correct(self):
        create_script_test_input_dir(script_name=self.SCRIPT_NAME_GET_BNET_CORRECT)

        bnet_path = get_bnet_path(bnet_base_dir=self.SCRIPT_NAME_GET_BNET_MISSING_CACHE)
        self.assertIsInstance(bnet_path, Path)

        delete_script_test_dir(script_name=self.SCRIPT_NAME_GET_BNET_CORRECT)

    def test_get_bnet_path_user_incorrect(self):
        # Incorrect example the user passed the directory which does not end with "Battle.net"
        with self.assertRaises(BnetPathNotFound):
            _ = get_bnet_path(bnet_base_dir=self.SCRIPT_NAME_GET_BNET_MISSING_BNET)

    def test_get_bnet_path_env_correct(self):
        # Setting the environment variable to be the correct path:
        os.environ[self.BNET_SC2_ENV_KEY] = self.test_output_dir
        bnet_path = get_bnet_path()

        self.assertIsInstance(bnet_path, Path)

        # Removing the key from the environment so that subsequent test runs
        # are not interfered with.
        os.environ.pop(self.BNET_SC2_ENV_KEY)

    def test_get_bnet_path_env_incorrect(self):
        # Setting the environment variable to be the incorrect path:
        os.environ[self.BNET_SC2_ENV_KEY] = ""

        with self.assertRaises(BnetPathNotFound):
            _ = get_bnet_path()

        # Removing the key from the environment so that subsequent test runs
        # are not interfered with.
        os.environ.pop(self.BNET_SC2_ENV_KEY)

    def test_get_bnet_path_incorrect(self):
        # When no directory is passed the program attempts to check the default
        # path for the StarCraft 2 existence. But SC2 is not installed in the
        # test environment so there is no way to get a correct Battle.net path.
        with self.assertRaises(BnetPathNotFound):
            _ = get_bnet_path()
