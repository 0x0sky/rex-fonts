"""Font identity policies for ReX-modified font binaries.

The source font's copyright, trademark, authorship and license metadata are
preserved. Only user-facing identity fields are replaced so a modified font
cannot be mistaken for the upstream original.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple


_PRIMARY_NAME_IDS = frozenset({1, 2, 3, 4, 6, 16, 17, 18, 21, 22})


@dataclass(frozen=True)
class FontPolicy:
    source_filename: str
    output_filename: str
    family_name: str
    subfamily_name: str
    postscript_name: str
    source_family_marker: str
    copyright_marker: str
    license_marker: str

    @property
    def full_name(self) -> str:
        if self.subfamily_name == "Regular":
            return self.family_name
        return "{} {}".format(self.family_name, self.subfamily_name)


STIX2 = FontPolicy(
    source_filename="STIX2Math.otf",
    output_filename="rex-stix2.otf",
    family_name="ReX Math",
    subfamily_name="Regular",
    postscript_name="ReXMath-Regular",
    source_family_marker="STIX Two Math",
    copyright_marker="STI Pub Companies",
    license_marker="SIL Open Font License",
)

_POLICIES: Dict[str, FontPolicy] = {
    STIX2.source_filename: STIX2,
    STIX2.output_filename: STIX2,
}


def policy_for_path(path: str) -> Optional[FontPolicy]:
    """Return a known redistribution policy for an input/output font path."""
    return _POLICIES.get(Path(path).name)


def decoded_name_records(name_table, name_id: int) -> Tuple[str, ...]:
    """Return distinct Unicode strings stored for one OpenType name ID."""
    values = []
    for record in name_table.names:
        if record.nameID != name_id:
            continue
        try:
            value = record.toUnicode()
        except UnicodeDecodeError:
            continue
        if value not in values:
            values.append(value)
    return tuple(values)


def primary_names(font) -> Tuple[str, ...]:
    """Return unique user-facing identity strings from the OpenType name table."""
    values = []
    for name_id in sorted(_PRIMARY_NAME_IDS):
        for value in decoded_name_records(font["name"], name_id):
            if value not in values:
                values.append(value)
    return tuple(values)


def _set_name(name_table, name_id: int, value: str) -> None:
    # Remove every locale/platform copy first. Leaving a stale Mac or localized
    # record can make an upstream name reappear in font menus.
    name_table.names = [
        record for record in name_table.names if record.nameID != name_id
    ]

    # The bundled STIX2 font carries Windows and Macintosh name records.
    name_table.setName(value, name_id, 3, 1, 0x0409)
    name_table.setName(value, name_id, 1, 0, 0)


def apply_identity(font, policy: FontPolicy) -> None:
    """Apply a distinct ReX identity while preserving legal source metadata."""
    name_table = font["name"]

    copyright_before = decoded_name_records(name_table, 0)
    trademark_before = decoded_name_records(name_table, 7)
    license_before = decoded_name_records(name_table, 13)
    license_url_before = decoded_name_records(name_table, 14)

    if not any(policy.copyright_marker in value for value in copyright_before):
        raise ValueError(
            "source copyright metadata does not match the expected font policy"
        )
    if not any(policy.license_marker in value for value in license_before):
        raise ValueError(
            "source license metadata does not match the expected font policy"
        )

    versions = decoded_name_records(name_table, 5)
    source_version = versions[0] if versions else "source version"
    unique_id = "{}; {} modified for ReX".format(
        policy.postscript_name, source_version
    )

    replacements = {
        1: policy.family_name,
        2: policy.subfamily_name,
        3: unique_id,
        4: policy.full_name,
        6: policy.postscript_name,
        16: policy.family_name,
        17: policy.subfamily_name,
        18: policy.full_name,
        21: policy.family_name,
        22: policy.subfamily_name,
    }
    for name_id, value in replacements.items():
        _set_name(name_table, name_id, value)

    if decoded_name_records(name_table, 0) != copyright_before:
        raise AssertionError("copyright metadata changed while renaming the font")
    if decoded_name_records(name_table, 7) != trademark_before:
        raise AssertionError("trademark metadata changed while renaming the font")
    if decoded_name_records(name_table, 13) != license_before:
        raise AssertionError("license metadata changed while renaming the font")
    if decoded_name_records(name_table, 14) != license_url_before:
        raise AssertionError("license URL metadata changed while renaming the font")
