import sys
import linecache

from .decorations import brk
from .logs import logstr
from .fills import add_fills


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
        lines = []
        fills_str = logstr.warn(add_fills(filler="-"))
        lines.append(fills_str)

        if self.class_name:
            func_name = f"{self.class_name}.{self.name}():"
        else:
            func_name = f"{self.name}:"
        file_info_str = f"* File {logstr.file(brk(self.filename))}, line {logstr.file(self.lineno)}, in {logstr.mesg(func_name)}"
        lines.append(logstr.warn(file_info_str))

        beg_line_no = max(1, self.lineno - self.head_n)
        end_line_no = self.lineno + self.tail_n
        line_num_width = len(str(end_line_no))
        for line_num in range(beg_line_no, end_line_no + 1):
            line_content = linecache.getline(self.filename, line_num).rstrip()
            line_num_content = f"| {line_num:>{line_num_width}} |  {line_content}"
            if line_num == self.lineno:
                # Highlight breakpoint line
                lines.append(logstr.warn(line_num_content))
            else:
                lines.append(logstr.line(line_num_content))

        if self.msg:
            exp_str = f"× BreakpointException: {self.msg}"
        else:
            exp_str = f"× BreakpointException"
        lines.append(logstr.warn(exp_str))
        lines.append(fills_str)

        return "\n".join(lines)


def raise_breakpoint(msg: str = "", head_n: int = 1, tail_n: int = 1):
    exc = BreakpointException(msg, head_n=head_n, tail_n=tail_n)
    sys.excepthook = lambda exc_type, exc_value, exc_tb: print(
        str(exc_value), file=sys.stderr
    )
    raise exc
