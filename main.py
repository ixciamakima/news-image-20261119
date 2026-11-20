#!/usr/bin/env python3
"""Copy the rendered front page to the make.fun output directory.

Stdlib only. The entry image (entry.png) lives next to this file; it is
copied to ``$MAKEFUN_OUTPUT_DIR/entry.png`` (default ``/output``).
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(SOURCE, "rb") as fh:
        data = fh.read()
    if len(data) == 0:
        print("error: entry.png is empty", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG file", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("error: entry.png is %d bytes, over the 1 MiB limit"
              % len(data), file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    with open(dest, "wb") as fh:
        fh.write(data)
    with open(dest, "rb") as fh:
        check = hashlib.sha256(fh.read()).hexdigest()
    if check != digest:
        print("error: copied file does not match source", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)" % (dest, len(data), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
