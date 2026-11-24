#!/usr/bin/env python3
"""Stardew Delight description banner (3:1, 1536x512) around the cooking-pot loop from scene.py.

Layers: the night-sky background at x8 (192x64 texels, stepped pixel corners), the pot scene at x7 with its top-left at
ART_ORIGIN, the title "STARDEW" at x6, "DELIGHT" at x10 and the tagline at x6 (pa.py lettering).

  python dev/art/make_banner.py

Writes docs/banner.png (still), docs/banner.gif (whole loop, exact palette, transparent corners, <= 5 MiB) and
docs/banner.webp (the same loop, lossless).
"""
import random
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gifkit  # noqa: E402
import pa  # noqa: E402
import scene  # noqa: E402
import sprites as S  # noqa: E402

ROOT = HERE.parent.parent
DOCS = ROOT / "docs"
W, H, GRID = 1536, 512, 8
ART_SCALE = 7
ART_ORIGIN = (1232 - 32 * ART_SCALE, 256 - 32 * ART_SCALE)
GIF_LIMIT = 5 * 1024 * 1024

GOLD = dict(bands=["#FFF6C2", "#FFE680", "#FFE680", "#FFE680", "#FFD04A", "#FFD04A", "#FFD04A", "#F5A623", "#F5A623",
                   "#F5A623"], extrude=["#8A4B25", "#5E3018"])
GREEN = dict(bands=["#F2FFC0", "#C3EA6C", "#C3EA6C", "#C3EA6C", "#8ED14E", "#8ED14E", "#8ED14E", "#5BB23E", "#5BB23E",
                    "#5BB23E"], extrude=["#236B33", "#17492D"])
INK = "#0B0F20"
TAGLINE = "ONE POT. WHOLE VALLEY."
ACCENT = "#8ED14E"


def lettering():
    top = pa.title_sprite("STARDEW", GOLD, INK)
    main = pa.title_sprite("DELIGHT", GREEN, INK)
    tag = pa.label_sprite(TAGLINE, lambda i: ACCENT if i > 9 else "#FFFFFF", INK)
    return [(top, 6, (72, 97)), (main, 10, (70, 193)), (tag, 6, (74, 361))]


def sky(frame=0, n=scene.FRAMES):
    """192x64 night sky: navy, faint dots and a handful of twinkling stars away from the lettering."""
    im = Image.new("RGBA", (W // GRID, H // GRID), S.C(S.NAVY))
    rnd = random.Random(1987)
    taken = set()
    for _ in range(46):
        x, y = rnd.randrange(2, 190), rnd.randrange(2, 62)
        if (x // 4, y // 4) in taken:
            continue
        taken.add((x // 4, y // 4))
        im.putpixel((x, y), S.C(S.SKY_DIM if rnd.random() < 0.7 else S.SKY_MID))
    twinkles = [(98, 9), (112, 51), (180, 12), (8, 56), (186, 48), (60, 6), (104, 30), (150, 58)]
    for i, (x, y) in enumerate(twinkles):
        ph = (frame + i * n // len(twinkles)) % n
        S.twinkle(im, x, y, ph < n // 3)
    return im


def base(frame):
    out = pa.scaled(sky(frame), GRID)
    for img, s, pos in lettering():
        big = pa.scaled(img, s)
        out.alpha_composite(big, pos)
    return out


def frame(i, back=None):
    out = back.copy() if back is not None else base(i)
    under, top = scene.art_layers(i)
    out.alpha_composite(pa.scaled(under, ART_SCALE), ART_ORIGIN)
    out.alpha_composite(pa.scaled(top, ART_SCALE), ART_ORIGIN)
    return out


def main():
    corners = pa.stepped_corners(W, H)
    frames = []
    for i in range(scene.FRAMES):
        f = frame(i)
        frames.append(f.convert("RGB"))
    DOCS.mkdir(exist_ok=True)
    still = frames[scene.STILL].convert("RGBA")
    still.putalpha(corners)
    still.save(DOCS / "banner.png", optimize=True)
    gif = DOCS / "banner.gif"
    colours = gifkit.write_gif(frames, gif, scene.FPS, key_mask=corners.point(lambda v: 255 - v))
    rgba = []
    for f in frames:
        g = f.convert("RGBA")
        g.putalpha(corners)
        rgba.append(g)
    gifkit.write_webp(rgba, DOCS / "banner.webp", scene.FPS)
    size = gif.stat().st_size
    print(f"docs/banner.png (frame {scene.STILL}); docs/banner.gif {size / 1024:.0f} KiB, {len(frames)} frames, "
          f"{colours} colours ({'OK' if size <= GIF_LIMIT else 'OVER'} 5 MiB); "
          f"docs/banner.webp {(DOCS / 'banner.webp').stat().st_size / 1024:.0f} KiB")
    if size > GIF_LIMIT:
        sys.exit(1)


if __name__ == "__main__":
    main()
