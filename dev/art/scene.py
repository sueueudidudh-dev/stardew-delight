"""The animated hero shared by the icon, the banner and the promo tile: a copper cooking pot on a campfire.

Loop (3.84 s, 25 fps, 96 frames) on a 64x64 texel canvas, in three 32-frame pops, one dish each:
the lid rattles and lets out steam, pops up behind the pot, the dish shoots out of the stew to the top of the frame,
bursts into a sparkle, hovers, dives back in, and the lid clangs shut. Everything is drawn at 1 texel = 1 pixel and
scaled up with nearest neighbour, so every output is the same pixel art at a different size.
"""
import math
import random

from PIL import Image, ImageFilter

import sprites as S

FPS, POP = 25, 32
DISHES = ["pizza", "pink_cake", "salad"]
FRAMES = POP * len(DISHES)
STILL = POP + 16                    # pink cake at the top of its hop, sparkle fading
LID_BASE = (32.0, 30.5)             # the closed lid's base centre on the canvas
DISH_CX = 32
CLIP_Y = 33                         # dish pixels at or below this row are under the stew

EASE = {
    "lin": lambda u: u,
    "in": lambda u: u * u,
    "out": lambda u: 1 - (1 - u) ** 2,
    "smooth": lambda u: u * u * (3 - 2 * u),
    "step": lambda u: 0.0,
}


def track(f, keys, default=None):
    """keys [(frame, value[, ease into this key])]; holds before the first and after the last key."""
    if f <= keys[0][0]:
        return keys[0][1]
    for a, b in zip(keys, keys[1:]):
        if f < b[0]:
            u = (f - a[0]) / (b[0] - a[0])
            e = EASE[b[2] if len(b) > 2 else "smooth"](u)
            if isinstance(a[1], tuple):
                return tuple(x + (y - x) * e for x, y in zip(a[1], b[1]))
            return a[1] + (b[1] - a[1]) * e
    return keys[-1][1]


# lid (dx, dy, tilt in degrees): rattles, blows open to the upper right, hovers, drops back
LID_KEYS = [(0, (0, 0, 0)), (2, (0, -1, 0), "step"), (3, (0, 0, 0), "step"), (5, (1, -1, -3), "step"),
            (6, (0, 0, 0), "step"), (8, (0, 1, 0), "step"), (9, (2, -5, 8), "step"), (10, (6, -9, 18), "out"),
            (11, (10, -12, 26), "out"), (12, (12, -13, 31), "out"), (13, (12, -12, 28), "smooth"), (16, (12, -13, 30)),
            (19, (12, -12, 27)), (21, (12, -12, 28)), (22, (11, -11, 25), "in"), (24, (7, -7, 15), "in"),
            (26, (2, -2, 4), "in"), (27, (0, 0, 0), "in")]
LID_SQUASH = {8: (1.06, 0.88), 9: (0.94, 1.08), 10: (0.96, 1.04), 27: (1.12, 0.82), 28: (0.96, 1.06), 29: (1.02, 0.98)}
DISH_BOTTOM = [(9, 37), (10, 31, "out"), (11, 26, "out"), (12, 22, "out"), (13, 20, "out"), (15, 21, "smooth"),
               (17, 20), (19, 21), (21, 20), (22, 21), (23, 24, "in"), (24, 28, "in"), (25, 33, "in"), (26, 39, "in")]
DISH_SQUASH = {10: (0.88, 1.16), 11: (0.9, 1.12), 12: (0.94, 1.06), 15: (1.14, 0.86), 16: (0.94, 1.06),
               23: (0.94, 1.08), 24: (0.9, 1.12), 25: (0.88, 1.14)}

_cache = {}


def spr(name, *args):
    key = (name, args)
    if key not in _cache:
        _cache[key] = getattr(S, name)(*args) if name != "dish" else S.dish(*args)
    return _cache[key]


def paste(layer, img, at, scale=(1.0, 1.0), anchor=(0.5, 1.0)):
    """Paste img with its anchor point at `at` (texels); scale is snapped to whole texels."""
    w = max(1, round(img.width * scale[0]))
    h = max(1, round(img.height * scale[1]))
    if (w, h) != img.size:
        img = img.resize((w, h), Image.NEAREST)
    x = round(at[0] - anchor[0] * w)
    y = round(at[1] - anchor[1] * h)
    layer.alpha_composite(img, (x, y)) if 0 <= x and 0 <= y and x + w <= layer.width and y + h <= layer.height \
        else _paste_clipped(layer, img, x, y)


def _paste_clipped(layer, img, x, y):
    tmp = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    tmp.paste(img, (x, y), img)
    layer.alpha_composite(tmp)


def lid_pose(f):
    dx, dy, ang = track(f, LID_KEYS)
    sq = LID_SQUASH.get(f, (1.0, 1.0))
    raised = 9 <= f <= 26
    return round(dx), round(dy), int(round(ang)), sq, raised


def dish_pose(f):
    if not 9 < f < 26:
        return None
    return track(f, DISH_BOTTOM), DISH_SQUASH.get(f, (1.0, 1.0))


