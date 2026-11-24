#!/usr/bin/env python3
"""Stardew Delight description art in the Profet page style: section headers, the divider and the promo tile.

  python dev/art/make_desc.py

docs/desc/title-<section>.png/.webp  1536x88 section headers (x4 pixel art, 384x22 texels): a wooden shelf plank with
                                     a dish from the mod at each end and a night-sky plaque in the middle carrying the
                                     section name in the title lettering
docs/desc/divider.png/.webp          1536x80: the plank with a dish at each end and a gold star in the middle
docs/promo-tile.png/.gif/.webp       768x352 tile (x4, 192x88 texels) for "more mods" lists: the animated pot, the
                                     title, the tagline and a badge

Everything is drawn at 1 texel = 1 pixel and scaled up with nearest neighbour. The dishes are read from the mod's
item textures, so re-run this after redrawing them.
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
from make_banner import ACCENT, GOLD, GREEN, TAGLINE  # noqa: E402

ROOT = HERE.parent.parent
DOCS = ROOT / "docs"
DESC = DOCS / "desc"
OUT = HERE / "out"
SCALE = 4
W = 384                        # header width in texels (1536 px)

INK, NAVY, RING = S.INK, S.NAVY, "#13182E"
DIM, GLINT, SHADE = "#4A5585", "#8F9AC8", "#2E3450"
HEAD = dict(bands=GOLD["bands"], extrude=[SHADE, SHADE])     # gold lettering casting a navy shadow on the plaque
WOOD = S.WOOD                  # deep .. light: 3A2216 5A3826 7A5238 9C7050 C89A64 E6C48E

# (file key, header text, dish on the left, dish on the right)
SECTIONS = [
    ("features", "FEATURES", "pizza", "pink_cake"),
    ("buffs", "BUFFS", "triple_shot_espresso", "lucky_lunch"),
    ("recipes", "RECIPES", "pumpkin_soup", "salad"),
    ("how-to-use", "HOW TO USE", "omelet", "pancakes"),
    ("compatibility", "COMPATIBILITY", "fish_taco", "maki_roll"),
    ("installation", "INSTALLATION", "survival_burger", "ginger_ale"),
    ("good-to-know", "GOOD TO KNOW", "strange_bun", "miners_treat"),
    ("credits", "CREDITS", "cookie", "chocolate_cake"),
    ("support", "SUPPORT", "crab_cakes", "pumpkin_pie"),
    ("license", "LICENSE", "maple_bar", "poppyseed_muffin"),
]
DIVIDER = ("fruit_salad", "blueberry_tart")

STAR = ["......#......",
        ".....###.....",
        ".....###.....",
        "....#####....",
        "#############",
        ".###########.",
        "..#########..",
        "...#######...",
        "...#######...",
        "..####.####..",
        "..###...###..",
        ".##.......##."]
STAR_BANDS = ["#FFF6C2", "#FFF6C2", "#FFE680", "#FFE680", "#FFE680", "#FFD04A", "#FFD04A", "#FFD04A", "#F5A623",
              "#F5A623", "#F5A623", "#F5A623"]


def C(h):
    return S.C(h)


def outlined(im, ink=INK):
    """Crop to the opaque pixels and add a one-texel ink outline (8 neighbours) around them."""
    im = im.crop(im.getbbox())
    out = Image.new("RGBA", (im.width + 2, im.height + 2), (0, 0, 0, 0))
    solid = {(x, y) for y in range(im.height) for x in range(im.width) if im.getpixel((x, y))[3] > 0}
    for x, y in solid:
        for dx, dy in pa.N8:
            if (x + dx, y + dy) not in solid:
                out.putpixel((x + dx + 1, y + dy + 1), C(ink))
    out.alpha_composite(im, (1, 1))
    return out


def star():
    im = Image.new("RGBA", (len(STAR[0]), len(STAR)), (0, 0, 0, 0))
    for y, row in enumerate(STAR):
        for x, ch in enumerate(row):
            if ch == "#":
                im.putpixel((x, y), C(STAR_BANDS[y]))
    im.putpixel((6, 1), C("#FFFFFF"))
    im.putpixel((5, 4), C("#FFFFFF"))
    return outlined(im)


def plank(im, x0, x1, y0):
    """The shelf: 7 rows (outline, light edge, three rows of grain, shadow, outline) from x0 to x1 inclusive.

    Planks are 28 texels long with a dark seam, a lit bevel and a nail either side; the pattern is anchored to the
    image, so every header shows the same boards."""
    rows = [INK, WOOD[4], WOOD[3], WOOD[3], WOOD[3], WOOD[2], INK]
    for x in range(x0, x1 + 1):
        for k, c in enumerate(rows):
            im.putpixel((x, y0 + k), C(c))
    for x in range(x0, x1 + 1):
        if x % 28 == 0:
            for k in range(1, 6):
                im.putpixel((x, y0 + k), C(WOOD[1]))
            if x + 1 <= x1:
                im.putpixel((x + 1, y0 + 1), C(WOOD[5]))
            for nx in (x - 3, x + 3):
                if x0 <= nx <= x1:
                    im.putpixel((nx, y0 + 3), C(S.IRON[4]))
                    im.putpixel((nx, y0 + 4), C(WOOD[1]))
    # grain: a few dashes per board, the same on every header
    for board in range(x0 // 28, x1 // 28 + 1):
        rnd = random.Random(board * 104729 + 7)
        for _ in range(3):
            row = rnd.choice((2, 3, 3, 4))
            start = board * 28 + rnd.randrange(6, 18)
            for x in range(start, start + rnd.randrange(3, 8)):
                if x0 <= x <= x1 and x % 28 not in (0, 25, 26, 27, 1, 2, 3, 4):
                    im.putpixel((x, y0 + row), C(WOOD[2]))
    return im


def twinkle(im, x, y, big):
    if big:
        im.putpixel((x, y), C(GLINT))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            im.putpixel((x + dx, y + dy), C(DIM))
    else:
        im.putpixel((x, y), C(DIM))


def panel(im, x0, y0, x1, y1, fill, outline=INK, ring=RING, r=2, thick=True):
    """Rounded pixel plaque: stepped corners of radius r with a darker inner ring at the corners (Profet style).

    thick=True draws the two-texel diagonal corner steps of the headers and tiles; False gives the plain one-texel steps
    of the badge."""
    for y in range(y0, y1 + 1):
        k = min(y - y0, y1 - y)          # distance from the nearest horizontal edge
        for x in range(x0, x1 + 1):
            j = min(x - x0, x1 - x)      # distance from the nearest vertical edge
            if k == 0:
                c = outline if j >= r else None
            elif k <= r and thick:
                lo = r - k
                c = None if j < lo else outline if j <= lo + 1 else ring if j == lo + 2 else fill
            elif k < r:
                lo = r - k
                c = None if j < lo else outline if j == lo else fill
            else:
                c = outline if j == 0 else (ring if (thick and j == 1 and k == r + 1) else fill)
            if c:
                im.putpixel((x, y), C(c))
    return im


def header(text, left, right, h=22):
    im = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    cy = h // 2
    lcap, rcap = outlined(S.dish(left)), outlined(S.dish(right))
    lx, rx = 1, W - 1 - rcap.width
    plank(im, lx + lcap.width // 2, rx + rcap.width // 2, cy - 3)
    im.alpha_composite(lcap, (lx, cy - lcap.height // 2))
    im.alpha_composite(rcap, (rx, cy - rcap.height // 2))
    if text:
        label = pa.title_sprite(text, HEAD, INK)
        tx = (W - label.width) // 2
        x0, x1 = tx - 11, tx + label.width - 1 + 11
        panel(im, x0, 1, x1, h - 2, NAVY)
        twinkle(im, x1 - 7, 5, True)
        twinkle(im, x0 + 8, 12, True)
        twinkle(im, x0 + 4, 15, False)
        twinkle(im, x1 - 8, 12, False)
        im.alpha_composite(label, (tx, 4))
    return im


def divider():
    im = header(None, *DIVIDER, h=20)
    s = star()
    im.alpha_composite(s, ((W - s.width) // 2, 10 - s.height // 2))
    return im


# --------------------------------------------------------------------------- promo tile
TW, TH = 192, 88
TILE_ART = (8, 12)
TILE_TEXT_X = 78


def tile_sky(frame, n=scene.FRAMES):
    im = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    panel(im, 0, 0, TW - 1, TH - 1, NAVY, r=3)
    rnd = random.Random(2024)
    taken = set()
    for _ in range(30):
        x, y = rnd.randrange(4, TW - 4), rnd.randrange(4, TH - 4)
        if (x // 5, y // 5) in taken or (TILE_TEXT_X - 2 <= x < 184 and 12 <= y < 76) or (x < 74 and y > 10):
            continue
        taken.add((x // 5, y // 5))
        im.putpixel((x, y), C(S.SKY_DIM if rnd.random() < 0.7 else S.SKY_MID))
    twinkles = [(150, 8), (178, 30), (96, 80), (184, 70), (64, 6), (16, 80)]
    for i, (x, y) in enumerate(twinkles):
        ph = (frame + i * n // len(twinkles)) % n
        S.twinkle(im, x, y, ph < n // 3)
    return im


def badge(text):
    """Dark pill with white lettering at x3 (it sits on the 4 px grid, the lettering on a 3 px one), full-res RGBA."""
    label = pa.scaled(pa.label_sprite(text, "#FFFFFF", "#000000"), 3)
    units = -(-(label.width + 32) // SCALE)
    pill = Image.new("RGBA", (units, 13), (0, 0, 0, 0))
    panel(pill, 0, 0, units - 1, 12, "#0F1325", r=2, thick=False)
    big = pa.scaled(pill, SCALE)
    big.alpha_composite(label, ((big.width - label.width) // 2, SCALE + (44 - label.height) // 2))
    return big


def tile_frames():
    top = pa.title_sprite("STARDEW", GOLD, INK)
    main = pa.title_sprite("DELIGHT", GREEN, INK)
    tag = pa.scaled(pa.label_sprite(TAGLINE, lambda i: ACCENT if i > 9 else "#FFFFFF", INK), 3)
    pill = badge("FARMER'S DELIGHT ADD-ON")
    frames = []
    for i in range(scene.FRAMES):
        sky = tile_sky(i)
        sky.alpha_composite(top, (TILE_TEXT_X, 15))
        sky.alpha_composite(main, (TILE_TEXT_X, 30))
        under, art = scene.art_layers(i)
        sky.alpha_composite(under, TILE_ART)
        sky.alpha_composite(art, TILE_ART)
        big = pa.scaled(sky, SCALE)
        big.alpha_composite(tag, (TILE_TEXT_X * SCALE, 48 * SCALE))
        big.alpha_composite(pill, (TILE_TEXT_X * SCALE - 4, 60 * SCALE))
        frames.append(big)
    return frames


def save_static(im, stem):
    big = pa.scaled(im, SCALE)
    big.save(stem.with_suffix(".png"), optimize=True)
    big.save(stem.with_suffix(".webp"), lossless=True, method=6)
    return big


def main():
    DESC.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(exist_ok=True)
    natives = []
    for key, text, left, right in SECTIONS:
        im = header(text, left, right)
        save_static(im, DESC / f"title-{key}")
        natives.append(im)
    div = divider()
    save_static(div, DESC / "divider")
    natives.append(div)
    print(f"docs/desc: {len(SECTIONS)} headers + divider")

    frames = tile_frames()
    alpha = frames[scene.STILL].getchannel("A")
    frames[scene.STILL].save(DOCS / "promo-tile.png", optimize=True)
    key = alpha.point(lambda v: 255 if v < 128 else 0)
    gif = DOCS / "promo-tile.gif"
    colours = gifkit.write_gif([f.convert("RGB") for f in frames], gif, scene.FPS, key_mask=key)
    gifkit.write_webp(frames, DOCS / "promo-tile.webp", scene.FPS)
    print(f"docs/promo-tile.png; .gif {gif.stat().st_size / 1024:.0f} KiB ({colours} colours); "
          f".webp {(DOCS / 'promo-tile.webp').stat().st_size / 1024:.0f} KiB")

    # native-resolution contact sheet for review
    hsum = sum(n.height + 2 for n in natives)
    sheet = Image.new("RGBA", (W, hsum + TH + 2), (40, 44, 52, 255))
    y = 0
    for n in natives:
        sheet.alpha_composite(n, (0, y))
        y += n.height + 2
    small = frames[scene.STILL].resize((TW, TH), Image.NEAREST)
    sheet.alpha_composite(small, (0, y))
    sheet.save(OUT / "desc_preview.png")


if __name__ == "__main__":
    main()
