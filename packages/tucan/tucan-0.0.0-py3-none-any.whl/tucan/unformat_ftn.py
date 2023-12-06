from typing import List
from loguru import logger

from tucan.unformat_common import (
    Statements,
    new_stmts,
    remove_strings,
    clean_blanks,
    clean_inline_comments,
    clean_pure_comments,
    align_multiline_blocks,
    split_multi_statement_lines,
    get_indent,
)

FORTRAN_KEYWORDS = [
    "allocatable",
    "allocate",
    "assign",
    "assignment",
    "backspace",
    "block",
    "call",
    "case",
    "close",
    "common",
    "contains",
    "continue",
    "cycle",
    "data",
    "deallocate",
    "dimension",
    "do",
    "else",
    "elseif",
    "elsewhere",
    "end",
    "endfile",
    "entry",
    "equivalence",
    "exit",
    "external",
    "forall",
    "format",
    "function",
    "go",
    "goto",
    "if",
    "implicit",
    "inquire",
    "interface",
    "intrinsic",
    "module",
    "namelist",
    "nullify",
    "only",
    "open",
    "operator",
    "optional",
    "parameter",
    "pause",
    "pointer",
    "print",
    "private",
    "procedure",
    "program",
    "public",
    "read",
    "real",
    "recursive",
    "result",
    "return",
    "rewind",
    "save",
    "select",
    "sequence",
    "stop",
    "subroutine",
    "target",
    "then",
    "to",
    "type",
    "use",
    "where",
    "while",
    "write",
]


def align_end_continuations(stmts: Statements) -> Statements:
    new_stmt = []
    new_lines = []
    last_line = ""
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if last_line.endswith("&"):
            new_stmt[-1] = last_line[:-1] + " " + line.strip().lstrip("&")
            new_lines[-1][1] = lend
        else:
            new_stmt.append(line)
            new_lines.append([lstart, lend])

        last_line = new_stmt[-1]
    return Statements(new_stmt, new_lines)


def align_start_continuations(stmts: Statements) -> Statements:
    new_stmt = []
    new_lines = []
    last_line = ""
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if line.lstrip().startswith("&"):
            new_stmt[-1] = last_line.rstrip("&") + " " + line.strip()[1:]
            new_lines[-1][1] = lend
        elif line.lstrip().startswith("$"):
            new_stmt[-1] = last_line.rstrip("$") + " " + line.strip()[1:]
            new_lines[-1][1] = lend
        else:
            new_stmt.append(line)
            new_lines.append([lstart, lend])

        last_line = new_stmt[-1]
    return Statements(new_stmt, new_lines)


def split_intrinsics(stmts: Statements) -> Statements:
    """_summary_

    Args:
        stms (Statements): _description_

    Returns:
        Statements: _description_
    """
    new_stmt = []
    new_lines = []
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if line.strip().startswith("endif"):
            new_stmt.append(line.replace("endif", "end if"))
        elif line.strip().startswith("enddo"):
            new_stmt.append(line.replace("enddo", "end do"))
        elif line.strip().startswith("endwhere"):
            new_stmt.append(line.replace("endwhere", "end where"))
        else:
            new_stmt.append(line)
        new_lines.append([lstart, lend])
    return Statements(new_stmt, new_lines)


def make_oneliners_conditionals_multilines(stmts: Statements) -> Statements:
    """_summary_

    Args:
        stmts (Statements): _description_

    Returns:
        Statements: _description_
    """
    new_stmt = []
    new_lines = []
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if "do" in line.split():
            if ": do" in line.strip():
                new_stmt.append(
                    line.replace(" ".join(line.split()), "do " + " ".join(line.split()))
                )
            else:
                new_stmt.append(line)

        elif line.strip().startswith("if "):
            if not line.strip().endswith("then") or "goto" in line:
                splitted_parts = split_oneliner(line)
                indent = get_indent(line)
                new_stmt.append(splitted_parts[0])
                new_lines.append([lstart, lend])
                new_stmt.append(indent + splitted_parts[-1])
                new_lines.append([lstart, lend])
                new_stmt.append(indent + "end if")
            elif "goto" in line:
                splitted_parts = split_oneliner(line)
                indent = get_indent(line)
                new_stmt.append(splitted_parts[0])
                new_lines.append([lstart, lend])
                new_stmt.append(indent + "end if")
            else:
                new_stmt.append(line)

        elif line.strip().startswith("where "):
            splitted_parts = split_oneliner(line)

            if not splitted_parts[-1]:
                new_stmt.append(line)
                new_lines.append([lstart, lend])
                continue

            indent = get_indent(line)
            new_stmt.append(splitted_parts[0])
            new_lines.append([lstart, lend])
            new_stmt.append(indent + splitted_parts[-1])
            new_lines.append([lstart, lend])
            new_stmt.append(indent + "end where")

        else:
            new_stmt.append(line)

        new_lines.append([lstart, lend])
    return Statements(new_stmt, new_lines)


