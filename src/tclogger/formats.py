"""Format utils"""

from typing import Union

from .logs import logstr
from .maths import max_key_len


def dict_to_str(
    d: Union[dict, list],
    indent: int = 4,
    max_depth: int = None,
    align_colon: bool = True,
    depth: int = 0,
) -> str:
    indent_str = " " * indent * (depth + 1)
    brace_indent_str = " " * indent * depth

    if max_depth is not None and depth > max_depth:
        return f"{{...}}"

    lines = []
    if isinstance(d, dict):
        key_len = max_key_len(d)
        for key, value in d.items():
            key_str = f"{key}"
            if align_colon:
                key_str = key_str.ljust(key_len)
            if isinstance(value, dict):
                value_str = dict_to_str(
                    value,
                    indent=indent,
                    max_depth=max_depth,
                    align_colon=align_colon,
                    depth=depth + 1,
                )
            elif isinstance(value, list):
                value_str = str(
                    [
                        dict_to_str(
                            v,
                            indent=indent,
                            max_depth=max_depth,
                            align_colon=align_colon,
                            depth=depth,
                        )
                        for v in value
                    ]
                )
            else:
                value_str = str(value)
            line = f"{indent_str}{logstr.note(key_str)} {logstr.hint(':')} {logstr.mesg(value_str)}"
            lines.append(line)
        lines_str = "\n".join(lines)
        dict_str = f"{{\n{lines_str}\n{brace_indent_str}}}"
    elif isinstance(d, list):
        dict_str = [
            dict_to_str(
                v,
                indent=indent,
                max_depth=max_depth,
                align_colon=align_colon,
                depth=depth,
            )
            for v in d
        ]
    else:
        dict_str = d

    return dict_str