def fx_events(f):
    """[(sprite name, args, centre (x, y))] for the local frame of a pop."""
    ev = []
    # steam escaping under the rattling lid
    for start, (x, y) in ((2, (13, 31)), (5, (50, 31))):
        a = f - start
        if 0 <= a < 5:
            ev.append(("puff", ((0, 0, 1, 1, 0)[a],), (x + (a if x > 32 else -a) // 2, y - a * 2)))
    # the lid blows: a ring at the mouth and two clouds
    if 9 <= f <= 11:
        ev.append(("ring", ((5, 7, 9)[f - 9],), (32, 29)))
    for start, (x, y), side in ((9, (22, 28), -1), (10, (42, 28), 1)):
        a = f - start
        if 0 <= a < 8:
            ev.append(("puff", ((1, 2, 2, 2, 1, 1, 0, 0)[a],), (x + side * a // 2, y - a * 2)))
    # sparkle burst at the top of the hop, then twinkles around the dish
    if 15 <= f <= 18:
        ev.append(("star", ((1, 2, 1, 0)[f - 15],), (20, 7)))
    for start, (x, y) in ((17, (13, 15)), (19, (40, 2)), (21, (19, 19))):
        if 0 <= f - start < 2:
            ev.append(("star", ((0, 0)[f - start],), (x, y)))
    # the lid lands
    for (x, y) in ((14, 33), (50, 33)):
        a = f - 27
        if 0 <= a < 4:
            ev.append(("puff", ((1, 1, 0, 0)[a],), (x + (-a if x < 32 else a), y - a)))
    return ev


def bubbles(f):
    out = []
    if 9 <= f <= 25:
        for k, (x, y) in enumerate(((22, 32), (38, 33), (29, 33), (43, 32))):
            ph = (f + k * 2) % 6
            if ph < 3:
                out.append((ph, (x, y)))
    return out


def splash(f):
    """Stew drops thrown up when a dish dives back in."""
    out = []
    a = f - 26
    if 0 <= a < 4:
        for vx, vy in ((-2, -3), (2, -3), (-1, -4)):
            out.append((32 + vx * (a + 1), 31 + vy * (a + 1) + (a + 1) * a))
    return out


def embers(i):
    out = []
    for j in range(6):
        start = (j * 17) % FRAMES
        a = (i - start) % FRAMES
        if a < 14:
            rnd = random.Random(j)
            x = 14 + rnd.randrange(36)
            out.append((x + (1 if (a // 3) % 2 else 0), 50 - a, S.FIRE[3] if a < 6 else S.FIRE[1]))
    return out


def render(i):
    """(art RGBA, under RGBA) for global frame i."""
    pop, f = divmod(i % FRAMES, POP)
    art = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    dx, dy, ang, lsq, raised = lid_pose(f)
    lid_img = spr("lid_tilted", ang)
    lid_at = (LID_BASE[0] + dx, LID_BASE[1] + dy)
    lid_anchor = (S.LID_PIVOT[0] / lid_img.width, S.LID_PIVOT[1] / lid_img.height)
    if raised:
        paste(art, lid_img, lid_at, lsq, lid_anchor)
    k = (i // 2) % 4
    for layer in (spr("back_log"), spr("flames", k), spr("logs"), spr("pot_back")):
        art.alpha_composite(layer)
    for ph, (x, y) in bubbles(f):
        paste(art, spr("bubble", ph), (x, y), anchor=(0.5, 0.5))
    pose = dish_pose(f)
    if pose:
        bottom, dsq = pose
        layer = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        paste(layer, spr("dish", DISHES[pop]), (DISH_CX, bottom), dsq)
        clip = Image.new("L", (64, 64), 255)
        clip.paste(0, (14, CLIP_Y, 50, 64))
        layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", (64, 64), 0), clip))
        art.alpha_composite(layer)
    art.alpha_composite(spr("pot_front"))
    art.alpha_composite(spr("flames_front", k))
    if not raised:
        paste(art, lid_img, lid_at, lsq, lid_anchor)
    for (x, y) in splash(f):
        if 0 <= x < 64 and 0 <= y < 64:
            art.putpixel((x, y), S.C(S.SOUP[3]))
    for name, args, at in fx_events(f):
        paste(art, spr(name, *args), at, anchor=(0.5, 0.5))
    for x, y, c in embers(i):
        if 0 <= x < 64 and 0 <= y < 64 and art.getpixel((x, y))[3] == 0:
            art.putpixel((x, y), S.C(c))
    return art, spr("under_layer")


def compose(i, bg=None):
    """Background, light pool and shadow, a one-texel ink outline around the art, the art. RGB 64x64."""
    art, under = render(i)
    out = (bg.copy() if bg is not None else S.icon_bg(i, FRAMES)).convert("RGBA")
    out.alpha_composite(under)
    ink = Image.new("RGBA", art.size, S.C(S.INK))
    ink.putalpha(art.getchannel("A").point(lambda v: 255 if v else 0).filter(ImageFilter.MaxFilter(3)))
    out.alpha_composite(ink)
    out.alpha_composite(art)
    return out.convert("RGB")


def art_layers(i):
    """(under, ink+art) as separate RGBA layers, for placing the hero on a bigger background."""
    art, under = render(i)
    top = Image.new("RGBA", art.size, (0, 0, 0, 0))
    ink = Image.new("RGBA", art.size, S.C(S.INK))
    ink.putalpha(art.getchannel("A").point(lambda v: 255 if v else 0).filter(ImageFilter.MaxFilter(3)))
    top.alpha_composite(ink)
    top.alpha_composite(art)
    return under, top
