"""Format utils"""

from typing import Union

from .colors import colored
from .logs import logstr
from .maths import max_key_len


def dict_to_str(
    d: Union[dict, list],
    indent: int = 2,
    depth: int = 0,
    max_depth: int = None,
    align_colon: bool = True,
    brace_colors: list[str] = ["light_blue", "light_cyan", "light_magenta"],
    key_colors: list[str] = ["light_blue", "light_cyan", "light_magenta"],
    value_colors: list[str] = ["white", "light_green"],
) -> str:
    indent_str = " " * indent * (depth + 1)
    brace_indent_str = " " * indent * depth

    if isinstance(key_colors, str):
        key_color = key_colors
    else:
        key_color = key_colors[depth % len(key_colors)]
    if isinstance(value_colors, str):
        value_color = value_colors
    else:
        value_color = value_colors[depth % len(value_colors)]
    if isinstance(brace_colors, str):
        brace_color = brace_colors
    else:
        brace_color = brace_colors[depth % len(brace_colors)]

    lb = colored("{", brace_color)
    rb = colored("}", brace_color)
    colon = colored(":", brace_color)
    comma = colored(",", brace_color)

    if max_depth is not None and depth > max_depth:
        return f"{lb}{colored('...',value_color)}{rb}"

    lines = []
    if isinstance(d, dict):
        key_len = max_key_len(d)
        for idx, (key, value) in enumerate(d.items()):
            key_str = f"{key}"
            if align_colon:
                key_str = key_str.ljust(key_len)
            value_str = dict_to_str(
                value,
                indent=indent,
                depth=depth + 1 if isinstance(value, dict) else depth,
                max_depth=max_depth,
                align_colon=align_colon,
                brace_colors=brace_colors,
                key_colors=key_colors,
                value_colors=value_colors,
            )
            colored_key_str = colored(key_str, key_color)
            colored_value_str = colored(value_str, value_color)
            line = f"{indent_str}{colored_key_str} {colon} {colored_value_str}"
            if idx < len(d) - 1:
                line += comma
            lines.append(line)
        lines_str = "\n".join(lines)
        dict_str = f"{lb}\n{lines_str}\n{brace_indent_str}{rb}"
    elif isinstance(d, list):
        dict_str = [
            dict_to_str(
                v,
                indent=indent,
                depth=depth,
                max_depth=max_depth,
                align_colon=align_colon,
                brace_colors=brace_colors,
                key_colors=key_colors,
                value_colors=value_colors,
            )
            for v in d
        ]
    else:
        dict_str = d

    return dict_str
