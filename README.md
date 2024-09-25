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
import random

from tclogger import TCLogger, logger, TCLogstr, logstr, colored, decolored
from tclogger import Runtimer, OSEnver, shell_cmd
from tclogger import get_now_ts, get_now_str, ts_to_str, str_to_ts, get_now_ts_str
from tclogger import CaseInsensitiveDict, DictStringifier, dict_to_str
from tclogger import FileLogger
from tclogger import TCLogbar


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


def test_logbar():
    epochs = 3
    total = 1000000
    logbar = TCLogbar(total=total, flush_interval=0.5, grid_mode="symbol")
    for epoch in range(epochs):
        for i in range(total):
            logbar.update(increment=1)
            logbar.set_head(f"[{epoch+1}/{epochs}]")
            # time.sleep(0.1 / total)
        logbar.reset()


if __name__ == "__main__":
    test_run_timer_and_logger()
    test_color()
    test_case_insensitive_dict()
    test_dict_to_str()
    test_file_logger()
    test_logbar()
```