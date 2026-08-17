'''OFL-aware metadata for fonts modified by ReX.'''

import os
import tempfile

from fontTools.ttLib import TTFont

REX_FAMILY = "ReX Math"
REX_FULL_NAME = "ReX Math"
REX_POSTSCRIPT_NAME = "ReXMath"
REX_UNIQUE_ID = "ReX: ReX Math: 1.0"
LICENSE_DESCRIPTION = (
    "This Font Software is licensed under the SIL Open Font License, "
    "Version 1.1. See the accompanying STIX-2.0.0-OFL.txt."
)
LICENSE_URL = "https://openfontlicense.org"
DESCRIPTION = (
    "ReX Math is a Modified Version of STIX Two Math 2.0.0 prepared for ReX. "
    "The ReX modification exposes otherwise inaccessible glyphs through "
    "Private Use Area cmap entries. STIX Two Math is acknowledged as the "
    "source; original copyright and trademark notices are retained."
)

# User-facing and identifier names must not retain STIX 2.0.0 Reserved Font
# Names on this Modified Version. We only add optional typographic/WWS names
# when the source already exposes those records.
_REQUIRED_NAMES = {
    1: REX_FAMILY,
    3: REX_UNIQUE_ID,
    4: REX_FULL_NAME,
    6: REX_POSTSCRIPT_NAME,
}
_OPTIONAL_NAMES = {
    16: REX_FAMILY,
    18: REX_FULL_NAME,
    21: REX_FAMILY,
}


def _set_name(name_table, name_id, value, required=False):
    targets = {
        (record.platformID, record.platEncID, record.langID)
        for record in name_table.names
        if record.nameID == name_id
    }

    if not targets and required:
        targets.add((3, 1, 0x409))

    for platform_id, encoding_id, language_id in targets:
        name_table.setName(
            value,
            name_id,
            platform_id,
            encoding_id,
            language_id,
        )


def apply_rex_license_metadata(font):
    '''Apply naming and OFL metadata to a ReX-modified font in memory.'''

    name_table = font["name"]

    for name_id, value in _REQUIRED_NAMES.items():
        _set_name(name_table, name_id, value, required=True)

    for name_id, value in _OPTIONAL_NAMES.items():
        _set_name(name_table, name_id, value)

    _set_name(name_table, 10, DESCRIPTION, required=True)
    _set_name(name_table, 13, LICENSE_DESCRIPTION, required=True)
    _set_name(name_table, 14, LICENSE_URL, required=True)

    # OFL permits embedding. Keep the generated derivative free of OS/2
    # embedding restrictions that would contradict that grant.
    if "OS/2" in font:
        font["OS/2"].fsType = 0

    # STIX Two Math is CFF-flavoured. The CFF names are independent from the
    # OpenType name table and therefore must be changed as well.
    if "CFF " in font:
        cff = font["CFF "].cff
        cff.fontNames = [REX_POSTSCRIPT_NAME]
        top_dict = cff.topDictIndex[0]
        top_dict.FamilyName = REX_FAMILY
        top_dict.FullName = REX_FULL_NAME


def update_font(path):
    '''Apply ReX metadata to an existing font atomically.'''

    path = os.path.abspath(path)
    font = TTFont(path, recalcBBoxes=False, recalcTimestamp=False)
    apply_rex_license_metadata(font)

    directory = os.path.dirname(path)
    fd, temporary = tempfile.mkstemp(prefix=".rex-license-", suffix=".otf", dir=directory)
    os.close(fd)
    try:
        font.save(temporary, reorderTables=False)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Apply OFL-aware ReX metadata to a modified OpenType font."
    )
    parser.add_argument("font")
    args = parser.parse_args()
    update_font(args.font)
