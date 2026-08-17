## Modifying fonts for ReX

This assumes that the font is an OpenType math font with a Math table.

- Run `python3 rexify.py` on the font. This will:
  - Place inaccessible glyphs in a CMAP table.
  - Apply ReX naming and SIL OFL metadata to Modified Versions.
  - Generate glyph metrics for each glyph required for ReX.

- Open FontForge, and re-encode to ISO 10646-1 (Unicode, Full). This will
  modify the glyph indices, optimizing the CMAP tables.

- Do codegen.

## Font licensing

The bundled STIX 2.0.0 font software is distributed under the SIL Open Font
License 1.1. ReX modifies that font, so generated derivatives use the primary
name `ReX Math` rather than STIX Reserved Font Names, preserve the original
copyright/trademark notices, and carry OFL metadata.

See `LICENSES/README.md` and `LICENSES/STIX-2.0.0-OFL.txt`. The original STIX
2.0.0 license PDF remains at `master/STIX_2.0.0_license.pdf`.

The OFL does not automatically license the Python tooling in this repository;
that software-license grant remains an upstream-maintainer decision.

## Open issues

Some work that still needs to be done:
- Generate a whitelist of symbols needed for ReX. This would require
  keeping track of all the glyphs required in the variants table.
