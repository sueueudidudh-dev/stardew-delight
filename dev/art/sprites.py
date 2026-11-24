"""Procedural pixel sprites for the Stardew Delight icon, banner and page art (64x64 texel scene).

A copper cooking pot simmers on a campfire; every sprite is drawn at 1 texel = 1 pixel and lit from the upper left.
`python sprites.py` writes them all to dev/art/sprites/ for inspection (the generators are used directly by the
other scripts, so nothing has to be re-exported by hand).
"""
import math
import random
from pathlib import Path

from PIL import Image

import pa

HERE = Path(__file__).resolve().parent
ITEMS = HERE.parent.parent / "src/main/resources/assets/stardewdelight/textures/item"

COPPER = ["#3A1A14", "#6E2E1C", "#A8482A", "#D46A34", "#F08F4A", "#FFC07A", "#FFE8C4"]
IRON = ["#1E2133", "#33384F", "#4E5573", "#767E9E", "#AEB4CC", "#E2E5F0"]
SOUP = ["#5A1A16", "#8E2A1E", "#C8452A", "#E8742E", "#FFB04A", "#FFE08A"]
WOOD = ["#3A2216", "#5A3826", "#7A5238", "#9C7050", "#C89A64", "#E6C48E"]
FIRE = ["#C2361C", "#F0641E", "#FF9A2E", "#FFCC4A", "#FFF0A0", "#FFFFFF"]
STEAM = ["#8E91B4", "#D4D6EA", "#FFFFFF"]
STAR = ["#FFFFFF", "#FFE14D", "#FFF7BD"]
NAVY = "#1A2140"
INK = "#0B0F20"
SKY_DIM, SKY_MID, SKY_TWINKLE = "#3A4473", "#6F7DB4", "#9FB0E8"
UNDER = {"shadow": "#10142A", "pool0": "#262A4A", "pool1": "#3E3550", "pool2": "#5E4250"}

CX = 32.0                     # the pot's centre line (between texel columns 31 and 32)
RIM_CY, RIM_A, RIM_B = 31.5, 16.5, 4.5
IN_A, IN_B = 14.5, 3.0
SOUP_CY, SOUP_A, SOUP_B = 32.4, 13.6, 2.1
BODY_HW = {31: 16, 32: 16, 33: 16, 34: 16, 35: 16, 36: 16, 37: 16, 38: 16, 39: 16, 40: 16, 41: 16, 42: 16, 43: 16,
           44: 16, 45: 15, 46: 15, 47: 14, 48: 13, 49: 12, 50: 10}
RIDGE = (40, 41)              # a raised band around the belly
POT_BOTTOM = max(BODY_HW)


def C(h):
    return pa.hexrgb(h) + (255,)


def ell(x, y, cx, cy, a, b):
    dx, dy = (x + 0.5 - cx) / a, (y + 0.5 - cy) / b
    return dx * dx + dy * dy


def new(w=64, h=64):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def from_grid(rows, pal):
    im = new(len(rows[0]), len(rows))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in pal:
                im.putpixel((x, y), C(pal[ch]))
    return im


def cyl_tone(nx):
    if nx < -0.86:
        return 2
    if nx < -0.70:
        return 3
    if nx < -0.30:
        return 4
    if nx < 0.32:
        return 3
    if nx < 0.74:
        return 2
    return 1


# --------------------------------------------------------------------------- the cooking pot
def rim_arc_bottom(x):
    """Lowest texel row inside the rim ellipse in column x (None outside)."""
    rows = [y for y in range(20, 40) if ell(x, y, CX, RIM_CY, RIM_A, RIM_B) <= 1]
    return max(rows) if rows else None


