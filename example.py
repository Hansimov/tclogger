import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import tclogger
from tclogger import TCLogger, logger, TCLogstr, logstr
from tclogger import (
    get_now_ts,
    get_now_str,
    ts_to_str,
    str_to_ts,
    get_now_ts_str,
    Runtimer,
)
from tclogger import OSEnver, shell_cmd

if __name__ == "__main__":
    with Runtimer():
        logger.note(tclogger.__file__)
        logger.mesg(get_now_ts())
        logger.success(get_now_str())
        logger.note(f"Now: {logstr.mesg(get_now_str())}, ({logstr.file(get_now_ts())})")

    # python example.py
