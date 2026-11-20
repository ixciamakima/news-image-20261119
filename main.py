#!/usr/bin/env python3
"""news-image-20261119 v3 entry program.

Copies the pre-rendered ``entry.png`` (the v2 front page: 50 stories of
Thursday 19 November 2026, 1024x1024) byte-for-byte into the output
directory.  Pure standard library only -- no Pillow, no fonts, no
network, no rendering -- so the program runs in the grader sandbox,
which has no third-party packages installed.

Output directory: first command-line argument, else the
``MAKEFUN_OUTPUT_DIR`` environment variable, else ``/output``.
Exits 0 on success (hash of the written file matches the source),
1 on any failure.
"""

import hashlib
import os
import sys

SOURCE_NAME = "entry.png"


def output_dir(argv):
    if len(argv) > 1:
        return argv[1]
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def sha256_hex(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_entry(out_dir):
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        print("missing source:", source, file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, SOURCE_NAME)
    source_hash = sha256_hex(source)
    with open(source, "rb") as src, open(dest, "wb") as dst:
        while True:
            chunk = src.read(1 << 20)
            if not chunk:
                break
            dst.write(chunk)
    written_hash = sha256_hex(dest)
    size = os.path.getsize(dest)
    source_size = os.path.getsize(source)
    if written_hash != source_hash or size != source_size:
        print("integrity mismatch after copy:", dest, file=sys.stderr)
        return 1
    print("wrote", dest, size, "bytes", written_hash[:16],
          "source", source_size, "bytes")
    return 0


def main(argv):
    try:
        return copy_entry(output_dir(argv))
    except OSError as exc:
        print("error:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
