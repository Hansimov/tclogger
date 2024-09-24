import sys

from datetime import timedelta
from typing import Union

from .times import get_now, t_to_str, dt_to_str, dt_to_sec


class TCLogbar:
    def __init__(
        self,
        count: int = 0,
        total: int = None,
        desc: str = "",
        cols: int = 25,
        show_at_init: bool = True,
        show_datetime: bool = True,
        show_iter_per_second: bool = True,
    ):
        self.count = count
        self.total = total
        self.desc = desc
        self.cols = cols
        self.show_at_init = show_at_init
        self.show_datetime = show_datetime
        self.show_iter_per_second = show_iter_per_second
        self.start_t = get_now()

    def is_num(self, num: Union[int, float]):
        return isinstance(num, (int, float))

    def log(self, msg: str = None):
        if msg is None:
            return

        msg_str = str(msg) + "\r"
        sys.stdout.write(msg_str)
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
            and self.total - self.count > 0
        ):
            self.remain_dt = timedelta(
                seconds=dt_seconds * (self.total - self.count) / self.count
            )
        else:
            self.remain_dt = None

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
        if self.remain_dt is not None:
            remain_str = dt_to_str(self.remain_dt)
        else:
            remain_str = "?"
        grid_str = " " * self.cols
        if self.total is not None:
            total_str = str(self.total)
        else:
            total_str = "?"

        if self.iter_per_second is not None:
            if self.iter_per_second > 1:
                iter_per_second_str = f"({round(self.iter_per_second)} it/s)"
            else:
                iter_per_second_str = f"({round(1/self.iter_per_second)} s/it)"
        else:
            iter_per_second_str = ""

        self.bar_str = f"[{now_str}] {self.desc}: |{grid_str}| {self.count}/{total_str} [{elapsed_str}<{remain_str}] {iter_per_second_str}"

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
