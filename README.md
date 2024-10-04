# tclogger
Python terminal colored logger

![](https://img.shields.io/pypi/v/tclogger?label=tclogger&color=blue&cacheSeconds=60)

## Install
```sh
pip install tclogger --upgrade
```

## Usage

Run example:

```sh
python example.py
```

See: [example.py](https://github.com/Hansimov/tclogger/blob/main/example.py)

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import tclogger
import time

from tclogger import TCLogger, logger, TCLogstr, logstr, colored, decolored
from tclogger import Runtimer, OSEnver, shell_cmd
from tclogger import get_now_ts, get_now_str, ts_to_str, str_to_ts, get_now_ts_str
from tclogger import CaseInsensitiveDict, DictStringifier, dict_to_str
from tclogger import FileLogger
from tclogger import TCLogbar, TCLogbarGroup


def test_run_timer_and_logger():
    with Runtimer():
        logger.note(tclogger.__file__)
        logger.mesg(get_now_ts())
        logger.success(get_now_str())
        logger.note(f"Now: {logstr.mesg(get_now_str())}, ({logstr.file(get_now_ts())})")


def test_color():
    s1 = colored("hello", color="green", bg_color="bg_red", fonts=["bold", "blink"])
    s2 = colored("world", color="red", bg_color="bg_blue", fonts=["bold", "underline"])
    s3 = colored(f"BEG {s1} __ {s2} END")
    logger.note(s3)
    logger.success(s3)
    s4 = decolored(logstr.success(s3))
    print(s4)


def test_case_insensitive_dict():
    d = CaseInsensitiveDict()
    d["Hello"] = "old world"
    print(d["hello"])
    print(d)
    d["hELLo"] = "New WORLD"
    print(d["HEllO"])
    print(d)


def test_dict_to_str():
    d = {
        "hello": "world",
        "now": get_now_str(),
        "list": [1, 2, 3, [4, 5], "6"],
        "nested": {"key1": "value1", "key2": "value2", "key_3": {"subkey": "subvalue"}},
    }
    s = dict_to_str(d, add_quotes=True, max_depth=1)
    logger.success(s)
    s = dict_to_str(d, add_quotes=False, is_colored=False, max_depth=0)
    print(s)


def test_file_logger():
    file_logger = FileLogger(Path(__file__).parent / "test.log")
    file_logger.log("This is an error message", "error")


def test_align_dict_list():
    data = {
        "_id": None,
        "view_avg": 15175,
        "view_maxn": [94092954, 86624275, 68368263, 57713196, 53493614],
        "view_percentile": [39, 152, 254, 539, 3032, 13602, 51956, 282149, 94092954],
        "coin_avg": 57,
        "coin_maxn": [3093375, 2021980, 1420923, 1354206, 1312931],
        "coin_percentile": [0, 0, 0, 1, 6, 24, 76, 682, 3093375],
        "danmaku_avg": 26,
        "danmaku_maxn": [762005, 365521, 349354, 335414, 334935],
        "danmaku_percentile": [0, 0, 0, 0, 2, 12, 57, 353, 762005],
        "percentiles": [0.2, 0.4, 0.5, 0.6, 0.8, 0.9, 0.95, 0.99, 1.0],
        "sub_lists": {
            "sub1": [1, 2, 4, 5, 6],
            "sub2": [21, 2, 35, 43, 89],
            "sub3": ["a", "abc", "gh", "jkl", "qerq"],
            "sub4": ["x", "ef", "i", "mkns", "adfa"],
        },
    }
    print(dict_to_str(data, align_list=True))


def test_logbar():
    epochs = 3
    total = 1000000
    logbar = TCLogbar(
        total=total, show_datetime=False, flush_interval=0.1, grid_mode="symbol"
    )
    for epoch in range(epochs):
        for i in range(total):
            logbar.update(increment=1)
            logbar.set_head(f"[{epoch+1}/{epochs}]")
        logbar.grid_mode = "shade"
        logbar.set_desc("THIS IS A SO LONG DESC WHICH IS USED TO TEST LINE UP")
        logbar.reset()


def test_logbar_group():
    epochs = 3
    total = 1000000
    epoch_bar = TCLogbar(total=epochs, show_datetime=False)
    epoch_bar.set_desc(f"[0/{epochs}]")
    epoch_bar.update(0, flush=True)

    progress_bar = TCLogbar(total=total, show_datetime=False)
    TCLogbarGroup([epoch_bar, progress_bar])
    for epoch in range(epochs):
        for i in range(total):
            progress_bar.set_desc(f"[{i+1}/{total}]")
            progress_bar.update(1)
        progress_bar.reset()
        epoch_bar.set_desc(f"[{epoch+1}/{epochs}]")
        epoch_bar.update(1, flush=True)


if __name__ == "__main__":
    test_run_timer_and_logger()
    test_color()
    test_case_insensitive_dict()
    test_dict_to_str()
    test_align_dict_list()
    test_file_logger()
    test_logbar()
    test_logbar_group()
```