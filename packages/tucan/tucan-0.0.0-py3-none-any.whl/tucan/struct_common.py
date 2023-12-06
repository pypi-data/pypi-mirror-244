import re
from typing import Tuple, List
from copy import deepcopy
from loguru import logger



def path_clean(path: list, paths_to_clean:Tuple[list]):
    """Remove the unwanted steps of the paths"""
    indexes_to_clean=[]
    for ptc in paths_to_clean:
        if list2pathref(path).startswith(list2pathref(ptc)):
            indexes_to_clean.append(len(ptc)-1)
    new_path=[]
    for i,step in enumerate(path):
        if i not in indexes_to_clean:
            new_path.append(step)
    return new_path


def list2pathref(path: list) -> str:
    """The way we will refer to path here in strings"""
    return ".".join(path)


def pathref_ascendants(pathstr: str) -> List[str]:
    """Return all ascendends of a path"""
    out = []
    path = pathstr.split(".")
    while len(path) > 1:
        path.pop(-1)
        out.append(list2pathref(path))
    return out


def struct_summary_str(main_structs: dict) -> str:
    out = []
    for part, data in main_structs.items():
        out.append(f'\n{data["type"]} {data["name"]}:')
        out.append(
            f'    At path {data["path"]}, lines {data["lines"][0]} -> {data["lines"][-1]}'
        )
        out.append(f'    {data["ssize"]} statements over {data["NLOC"]} lines')
        out.append(f'    Complexity {data["CCN"]}')
        if data["callables"]:
            list_str = "\n       - " + "\n       - ".join(data["callables"])

            out.append(f'    Refers to {len(data["callables"])} callables:{list_str}')
        else:
            out.append(f"    Contains no other callables")
        if data["contains"]:
            list_str = "\n    - " + "\n    - ".join(data["contains"])
            out.append(f'    Contains {len(data["contains"])} elements:{list_str}')
        else:
            out.append(f"    Contains no other structures")

    return "\n".join(out)


def find_words_before_left_parenthesis(code: List[str]) -> List[str]:
    """Find all words before a left parenthesis in a code"""
    # Define a regular expression pattern to find words before a left parenthesis
    pattern = r"(\w+)\("
    # Use re.findall to find all matches in the code
    matches = re.findall(pattern, "\n".join(code))
    return matches


########################################################
# BUFFER of detection


def buffer_item(
    type_: str,
    name: str,
    first_line: str,
    line_idx: int,
    statement_idx: int,
)-> Tuple[str,str,str,int,int]:
    """Forces buffers to keep the same logic across languages"""
    return (
        type_,
        name,
        first_line,
        line_idx,
        statement_idx,
    )


########################################################
# STACK of detection


def stack_item(
    type_: str,
    name: str,
    path: list,
    start_line_idx: int,
    start_statement_idx: int,
    start_line: str,
    end_line_idx: int,
    end_statement_idx: int,
    end_line: str,
)-> Tuple[str,str,list,int,int,str, int,int,str]:
    """Forces stacks to keep the same logic across languages"""

    if path[-1] != name:  # last item of path should be name
        logger.warning(f"Path {str(path)} does not end with {name}")
    return (
        type_,
        name,
        path,
        start_line_idx,
        start_statement_idx,
        start_line,
        end_line_idx,
        end_statement_idx,
        end_line,
    )


def struct_from_stack(stack: list, main_types: list, skip_types:list=None)-> dict:
    """Build a dictionary of all structures"""
    # Build nested structure
    struct = {}
    if skip_types is None:
        skip_types=[]

    path_to_skip=[]
    for (
        type_,
        name,
        path,
        start_line_idx,
        start_statement_idx,
        start_line,
        end_line_idx,
        end_statement_idx,
        end_line,
    ) in stack:
        if type_ in skip_types:
            path_to_skip.append(path)
    
    
    for (
        type_,
        name,
        path,
        start_line_idx,
        start_statement_idx,
        start_line,
        end_line_idx,
        end_statement_idx,
        end_line,
    ) in stack:
        # logger.warning(path)
        # logger.warning(path_to_skip)

        cleaned_path = path_clean(path,path_to_skip)
        # logger.warning(cleaned_path)
        if type_ in main_types:
            struct[list2pathref(cleaned_path)] = {
                "path": cleaned_path,
                "name": name,
                "type": type_,
                "linestart": start_line,
                "lines": [start_line_idx, end_line_idx],
                "statements": [start_statement_idx, end_statement_idx],
                "contains": [],
            }

    return struct


def get_struct_sizes(struct:dict)->dict:
    """Compute the size of strict items (statefull)"""
    struct_aspects = {}
    for part, data in struct.items():
        struct_aspects[part] = {}
        struct_aspects[part]["NLOC"] = data["lines"][-1] - data["lines"][0] + 1
        struct_aspects[part]["ssize"] = data["statements"][-1] - data["statements"][0]
        struct_aspects[part]["callables"] = []
        struct_aspects[part]["CCN"] = []
    return struct_aspects


def struct_augment(struct_in:dict, struct_aspects:dict)-> dict:
    """Complete the description of each struct item
    """
    struct = deepcopy(struct_in)
    # first lines computation
    for _, data in struct.items():
        data["NLOC"] = data["lines"][-1] - data["lines"][0] + 1
        data["ssize"] = data["statements"][-1] - data["statements"][0] + 1

    # add internal links
    for _, data in struct.items():
        path = data["path"]
        if len(data["path"]) > 1:
            parent = path[:-1]
            struct[list2pathref(parent)]["contains"].append(list2pathref(path))

    # add language specific analyses
    for part, data in struct.items():
        # names=[cont.split(".")[-1] for cont in data["contains"]]
        data["callables"] = struct_aspects[part][
            "callables"
        ]  # [cal_ for cal_ in struct_aspects[part]["callables"] if cal_ not in names]
        data["CCN"] = struct_aspects[part]["CCN"]

    # filter callables, RECURSIVELY OF COURSE!
    for pathref in sorted(list(struct.keys()), reverse=True):
        to_remove = struct_aspects[pathref]["callables"].copy()
        # print(pathref)
        # Commented to avoid removing a callables that is in contains
        # to_remove.append(pathref.split(".")[-1])
        for ascd in pathref_ascendants(pathref):
            # print(ascd, to_remove)
            for rm in to_remove:
                # print("TO BE REMOVED")
                # print(struct[ascd]["callables"])
                try:
                    struct[ascd]["callables"].remove(rm)
                except ValueError:
                    logger.warning(f"In path {ascd}, {rm} missing in callables")

    # limit size to actual statements (not sure if it is preferable to remove it)
    # for part, data  in struct.items():
    #     for child in data["contains"]:
    #         data["lsize"] -= struct[child]["lsize"]
    #         data["ssize"] -= struct[child]["ssize"]

    return struct
