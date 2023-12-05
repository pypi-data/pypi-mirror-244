"""make input and output file path legal"""


import os


def _check_path(path: str, is_folder: bool = False):
    """Return a legal path, ensuring it exists."""
    path = path.replace("\\", "/")
    if is_folder and path[-1] != "/":
        path += "/"

    return path


def check_infile(file_path: str):
    """return legal flie path."""
    file_path = _check_path(file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"cannot find file: {file_path}")
    return file_path


def check_inpath(folder_path: str):
    """return legal folder path, end with '/'."""
    folder_path = _check_path(folder_path, is_folder=True)
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"cannot find folder: {folder_path}")
    return folder_path


def check_outpath(folder_path: str, overwriting: bool = True, creating: bool = True):
    """Create a folder if it does not exist. Return legal folder path."""
    folder_path = _check_path(folder_path, is_folder=True)
    if os.path.exists(folder_path) and not overwriting:
        raise FileExistsError(f"file existed: {folder_path}")
    elif not os.path.exists(folder_path):
        if creating:
            os.makedirs(folder_path)
        else:
            raise FileNotFoundError(f"cannot find folder: {folder_path}")
    return folder_path


def check_outfile(file_path: str, overwriting: bool = True, creating: bool = True):
    """Create a folder if it does not exist. Return legal file path."""
    file_path = _check_path(file_path)
    folder_path = os.path.dirname(file_path)
    if os.path.exists(file_path) and not overwriting:
        raise FileExistsError(f"file existed: {file_path}")
    check_outpath(folder_path, creating=creating)
    return file_path


def check_inany(inpath: str):
    """return legal input path."""
    if os.path.isdir(inpath):
        return _check_path(inpath, is_folder=True)
    elif os.path.isfile(inpath):
        return _check_path(inpath)
    else:
        raise FileNotFoundError(f"cannot find file or folder: {inpath}")


__all__ = [
    "check_infile",
    "check_inpath",
    "check_outpath",
    "check_outfile",
    "check_inany",
]
