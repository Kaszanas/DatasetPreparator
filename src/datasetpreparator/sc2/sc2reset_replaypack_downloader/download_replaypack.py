from pathlib import Path
import requests
import tqdm

from datasetpreparator.sc2.sc2reset_replaypack_downloader.get_md5 import get_md5


def download_replaypack(
    destination_dir: Path,
    replaypack_name: str,
    replaypack_url: str,
    replaypack_md5: str,
) -> str:
    """
    Exposes logic for downloading a single StarCraft II replaypack from an url.

    Parameters
    ----------
    destination_dir : Path
        Specifies the destination directory where the replaypack will be saved.
    replaypack_name : str
        Specifies the name of a replaypack that will\
        be used for the downloaded .zip archive.
    replaypack_url : str
        Specifies the url that is a direct link\
        to the .zip which will be downloaded.

    Returns
    -------
    str
        Returns the filepath to the downloaded .zip archive.

    Examples
    --------
    The use of this method is intended
    to download a .zip replaypack containing StarCraft II games.

    Replaypack download directory should be empty before running
    this function.

    Replaypack name will be used as the name for the downloaded .zip archive.

    Replaypack url should be valid and poiting directly to a .zip archive hosted
    on some server.

    The parameters should be set as in the example below. Please note that this is
    not a working example but rather an illustrative one.

    >>> replaypack_download_dir = "datasets/download_directory"
    >>> replaypack_name = "TournamentName"
    >>> replaypack_url = "some_url"
    >>> replaypack_md5 = "some_md5"
    >>> download_replaypack_object = download_replaypack(
    ...    destination_dir=replaypack_download_dir,
    ...    replaypack_name=replaypack_name,
    ...    replaypack_url=replaypack_url,
    ...    replaypack_md5=replaypack_md5)

    >>> assert isinstance(replaypack_download_dir, str)
    >>> assert isinstance(replaypack_name, str)
    >>> assert isinstance(replaypack_url, str)
    >>> assert isinstance(replaypack_md5, str)
    >>> assert len(os.listdir(replaypack_download_dir)) == 0
    >>> assert existing_files[0].endswith(".zip")
    """

    filename_with_ext = replaypack_name + ".zip"
    download_filepath = Path(destination_dir, filename_with_ext)

    # The file was previously downloaded so return it immediately:
    if download_filepath.exists():
        md5_checksum = get_md5(file=download_filepath)
        if md5_checksum == replaypack_md5:
            return download_filepath

    if not destination_dir.exists():
        destination_dir.mkdir()

    # Send a request and save the response content into a .zip file.
    # The .zip file should be a replaypack:
    response = requests.get(url=replaypack_url)

    with requests.get(url=replaypack_url, stream=True) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))

        tqdm_params = {
            "desc": replaypack_name,
            "total": total,
            "miniters": 1,
            "unit": "B",
            "unit_scale": True,
            "unit_divisor": 1024,
        }

        with download_filepath.open(mode="wb") as output_zip_file:
            with tqdm.tqdm(**tqdm_params) as pb:
                for chunk in response.iter_content(chunk_size=8192):
                    pb.update(len(chunk))
                    output_zip_file.write(chunk)

    return download_filepath