def pot_back():
    """Far half of the rim, the inner wall and the stew."""
    im = new()
    rnd = random.Random(7)
    for y in range(24, 40):
        for x in range(10, 54):
            if ell(x, y, CX, RIM_CY, RIM_A, RIM_B) > 1:
                continue
            inner = ell(x, y, CX, RIM_CY, IN_A, IN_B) <= 1
            nx = (x + 0.5 - CX) / RIM_A
            if not inner:
                if y + 0.5 >= RIM_CY:
                    continue                      # near half of the rim belongs to pot_front
                tone = 4 if nx < -0.35 else 3 if nx < 0.45 else 2
                if y + 0.5 < RIM_CY - RIM_B + 1.6:
                    tone = min(tone + 1, 5) if nx < 0 else tone   # the far lip catches the light
                im.putpixel((x, y), C(COPPER[tone]))
                continue
            if ell(x, y, CX, SOUP_CY, SOUP_A, SOUP_B) <= 1:
                d = ell(x, y, CX, SOUP_CY, SOUP_A, SOUP_B)
                top = (y + 0.5) < SOUP_CY - 0.6
                tone = 2 if top or d > 0.72 else 3
                if nx < -0.25 and not top and d < 0.55:
                    tone = 4
                im.putpixel((x, y), C(SOUP[tone]))
            else:
                im.putpixel((x, y), C(COPPER[0] if (y + 0.5) < RIM_CY - 1.2 else COPPER[1]))
    # chunks in the stew: herbs, potato, carrot
    for (x, y, c) in [(22, 32, "#6FB33E"), (27, 33, "#F2E6C8"), (36, 32, "#6FB33E"), (40, 33, "#FFB04A"),
                      (31, 34, "#F2E6C8"), (25, 34, "#FFB04A"), (44, 32, "#4E8C2E"), (34, 34, "#6FB33E")]:
        if im.getpixel((x, y))[3]:
            im.putpixel((x, y), C(c))
    im.putpixel((19, 33), C(SOUP[5]))
    im.putpixel((20, 33), C(SOUP[4]))
    return im


def pot_front():
    """Near half of the rim, the rim lip, the belly with its ridge, and the two iron handles."""
    im = new()
    for x in range(10, 54):
        arc = rim_arc_bottom(x)
        for y in range(24, 54):
            nx = (x + 0.5 - CX) / RIM_A
            in_rim = ell(x, y, CX, RIM_CY, RIM_A, RIM_B) <= 1
            if in_rim:
                if ell(x, y, CX, RIM_CY, IN_A, IN_B) <= 1 or y + 0.5 < RIM_CY:
                    continue
                tone = 5 if nx < -0.42 else 4 if nx < 0.2 else 3 if nx < 0.62 else 2
                im.putpixel((x, y), C(COPPER[tone]))
                continue
            hw = BODY_HW.get(y)
            if hw is None or not (CX - hw <= x + 0.5 <= CX + hw):
                continue
            bx = (x + 0.5 - CX) / hw
            if arc is not None and arc < y <= arc + 2:            # the rim lip: a lit face, then a groove
                tone = (cyl_tone(bx) + 1) if y == arc + 1 else 1
                im.putpixel((x, y), C(COPPER[min(tone, 5)]))
                continue
            tone = cyl_tone(bx)
            if y == RIDGE[0]:
                tone = max(tone - 1, 1)
            elif y == RIDGE[1]:
                tone = min(tone + 1, 5)
            elif 36 <= y <= 45 and -0.62 <= bx <= -0.46:
                tone = 5                                           # vertical highlight streak
            if y >= 47:
                tone = max(tone - 1, 1)
            if y >= 49:
                tone = max(tone - 1, 0)
            im.putpixel((x, y), C(COPPER[tone]))
    for (x, y) in [(21, 38), (21, 39)]:
        im.putpixel((x, y), C(COPPER[6]))
    # iron handles (left, mirrored to the right)
    hp = {"h": IRON[4], "m": IRON[3], "n": IRON[2], "d": IRON[1]}
    handle = [".hhhm.",
              "hm....",
              "m.....",
              "n.....",
              "dn....",
              ".dddd."]
    for r, row in enumerate(handle):
        for c, ch in enumerate(row):
            if ch in hp:
                im.putpixel((11 + c, 36 + r), C(hp[ch]))
                mir = {"h": "m", "m": "n", "n": "d", "d": "d"}[ch]
                im.putpixel((63 - (11 + c), 36 + r), C(hp[mir]))
    # handle plates riveted to the belly
    for y in (37, 38, 39, 40):
        im.putpixel((16, y), C(IRON[3] if y < 39 else IRON[2]))
        im.putpixel((47, y), C(IRON[2] if y < 39 else IRON[1]))
    return im


