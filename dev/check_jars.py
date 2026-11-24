"""Checks the built jars in build/libs/<mod version>/ without starting Minecraft.

  python dev/check_jars.py

For every jar: loader metadata (and no metadata of other loaders), entrypoint + mixin classes, class file version
for the target Java, valid JSON, 78 item models/textures/translations, recipes and advancements in the data folders
of that Minecraft version, Farmer's Delight category tags, item definitions (1.21.4+), pack.mcmeta (Forge).
"""
import io
import json
import os
import re
import struct
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = 'stardewdelight'
DISHES = 78


def ver(s):
    return tuple(int(x) for x in s.split('.'))


def mod_version():
    m = re.search(r'^mod\.version\s*=\s*"([^"]+)"', open(os.path.join(ROOT, 'stonecutter.properties.toml'), encoding='utf-8').read(), re.M)
    return m.group(1)


def check(path):
    name = os.path.basename(path)
    m = re.match(rf'{NS}-(fabric|forge|neoforge)-([0-9.]+)-(.+)\.jar$', name)
    loader, mc = m.group(1), ver(m.group(2))
    java = 25 if mc >= (26, 1) else 21 if mc >= (1, 20, 5) else 17
    z = zipfile.ZipFile(path)
    names = set(z.namelist())
    problems = []

    meta = {'fabric': 'fabric.mod.json', 'forge': 'META-INF/mods.toml', 'neoforge': 'META-INF/neoforge.mods.toml'}
    for ld, f in meta.items():
        if (f in names) != (ld == loader):
            problems.append(f'{f} {"missing" if ld == loader else "must not be here"}')
    text = z.read(meta[loader]).decode('utf-8') if meta[loader] in names else ''
    if '${' in text:
        problems.append(f'{meta[loader]} has unexpanded ${{...}}')
    mcrange = re.search(r'"minecraft":\s*"([^"]+)"', text) or re.search(r'modId="minecraft"[^\[]*?versionRange="([^"]+)"', text, re.S)

    entry = {'fabric': 'StardewDelightFabric', 'forge': 'StardewDelightForge', 'neoforge': 'StardewDelightNeoForge'}[loader]
    classes = [n for n in names if n.endswith('.class')]
    for c in (f'com/{NS}/{entry}.class', f'com/{NS}/mixin/LivingEntityMixin.class', f'com/{NS}/Dishes.class'):
        if c not in names:
            problems.append('missing ' + c)
    for other in {'StardewDelightFabric', 'StardewDelightForge', 'StardewDelightNeoForge'} - {entry}:
        if f'com/{NS}/{other}.class' in names:
            problems.append(f'{other}.class from another loader')
    majors = {struct.unpack('>H', z.read(c)[6:8])[0] for c in classes}
    if majors != {java + 44}:
        problems.append(f'class file versions {sorted(majors)} (want {java + 44} = Java {java})')

    mixins = json.loads(z.read(f'{NS}.mixins.json'))
    if mixins.get('compatibilityLevel') != f'JAVA_{java}':
        problems.append(f'mixins compatibilityLevel {mixins.get("compatibilityLevel")}')
    if loader == 'forge':
        if mixins.get('refmap') not in names:
            problems.append('forge: refmap missing')
        if 'MixinConfigs' not in z.read('META-INF/MANIFEST.MF').decode():
            problems.append('forge: MixinConfigs missing in MANIFEST.MF')
        if 'pack.mcmeta' not in names:
            problems.append('forge: pack.mcmeta missing')

    for n in names:
        if n.endswith(('.json', '.mcmeta')):
            try:
                json.loads(z.read(n).decode('utf-8'))
            except Exception as e:
                problems.append(f'invalid json {n}: {str(e)[:60]}')

    models = {n.split('/')[-1][:-5] for n in names if n.startswith(f'assets/{NS}/models/item/') and n.endswith('.json')}
    textures = {n.split('/')[-1][:-4] for n in names if n.startswith(f'assets/{NS}/textures/item/') and n.endswith('.png')}
    defs = {n.split('/')[-1][:-5] for n in names if n.startswith(f'assets/{NS}/items/') and n.endswith('.json')}
    lang = {c: json.loads(z.read(f'assets/{NS}/lang/{c}.json')) for c in ('en_us', 'ru_ru')}
    if len(models) != DISHES:
        problems.append(f'{len(models)} item models')
    if models - textures:
        problems.append(f'models without textures: {sorted(models - textures)[:5]}')
    for c, d in lang.items():
        lacking = [i for i in models if f'item.{NS}.{i}' not in d]
        if lacking:
            problems.append(f'{c} lacks {lacking[:5]}')
    if mc >= (1, 21, 4) and defs != models:
        problems.append(f'item definitions: {len(defs)} (want {DISHES})')
    if mc < (1, 21, 4) and defs:
        problems.append('item definitions in a version before 1.21.4')

    rec, adv, tag = ('recipes', 'advancements', 'tags/items') if mc < (1, 21) else ('recipe', 'advancement', 'tags/item')
    recipes = [n for n in names if n.startswith(f'data/{NS}/{rec}/') and n.endswith('.json')]
    advancements = [n for n in names if n.startswith(f'data/{NS}/{adv}/') and n.endswith('.json')]
    tags = [n for n in names if n.startswith(f'data/farmersdelight/{tag}/') and n.endswith('.json')]
    wrong = [n for n in names if re.match(rf'data/[^/]+/({"recipe|advancement|tags/item" if mc < (1, 21) else "recipes|advancements|tags/items"})/', n)]
    if len(recipes) != DISHES or len(advancements) != DISHES or len(tags) != 4:
        problems.append(f'{len(recipes)} recipes, {len(advancements)} advancements, {len(tags)} tags')
    if wrong:
        problems.append(f'data in folders of another version: {wrong[:3]}')
    for n in recipes:
        r = json.loads(z.read(n))
        for ref in re.findall(rf'"{NS}:([a-z_]+)"', json.dumps(r)):
            if ref not in models:
                problems.append(f'{n} -> unknown {NS}:{ref}')

    status = 'OK' if not problems else f'{len(problems)} PROBLEMS'
    print(f'{name:48} {status:12} Java {java}, mc {mcrange.group(1) if mcrange else "?"}, '
          f'{len(classes)} classes, {len(recipes)} recipes')
    for p in problems[:20]:
        print('   - ' + p)
    return not problems


def main():
    d = os.path.join(ROOT, 'build', 'libs', mod_version())
    jars = sorted(f for f in os.listdir(d) if f.endswith('.jar'))
    good = sum(check(os.path.join(d, f)) for f in jars)
    print(f'\n{good} of {len(jars)} jars OK')
    sys.exit(0 if good == len(jars) else 1)


if __name__ == '__main__':
    main()
