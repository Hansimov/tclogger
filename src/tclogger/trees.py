from pathlib import Path
from typing import Literal

from .types import PathType, PathsType, StrsType
from .paths import norm_path, strf_path
from .matches import iterate_folder
from .logs import logstr

CON_PIPE = "─"  # pipe of connect line
MID_PIPE = "├"  # pipe of files not the last
END_PIPE = "└"  # pipe of files the last
IND_PIPE = "│"  # pipe of indent before each file
FOLD_BULLET = ">"  # bullet for folder
FILE_BULLET = "*"  # bullet for file


class PathObj:
    def __init__(self, path: Path, match_bool: bool, level: int):
        self.path = path
        self.match_bool = match_bool
        self.level = level
        self.parent = None
        self.idx = None
        self.prev: "PathObj" = None
        self.next: "PathObj" = None
        self.is_last_obj = None  # last folder or last file
        self.files_count = None  # only for folder
        self.lines_count = None  # only for file

    def is_file(self) -> bool:
        return self.path.is_file()

    def is_folder(self) -> bool:
        return self.path.is_dir()

    def full_str(self) -> str:
        return strf_path(self.path)

    def full_str_with_slash(self) -> str:
        path_str = self.full_str()
        if self.is_folder():
            path_str += "/"
        return path_str

    def short_str(self) -> str:
        return self.path.name

    def short_str_with_slash(self) -> str:
        path_str = self.short_str()
        if self.is_folder():
            path_str += "/"
        return path_str

    def set_idx(self, idx: int):
        self.idx = idx

    def set_prev(self, prev: "PathObj"):
        self.prev = prev

    def set_next(self, next: "PathObj"):
        self.next = next

    def set_parent(self, parent: "PathObj"):
        self.parent = parent

    def set_is_last_obj(self):
        self.is_last_obj = True

    def get_closest_prev_folder(self) -> "PathObj":
        if not self.prev:
            return None
        if self.prev.is_folder():
            return self.prev
        else:
            return self.prev.get_closest_prev_folder()

    def get_closest_next_folder(self) -> "PathObj":
        if not self.next:
            return None
        if self.next.is_folder():
            return self.next
        else:
            return self.next.get_closest_next_folder()

    def get_closest_prev_file(self) -> "PathObj":
        if not self.prev:
            return None
        if self.prev.is_file():
            return self.prev
        else:
            return self.prev.get_closest_prev_file()

    def get_closest_next_file(self) -> "PathObj":
        if not self.next:
            return None
        if self.next.is_file():
            return self.next
        else:
            return self.next.get_closest_next_file()


def get_path_obj_parent(
    path_obj: PathObj,
    path_objs: list[PathObj],
    beg_idx: int = None,
    end_idx: int = None,
) -> PathObj:
    if beg_idx is None:
        beg_idx = 0
    if end_idx is None:
        end_idx = len(path_objs)
    for i in range(end_idx - 1, beg_idx - 1, -1):
        po = path_objs[i]
        if po.path == path_obj.path.parent:
            return po
    return None


def get_path_obj_last_child(
    path_obj: PathObj,
    path_objs: list[PathObj],
    beg_idx: int = None,
    end_idx: int = None,
):
    if beg_idx is None:
        beg_idx = 0
    if end_idx is None:
        end_idx = len(path_objs)
    for i in range(beg_idx, end_idx):
        po = path_objs[i]
        if i == len(path_objs) - 1:
            return po
        if po.parent and po.parent.path != path_obj.path:
            ro = path_objs[i - 1]
            if ro != path_obj:
                return ro
            break
    return None


