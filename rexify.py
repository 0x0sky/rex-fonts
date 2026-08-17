'''
rexify.py

Prepare an OpenType font for use with ReX. Rexify will look for glyphs that
are not accessible from a CMAP, place those glyphs into a Private Usage Area
and modify the CMAPs to include these glyphs. This is necessary for when
you want to render math in SVG by referring to glyphs from their usv.
'''

import os
from fontTools.ttLib import TTFont
from tools.accessible import make_accessible
from tools.constants import gen_constants
from tools.glyphs import gen_glyphs
from tools.kerning import gen_kerning
from tools.license_metadata import apply_rex_license_metadata
from tools.symbols import gen_symbols
from tools.variants import gen_variants

# TODO: Delete undesired glyphs.


def rexify(font, out):
    '''
    Rexify font.

    This will take all inaccessible glyphs from the font,
    place them in a PUA, and modify the CMAPs so that these
    glyphs are publicly accessible.

    This will also apply metadata for the modified ReX font and
    generate the required tables for ReX.
    '''

    # Make glyphs accessible.
    ttfont = TTFont(font, recalcBBoxes=False, recalcTimestamp=False)
    make_accessible(ttfont)
    apply_rex_license_metadata(ttfont)
    ttfont.save(out + os.path.basename(font), reorderTables=False)

    gen_constants(ttfont, out)
    gen_glyphs(ttfont, out)
    gen_kerning(ttfont, out)
    gen_symbols(ttfont, out)
    gen_variants(ttfont, out)


if __name__ == "__main__":
    import sys

    USAGE = "usage: rexify.py in.otf out/\n" \
            "`rexify.py` will gather all glyphs from `in.otf` that aren't accessible " \
            "from a CMAP and place them into Private Use Area codepoints. Then " \
            "`rexify.py` will update the CMAPs to make these glyphs accessible."

    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(2)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(USAGE)
        sys.exit(0)

    FONT = sys.argv[1]
    OUT = sys.argv[2]

    if not os.path.exists(OUT):
        print("Creating directory:", OUT)
        os.makedirs(OUT)

    print("Rexifying:", FONT)
    rexify(FONT, OUT)
    print("Finished rexifying:", FONT)
