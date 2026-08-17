#!/usr/bin/env python3
"""Normalize metadata of an already-generated ReX font binary."""

import argparse

from fontTools.ttLib import TTFont

from tools.font_metadata import apply_identity, policy_for_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("font", help="generated ReX OTF to normalize in place")
    args = parser.parse_args()

    policy = policy_for_path(args.font)
    if policy is None:
        parser.error("no font metadata policy is defined for {!r}".format(args.font))

    font = TTFont(
        args.font,
        recalcBBoxes=False,
        recalcTimestamp=False,
        lazy=False,
    )
    apply_identity(font, policy)
    font.save(args.font, reorderTables=False)


if __name__ == "__main__":
    main()
