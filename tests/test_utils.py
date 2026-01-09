import json
import logging
import shutil
from pathlib import Path
from typing import List


from tests.test_settings import TEST_DIR_NAME, TEST_FILES_NAME, TEST_WORKSPACE


def get_workspace_dir() -> Path:
    """
    Getting path to the workspace where tests are run.
    This function is future proof for testing outsite of local environments.

    Returns
    -------
    Path
        Returns the path to the workspace.
    """

    logging.info("Entered get_workspace_dir(), attempting to set workspace_dir.")

    workspace_dir = Path(TEST_WORKSPACE).resolve()
    logging.info(f"Successfully set workspace_dir = {workspace_dir}")
    return workspace_dir


def get_script_test_dir(script_name: str) -> Path:
    """
    Getting the path to a specific script test directory.

    Parameters
    ----------
    script_name : str
        Script name for which the test dir will be retrieved.

    Returns
    -------
    Path
        Returns the path to the script test directory.
    """

    workspace_dir = get_workspace_dir()

    test_dir = Path(
        workspace_dir, f"{TEST_DIR_NAME}/{TEST_FILES_NAME}/{script_name}"
    ).resolve()

    if test_dir.exists():
        return test_dir

    return test_dir


def delete_script_test_dir(script_name: str) -> None:
    """
    Deletes the test directory for a specified script.

    Parameters
    ----------
    script_name : str
        Script name for which the test directory will be deleted.
    """

    script_test_dir = get_script_test_dir(script_name=script_name)

    if not script_test_dir.exists():
        logging.info(f"Did not detect {script_test_dir.as_posix()} to exist")
        return

    shutil.rmtree(script_test_dir.as_posix())


def create_script_test_input_dir(script_name: str) -> Path:
    """
    Creates test input directory for tests.

    Parameters
    ----------
    script_name : str
        Script name for which the test output dir will be created.

    Returns
    -------
    Path
        Returns path to the test input directory.
    """

    workspace_dir = get_workspace_dir()

    input_dir = Path(
        workspace_dir, f"{TEST_DIR_NAME}/{TEST_FILES_NAME}/{script_name}/input/"
    ).resolve()

    if not input_dir.exists():
        input_dir.mkdir(parents=True)

    return input_dir


# TODO: Additionally, there should be a script that downloads test input files if they are not already available:
def get_script_test_input_dir(script_name: str) -> Path:
    """
    Getting path to the files required for testing.

    Parameters
    ----------
    script_name : str
        Script name for which the test input dir will be retrieved.

    Returns
    -------
    Path
        Returns an absolute path to the test input directory.
    """
    workspace_dir = get_workspace_dir()
    logging.info(f"Successfully set workspace_dir = {workspace_dir}")

    input_dir = Path(
        workspace_dir, f"{TEST_DIR_NAME}/{TEST_FILES_NAME}/{script_name}/input"
    ).resolve()
    logging.info(f"Successfully set input_dir = {input_dir}, returning.")

    return input_dir


def delete_script_test_input(script_name: str) -> None:
    """
    Deletes output of tests.

    Parameters
    ----------
    script_name : str
        Script name for which the directory will be cleaned.
    """

    test_dir = get_script_test_input_dir(script_name=script_name)
    logging.info(f"Successfully set {test_dir.as_posix()=}")

    if not test_dir.exists():
        logging.info("Did not detect test_output to exist, exiting function")
        return

    logging.info(
        f"Detected that test_output exists, \
            performing removal by calling shutil.rmtree({test_dir})"
    )
    shutil.rmtree(test_dir.as_posix())


def create_script_test_output_dir(script_name: str) -> Path:
    """
    Creates test output directories for tests.

    Parameters
    ----------
    script_name : str
        Script name for which the test oput dir will be created.

    Returns
    -------
    Path
        Returns path to the test output directory.
    """

    workspace_dir = get_workspace_dir()
    logging.info(f"Successfully set workspace_dir = {workspace_dir}")

    test_output_path = Path(
        workspace_dir, f"{TEST_DIR_NAME}/{TEST_FILES_NAME}/{script_name}/output"
    ).resolve()

    if not test_output_path.exists():
        logging.info(
            f"Detected that output_path does not exist, \
            calling os.mkdir({test_output_path})"
        )
        test_output_path.mkdir(parents=True)

    return test_output_path


