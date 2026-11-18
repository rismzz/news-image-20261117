#!/usr/bin/env python3
"""news-image-20261117: copy the poster image to the output directory.

Round 2: the entry image (entry.png, a 1024x1024 poster summing up the
world news of Tuesday 17 November 2026, rendered by render_poster.py)
lives in this repository next to this program. This program copies it,
byte for byte, to $MAKEFUN_OUTPUT_DIR/entry.png (default
/output/entry.png), creating the output directory if needed. No network,
no randomness: every run writes the same bytes. Exit 0 on success.
"""

import os
import shutil
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        print("error: %s not found next to main.py" % source, file=sys.stderr)
        return 1
    if os.path.getsize(source) > 1048576:
        print("error: entry.png exceeds the 1 MiB limit", file=sys.stderr)
        return 1
    with open(source, "rb") as fh:
        magic = fh.read(8)
    is_png = magic.startswith(b"\x89PNG\r\n\x1a\n")
    is_jpeg = magic.startswith(b"\xff\xd8\xff")
    if not (is_png or is_jpeg):
        print("error: entry.png is neither a PNG nor a JPEG", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(source, dest)
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
