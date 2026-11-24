#!/usr/bin/env python3
"""Stardew Delight icon: the cooking-pot loop from scene.py on the night-sky background.

  python dev/art/make_icon.py

Writes
  docs/icon-animated.gif   Modrinth / CurseForge animated icon, 256 px (x4), must stay <= 256 KiB
  docs/icon-animated.webp  the same loop, lossless WebP
  docs/icon-512.png        still (frame scene.STILL) at x8
  src/main/resources/stardewdelight_logo.png   the in-game mod logo, still at x2 (128 px)
  dev/art/out/contact.png, contact_96.png      every frame, for review
"""
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gifkit  # noqa: E402
import scene  # noqa: E402

ROOT = HERE.parent.parent
DOCS = ROOT / "docs"
OUT = HERE / "out"
MOD_LOGO = ROOT / "src/main/resources/stardewdelight_logo.png"
GIF_SCALE, PNG_SCALE, MOD_SCALE = 4, 8, 2
GIF_LIMIT = 256 * 1024


def up(im, s):
    return im.resize((im.width * s, im.height * s), Image.NEAREST)


def main():
    frames = [scene.compose(i) for i in range(scene.FRAMES)]
    DOCS.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    gif = DOCS / "icon-animated.gif"
    big = [up(f, GIF_SCALE) for f in frames]
    colours = gifkit.write_gif(big, gif, scene.FPS)
    gifkit.write_webp(big, DOCS / "icon-animated.webp", scene.FPS)
    still = frames[scene.STILL]
    up(still, PNG_SCALE).save(DOCS / "icon-512.png", optimize=True)
    up(still, MOD_SCALE).save(MOD_LOGO, optimize=True)
    still.save(OUT / "icon-still-64.png")
    gifkit.sheet(frames, 128).save(OUT / "contact.png")
    gifkit.sheet(frames, 96).save(OUT / "contact_96.png")
    size = gif.stat().st_size
    print(f"{gif.relative_to(ROOT)}: {size / 1024:.1f} KiB, {len(frames)} frames, {colours} colours "
          f"({'OK' if size <= GIF_LIMIT else 'OVER'} the 256 KiB icon limit)")
    print(f"webp {(DOCS / 'icon-animated.webp').stat().st_size / 1024:.1f} KiB; still = frame {scene.STILL}")
    if size > GIF_LIMIT:
        sys.exit(1)


if __name__ == "__main__":
    main()
