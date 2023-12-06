import re
from typing import Tuple, List
from loguru import logger
from tucan.unformat_common import Statements
from tucan.struct_common import (
    find_words_before_left_parenthesis,
    buffer_item,
    stack_item,
    struct_from_stack,
    struct_augment,
)


PARTS = [
    "program ",
    "module ",
    "function ",
    "subroutine ",
    "interface ",
    "pure ",
    "abstract ",
    "recursive ",
]


NESTS = ["if ", "select ", "do ", "where ", "type ", "type,", "associate ", "block "]

INTRINSICS = [
    "abs",
    "aimag",
    "aint",
    "all",
    "allocated",
    "anint",
    "any",
    "asin",
    "atan",
    "atan2",
    "bit_size",
    "btest",
    "ceiling",
    "char",
    "character",
    "cmplx",
    "conjg",
    "cos",
    "cosh",
    "count",
    "cshift",
    "date_and_time",
    "digits",
    "dim",
    "dot_product",
    "dprod",
    "dshiftl",
    "dshiftr",
    "eor",
    "epsilon",
    "erf",
    "erfc",
    "etime",
    "exp",
    "exponent",
    "extends_type_of",
    "floor",
    "fraction",
    "gamma",
    "huge",
    "iachar",
    "iall",
    "iand",
    "iany",
    "ibclr",
    "ibits",
    "ibset",
    "ichar",
    "idate",
    "idim",
    "idint",
    "idnint",
    "ieor",
    "ierrno",
    "ifix",
    "index",
    "int",
    "integer",
    "ior",
    "iparity",
    "irand",
    "ishft",
    "ishftc",
    "is_iostat_end",
    "is_iostat_eor",
    "kind",
    "lbound",
    "lcm",
    "len",
    "len_trim",
    "lge",
    "lgt",
    "lle",
    "llt",
    "log",
    "log10",
    "log_gamma",
    "logical",
    "maskl",
    "maskr",
    "matmul",
    "max",
    "maxexponent",
    "maxloc",
    "maxval",
    "merge",
    "merge_bits",
    "min",
    "minexponent",
    "minloc",
    "minval",
    "mod",
    "modulo",
    "nearest",
    "norm2",
    "not",
    "null",
    "nworkers",
    "pack",
    "parity",
    "popcnt",
    "poppar",
    "precision",
    "present",
    "product",
    "radix",
    "range",
    "real",
    "repeat",
    "reshape",
    "rrspacing",
    "scale",
    "scan",
    "selected_int_kind",
    "selected_real_kind",
    "set_exponent",
    "shape",
    "shifta",
    "shiftl",
    "shiftr",
    "sign",
    "sin",
    "sinh",
    "size",
    "spacing",
    "spread",
    "sqrt",
    "storage_size",
    "sum",
    "system_clock",
    "tan",
    "tanh",
    "this_image",
    "tiny",
    "trailz",
    "transfer",
    "transpose",
    "trim",
    "ubound",
    "unpack",
    "verify",
    "xor",
    "if",
    "intent",
]


def extract_struct_ftn(stmts: Statements) -> dict:
    """Main calls to build structure form statements

    statements is the output of tucan.unformat_ftn.unformat_ftn
    """
    clean_code = stmts.to_code()
    all_structs = _extract_on_cleaned_ftn(stmts)
    struct_aspects = _struct_analyses_ftn(all_structs, clean_code)
    all_structs = struct_augment(all_structs, struct_aspects)
    return all_structs


def _extract_on_cleaned_ftn(stmts: Statements) -> dict:
    """Extract structure from cleaned statements."""
    buffer = []
    stack = []
    path = []

    entry_ = []
    out_ = []
    stat_idx = 0
    for line, (line_idx1, line_idx2) in zip(stmts.stmt, stmts.lines):
        stat_idx += 1
        # you must also note nests because bare end statement can jam the system
        for part in PARTS + NESTS:
            if line.strip().startswith(part):
                if (
                    line.strip().startswith("type")
                    and "is" in line.split("(")[0].split()
                ):
                    continue
                elif line.strip().startswith("module") and "procedure" in line.split():
                    continue
                entry_.append(part)
                # print(entry_)
                name = _parse_name_ftn(line)
                buffer.append(
                    buffer_item(
                        type_=part,
                        name=name,
                        first_line=line,
                        line_idx=line_idx1,
                        statement_idx=stat_idx,
                    )
                )
                path.append(name)
                continue

        if line.strip().startswith("end ") or line.strip() == "end":
            out_.append(line)
            # print(out_)
            (type_, name, line_start, line_idx, statement_idx) = buffer[-1]
            stack.append(
                stack_item(
                    type_=type_,
                    name=name,
                    path=path.copy(),
                    start_line_idx=line_idx,
                    start_statement_idx=statement_idx,
                    start_line=line_start,
                    end_line_idx=line_idx2,
                    end_statement_idx=stat_idx,
                    end_line=line,
                )
            )
            path.pop(-1)
            buffer.pop(-1)
            continue

    # Check specific to fortran
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
        if type_.strip() not in end_line:
            logger.debug(
                f"End mismatch at {path} : '{start_line_idx}' to '{end_line_idx}'. For {type_} in {end_line}"
            )
    if len(entry_) != len(out_):
        logger.error(
            "Missing one structure statement such as end if... removing file from current analysis"
        )
        return {}

    return struct_from_stack(stack, main_types=PARTS)


def _parse_name_ftn(line: str):
    """expect a lowercase stripped line
    takes the second word as the name
    """
    name = line.replace("(", " ").split()[1]
    return name


##### Main structs


def _struct_analyses_ftn(all_structs: dict, clean_code: list) -> dict:
    """Python specific analyses"""
    struct_aspects = {}
    for part, data in all_structs.items():
        sub_code = clean_code[data["statements"][0] : data["statements"][-1]]
        struct_aspects[part] = {}
        struct_aspects[part]["callables"] = find_callables_ftn(sub_code)
        struct_aspects[part]["CCN"] = compute_ccn_approx_ftn(sub_code)
    return struct_aspects


def find_callables_ftn(code: list) -> list:
    """Find callables in python"""
    candidates = find_words_before_left_parenthesis(code)

    # NB we expect lines like 'call mysubroutine()' to be caught by left parenthesis law

    matches = [cand for cand in set(candidates) if cand not in INTRINSICS]
    return sorted(matches)  # Must be sorted for testing


def compute_ccn_approx_ftn(code: list) -> int:
    """Count decision points (if, else if, do, select, etc.)"""
    decision_points = re.findall(
        r"(?i)(if |else if|do |select case|select default)", "\n".join(code)
    )
    complexity = len(decision_points) + 1
    return complexity
