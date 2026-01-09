import logging
import zipfile
from pathlib import Path
from typing import List


def unpack_chunk(zip_path: Path, filenames: List[str], output_extract_path: Path):
    """
    Helper function for unpacking a chunk of files from an archive.

    Parameters
    ----------
    zip_path : Path
        Specifies the path to the archive file that will be extracted.
    filenames : List[str]
        Specifies a list of the filenames which are within the archive\
        and will be extracted.
    output_extract_path : Path
        Specifies the path to which the files will be extracted to.

    Examples
    --------
    The use of this method is intended to extract a zipfile from the .zip file.

    You should set every parameter, zip_path, filenames and path_to_extract.

    May help you to work with dataset.

    The parameters should be set as in the example below.

    >>> unpack_chunk_object = unpack_chunk(
    ... zip_path="./directory/zip_path",
    ... filenames="./directory/filenames",
    ... path_to_extract="./directory/path_to_extract")

    >>> assert isinstance(zip_path, str)
    >>> assert all(isinstance(filename, str) for filename in filenames)
    >>> assert isinstance(path_to_extract, str)
    """

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        for filename in filenames:
            try:
                zip_file.extract(filename, str(output_extract_path))
            except zipfile.error as e:
                logging.error(
                    f"zipfile error was raised: {e}",
                    exc_info=True,
                )
