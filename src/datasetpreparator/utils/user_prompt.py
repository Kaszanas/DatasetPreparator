from pathlib import Path


def user_prompt_possible_overwrite(filepath: Path, force: bool) -> bool:
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
    if force:
        return True

    # File or directory does not exist, so it can be created,
    # there is no risk of overwriting anything:
    if not filepath.exists():
        return True

    return_map = {
        "y": True,
        "n": False,
    }

    # File or directory exists, so we need to prompt the user to confirm
    # if they want to potentially overwrite something and loose data:
    if filepath.exists():
        print(f"File {filepath} already exists.")
        user_input = input("Do you want to overwrite it? (y/n): ")

        if user_input.lower() in return_map:
            return return_map[user_input.lower()]

        print("Invalid input, please type 'y' or 'n'.")
        return user_prompt_possible_overwrite(filepath, force)

    return False
