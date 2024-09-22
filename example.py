import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import tclogger
from tclogger import TCLogger, logger, TCLogstr, logstr, colored, decolored
from tclogger import Runtimer, OSEnver, shell_cmd
from tclogger import get_now_ts, get_now_str, ts_to_str, str_to_ts, get_now_ts_str
from tclogger import DictStringifier, dict_to_str
from tclogger import FileLogger

if __name__ == "__main__":
    with Runtimer():
        logger.note(tclogger.__file__)
        logger.mesg(get_now_ts())
        logger.success(get_now_str())
        logger.note(f"Now: {logstr.mesg(get_now_str())}, ({logstr.file(get_now_ts())})")

    s1 = colored("hello", color="green", bg_color="bg_red", fonts=["bold", "blink"])
    s2 = colored("world", color="red", bg_color="bg_blue", fonts=["bold", "underline"])
    s3 = colored(f"BEG {s1} __ {s2} END")
    logger.note(s3)
    logger.success(s3)
    s4 = decolored(logstr.success(s3))
    print(s4)

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

    file_logger = FileLogger(Path(__file__).parent / "test.log")
    file_logger.log("This is an error message", "error")

    # python example.py
