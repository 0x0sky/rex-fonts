'''Validate licensing metadata on a ReX-modified font.'''

from fontTools.ttLib import TTFont

try:
    from tools.license_metadata import (
        LICENSE_URL,
        REX_FAMILY,
        REX_FULL_NAME,
        REX_POSTSCRIPT_NAME,
    )
except ModuleNotFoundError as error:
    if error.name != "tools":
        raise
    from license_metadata import (
        LICENSE_URL,
        REX_FAMILY,
        REX_FULL_NAME,
        REX_POSTSCRIPT_NAME,
    )

PRIMARY_NAME_IDS = (1, 3, 4, 6, 16, 18, 21)
RESERVED_TOKENS = ("STIX", "TM Math")


def values(font, name_id):
    return [record.toUnicode() for record in font["name"].names if record.nameID == name_id]


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def check(path):
    font = TTFont(path, recalcBBoxes=False, recalcTimestamp=False)

    for name_id in PRIMARY_NAME_IDS:
        for value in values(font, name_id):
            require(
                not any(token.lower() in value.lower() for token in RESERVED_TOKENS),
                "Reserved source name remains in primary name record {}: {!r}".format(name_id, value),
            )

    require(REX_FAMILY in values(font, 1), "Missing ReX Math family name")
    require(REX_FULL_NAME in values(font, 4), "Missing ReX Math full name")
    require(REX_POSTSCRIPT_NAME in values(font, 6), "Missing ReXMath PostScript name")

    licenses = values(font, 13)
    require(
        any("SIL Open Font License" in value and "Version 1.1" in value for value in licenses),
        "Missing SIL OFL 1.1 metadata",
    )
    require(LICENSE_URL in values(font, 14), "Missing OFL URL metadata")

    descriptions = values(font, 10)
    require(
        any("Modified Version" in value and "STIX Two Math 2.0.0" in value for value in descriptions),
        "Missing source/modification attribution",
    )

    copyrights = values(font, 0)
    require(
        any("STI Pub" in value for value in copyrights),
        "Original STIX copyright notice was not preserved",
    )

    if "OS/2" in font:
        require(font["OS/2"].fsType == 0, "OS/2 embedding restrictions conflict with OFL")

    if "CFF " in font:
        cff = font["CFF "].cff
        require(cff.fontNames == [REX_POSTSCRIPT_NAME], "CFF font name is not ReXMath")
        top_dict = cff.topDictIndex[0]
        require(top_dict.FamilyName == REX_FAMILY, "CFF family name is not ReX Math")
        require(top_dict.FullName == REX_FULL_NAME, "CFF full name is not ReX Math")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("font")
    args = parser.parse_args()
    check(args.font)
    print("license metadata OK:", args.font)
