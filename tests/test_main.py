# Standard imports:
import unittest
import sys
import os
import logging

from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()

WORKSPACE_DIRECTORY = os.getenv("TEST_WORKSPACE")

from tests.test_utils import get_workspace_dir  # noqa: E402


# TODO: Fix this file so that the tests can be run with debugger.
def suite():
    suite = unittest.TestSuite()
    start_dir = os.path.join(get_workspace_dir(), "tests")
    suite = unittest.TestLoader().discover(
        start_dir=start_dir,
        pattern="sc2reset_replaypack_downloader_test.py",  # *_test.py
    )
    return suite


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    print(get_workspace_dir())
    my_suite = suite()
    result = unittest.TextTestRunner(verbosity=2).run(my_suite)

    # if result.wasSuccessful():
    #     exit(0)
    # else:
    #     exit(1)
