"""Global function to handle the struct analysis of various languages"""
from loguru import logger

from tucan.unformat_py import unformat_py
from tucan.unformat_ftn import unformat_ftn
from tucan.struct_py import extract_struct_py
from tucan.struct_ftn import extract_struct_ftn


def struct_main(filename: str) -> dict:
    """
    Extract structure of a fortran or python file.
    - Find the nested structures of a code
    - Find the callables in each structure
    - Evaluate sizes, CCN

    Args:
        filename (str): __description__

    Returns:
        dict:

    """
    logger.info(f"Struct analysis on {filename}")
    with open(filename, "r") as fin:
        code = fin.read().splitlines()

    code = [line.lower() for line in code]  # Lower case for all

    if filename.lower().endswith(".py"):
        logger.debug(f"Python code detected ...")
        statements = unformat_py(code)
        struct_ = extract_struct_py(statements)
    elif filename.lower().endswith((".f", ".F", ".f77", ".f90")):
        logger.debug(f"Fortran code detected ...")
        statements = unformat_ftn(code)
        struct_ = extract_struct_ftn(statements)
    else:
        ext = filename.lower().split(".")[-1]
        logger.error(f"Extension {ext} not supported, exiting ...")
        struct_ = {}
        return

    return struct_
