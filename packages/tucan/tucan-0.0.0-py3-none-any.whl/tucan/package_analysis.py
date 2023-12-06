"""Module that aims to analyze a whole package based 
on the other unitary function of the package"""


# Join the databse


from pathlib import Path
from loguru import logger
from tucan.unformat_main import unformat_main
from tucan.struct_main import struct_main


def _rec_travel_through_package(path: str, optionnal_paths: list = None) -> list:
    """
    List all paths from a folder and its subfolders recursively.

    Args:
        path (str): Main folder path
        optionnals_paths (list, optional): . Defaults to [].

    Returns:
        list: _description_
    """
    if not optionnal_paths:
        optionnal_paths = []

    current_paths_list = [path, *optionnal_paths]

    paths_ = []
    for current_path in current_paths_list:
        current_path = Path(current_path)
        for element in current_path.iterdir():
            if element.is_dir():
                paths_.extend(_rec_travel_through_package(element.as_posix()))
            else:
                if element.as_posix() not in paths_:
                    paths_.append(element.as_posix())
    return paths_


def clean_extensions_in_paths(paths_list: list) -> list:
    """_summary_

    Args:
        paths_list (list): _description_

    Returns:
        list: _description_
    """
    clean_paths = []
    for path in paths_list:
        if path.split("/")[-1].startswith("."):
            pass
        elif path.endswith((".py", ".f90", ".f", ".F", ".f77")):
            clean_paths.append(path)

    return [
        *set(clean_paths),
    ]


def run_unformat(clean_paths: list) -> dict:
    """_summary_

    Args:
        clean_paths (list): _description_

    Returns:
        dict: _description_
    """
    statements = {}
    for file in clean_paths:
        statements[file] = unformat_main(file).to_nob()

        nbr_of_stmt = 0
        if statements[file]:
            nbr_of_stmt = len(statements[file])
        logger.info(f"Found {nbr_of_stmt} statements for {file}")

    return statements


def run_struct(clean_paths: list) -> dict:
    """_summary_

    Args:
        clean_paths (list): _description_

    Returns:
        dict: _description_
    """
    full_struct = {}
    files = []

    for path_ in clean_paths:
        if not Path(path_).is_dir():
            files.append(path_)

    files = clean_extensions_in_paths(files)
    for file in files:
        full_struct[file] = struct_main(file)
        total_stmts = 0
        for _, data in full_struct[file].items():
            total_stmts += data["ssize"]
        logger.info(f"Found {total_stmts} statements for {file}")

    return full_struct
