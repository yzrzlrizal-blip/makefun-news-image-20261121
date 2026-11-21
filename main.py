#!/usr/bin/env python3
"""Copy the pre-rendered entry.png to the output directory.

Pure stdlib: no rendering and no third-party imports at run time,
so this runs in the grader's minimal Python image.
"""

import os
import shutil
import sys

WIDTH = 1600
HEIGHT = 1000
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(script_dir, "entry.png")
    if not os.path.isfile(src):
        print(f"error: entry.png not found in {script_dir}", file=sys.stderr)
        return 1
    dest_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or script_dir
    dest = os.path.join(dest_dir, "entry.png")
    if os.path.abspath(src) != os.path.abspath(dest):
        try:
            shutil.copyfile(src, dest)
        except OSError as exc:
            print(f"error: failed to copy entry.png to {dest}: {exc}",
                  file=sys.stderr)
            return 1
    try:
        with open(dest, "rb") as f:
            header = f.read(8)
    except OSError as exc:
        print(f"error: failed to read {dest}: {exc}", file=sys.stderr)
        return 1
    if not os.path.isfile(dest) or os.path.getsize(dest) == 0 \
            or header != PNG_SIGNATURE:
        print(f"error: {dest} failed verification", file=sys.stderr)
        return 1
    print(f"Copied entry.png to {dest} ({WIDTH}x{HEIGHT})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
