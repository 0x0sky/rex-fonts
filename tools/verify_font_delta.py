#!/usr/bin/env python3
"""Assert that license cleanup changed only OpenType identity metadata."""

import argparse
import sys

from fontTools.ttLib import TTFont


_ALLOWED_CHANGED_TABLES = {"name", "head"}


def verify_delta(before_path: str, after_path: str) -> None:
    before = TTFont(before_path, recalcBBoxes=False, recalcTimestamp=False, lazy=True)
    after = TTFont(after_path, recalcBBoxes=False, recalcTimestamp=False, lazy=True)

    before_tables = set(before.keys())
    after_tables = set(after.keys())
    if before_tables != after_tables:
        raise ValueError(
            "OpenType table set changed: {!r} != {!r}".format(
                sorted(before_tables), sorted(after_tables)
            )
        )

    changed = []
    for tag in sorted(before_tables - _ALLOWED_CHANGED_TABLES):
        if before.getTableData(tag) != after.getTableData(tag):
            changed.append(tag)

    if changed:
        raise ValueError(
            "non-metadata OpenType tables changed: {}".format(", ".join(changed))
        )

    print("{} -> {}: only name/head tables changed".format(before_path, after_path))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("before")
    parser.add_argument("after")
    args = parser.parse_args()

    try:
        verify_delta(args.before, args.after)
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
