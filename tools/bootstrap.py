#!/usr/bin/env python3
"""Восстанавливает всё, что в проекте генерируется или берётся из Stardew Kitchen, — чтобы в git хранились только исходники.

  python tools/bootstrap.py [путь к stardewkitchen-*.jar]

1. Достаёт из jar Stardew Kitchen иконки эффектов и языковые файлы (tools/lang).
   Текстуры блюд оттуда больше не берутся: они рисуются в стиле Farmer's Delight скриптом tools/fd_textures.py.
2. Скачивает Gradle wrapper (gradlew, gradlew.bat, gradle-wrapper.jar), если его нет.
3. Запускает tools/fd_textures.py (текстуры блюд), tools/gen.py (код предметов, рецепты, модели, теги, языки)
   и dev/art (оформление страницы мода).
"""
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JAR = ROOT.parent / "StardewKitchen" / "stardewkitchen-1.0.0.jar"
SRC = "assets/stardewkitchen/"
DST = ROOT / "src/main/resources/assets/stardewdelight"
GRADLE = "https://raw.githubusercontent.com/gradle/gradle/v8.14.3/"
WRAPPER = ["gradlew", "gradlew.bat", "gradle/wrapper/gradle-wrapper.jar"]


def from_jar(jar: Path) -> None:
    with zipfile.ZipFile(jar) as z:
        n = 0
        for name in z.namelist():
            if not name.startswith(SRC) or name.endswith("/"):
                continue
            rel = name[len(SRC):]
            if rel.startswith("textures/mob_effect/"):
                out = DST / rel
            elif rel.startswith("lang/"):
                out = ROOT / "tools" / rel
            else:
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(z.read(name))
            n += 1
    print(f"из {jar.name}: {n} файлов")


def wrapper() -> None:
    for rel in WRAPPER:
        out = ROOT / rel
        if out.exists():
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(GRADLE + rel) as r:
            out.write_bytes(r.read())
        print("скачан", rel)


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


if __name__ == "__main__":
    jar = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_JAR
    if not jar.exists():
        sys.exit(f"нет {jar}: укажите путь к jar Stardew Kitchen")
    from_jar(jar)
    wrapper()
    run("tools/fd_textures.py")
    run("tools/gen.py")
    run("dev/art/make_art.py")
    run("dev/art/make_description.py")
