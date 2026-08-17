#!/usr/bin/env python3
"""Verify redistribution metadata for generated ReX font binaries."""

import argparse
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

from tools.font_metadata import decoded_name_records, policy_for_path, primary_names


_LEGAL_NAME_IDS = (0, 7, 13, 14)


def verify(path: str) -> None:
    policy = policy_for_path(path)
    if policy is None:
        raise ValueError("no font metadata policy is defined for {!r}".format(path))

    font = TTFont(path, recalcBBoxes=False, recalcTimestamp=False, lazy=True)

    expected = {
        1: policy.family_name,
        2: policy.subfamily_name,
        4: policy.full_name,
        6: policy.postscript_name,
        16: policy.family_name,
        17: policy.subfamily_name,
        18: policy.full_name,
        21: policy.family_name,
        22: policy.subfamily_name,
    }
    for name_id, value in expected.items():
        actual = decoded_name_records(font["name"], name_id)
        if not actual or any(item != value for item in actual):
            raise ValueError(
                "name ID {} must be {!r}; got {!r}".format(name_id, value, actual)
            )

    primary = primary_names(font)
    if any("STIX" in value or "TM Math" in value for value in primary):
        raise ValueError(
            "modified font still exposes a protected/upstream identity: {!r}".format(
                primary
            )
        )

    source_path = Path("master") / policy.source_filename
    source = TTFont(
        str(source_path),
        recalcBBoxes=False,
        recalcTimestamp=False,
        lazy=True,
    )
    for name_id in _LEGAL_NAME_IDS:
        expected_legal = decoded_name_records(source["name"], name_id)
        actual_legal = decoded_name_records(font["name"], name_id)
        if set(actual_legal) != set(expected_legal):
            raise ValueError(
                "legal name ID {} differs from source {!r}: {!r} != {!r}".format(
                    name_id, source_path, actual_legal, expected_legal
                )
            )

    if not any(
        policy.copyright_marker in value
        for value in decoded_name_records(font["name"], 0)
    ):
        raise ValueError("upstream copyright metadata is missing")
    if not any(
        policy.license_marker in value
        for value in decoded_name_records(font["name"], 13)
    ):
        raise ValueError("upstream license metadata is missing")

    if "OS/2" in font and font["OS/2"].fsType != 0:
        raise ValueError(
            "font has restrictive OS/2 embedding flags: fsType={}".format(
                font["OS/2"].fsType
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fonts", nargs="+")
    args = parser.parse_args()

    failures = []
    for path in args.fonts:
        try:
            verify(path)
            print("{}: metadata OK".format(path))
        except Exception as error:
            failures.append("{}: {}".format(path, error))

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
