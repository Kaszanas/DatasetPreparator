import logging
from pathlib import Path

from datasetpreparator.utils.user_prompt import user_prompt_overwrite_ok
from tqdm import tqdm
import shutil


def move_files(
    input_path: Path,
    output_path: Path,
    force_overwrite: bool,
    extension: str = ".zip",
) -> None:
    # Make sure that the output directory exists, and potentially overwrite
    # its contents if the user agrees:
    if user_prompt_overwrite_ok(path=output_path, force_overwrite=force_overwrite):
        output_path.mkdir(exist_ok=True)

    logging.info(
        f"Searching for files with extension {extension} in {str(input_path)}..."
    )

    files = list(input_path.glob(f"*{extension}"))

    logging.info(f"Copying {len(files)} files to {str(output_path)}...")

    for file in tqdm(
        files,
        desc="Copying files",
        unit="file",
    ):
        shutil.move(file, output_path / file.name)
