"""Format utils"""

from typing import Union

from .colors import colored
from .logs import logstr
from .maths import max_key_len


class DictStringifier:
    def __init__(
        self,
        indent: int = 2,
        max_depth: int = None,
        align_colon: bool = True,
        brace_colors: list[str] = ["light_blue", "light_cyan", "light_magenta"],
        key_colors: list[str] = ["light_blue", "light_cyan", "light_magenta"],
        value_colors: list[str] = ["white"],
    ):
        self.indent = indent
        self.max_depth = max_depth
        self.align_colon = align_colon
        self.depth_configs = {}
        self.brace_colors = brace_colors
        self.key_colors = key_colors
        self.value_colors = value_colors

    def get_depth_config(self, depth: int):
        if depth in self.depth_configs:
            return self.depth_configs[depth]

        if isinstance(self.key_colors, str):
            key_color = self.key_colors
        else:
            key_color = self.key_colors[depth % len(self.key_colors)]
        if isinstance(self.value_colors, str):
            value_color = self.value_colors
        else:
            value_color = self.value_colors[depth % len(self.value_colors)]
        if isinstance(self.brace_colors, str):
            brace_color = self.brace_colors
        else:
            brace_color = self.brace_colors[depth % len(self.brace_colors)]

        indent_str = " " * self.indent * (depth + 1)
        brace_indent_str = " " * self.indent * depth
        lb = colored("{", brace_color)
        rb = colored("}", brace_color)
        colon = colored(":", brace_color)
        comma = colored(",", brace_color)

        self.depth_configs[depth] = {
            "key_color": key_color,
            "value_color": value_color,
            "brace_color": brace_color,
            "indent_str": indent_str,
            "brace_indent_str": brace_indent_str,
            "lb": lb,
            "rb": rb,
            "colon": colon,
            "comma": comma,
        }

        return self.depth_configs[depth]

    def dict_to_str(
        self,
        d: Union[dict, list],
        depth: int = 0,
    ) -> str:
        configs = self.get_depth_config(depth)
        key_color = configs["key_color"]
        value_color = configs["value_color"]
        indent_str = configs["indent_str"]
        brace_indent_str = configs["brace_indent_str"]
        lb = configs["lb"]
        rb = configs["rb"]
        colon = configs["colon"]
        comma = configs["comma"]

        if self.max_depth is not None and depth > self.max_depth:
            return f"{lb}{colored('...',value_color)}{rb}"

        lines = []
        if isinstance(d, dict):
            key_len = max_key_len(d)
            for idx, (key, value) in enumerate(d.items()):
                key_str = f"{key}"
                if self.align_colon:
                    key_str = key_str.ljust(key_len)
                value_str = self.dict_to_str(
                    value,
                    depth=depth + 1 if isinstance(value, dict) else depth,
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
            dict_str = [self.dict_to_str(v, depth=depth) for v in d]
        else:
            dict_str = d

        return dict_str


def dict_to_str(
    d: dict,
    indent: int = 2,
    max_depth: int = None,
    align_colon: bool = True,
    brace_colors: list[str] = ["light_blue", "light_cyan", "light_magenta"],
    key_colors: list[str] = ["light_blue", "light_cyan", "light_magenta"],
    value_colors: list[str] = ["white"],
) -> str:
    ds = DictStringifier(
        indent=indent,
        max_depth=max_depth,
        align_colon=align_colon,
        brace_colors=brace_colors,
        key_colors=key_colors,
        value_colors=value_colors,
    )
    return ds.dict_to_str(d)
