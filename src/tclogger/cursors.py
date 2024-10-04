import sys

from typing import Literal


class CursorController:
    """ANSI Escape Sequences
    - https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    """

    def move(self, row: int = 0, col: int = 0, write: bool = True):
        """Move cursor to the relative position:
        - row > 0: rows up
        - row < 0: rows down
        - col > 0: cols right
        - col < 0: cols left
        """
        move_str = ""

        if row > 0:
            move_str = f"\033[{row}A"  # move cursor up by row
        elif row < 0:
            move_str = f"\033[{row}B"  # move cursor down by row
        else:
            move_str = ""

        if col > 0:
            move_str += f"\033[{col}C"  # move cursor right by col
        elif col < 0:
            move_str += f"\033[{col}D"  # move cursor left by col
        else:
            pass

        if write and move_str:
            sys.stdout.write(move_str)
            sys.stdout.flush()

        return move_str

    def move_to_beg(self, row: int = 0, write: bool = True):
        """Move cursor to the beginning of the relative row:
        - row > 0: rows up
        - row < 0: rows down
        - row = 0: current row
        """
        if row > 0:
            move_str = f"\033[{row}F"  # move cursor to line beginning of rows above
        elif row < 0:
            move_str = f"\033[{row}E"  # move cursor to line beginning of rows below
        else:
            move_str = f"\033[1G"  # move cursor to line beginning of current row

        if write and move_str:
            sys.stdout.write(move_str)
            sys.stdout.flush()

        return move_str

    def move_to_col(self, col: int = 0, write: bool = True):
        """Move cursor to column of current line."""
        if col > 0:
            move_str = f"\033[{col}G"  # move cursor to column of current line
        else:
            move_str = ""

        if write and move_str:
            sys.stdout.write(move_str)
            sys.stdout.flush()

        return move_str

    def erase_line(
        self,
        part: Literal["cursor_to_end", "beg_to_cursor", "beg_to_end"] = "beg_to_end",
        write: bool = True,
    ):
        """Erase the line:
        - cursor_to_end: erase from cursor to the end of the line
        - beg_to_cursor: erase from the beginning of the line to the cursor
        - beg_to_end: erase entire line
        """
        if part == "cursor_to_end":
            erase_str = "\033[0K"  # erase from cursor to the end of the line
        elif part == "beg_to_cursor":
            erase_str = "\033[1K"  # erase from the beginning of the line to the cursor
        elif part == "beg_to_end":
            erase_str = "\033[2K"  # erase entire line
        else:
            erase_str = ""

        if write and erase_str:
            sys.stdout.write(erase_str)
            sys.stdout.flush()
        return erase_str
