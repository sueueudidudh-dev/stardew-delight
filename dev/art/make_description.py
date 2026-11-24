#!/usr/bin/env python3
"""Описание для CurseForge/Modrinth в стиле страниц Profet: баннер, жирная строка-крючок, заголовки-картинки разделов,
таблицы-галереи и разделитель в конце.

  python3 dev/art/make_description.py https://raw.githubusercontent.com/<ник>/<репозиторий>/main

Картинки должны лежать по этому адресу (папка docs/ этого проекта, запушенная на GitHub). Результат:
docs/description.md (Markdown для CurseForge/Modrinth) и docs/description.html (для HTML-режима CurseForge).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://raw.githubusercontent.com/USER/stardew-delight/main").rstrip("/")


def img(path, alt=""):
    return f"![{alt}]({BASE}/docs/{path})"


def title(key, alt):
    return img(f"desc/title-{key}.webp", alt)


MD = f"""{img("banner.webp", "Stardew Delight")}

**Every dish from Stardew Valley, cooked the Farmer's Delight way: in the cooking pot, on the cutting board and at the crafting table.**

Stardew Delight is an add-on for **Farmer's Delight** on **Minecraft Java 1.20.1** with **Forge**. It brings the whole Stardew Valley cookbook into your kitchen: 78 new dishes, plus Farmer's Delight's Fried Egg and vanilla Bread for the full 80. Every dish fills you up differently and gives the buff it gives in the valley.

{img("clips/cookbook.webp", "The whole cookbook")}

{title("features", "Features")}

- **The whole cookbook.** From a humble Hashbrowns to Lobster Bisque, Pink Cake and the Complete Breakfast. Every dish has its own texture drawn in Farmer's Delight's style: the same wooden bowls, glass mugs, outlines and palette.
- **Cooked like Farmer's Delight food.** Soups, stews, curries and puddings simmer in the cooking pot, salads and baking come together at the crafting table, and sashimi is sliced on the cutting board.
- **Farmer's Delight ingredients.** Onions, tomatoes, cabbage, rice, wheat dough, raw pasta, tomato sauce, pie crust and pumpkin slices all have a use, so your crop fields feed the valley's menu.
- **Served like Farmer's Delight food.** Soups, stews, salads and main courses come in a bowl, stack to 16 and hand the bowl back; drinks come in a bottle; sandwiches, tacos, pizza, rolls and baking are eaten by hand. The cooking pot asks for the right container.
- **Stardew buffs.** Haste, Speed, Luck, Resistance, Water Breathing, Night Vision, Hero of the Village and more, with the valley's durations.
- **Comfort and Nourishment.** Hot soups also give Farmer's Delight's **Comfort**, hearty main courses in a bowl give **Nourishment**.
- **Two new effects.** **Magnetism** pulls nearby items and XP orbs to you. **Debuff Immunity** clears poison, weakness, nausea and other harmful effects and keeps them away.
- **Clear tooltips.** Every dish shows its hunger, saturation and every effect with its duration.

{title("buffs", "Buffs")}

| Dish | What it gives |
| --- | --- |
| **Miner's Treat** | Haste III, Night Vision, Magnetism |
| **Seafoam Pudding** | Luck IV, Water Breathing, Dolphin's Grace |
| **Complete Breakfast** | Haste II, Absorption II, Nourishment |
| **Spicy Eel** | Speed, Fire Resistance, Hero of the Village |
| **Lobster Bisque** | Luck III, Water Breathing, Absorption II, Comfort |
| **Triple Shot Espresso** | Speed II, Haste |
| **Squid Ink Ravioli** | Haste, Debuff Immunity |
| **Strange Bun** | Night Vision and a random teleport |

{title("recipes", "Recipes")}

- **Cooking pot:** Parsnip Soup (carrot ×2, milk, onion), Tom Kha Soup (tropical fish, brown mushroom, milk, onion), Tropical Curry (rice, melon slice, cocoa beans, blaze powder), Fiddlehead Risotto (rice, fern, onion, milk) and 44 more.
- **Crafting table:** Pizza (wheat dough, tomato sauce, milk), Complete Breakfast (fried egg, milk, Hashbrowns, Pancakes, bowl), Fish Taco (cooked fish, Tortilla, cabbage, tomato), Rhubarb Pie (pie crust, sugar cane ×2, sugar) and more.
- **Cutting board:** Sashimi, two from a tropical fish with any knife.

Every recipe shows up in the recipe book as soon as you pick up one of its ingredients, and in JEI.

{title("how-to-use", "How to use")}

1. Grow Farmer's Delight crops and set up a cooking pot over a heat source.
2. Pick up an ingredient: its Stardew recipes unlock in the recipe book.
3. Cook, eat, enjoy the buff. All dishes are in the **Stardew Delight** creative tab.

{title("compatibility", "Compatibility")}

- Recipes use Forge tags the way Farmer's Delight does (`#forge:crops/carrot`, `#forge:crops/potato`, `#forge:crops/onion`, `#forge:milk`, `#forge:raw_fishes/cod`, …), so crops and fish from other mods work as ingredients.
- Dishes are tagged `farmersdelight:meals`, `sweets`, `snacks` and `drinks`.
- Tested with Farmer's Delight 1.20.1-1.3.4.

{title("installation", "Installation")}

Put the jar in the `mods` folder together with **Farmer's Delight** (required). Minecraft 1.20.1, Forge 47 or newer. Needed on both the client and the server.

{title("credits", "Credits")}

- Dishes and the original idea: **Stardew Valley** by ConcernedApe. This is an unofficial fan-made mod and is not affiliated with ConcernedApe.
- **Farmer's Delight** by vectorwing.
- Add-on and textures: Karasik.

{title("license", "License")}

© 2026 Karasik. All rights reserved. You can use Stardew Delight in modpacks and videos; please don't re-upload it or present it as your own.

{img("desc/divider.webp")}
"""


def to_html(md: str) -> str:
    """Небольшой конвертер ровно под этот текст (картинки, абзацы, списки, таблицы, жирный, код)."""
    import html
    import re

    def inline(t):
        t = html.escape(t, quote=False)
        t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        return t

    out, lines, i = [], md.strip().split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"<li>{inline(lines[i][2:])}</li>")
                i += 1
            out.append("</ul>")
        elif re.match(r"\d+\. ", ln):
            out.append("<ol>")
            while i < len(lines) and re.match(r"\d+\. ", lines[i]):
                out.append(f"<li>{inline(lines[i].split('. ', 1)[1])}</li>")
                i += 1
            out.append("</ol>")
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr></thead><tbody>")
            for r in rows[2:]:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</tbody></table>")
        else:
            out.append(f"<p>{inline(ln)}</p>")
            i += 1
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs/description.md").write_text(MD, encoding="utf-8")
    (ROOT / "docs/description.html").write_text(to_html(MD), encoding="utf-8")
    print(f"docs/description.md, docs/description.html (картинки: {BASE}/docs/...)")
