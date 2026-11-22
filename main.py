#!/usr/bin/env python3
"""Deliver the poster image to /output/entry.png.

This repository ships its artwork as a file named entry.png sitting
beside this script. Executing the program copies that file to the
output path, making the /output directory first if it is absent,
and reports what it did.
"""

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
DEST = Path("/output") / "entry.png"

PNG_HEADER = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576  # 1 MiB


def check_source(path: Path) -> None:
    """Abort unless path is a genuine PNG of at most 1 MiB."""
    size = path.stat().st_size
    if size > MAX_BYTES:
        sys.exit(
            f"error: {path.name} weighs {size} bytes, "
            f"over the 1 MiB ceiling of {MAX_BYTES} bytes"
        )
    with path.open("rb") as handle:
        head = handle.read(len(PNG_HEADER))
    if head != PNG_HEADER:
        sys.exit(f"error: {path.name} lacks the PNG magic bytes at its start")


def main() -> int:
    if not SOURCE.is_file():
        print(f"error: cannot find the bundled image at {SOURCE}", file=sys.stderr)
        return 1
    check_source(SOURCE)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    print(f"copied {SOURCE} -> {DEST} ({DEST.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
