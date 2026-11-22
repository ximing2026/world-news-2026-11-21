#!/usr/bin/env python3
"""Place a copy of the bundled poster at /output/entry.png.

The artwork ships in this repository as entry.png, in the same folder
as this script. Running the program copies it to the location the
bounty harness reads from, creating the output folder first when it is
missing.
"""

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
DEST_DIR = Path("/output")
DEST = DEST_DIR / "entry.png"

PNG_SIGNATURE = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
SIZE_LIMIT = 1048576  # 1 MiB


def guard(source: Path) -> None:
    """Exit with an error unless source is a PNG no larger than 1 MiB."""
    size = source.stat().st_size
    if size > SIZE_LIMIT:
        sys.exit(
            f"error: {source.name} is {size} bytes, "
            f"which exceeds the 1 MiB limit of {SIZE_LIMIT} bytes"
        )
    with source.open("rb") as handle:
        opening = handle.read(len(PNG_SIGNATURE))
    if opening != PNG_SIGNATURE:
        sys.exit(f"error: {source.name} does not begin with the PNG magic bytes")


def main() -> int:
    if not SOURCE.is_file():
        print(f"error: source image not found: {SOURCE}", file=sys.stderr)
        return 1

    guard(SOURCE)

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    print(f"Done: copied {SOURCE.name} to {DEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
