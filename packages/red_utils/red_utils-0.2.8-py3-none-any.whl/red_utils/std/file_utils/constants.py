from __future__ import annotations

from datetime import datetime

default_json_dir: str = "data/json"


def file_ts(fmt: str = "%Y-%m-%d_%H:%M:%S") -> str:
    """Return a formatted timestamp, useful for prepending to dir/file names."""
    now: str = datetime.now().strftime(fmt)

    return now
