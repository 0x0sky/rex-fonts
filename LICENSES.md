# Bundled font notices

## STIX Two Math 2.0.0

Source font: `master/STIX2Math.otf`.

Generated ReX font: `out/stix2/rex-stix2.otf`.

The bundled STIX source is distributed under the SIL Open Font License 1.1.
Its original license document is retained at
`master/STIX_2.0.0_license.pdf`, and its copyright, trademark and license
records remain embedded in the generated font.

`rexify.py` modifies the font by adding CMAP mappings for otherwise
inaccessible math glyphs. The generated artifact therefore uses the distinct
user-facing name `ReX Math`. See `FONTLOG.md` for the modification record.

XITS and Latin Modern Math are separate bundled sources with their own
upstream terms. This change does not modify their generated artifacts.
