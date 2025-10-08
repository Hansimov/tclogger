import sys
import linecache

from .decorations import brk
from .logs import logstr


class BreakpointException(Exception):
    def __init__(self, *args, head_n: int = 1, tail_n: int = 1, **kwargs):
        super().__init__(*args, **kwargs)
        self.__suppress_context__ = True
        # Get the frame where raise_breakpoint() was called
        frame = sys._getframe(2)
        self.filename = frame.f_code.co_filename
        self.lineno = frame.f_lineno
        self.name = frame.f_code.co_name
        self.head_n = head_n
        self.tail_n = tail_n
        self.msg = args[0] if args else ""

        # Get class name if the function is a method
        self.class_name = None
        if "self" in frame.f_locals:
            self.class_name = frame.f_locals["self"].__class__.__name__
        elif "cls" in frame.f_locals:
            self.class_name = frame.f_locals["cls"].__name__

    def __str__(self):
        # Format function/method name with class
        if self.class_name:
            func_name = f"{self.class_name}.{self.name}():"
        else:
            func_name = f"{self.name}:"

        # Build the output string
        lines = []
        lines.append(
            f"\n* File {logstr.file(brk(self.filename))}, line {logstr.file(self.lineno)}, in {logstr.mesg(func_name)}"
        )

        # Add context lines
        start_line = max(1, self.lineno - self.head_n)
        end_line = self.lineno + self.tail_n

        for line_num in range(start_line, end_line + 1):
            line_content = linecache.getline(self.filename, line_num).rstrip()
            if line_num == self.lineno:
                # Highlight the breakpoint line
                lines.append(f"  {logstr.warn(line_content)}")
            else:
                # Show context lines with line numbers
                lines.append(f"  {logstr.line(line_content)}")

        # Add exception message at the end
        if self.msg:
            lines.append(f"× BreakpointException: {self.msg}")
        else:
            lines.append(f"× BreakpointException")

        return "\n".join(lines)


def raise_breakpoint(msg: str = "", head_n: int = 0, tail_n: int = 0):
    exc = BreakpointException(msg, head_n=head_n, tail_n=tail_n)
    sys.excepthook = lambda exc_type, exc_value, exc_tb: print(
        logstr.warn(str(exc_value)), file=sys.stderr
    )
    raise exc