def get_script_test_output_dir(script_name: str) -> Path:
    """
    Getting the path to the test output directory
    and to the thumbnail output directory.

    Parameters
    ----------
    script_name : str
        Script name for which the test input dir will be retrieved.

    Returns
    -------
    Path
        Paths to the test output directory.
    """

    logging.info(
        "Entered get_output_dir(), calling workspace_dir = get_workspace_dir()"
    )
    workspace_dir = get_workspace_dir()
    logging.info(
        f"Successfully set workspace_dir = {workspace_dir}, returning output_dir = "
    )
    test_output_dir = Path(
        workspace_dir, f"{TEST_DIR_NAME}/{TEST_FILES_NAME}/{script_name}/output"
    ).resolve()

    return test_output_dir


def delete_script_test_output(script_name: str) -> None:
    """
    Deletes output of tests.

    Parameters
    ----------
    script_name : str
        Script name for which the directory will be cleaned.
    """

    test_dir = get_script_test_output_dir(script_name=script_name)
    logging.info(f"Successfully set {test_dir.as_posix()=}")

    if not test_dir.exists():
        logging.info("Did not detect test_output to exist, exiting function")
        return

    logging.info(
        f"Detected that test_output exists, \
            performing removal by calling shutil.rmtree({test_dir})"
    )
    shutil.rmtree(test_dir.as_posix())


def create_nested_test_directories(input_path: Path, n_dirs: int) -> List[Path]:
    """
    Created multiple nested directories for testing.

    Parameters
    ----------
    input_path : Path
        Input path in which the nested directories will be created.
    n_dirs : int
        Number of directories that will be created

    Returns
    -------
    List[Path]
        Returns the list of created directories.
    """
    created_nested_dirs = []

    for i in range(n_dirs):
        nested_dir = Path(input_path, f"dir_{i}")

        if not nested_dir.exists():
            nested_dir.mkdir()
            created_nested_dirs.append(nested_dir)

    return created_nested_dirs


def create_test_text_files(
    input_path: Path,
    n_files: int,
    filenames: List[str],
    extension: str = ".SC2Replay",
):
    """
    Creates example text files with a specified extension.

    Parameters
    ----------
    input_path : Path
        Specifies the input path where the test files will be created.
    n_files : int
        Number of files which will be created. If a list of filenames is passed
        this argument is not used.
    filenames : List[str]
        List of filenames to use.
    extension : str
        Extension which will be used to create the test files.
    """

    # Filenames were not passed so we can create n_files:
    if not filenames:
        for i in range(n_files):
            example_file = Path(input_path, f"example_file_{i}").with_suffix(extension)
            create_file(filepath=example_file)

    # User passed the filenames so we create them from the list
    for filename in filenames:
        filepath = Path(input_path, filename).with_suffix(extension)
        create_file(filepath=filepath)


def create_file(filepath: Path) -> Path:
    if not filepath.exists():
        with filepath.open(mode="w", encoding="utf-8") as ef:
            ef.write("Example Content")

    return filepath


def create_test_json_files(
    input_path: Path,
    test_key: str = "test_key",
    test_key_other: str = "test_key_other",
    test_key_content: str = "test_key_data",
) -> List[Path]:
    """
    Creates JSON files for test purposes.

    Parameters
    ----------
    input_path : Path
        Path at which the JSON files will be created.
    test_key : str
        Additional key which will be used to verify merging logic.
    test_key_content : str
        Content for the additional test key.

    Returns
    -------
    List[Path]
        Returns a list of paths to tje JSON files that were created.
    """

    json_files = []
    for i in range(2):
        json_path = Path(input_path, f"json_{i}").with_suffix(".json")

        data = {f"key_{i}": f"{i}" for i in range(10)}
        # One of the keys will be different to verify if the merging logic works:
        if i == 1:
            data[f"{test_key}"] = test_key_content
        data[f"{test_key_other}"] = test_key_content

        if not json_path.exists():
            with json_path.open(mode="w", encoding="utf-8") as json_f:
                json.dump(data, json_f)

            json_files.append(json_path)

    return json_files


def dir_test_cleanup(
    script_name: str,
    delete_script_test_dir_bool: bool,
    delete_script_test_input_bool: bool,
    delete_script_test_output_bool: bool,
) -> None:
    # Removes entire script test directory and returns as it
    # contains both input and output directories:
    if delete_script_test_dir_bool:
        logging.info(f"{delete_script_test_dir_bool=}, deleting script test dir.")
        delete_script_test_dir(script_name=script_name)
        return

    if delete_script_test_input_bool:
        logging.info(f"{delete_script_test_input_bool=}, deleting script test input.")
        delete_script_test_input(script_name=script_name)

    if delete_script_test_output_bool:
        logging.info(f"{delete_script_test_output_bool=}, deleting script test output.")
        delete_script_test_output(script_name=script_name)
