import sys

from datetime import timedelta
from typing import Union

from .times import get_now, t_to_str, dt_to_str, dt_to_sec
from .maths import int_bits
from .logs import logstr


class TCLogbar:
    PROGRESS_LOGSTR = {
        0: logstr.file,
        25: logstr.note,
        50: logstr.hint,
        75: logstr.err,
        100: logstr.success,
    }

    def __init__(
        self,
        count: int = 0,
        total: int = None,
        desc: str = "",
        cols: int = 25,
        show_at_init: bool = True,
        show_datetime: bool = True,
        show_iter_per_second: bool = True,
        show_color: bool = True,
    ):
        self.count = count
        self.total = total
        self.desc = desc
        self.cols = cols
        self.show_at_init = show_at_init
        self.show_datetime = show_datetime
        self.show_iter_per_second = show_iter_per_second
        self.show_color = show_color
        self.start_t = get_now()

    def is_num(self, num: Union[int, float]):
        return isinstance(num, (int, float))

    def log(self, msg: str = None):
        if msg is None:
            return
        line = f"\033[2K\033[1G{msg}"
        sys.stdout.write(line)
        sys.stdout.flush()

    def end(self):
        sys.stdout.write("\n")
        sys.stdout.flush()

    def update(
        self,
        add_count: int = None,
        count: int = None,
        desc: str = None,
        update_bar: bool = True,
    ):
        if count is not None:
            self.count = count
        elif add_count is not None:
            self.count += add_count
        else:
            pass

        if desc is not None:
            self.desc = desc

        self.now = get_now()
        self.dt = self.now - self.start_t
        dt_seconds = dt_to_sec(self.dt, precision=3)
        if (
            self.is_num(self.total)
            and self.is_num(self.count)
            and self.count > 0
            and self.total - self.count >= 0
        ):
            self.remain_dt = timedelta(
                seconds=dt_seconds * (self.total - self.count) / self.count
            )
        else:
            self.remain_dt = None

        if self.is_num(self.total) and self.is_num(self.count) and self.total > 0:
            self.percent = min(round(self.count / self.total * 100), 100)
        else:
            self.percent = None

        if self.is_num(self.count) and self.count > 0 and dt_seconds > 0:
            self.iter_per_second = round(self.count / dt_seconds, ndigits=1)
        else:
            self.iter_per_second = None

        if update_bar:
            self.construct_bar_str()
            self.log(self.bar_str)

    def construct_bar_str(self):
        now_str = t_to_str(self.now)
        elapsed_str = dt_to_str(self.dt)

        if self.percent is not None:
            percent_str = f"{self.percent:>3}%"
            filled_cols = int(self.cols * self.percent / 100)
            grid_percent_str = f" {self.percent}%"
            if filled_cols + len(grid_percent_str) < self.cols:
                grid_str = (
                    filled_cols * "█"
                    + grid_percent_str
                    + (self.cols - filled_cols - len(grid_percent_str)) * " "
                )
            else:
                grid_str = filled_cols * "█" + (self.cols - filled_cols) * " "
        else:
            percent_str = f"{'?':>3}%"
            grid_str = self.cols * " "

        if self.remain_dt is not None:
            remain_str = dt_to_str(self.remain_dt)
        else:
            remain_str = "??:??"

        if self.is_num(self.total):
            total_bits = int_bits(self.total)
            total_str = str(self.total)
        else:
            total_bits = 0
            total_str = "?"

        if self.is_num(self.count):
            count_str = f"{self.count:_>{total_bits}}"
        else:
            count_str = "?"

        if self.iter_per_second is not None:
            if self.iter_per_second > 1:
                iter_per_second_str = f"({round(self.iter_per_second)} it/s)"
            else:
                iter_per_second_str = f"({round(1/self.iter_per_second)} s/it)"
        else:
            iter_per_second_str = ""

        if self.show_color:
            logstr_progress = self.PROGRESS_LOGSTR[self.percent // 25 * 25]
            count_str = logstr_progress(count_str)
            total_str = logstr.line(total_str)
            now_str = logstr.mesg(now_str)
            percent_str = logstr_progress(percent_str)
            grid_str = logstr_progress(grid_str)
            elapsed_str = logstr.file(elapsed_str)
            remain_str = logstr_progress(remain_str)
            iter_per_second_str = logstr.file(iter_per_second_str)

        self.bar_str = (
            f"[{now_str}] {self.desc}: "
            f"{count_str}/{total_str} "
            f"({percent_str}) "
            f"▌{grid_str}▐ "
            f"[{elapsed_str}<{remain_str}] "
            f"{iter_per_second_str}"
        )

    def set_cols(self, cols: int = None):
        self.cols = cols

    def set_total(self, total: int = None):
        self.total = total

    def set_count(self, count: int = None):
        self.count = count

    def add_count(self, add_count: int = None):
        self.count += add_count

    def set_desc(self, desc: str = None):
        self.desc = desc

    def hide(self):
        pass

    def show(self):
        pass