def split_oneliner(line: str) -> list:
    """_summary_

    Args:
        line (str): _description_

    Returns:
        list: _description_
    """
    path = []
    new_stmt = ""
    split_parts = []
    for idx, char in enumerate(line):
        if "(" in char:
            new_stmt += char
            path.append(char)
        elif ")" in char:
            new_stmt += char
            path.pop(-1)
            if not path:
                split_parts.append(new_stmt)
                split_parts.append(line[idx + 1 :])
                break
        else:
            new_stmt += char

    return split_parts


def remove_space_in_front_of_variables(stmts: Statements) -> Statements:
    """_summary_

    Args:
        stmts (Statements): _description_

    Returns:
        Statements: _description_
    """
    new_stmt = []
    new_lines = []
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        stmt = line
        for keyword in FORTRAN_KEYWORDS:
            if keyword in line.split() and "=" in line:
                if line.split()[1] == "=":
                    stmt = line.replace(line.split()[0] + " =", line.split()[0] + "=")
                    logger.warning(
                        f"A Fortran Keywords {keyword} is used as a variable in the code. Bad Practice Should Be Avoided"
                    )
                continue
            continue

        new_stmt.append(stmt)
        new_lines.append([lstart, lend])

    return Statements(new_stmt, new_lines)


def remove_deprecated_function_def(stmts: Statements) -> Statements:
    new_stmt = []
    new_lines = []
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        stmt = line
        for deprecated_first_word in ["real", "integer", "type", "logical"]:
            if line.strip().startswith(deprecated_first_word) and "function" in line:
                stmt = "function" + "".join(line.split("function")[1:])
                logger.warning(
                    f"{line.split('function')[0]} found at the beginning of the function declaration, this is an old form. Using REAL(kind=x) is better."
                )
        new_stmt.append(stmt)
        new_lines.append([lstart, lend])
    return Statements(new_stmt, new_lines)


def remove_awful_do_loop(stmts: Statements) -> Statements:
    """_summary_

    Args:
        stmts (Statements): _description_

    Returns:
        Statements: _description_
    """
    new_stmt = []
    new_lines = []
    odd_do_loop = False
    count = 0
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        stmt = line

        if line.strip().startswith("do "):
            try:
                value = int(line.split()[1].strip())
                odd_do_loop = True
                count += 1
            except ValueError:
                pass

        elif odd_do_loop:
            if line.strip().startswith(str(value)):
                odd_do_loop = False
                stmt = "end do"
                for number_of_loop in range(count):
                    new_stmt.append(stmt)
                    new_lines.append([lstart, lend])
                count = 0
                continue

        new_stmt.append(stmt)
        new_lines.append([lstart, lend])

    return Statements(new_stmt, new_lines)


def space_after_keyword(stmts: Statements) -> Statements:
    stack_keywords = {"if(": "if (", "is(": "is (", "associate(": "associate ("}
    new_stmt = []
    new_lines = []

    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        stmt = line
        for keyword in stack_keywords.keys():
            if keyword in line:
                stmt = line.replace(keyword, stack_keywords[keyword])

        # Exception if the line is only a "do" statement (e.g. Neko)
        for keyword in ["do", "interface", "block"]:
            if line.strip() == keyword:
                stmt = line.replace(keyword, keyword + " ()")
        new_stmt.append(stmt)
        new_lines.append([lstart, lend])

    return Statements(new_stmt, new_lines)


def suppress_goto_references(stmts: Statements) -> Statements:
    new_stmt = []
    new_lines = []
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        stmt = line
        for keyword in FORTRAN_KEYWORDS:
            if keyword in line.split() and line.split()[0].isdigit():
                stmt = line.replace(line.split()[0], len(line.split()[0]) * " ")

        new_stmt.append(stmt)
        new_lines.append([lstart, lend])

    return Statements(new_stmt, new_lines)


def unformat_ftn(code: List[str]) -> Statements:
    """
    Unformat Fortran code by stripping comments and moving leading '&' characters.

    Args:
        code (List[str]): List of Fortran code lines.

    Returns:
        List[Tuple[str, Tuple[int, int]]]: List of unformatted code statements along with line number ranges.
    """
    stmts = new_stmts(code)
    stmts.stmt = remove_strings(stmts.stmt, '"')
    stmts.stmt = remove_strings(stmts.stmt, "'")
    stmts = clean_blanks(stmts)
    stmts = align_end_continuations(stmts)
    stmts = align_start_continuations(stmts)
    stmts = clean_pure_comments(stmts, "c")
    stmts = clean_pure_comments(stmts, "C")
    stmts = clean_pure_comments(stmts, "*")
    stmts = clean_inline_comments(stmts, "!")
    stmts = align_multiline_blocks(stmts, "(/", "/)")
    stmts = split_multi_statement_lines(stmts)
    stmts = split_intrinsics(stmts)
    stmts = space_after_keyword(stmts)
    stmts = remove_deprecated_function_def(stmts)
    stmts = remove_awful_do_loop(stmts)
    stmts = suppress_goto_references(stmts)
    stmts = make_oneliners_conditionals_multilines(stmts)
    stmts = remove_space_in_front_of_variables(stmts)

    return stmts