def path_obj_to_str(
    path_obj: PathObj,
    name_style: Literal["short", "full"] = "short",
    prefix_style: Literal["pipe", "bullet", "space"] = "pipe",
    branch_style: Literal["pipe", "bullet", "space"] = "pipe",
    show_file_lines_count: bool = True,
    show_folder_files_count: bool = True,
    show_folder_slash: bool = True,
    show_color: bool = True,
    indent_width: int = 4,
) -> str:
    level = path_obj.level

    # path_str
    if name_style == "short":
        path_str = path_obj.short_str()
    else:
        path_str = path_obj.full_str()
    if show_folder_slash and path_obj.is_folder():
        path_str += "/"

    # init before_strs
    before_strs = [" "] * (level * indent_width)

    # set branch chars (| before prefix)
    if level >= 2 and branch_style == "pipe":
        # dlevel: level of deepest folder who is last obj
        dlevel = level
        parent = path_obj.parent
        while parent:
            if parent.is_last_obj:
                dlevel = parent.level
                break
            parent = parent.parent
        for lv in range(dlevel, level - 1):
            before_strs[lv * indent_width + 1] = IND_PIPE
    else:
        pass

    # set prefix chars (chars before path_str)
    if level >= 1 and prefix_style == "pipe":
        if path_obj.is_last_obj:
            before_strs[-indent_width] = END_PIPE
        else:
            before_strs[-indent_width] = MID_PIPE
        if indent_width > 2:
            before_strs[-indent_width + 1 : -1] = [CON_PIPE] * (indent_width - 2)
    elif prefix_style == "bullet":
        if path_obj.is_folder():
            before_strs[-indent_width] = FOLD_BULLET
        else:  # path_obj.is_file()
            before_strs[-indent_width] = FILE_BULLET
    else:
        pass

    # join before_strs
    before_str = "".join(before_strs)

    # set path_obj_str
    path_obj_str = f"{before_str}{path_str} ({level})"

    # set color
    if show_color:
        if path_obj.match_bool is False:
            path_obj_str = logstr.warn(path_obj_str)
        elif path_obj.is_folder():
            path_obj_str = logstr.note(path_obj_str)
        elif path_obj.is_file():
            path_obj_str = logstr.file(path_obj_str)

    return path_obj_str


def tree_folder(
    # params of paths matching
    root: PathType = ".",
    includes: StrsType = None,
    excludes: StrsType = None,
    unmatch_bool: bool = True,
    ignore_case: bool = True,
    use_gitignore: bool = True,
    # params of tree formatting
    name_style: Literal["short", "full"] = "short",
    prefix_style: Literal["pipe", "bullet", "space"] = "pipe",
    branch_style: Literal["pipe", "bullet", "space"] = "pipe",
    show_file_lines_count: bool = True,
    show_folder_files_count: bool = True,
    show_folder_slash: bool = True,
    show_color: bool = True,
    indent_width: int = 4,
    max_level: int = None,
    verbose: bool = True,
) -> str:
    """
    Example output:

    tclogger/
    ├── example.py
    ├── pyproject.toml
    ├── README.md
    ├── src/
    │   ├── tclogger/
    │   │   ├── trees.py
    |   │   ├── ...
    │   │   └── types.py
    │   └── tclogger.egg-info/
    │       ├── ...
    │       └── top_level.txt
    └── test.log
    """
    # create path objs
    root = norm_path(root)
    path_objs: list[PathObj] = []
    root_obj = PathObj(root, True, 0)
    path_objs.append(root_obj)
    p: PathType
    for p, match_bool, level in iterate_folder(
        root,
        includes=includes,
        excludes=excludes,
        yield_folder=True,
        unmatch_bool=unmatch_bool,
        ignore_case=ignore_case,
        use_gitignore=use_gitignore,
        verbose=verbose,
        indent=0,
    ):
        path_obj = PathObj(p, match_bool, level)
        path_objs.append(path_obj)

    # sort path objs by full_str
    path_objs = sorted(path_objs, key=lambda po: po.full_str_with_slash())

    # set idx, prev, next
    prev: PathObj = None
    for idx, path_obj in enumerate(path_objs):
        path_obj.set_idx(idx)
        path_obj.set_prev(prev)
        if prev:
            prev.set_next(path_obj)
        prev = path_obj

    # set parent
    for idx, path_obj in enumerate(path_objs):
        parent = get_path_obj_parent(path_obj, path_objs, end_idx=idx)
        path_obj.set_parent(parent)

    # set is_last_obj
    for idx, path_obj in enumerate(path_objs):
        if path_obj.is_folder():
            last_child = get_path_obj_last_child(path_obj, path_objs, beg_idx=idx + 1)
            if last_child:
                last_child.set_is_last_obj()

    path_obj_to_str_params = {
        "name_style": name_style,
        "prefix_style": prefix_style,
        "branch_style": branch_style,
        "show_file_lines_count": show_file_lines_count,
        "show_folder_files_count": show_folder_files_count,
        "show_folder_slash": show_folder_slash,
        "show_color": show_color,
        "indent_width": indent_width,
    }

    # format path objs to strings
    path_obj_strs = []
    for path_obj in path_objs:
        path_obj_str = path_obj_to_str(path_obj, **path_obj_to_str_params)
        path_obj_strs.append(path_obj_str)

    print("path_obj_strs:")
    for path_obj_str in path_obj_strs:
        print(path_obj_str)
