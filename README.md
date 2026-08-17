## Modifying fonts for ReX

This assumes that the font is an OpenType math font with a Math table.

- Run `python3 rexify.py` on the font. This will:
  - Place inaccessible glyphs in a CMAP table.
  - Generate glyph metrics for each glyph required for ReX.
  - For bundled fonts with an explicit redistribution policy, assign a
    distinct ReX font identity while preserving upstream legal metadata.

- Open FontForge, and re-encode to ISO 10646-1 (Unicode, Full). This will
  modify the glyph indices, optimizing the CMAP tables.

- Do codegen.

## Font licensing

`rexify.py` modifies font binaries. Modified fonts must continue to follow
the license of their source font.

For bundled STIX Two Math 2.0.0, the generated font is named `ReX Math`
instead of retaining the upstream primary font identity. The source
copyright, trademark and SIL Open Font License metadata are preserved.
The original STIX license document remains at
`master/STIX_2.0.0_license.pdf`.

See `LICENSES.md` and `FONTLOG.md` for redistribution and modification
details. `tools/verify_font_metadata.py` checks the generated STIX2 artifact.

## Open issues

Some work that still needs to be done:

- Generate a whitelist of symbols needed for ReX. This would require
  keeping track of all the glyphs required in the variants table.
