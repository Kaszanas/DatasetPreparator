from pathlib import Path
import logging


def user_prompt_overwrite_ok(path: Path, force_overwrite: bool) -> bool:
    """
    Prompts the user to confirm if they want to potentially overwrite a file or directory if
    it already exists.

    Parameters
    ----------
    filepath : Path
        Filepath to the file or directory that might be overwritten if it already exists.
    force : bool
        Flag that specifies if the user wants to overwrite the file or directory without
        being prompted.

    Returns
    -------
    bool
        True if the file is permitted to be overwritten, False otherwise.
    """

    # User passed the force flag, so the files or directories can be overwritten:
    if force_overwrite:
        return True

    # File or directory does not exist, so it can be created,
    # there is no risk of overwriting anything:
    if not path.exists():
        logging.debug(f"Path {str(path.resolve())} does not exist. Safe to create.")
        return True

    # Directory is empty, so it can be overwritten without any risk:
    if path.is_dir() and len(list(path.iterdir())) == 0:
        logging.debug(f"Directory {str(path.resolve())} is empty. Safe to overwrite.")
        return True

    return_map = {
        "y": True,
        "n": False,
    }

    # File or directory exists, so we need to prompt the user to confirm
    # if they want to potentially overwrite something and loose data:
    print(f"File {path} already exists.")
    user_input = input("Do you want to overwrite it? (y/n): ")

    if user_input.lower() in return_map:
        logging.debug(
            f"User input: {user_input.lower()}, returning: {return_map[user_input.lower()]}"
        )
        return return_map[user_input.lower()]

    logging.debug(
        f"Invalid input provided: {user_input.lower()}, calling the function recursively."
    )
    print("Invalid input, please type 'y' or 'n'.")
    return user_prompt_overwrite_ok(path, force_overwrite)
