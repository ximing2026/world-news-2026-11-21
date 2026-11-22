#!/usr/bin/env python3
"""Copy the bundled poster image to /output/entry.png."""

import shutil
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # 1 MiB


def check_source(source: Path) -> None:
    """Refuse to copy anything that is not a PNG of at most 1 MiB."""
    if not source.is_file():
        sys.exit(f"error: source image not found: {source}")
    size = source.stat().st_size
    if size > MAX_BYTES:
        sys.exit(
            f"error: {source.name} is {size} bytes, over the 1 MiB limit"
        )
    with source.open("rb") as handle:
        header = handle.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        sys.exit(f"error: {source.name} does not start with PNG magic bytes")


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    check_source(source)
    target = Path("/output/entry.png")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    print(f"Copied {source.name} to {target}")


if __name__ == "__main__":
    main()
