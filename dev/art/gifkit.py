"""Exact-palette GIF and lossless animated WebP writers shared by the release-art scripts."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def write_gif(frames, out: Path, fps: int, key_mask=None, verify=True) -> int:
    """RGB frames -> GIF with every colour kept exactly. Slot 255 is transparent: it marks every pixel unchanged since
    the previous frame (disposal 1 keeps what is underneath) and, with key_mask (L, 255 = transparent), the pixels that
    must always stay see-through (the banner's stepped corners). Returns the colour count."""
    stack = np.stack([np.array(f.convert("RGB")) for f in frames]).astype(np.uint32)
    code = (stack[..., 0] << 16) | (stack[..., 1] << 8) | stack[..., 2]
    colours = np.unique(code)
    if len(colours) > 255:
        sys.exit(f"{out.name}: {len(colours)} colours - more than a GIF palette holds next to the transparent slot")
    idx = np.searchsorted(colours, code).astype(np.uint8)
    pal = []
    for c in colours:
        pal += [int(c >> 16) & 255, int(c >> 8) & 255, int(c) & 255]
    pal += [0, 0, 0] * (255 - len(colours)) + [255, 0, 255]
    key = np.array(key_mask) > 127 if key_mask is not None else None
    ims = []
    for i in range(len(frames)):
        q = idx[i].copy()
        if i:
            q[idx[i] == idx[i - 1]] = 255
        if key is not None:
            q[key] = 255
        p = Image.fromarray(q, "P")
        p.putpalette(pal)
        ims.append(p)
    ims[0].save(out, save_all=True, append_images=ims[1:], duration=1000 // fps, loop=0, optimize=False, disposal=1,
                transparency=255)
    if verify:
        back, i = Image.open(out), 0
        keep = ~key if key is not None else None
        for n in range(back.n_frames):
            back.seek(n)
            got = np.array(back.convert("RGB"))
            for _ in range(max(1, round(back.info.get("duration", 1000 // fps) * fps / 1000))):
                want = np.array(frames[i].convert("RGB"))
                g, w = (got[keep], want[keep]) if keep is not None else (got, want)
                if not np.array_equal(g, w):
                    sys.exit(f"{out.name}: frame {i} decodes differently ({(g != w).any(-1).sum()} px)")
                i += 1
        if i != len(frames):
            sys.exit(f"{out.name}: {i} frames decoded, {len(frames)} expected")
    return len(colours)


def write_webp(frames, out: Path, fps: int, lossless=True, quality=90):
    """Animated WebP (lossless by default). RGBA frames keep their transparency."""
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=1000 // fps, loop=0, lossless=lossless,
                   quality=quality, method=6)


def sheet(frames, cell, cols=12, pad=4, bg=(20, 20, 28)):
    from PIL import ImageDraw
    rows = (len(frames) + cols - 1) // cols
    out = Image.new("RGB", (cols * (cell + pad) + pad, rows * (cell + pad) + pad), bg)
    d = ImageDraw.Draw(out)
    for k, f in enumerate(frames):
        x, y = pad + (k % cols) * (cell + pad), pad + (k // cols) * (cell + pad)
        out.paste(f.resize((cell, cell), Image.NEAREST if cell % f.width == 0 else Image.LANCZOS), (x, y))
        d.text((x + 2, y + 1), str(k), fill=(255, 255, 255))
    return out
