#!/usr/bin/env python3
"""Showcase clip for the description: the whole Stardew Delight cookbook filling up, dish by dish.

  python dev/art/make_clips.py

docs/clips/cookbook.gif / .webp  768x432 (x3 pixel art, 256x144 texels): every dish texture of the mod drops into a
                                 13x6 grid with a sparkle while the counter runs to the total, holds, then the shelf
                                 clears row by row in puffs of steam and the loop starts again.
"""
import random
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gifkit  # noqa: E402
import pa  # noqa: E402
import sprites as S  # noqa: E402
from make_banner import GOLD  # noqa: E402
from make_desc import NAVY, outlined, panel  # noqa: E402

ROOT = HERE.parent.parent
CLIPS = ROOT / "docs" / "clips"
W, H, SCALE, FPS = 256, 144, 3, 25
COLS, CELL = 13, 18
GRID_Y = 30
HOLD, CLEAR_STEP, EMPTY = 50, 3, 8


def dishes():
    return sorted(p.stem for p in S.ITEMS.glob("*.png"))


def background():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    panel(im, 0, 0, W - 1, H - 1, NAVY, r=3)
    rnd = random.Random(78)
    for _ in range(40):
        x, y = rnd.randrange(4, W - 4), rnd.randrange(4, H - 4)
        if GRID_Y - 4 <= y:
            continue
        im.putpixel((x, y), S.C(S.SKY_DIM if rnd.random() < 0.7 else S.SKY_MID))
    for x in range(8, W - 8):          # a faint shelf line under every row
        for r in range(6):
            y = GRID_Y + r * CELL + 17
            if y < H - 3 and (x // 2) % 2 == 0:
                im.putpixel((x, y), S.C("#262C52"))
    return im


def main():
    names = dishes()
    sprites = [outlined(S.dish(n)) for n in names]
    rows = (len(names) + COLS - 1) // COLS
    x0 = (W - COLS * CELL) // 2
    cells = [(x0 + (k % COLS) * CELL, GRID_Y + (k // COLS) * CELL) for k in range(len(names))]
    title = pa.title_sprite("COOKBOOK", GOLD, S.INK)
    bg = background()
    bg.alpha_composite(title, (x0, 9))

    fill = len(names) + 4
    clear0 = fill + HOLD
    total = clear0 + rows * CLEAR_STEP + 6 + EMPTY
    drop = [-4, -2, 1, 0]
    frames = []
    for f in range(total):
        im = bg.copy()
        shown = min(len(names), f + 1) if f < clear0 else len(names)
        for k, spr in enumerate(sprites):
            row = k // COLS
            gone_at = clear0 + row * CLEAR_STEP
            if k > f or f >= gone_at:
                continue
            age = f - k
            cx, cy = cells[k]
            dy = drop[age] if age < len(drop) else 0
            im.alpha_composite(spr, (cx + (CELL - spr.width) // 2, cy + (CELL - 1 - spr.height) + dy))
            if age < 3:
                s = S.star((1, 2, 0)[age])
                im.alpha_composite(s, (cx + 13 - s.width // 2, cy + 1 - s.height // 2))
        for row in range(rows):              # steam puffs where a row has just cleared
            a = f - (clear0 + row * CLEAR_STEP)
            if 0 <= a < 6:
                p = S.puff((1, 2, 2, 1, 0, 0)[a])
                for c in range(0, COLS, 2):
                    cx, cy = x0 + c * CELL + 9, GRID_Y + row * CELL + 10 - a
                    im.alpha_composite(p, (cx - p.width // 2, cy - p.height // 2))
        if f >= clear0:
            shown = sum(1 for k in range(len(names)) if f < clear0 + (k // COLS) * CLEAR_STEP)
        counter = pa.label_sprite(f"{shown}/{len(names)}", "#FFFFFF", S.INK)
        im.alpha_composite(counter, (x0 + COLS * CELL - counter.width, 12))
        frames.append(pa.scaled(im, SCALE))

    CLIPS.mkdir(parents=True, exist_ok=True)
    alpha = frames[0].getchannel("A")
    key = alpha.point(lambda v: 255 if v < 128 else 0)
    gif = CLIPS / "cookbook.gif"
    # 78 textures bring ~650 colours: map every frame onto one shared 254-colour palette (no dithering) for the GIF
    probe = [frames[clear0 - 1], frames[clear0 + 1], frames[2]]
    mosaic = Image.new("RGB", (sum(p.width for p in probe), probe[0].height))
    x = 0
    for p in probe:
        mosaic.paste(p.convert("RGB"), (x, 0))
        x += p.width
    pal = mosaic.quantize(254, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    rgb = [fr.convert("RGB").quantize(palette=pal, dither=Image.Dither.NONE).convert("RGB") for fr in frames]
    colours = gifkit.write_gif(rgb, gif, FPS, key_mask=key)
    gifkit.write_webp(frames, CLIPS / "cookbook.webp", FPS)
    frames[clear0 - 1].save(HERE / "out" / "cookbook_still.png")
    print(f"docs/clips/cookbook.gif {gif.stat().st_size / 1024:.0f} KiB, {len(frames)} frames, {colours} colours; "
          f".webp {(CLIPS / 'cookbook.webp').stat().st_size / 1024:.0f} KiB")


if __name__ == "__main__":
    main()
