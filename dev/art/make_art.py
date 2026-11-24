#!/usr/bin/env python3
"""Всё оформление страницы мода одной командой (Python 3 + Pillow + numpy):

  python dev/art/make_art.py

  make_icon.py    docs/icon-animated.gif (256 px, <= 256 KiB), .webp, docs/icon-512.png, src/main/resources/stardewdelight_logo.png
  make_banner.py  docs/banner.png/.gif/.webp (1536x512)
  make_desc.py    docs/desc/title-*.png/.webp, docs/desc/divider.*, docs/promo-tile.png/.gif/.webp
  make_clips.py   docs/clips/cookbook.gif/.webp (все блюда мода)

Сцена (кастрюля на костре) — scene.py + sprites.py, шрифты — pa.py, запись GIF/WebP — gifkit.py.
Блюда берутся из текстур мода, поэтому после перерисовки текстур просто запустите скрипт заново.
"""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

for name in ("make_icon", "make_banner", "make_desc", "make_clips"):
    print(f"== {name}")
    runpy.run_path(str(HERE / f"{name}.py"), run_name="__main__")