def lid():
    """Copper dome lid with an iron knob; 34x17, base centre at (17.0, 12.5). Closed, it sits at (15, 18)."""
    w, h, cx, cy = 34, 17, 17.0, 12.5
    im = new(w, h)
    L = (-0.52, -0.72, 0.46)
    n = math.sqrt(sum(v * v for v in L))
    L = tuple(v / n for v in L)
    for y in range(h):
        for x in range(w):
            u, v = (x + 0.5 - cx) / 15.5, (y + 0.5 - cy) / 8.2
            in_dome = (y + 0.5) <= cy and u * u + v * v <= 1
            in_base = ell(x, y, cx, cy, 16.5, 4.0) <= 1
            if not (in_dome or in_base):
                continue
            if in_dome:
                z = math.sqrt(max(0.0, 1 - u * u - v * v))
                d = u * L[0] + v * L[1] + z * L[2]
                tone = 2 if d < 0.22 else 3 if d < 0.55 else 4 if d < 0.82 else 5 if d < 0.965 else 6
                im.putpixel((x, y), C(COPPER[tone]))
            else:
                nx = (x + 0.5 - cx) / 16.5
                last = ell(x, y + 1, cx, cy, 16.5, 4.0) > 1
                tone = 1 if last else (5 if nx < -0.55 else 4 if nx < 0.1 else 3 if nx < 0.6 else 2)
                im.putpixel((x, y), C(COPPER[tone]))
    knob = ["..hhmm..",
            ".hhmmmn.",
            ".mmmmnn.",
            "..dnnd..",
            "...dd..."]
    kp = {"h": IRON[5], "m": IRON[3], "n": IRON[2], "d": IRON[1]}
    for r, row in enumerate(knob):
        for c, ch in enumerate(row):
            if ch in kp:
                im.putpixel((13 + c, r), C(kp[ch]))
    return im


LID_PIVOT = (24.0, 27.5)      # where the lid's base centre sits inside lid_tilted()'s 48x48 image


def _lid_sample(lx, ly):
    """Colour of the lid at local point (lx, ly) relative to its base centre (screen axes, unrotated), or None.
    Also returns the local normal so the caller can light it after rotating."""
    # knob
    if ell_f(lx, ly, 0.0, -10.4, 3.7, 2.3) <= 1:
        u, v = lx / 3.7, (ly + 10.4) / 2.3
        return "knob", (u, v, math.sqrt(max(0.0, 1 - u * u - v * v)))
    if abs(lx) < 1.3 and -9.0 <= ly <= -7.6:
        return "stem", (0.0, 0.0, 1.0)
    u, v = lx / 15.5, ly / 8.2
    if ly <= 0 and u * u + v * v <= 1:
        return "dome", (u, v, math.sqrt(max(0.0, 1 - u * u - v * v)))
    if ell_f(lx, ly, 0.0, 0.0, 16.5, 4.0) <= 1:
        return "flange", (lx / 16.5, 0.0, 1.0)
    return None, None


def ell_f(x, y, cx, cy, a, b):
    dx, dy = (x - cx) / a, (y - cy) / b
    return dx * dx + dy * dy


def lid_tilted(angle):
    """The lid rotated by `angle` degrees (clockwise on screen) and lit from the upper left after rotating, so it
    stays crisp pixel art at any tilt. 48x48, base centre at LID_PIVOT."""
    im = new(48, 48)
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    L = (-0.52, -0.72, 0.46)
    n = math.sqrt(sum(v * v for v in L))
    L = tuple(v / n for v in L)

    def local(px, py):
        dx, dy = px - LID_PIVOT[0], py - LID_PIVOT[1]
        return dx * ca + dy * sa, -dx * sa + dy * ca

    for y in range(48):
        for x in range(48):
            part, nrm = _lid_sample(*local(x + 0.5, y + 0.5))
            if part is None:
                continue
            below, _ = _lid_sample(*local(x + 0.5, y + 1.5))
            nu, nv, nz = nrm
            su, sv = nu * ca - nv * sa, nu * sa + nv * ca          # normal back to screen axes
            d = su * L[0] + sv * L[1] + nz * L[2]
            if part in ("knob", "stem"):
                tone = 1 if part == "stem" or d < 0.25 else 2 if d < 0.55 else 3 if d < 0.85 else 5
                im.putpixel((x, y), C(IRON[tone]))
            elif part == "dome":
                tone = 2 if d < 0.22 else 3 if d < 0.55 else 4 if d < 0.82 else 5 if d < 0.965 else 6
                im.putpixel((x, y), C(COPPER[tone]))
            else:
                lx, _ = local(x + 0.5, y + 0.5)
                s = lx / 16.5 * ca
                tone = 1 if below is None else (5 if s < -0.55 else 4 if s < 0.1 else 3 if s < 0.6 else 2)
                im.putpixel((x, y), C(COPPER[tone]))
    return im


