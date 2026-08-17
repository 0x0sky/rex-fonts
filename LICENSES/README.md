# Licensing

This repository contains both third-party font software and ReX tooling. They
must not be treated as if they share one license automatically.

## STIX 2.0.0 font software

`master/STIX2Math.otf` originates from STIX 2.0.0 and is licensed under the
SIL Open Font License 1.1. The original distribution license is retained as
`master/STIX_2.0.0_license.pdf`; a text copy suitable for redistribution is
provided as `LICENSES/STIX-2.0.0-OFL.txt`.

STIX 2.0.0 reserved `STIX Fonts` and `TM Math`. ReX changes the source font's
cmap, so the generated font is a Modified Version under the OFL. Generated ReX
fonts therefore use the primary name `ReX Math` / PostScript name `ReXMath`,
while retaining the original copyright and trademark notices and explicitly
acknowledging STIX Two Math 2.0.0 as their source.

The generated font's OpenType metadata also embeds the OFL identification and
license URL, and its OS/2 embedding restriction bits are cleared to match the
OFL grant.

## ReX tooling

The OFL applies to the font software; it must not be used to imply a license
grant for unrelated Python tooling in this repository. This repository does
not currently contain an explicit software-license grant for that tooling.
Only the relevant copyright holder(s) can choose or confirm that license.

This separation is intentional: this change fixes redistribution of the
modified font without inventing licensing terms for upstream-authored code.
