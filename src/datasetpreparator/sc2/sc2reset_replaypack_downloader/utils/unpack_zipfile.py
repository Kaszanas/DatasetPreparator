import math
import zipfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import List

import tqdm

from datasetpreparator.sc2.sc2reset_replaypack_downloader.utils.unpack_chunk import (
    unpack_chunk,
)


def unpack_zipfile(
    destination_dir: Path,
    destination_subdir: Path,
    zip_path: Path,
    n_workers: int,
) -> str:
    """
    Helper function that unpacks the content of .zip archive.

    Parameters
    ----------
    destination_dir : Path
        Specifies the destination directory where multiple .zip archives are stored.
    destination_subdir : Path
        Specifies the subdirectory where the content will be extracted.
    zip_path : Path
        Specifies the path to the zip file that will be extracted.
    n_workers : int
        Specifies the number of workers that will be used for unpacking the archive.

    Returns
    -------
    str
        Returns a path to the extracted content.

    Raises
    ------
    Exception
        Raises an exception if the number of workers is less or equal to zero.

    Examples
    --------
    The use of this method is intended to extract a zipfile.

    You should set every parameter, destination, subdir, zip_path and n_workers.

    May help you to work with dataset.

    The parameters should be set as in the example below.

    >>> from pathlib import Path
    >>> unpack_zipfile_object = unpack_zipfile(
    ... destination_dir=Path("./directory/destination_dir"),
    ... subdir=Path("destination_subdir"),
    ... zip_path=Path("./directory/zip_path"),
    ... n_workers=1)

    >>> assert isinstance(destination_dir, Path)
    >>> assert isinstance(subdir, Path)
    >>> assert isinstance(zip_path, Path)
    >>> assert isinstance(n_workers, int)
    >>> assert n_workers >= 1
    """

    if n_workers <= 0:
        raise Exception("Number of workers cannot be equal or less than zero!")

    file_list: List[str] = []
    path_to_extract = Path(destination_dir, destination_subdir)
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        # Checking the existence of the extraction output directory
        # If it doesn't exist it will be created:
        if not path_to_extract.exists():
            path_to_extract.mkdir(parents=True, exist_ok=False)

        file_list = zip_file.namelist()

    chunksize = math.ceil(len(file_list) / n_workers)

    with ProcessPoolExecutor(n_workers) as exe:
        for index in tqdm.tqdm(
            range(0, len(file_list), chunksize),
            desc=f"Extracting {path_to_extract.name}: ",
        ):
            filenames = file_list[index : (index + chunksize)]
            _ = exe.submit(unpack_chunk, zip_path, filenames, path_to_extract)

    return path_to_extract