# --------------------------------------------------------------------------- campfire
def _log(im, p0, p1, half, face_at_p1=True, seed=0):
    rnd = random.Random(seed)
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    px_, py_ = -uy, ux                       # perpendicular (points "down" for logs going right)
    if py_ < 0:
        px_, py_ = -px_, -py_
    streak = {k: rnd.random() < 0.18 for k in range(-4, 80)}
    for y in range(40, 64):
        for x in range(0, 64):
            qx, qy = x + 0.5 - x0, y + 0.5 - y0
            t = qx * ux + qy * uy
            s = qx * px_ + qy * py_
            if not (0 <= t <= ln and abs(s) <= half):
                continue
            k = s / half                       # -1 top edge .. 1 bottom edge
            tone = 3 if k < -0.45 else 2 if k < 0.45 else 1
            if streak.get(int(t // 3)) and abs(k) < 0.5:
                tone = max(tone - 1, 1)
            im.putpixel((x, y), C(WOOD[tone]))
    if face_at_p1:
        fx, fy = x1, y1
        for y in range(40, 64):
            for x in range(0, 64):
                d = ell(x, y, fx, fy, half * 0.95, half * 1.05)
                if d <= 1:
                    c = WOOD[1] if d > 0.62 else WOOD[5] if d > 0.30 else WOOD[4] if d > 0.08 else WOOD[3]
                    im.putpixel((x, y), C(c))


def logs():
    """Two logs crossed in an X under the pot, cut faces at the outer ends."""
    im = new()
    _log(im, (48.5, 61.4), (15.5, 56.0), 2.1, True, 3)
    _log(im, (15.5, 61.4), (48.5, 56.0), 2.1, True, 5)
    for fx, fy in ((15.5, 61.4), (48.5, 61.4)):
        for y in range(50, 64):
            for x in range(64):
                d = ell(x, y, fx, fy, 2.0, 2.3)
                if d <= 1:
                    c = WOOD[1] if d > 0.62 else WOOD[5] if d > 0.30 else WOOD[4] if d > 0.08 else WOOD[3]
                    im.putpixel((x, y), C(c))
    return im


def back_log():
    im = new()
    _log(im, (19.0, 57.2), (45.0, 57.2), 1.8, False, 11)
    return im


TONGUES = [(13.0, 13.0, 2.8), (17.5, 11.5, 3.1), (22.5, 9.5, 3.1), (27.5, 10.5, 3.1), (32.0, 9.0, 3.1),
           (36.5, 10.5, 3.1), (41.5, 9.5, 3.1), (46.5, 11.5, 3.1), (51.0, 13.0, 2.8)]
FRONT_TONGUES = [(17.5, 8.0, 2.3), (46.5, 8.0, 2.3)]


def flames(k, base_y=57.5, tongues=None):
    """Flame frame k (0..3); `tongues` defaults to the full fire behind the pot."""
    im = new()
    inten = {}
    for i, (bx, bh, bw) in enumerate(tongues or TONGUES):
        ph = (k + i * 3) % 4
        h = bh * (0.82, 1.0, 1.14, 0.94)[ph]
        sway = (0, 0.8, 0, -0.8)[(k + i) % 4]
        for y in range(int(base_y - h - 1), int(base_y) + 1):
            t = (base_y - (y + 0.5)) / h
            if t < 0 or t > 1:
                continue
            hwid = bw * (math.sin(math.pi * min(1.0, t * 1.15 + 0.12)) ** 0.8) * (1 - t * 0.55)
            xc = bx + sway * t * t
            for x in range(int(xc - hwid - 1), int(xc + hwid) + 2):
                s = abs(x + 0.5 - xc) / max(hwid, 0.01)
                if s > 1:
                    continue
                v = (1 - t) * 0.75 + (1 - s) * 0.55
                if v > inten.get((x, y), -1):
                    inten[(x, y)] = v
    for (x, y), v in inten.items():
        c = FIRE[4] if v > 1.08 else FIRE[3] if v > 0.86 else FIRE[2] if v > 0.62 else FIRE[1] if v > 0.40 else FIRE[0]
        if 0 <= x < 64 and 0 <= y < 64:
            im.putpixel((x, y), C(c))
    return im


def flames_front(k):
    """The two tongues that lick up over the pot's lower corners."""
    return flames(k, 55.5, FRONT_TONGUES)


# --------------------------------------------------------------------------- FX
def puff(size):
    """Steam puff, size 0..2."""
    r = (2.2, 3.2, 4.4)[size]
    n = int(r * 2 + 6)
    im = new(n, n)
    c = n / 2
    blobs = [(c - r * 0.45, c + r * 0.15, r * 0.72), (c + r * 0.4, c + r * 0.2, r * 0.66), (c, c - r * 0.25, r * 0.78)]
    for y in range(n):
        for x in range(n):
            inside = [math.hypot(x + 0.5 - bx, y + 0.5 - by) <= br for bx, by, br in blobs]
            if not any(inside):
                continue
            shade = (x + 0.5 - c) + (y + 0.5 - c) > r * 0.55
            im.putpixel((x, y), C(STEAM[1] if shade else STEAM[2]))
    return im


def star(size):
    """Four-point sparkle: size 0 = 7x7, 1 = 11x11, 2 = 15x15."""
    n = (7, 11, 15)[size]
    c = n // 2
    im = new(n, n)
    arm = c
    for i in range(-arm, arm + 1):
        for (x, y) in ((c + i, c), (c, c + i)):
            d = abs(i)
            col = STAR[0] if d >= arm - (1 if size else 0) else STAR[1]
            im.putpixel((x, y), C(col))
    body = max(1, size)
    for y in range(-body, body + 1):
        for x in range(-body, body + 1):
            if abs(x) + abs(y) <= body:
                im.putpixel((c + x, c + y), C(STAR[2] if abs(x) + abs(y) < body else STAR[1]))
    if size:
        for d in (1, 2) if size == 2 else (1,):
            for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                im.putpixel((c + sx * (body + d), c + sy * (body + d)), C(STAR[0]))
    im.putpixel((c, c), C(STAR[0]))
    return im


def ring(r):
    n = r * 2 + 3
    im = new(n, n)
    c = n / 2
    for y in range(n):
        for x in range(n):
            d = math.hypot(x + 0.5 - c, y + 0.5 - c)
            if r - 0.7 <= d <= r + 0.7:
                ang = math.atan2(y + 0.5 - c, x + 0.5 - c)
                if math.sin(ang * 4) > 0.82:
                    continue
                im.putpixel((x, y), C(STAR[0] if d > r else STAR[1]))
    return im


def bubble(k):
    """Stew bubble frame k (0 dot, 1 bubble, 2 pop)."""
    if k == 0:
        return from_grid(["s"], {"s": SOUP[4]})
    if k == 1:
        return from_grid([".h.", "hsh", ".h."], {"h": SOUP[4], "s": SOUP[5]})
    return from_grid(["h.h", "...", "h.h"], {"h": SOUP[5]})


# --------------------------------------------------------------------------- dishes and backgrounds
def dish(name):
    return Image.open(ITEMS / f"{name}.png").convert("RGBA")


TWINKLES_ICON = [(7, 9), (55, 47), (9, 44)]
DOTS_ICON = [(3, 22, SKY_DIM), (14, 3, SKY_MID), (25, 12, SKY_DIM), (60, 4, SKY_DIM), (59, 27, SKY_MID),
             (4, 57, SKY_DIM), (61, 60, SKY_DIM), (50, 20, SKY_DIM), (18, 25, SKY_DIM), (44, 2, SKY_MID)]


def twinkle(im, x, y, big):
    im.putpixel((x, y), C("#FFFFFF"))
    if big:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            im.putpixel((x + dx, y + dy), C(SKY_TWINKLE))


def icon_bg(frame=0, n=96):
    im = Image.new("RGBA", (64, 64), C(NAVY))
    for x, y, c in DOTS_ICON:
        im.putpixel((x, y), C(c))
    for i, (x, y) in enumerate(TWINKLES_ICON):
        ph = (frame + i * n // 3) % n
        twinkle(im, x, y, ph < n // 2)
    return im


def under_layer():
    """Ground shadow and the fire's light pool (drawn under the outline)."""
    im = new()
    for y in range(48, 64):
        for x in range(64):
            d = ell(x, y, 32.0, 60.8, 28.5, 4.2)
            if d <= 1:
                im.putpixel((x, y), C(UNDER["pool0"] if d > 0.55 else UNDER["pool1"] if d > 0.22 else UNDER["pool2"]))
    for y in range(48, 64):
        for x in range(64):
            if ell(x, y, 32.0, 62.0, 21.5, 1.9) <= 1:
                im.putpixel((x, y), C(UNDER["shadow"]))
    return im


def save_all():
    out = HERE / "sprites"
    out.mkdir(exist_ok=True)
    pot_back().save(out / "pot_back.png")
    pot_front().save(out / "pot_front.png")
    lid().save(out / "lid.png")
    logs().save(out / "logs.png")
    back_log().save(out / "back_log.png")
    for k in range(4):
        flames(k).save(out / f"flames_{k}.png")
    for s in range(3):
        puff(s).save(out / f"puff_{s}.png")
        star(s).save(out / f"star_{s}.png")
        bubble(s).save(out / f"bubble_{s}.png")
    for r in (4, 6, 8):
        ring(r).save(out / f"ring_{r}.png")
    under_layer().save(out / "under.png")
    icon_bg().save(out / "icon_bg.png")
    print("sprites written to", out)


if __name__ == "__main__":
    save_all()
