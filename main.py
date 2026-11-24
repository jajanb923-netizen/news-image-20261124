#!/usr/bin/env python3
"""news-image-20261124 entrypoint.

Copies the front-page image for Tuesday 24 November 2026 to the
grader's output directory. Standard library only, no network, fully
deterministic: the image is a fixed file shipped in this repository.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    data = target.read_bytes()
    # Fail loudly instead of shipping a broken image: the gate rejects
    # anything that is not a whole PNG of at most 1 MiB.
    if not data.startswith(PNG_SIGNATURE):
        print("error: output is not a PNG", file=sys.stderr)
        raise SystemExit(1)
    if len(data) > MAX_BYTES:
        print(f"error: output is {len(data)} bytes, over 1 MiB",
              file=sys.stderr)
        raise SystemExit(1)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
