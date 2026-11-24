"""Генератор кода и данных для Stardew Delight.

Читает tools/items.json (параметры блюд, перенесённые из Stardew Kitchen) и таблицу рецептов ниже и пишет:
  * src/main/java/com/stardewdelight/Dishes.java — список блюд (одинаковый для всех версий);
  * общие ассеты: модели предметов и языковые файлы (src/main/resources/assets/stardewdelight);
  * данные для каждой версии Minecraft и загрузчика (versions/<версия>-<загрузчик>/generated):
    рецепты, достижения-разблокировки, теги категорий Farmer's Delight, определения предметов (1.21.4+)
    и pack.mcmeta (Forge). Форматы и теги в каждой версии свои — см. TARGETS.

Заодно проверяет, что всё устроено как в Farmer's Delight: блюда из meals — в миске, снеки — в руках,
у рецептов на верстаке есть миска, тара на текстуре (tools/fd_textures.py) совпадает с тарой предмета.

  python tools/gen.py            — всё
  python tools/gen.py --check    — только проверки
"""
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = 'stardewdelight'
RES = os.path.join(ROOT, 'src/main/resources')
DISHES_JAVA = os.path.join(ROOT, 'src/main/java/com/stardewdelight/Dishes.java')

SKIP = {'fried_egg', 'bread'}  # уже есть: farmersdelight:fried_egg и minecraft:bread
items = [i for i in json.load(open(os.path.join(ROOT, 'tools/items.json'), encoding='utf-8')) if i['id'] not in SKIP]

# Имена эффектов в items.json -> id в реестре (id не меняются от версии к версии, в отличие от имён полей MobEffects)
EFFECT_ID = {
    'HASTE': 'minecraft:haste', 'SPEED': 'minecraft:speed', 'JUMP_BOOST': 'minecraft:jump_boost',
    'RESISTANCE': 'minecraft:resistance', 'STRENGTH': 'minecraft:strength', 'NAUSEA': 'minecraft:nausea',
    'ABSORPTION': 'minecraft:absorption', 'NIGHT_VISION': 'minecraft:night_vision', 'LUCK': 'minecraft:luck',
    'HERO_OF_THE_VILLAGE': 'minecraft:hero_of_the_village', 'WATER_BREATHING': 'minecraft:water_breathing',
    'DOLPHINS_GRACE': 'minecraft:dolphins_grace', 'FIRE_RESISTANCE': 'minecraft:fire_resistance',
    'REGENERATION': 'minecraft:regeneration',
    'SK_MAGNETISM': f'{MOD}:magnetism', 'SK_IMMUNITY': f'{MOD}:immunity',
    'FD_COMFORT': 'farmersdelight:comfort', 'FD_NOURISHMENT': 'farmersdelight:nourishment',
}

# Эффекты Farmer's Delight, как у его собственных блюд: «Уют» (Comfort) — горячие супы и рагу,
# «Сытость» (Nourishment) — плотные вторые блюда в миске. Салаты, сладкое, снеки и напитки — без них.
SHORT, MEDIUM, LONG = 1200, 3600, 6000
FD_EXTRA = {
    # Comfort — горячие супы и похлёбки
    'parsnip_soup': ('FD_COMFORT', MEDIUM), 'vegetable_medley': ('FD_COMFORT', MEDIUM), 'bean_hotpot': ('FD_COMFORT', MEDIUM),
    'tom_kha_soup': ('FD_COMFORT', MEDIUM), 'trout_soup': ('FD_COMFORT', MEDIUM), 'algae_soup': ('FD_COMFORT', MEDIUM),
    'pale_broth': ('FD_COMFORT', MEDIUM), 'pumpkin_soup': ('FD_COMFORT', MEDIUM), 'poi': ('FD_COMFORT', MEDIUM),
    'autumns_bounty': ('FD_COMFORT', LONG), 'chowder': ('FD_COMFORT', LONG), 'lobster_bisque': ('FD_COMFORT', LONG),
    'fish_stew': ('FD_COMFORT', LONG),
    # Nourishment — плотные вторые блюда в миске
    'complete_breakfast': ('FD_NOURISHMENT', LONG), 'farmers_lunch': ('FD_NOURISHMENT', LONG), 'red_plate': ('FD_NOURISHMENT', LONG),
    'salmon_dinner': ('FD_NOURISHMENT', MEDIUM), 'stir_fry': ('FD_NOURISHMENT', MEDIUM),
    'fiddlehead_risotto': ('FD_NOURISHMENT', MEDIUM), 'tropical_curry': ('FD_NOURISHMENT', MEDIUM),
    'eggplant_parmesan': ('FD_NOURISHMENT', MEDIUM), 'super_meal': ('FD_NOURISHMENT', MEDIUM),
    'roots_platter': ('FD_NOURISHMENT', MEDIUM), 'dish_o_the_sea': ('FD_NOURISHMENT', MEDIUM),
    'spaghetti': ('FD_NOURISHMENT', MEDIUM), 'glazed_yams': ('FD_NOURISHMENT', MEDIUM), 'cheese_cauliflower': ('FD_NOURISHMENT', MEDIUM),
    'fried_mushroom': ('FD_NOURISHMENT', MEDIUM), 'spicy_eel': ('FD_NOURISHMENT', MEDIUM), 'stuffing': ('FD_NOURISHMENT', MEDIUM),
    'escargot': ('FD_NOURISHMENT', MEDIUM), 'squid_ink_ravioli': ('FD_NOURISHMENT', MEDIUM),
    'baked_fish': ('FD_NOURISHMENT', SHORT), 'carp_surprise': ('FD_NOURISHMENT', SHORT), 'crispy_bass': ('FD_NOURISHMENT', SHORT),
    'fried_eel': ('FD_NOURISHMENT', SHORT),
}

# Категории Farmer's Delight (теги farmersdelight:*). Всё, что не напиток, не сладость и не снек, — meals (в миске).
SWEETS = {'cranberry_sauce', 'rice_pudding', 'plum_pudding', 'banana_pudding', 'mango_sticky_rice', 'ice_cream', 'fruit_salad',
          'seafoam_pudding', 'chocolate_cake', 'pink_cake', 'rhubarb_pie', 'pumpkin_pie', 'blueberry_tart', 'blackberry_cobbler',
          'cookie', 'cranberry_candy', 'poppyseed_muffin', 'maple_bar', 'miners_treat'}
SNACKS = {'tortilla', 'roasted_hazelnuts', 'sashimi', 'maki_roll', 'bruschetta', 'hashbrowns', 'pancakes', 'fried_calamari',
          'strange_bun', 'pepper_poppers', 'omelet', 'lucky_lunch', 'pizza', 'fish_taco', 'survival_burger', 'crab_cakes'}
DROP_LANG = {'tooltip.stardewkitchen.effects'}  # осталось от Stardew Kitchen, в моде не используется
# Ванильные продукты с общим тегом: в рецептах — только тег (как у самого FD), чтобы подходили культуры других модов.
VANILLA_WITH_TAG = {'minecraft:carrot': '#forge:crops/carrot', 'minecraft:potato': '#forge:crops/potato',
                    'minecraft:beetroot': '#forge:crops/beetroot', 'minecraft:wheat': '#forge:crops/wheat',
                    'minecraft:cod': '#forge:raw_fishes/cod'}


def category(it):
    i = it['id']
    return 'drinks' if it['drink'] else 'sweets' if i in SWEETS else 'snacks' if i in SNACKS else 'meals'

# ---------------------------------------------------------------------------------------------------------------
# Рецепты. pot = кастрюля FD (cooking pot), craft = верстак (shapeless), cut = разделочная доска с ножом.
# "#тег" — тег предмета, иначе id предмета. Префикс "sd:" = наш мод, "fd:" = farmersdelight.
# Теги записаны в именах Forge 1.20.1 (#forge:...) — для других версий их переводит TAGS ниже.
# Для блюд в миске/бутылке кастрюля сама требует тару (берётся из craftRemainder предмета).
# ---------------------------------------------------------------------------------------------------------------
R = [
 # --- Завтраки и яйца ---
 ('omelet', 'pot', ['#forge:eggs', '#forge:eggs', '#forge:milk']),
 ('hashbrowns', 'pot', ['#forge:crops/potato', '#forge:crops/potato', '#forge:crops/onion']),
 ('pancakes', 'craft', ['#forge:dough', '#forge:eggs', '#forge:milk']),
 ('complete_breakfast', 'craft', ['fd:fried_egg', '#forge:milk', 'sd:hashbrowns', 'sd:pancakes', 'minecraft:bowl']),
 ('farmers_lunch', 'craft', ['sd:omelet', '#forge:crops/carrot', '#forge:salad_ingredients', 'minecraft:bowl']),
 ('triple_shot_espresso', 'pot', ['minecraft:cocoa_beans', 'minecraft:cocoa_beans', 'minecraft:cocoa_beans'], {'tab': 'drinks'}),
 ('ginger_ale', 'pot', ['#forge:crops/carrot', '#forge:crops/carrot', 'minecraft:sugar', 'minecraft:honey_bottle'], {'tab': 'drinks'}),
 # --- Супы и похлёбки (кастрюля, миска) ---
 ('parsnip_soup', 'pot', ['#forge:crops/carrot', '#forge:crops/carrot', '#forge:milk', '#forge:crops/onion']),
 ('vegetable_medley', 'pot', ['#forge:crops/tomato', '#forge:crops/beetroot', '#forge:crops/carrot']),
 ('bean_hotpot', 'pot', ['minecraft:pumpkin_seeds', 'minecraft:pumpkin_seeds', 'fd:tomato_sauce', '#forge:crops/onion']),
 ('tom_kha_soup', 'pot', ['#forge:raw_fishes/tropical_fish', 'minecraft:brown_mushroom', '#forge:milk', '#forge:crops/onion']),
 ('trout_soup', 'pot', ['#forge:raw_fishes/salmon', 'minecraft:kelp', '#forge:crops/onion']),
 ('algae_soup', 'pot', ['minecraft:kelp', 'minecraft:kelp', 'minecraft:kelp']),
 ('pale_broth', 'pot', ['minecraft:dried_kelp', 'minecraft:dried_kelp', 'minecraft:bone_meal']),
 ('pumpkin_soup', 'pot', ['fd:pumpkin_slice', 'fd:pumpkin_slice', '#forge:milk', '#forge:crops/onion']),
 ('autumns_bounty', 'pot', ['fd:pumpkin_slice', '#forge:crops/potato', '#forge:crops/carrot', 'minecraft:sugar']),
 ('chowder', 'pot', ['#forge:raw_fishes/cod', '#forge:crops/potato', '#forge:milk', '#forge:crops/onion']),
 ('lobster_bisque', 'pot', ['#forge:raw_fishes/tropical_fish', '#forge:raw_fishes/tropical_fish', '#forge:milk', '#forge:crops/tomato']),
 ('fish_stew', 'pot', ['#forge:raw_fishes', '#forge:raw_fishes', '#forge:raw_fishes', '#forge:crops/tomato', '#forge:crops/onion']),
 ('poi', 'pot', ['#forge:crops/potato', '#forge:crops/potato', '#forge:crops/potato', '#forge:crops/potato']),
 ('tropical_curry', 'pot', ['#forge:crops/rice', 'minecraft:melon_slice', 'minecraft:cocoa_beans', 'minecraft:blaze_powder']),
 ('fiddlehead_risotto', 'pot', ['#forge:crops/rice', 'minecraft:fern', '#forge:crops/onion', '#forge:milk']),
 ('stir_fry', 'pot', ['#forge:crops/carrot', 'minecraft:brown_mushroom', '#forge:crops/cabbage', 'minecraft:glow_berries']),
 # --- Вторые блюда в широкой миске (кастрюля сама просит миску; на верстаке миска — ингредиент) ---
 ('cheese_cauliflower', 'pot', ['#forge:crops/cabbage', '#forge:milk', '#forge:milk']),
 ('baked_fish', 'pot', ['#forge:raw_fishes', '#forge:raw_fishes', '#forge:crops/wheat']),
 ('fried_mushroom', 'pot', ['minecraft:brown_mushroom', 'minecraft:red_mushroom', '#forge:crops/onion']),
 ('glazed_yams', 'pot', ['#forge:crops/potato', 'minecraft:sugar', 'minecraft:honey_bottle']),
 ('carp_surprise', 'pot', ['#forge:raw_fishes/cod', '#forge:raw_fishes/cod', '#forge:raw_fishes/cod', '#forge:raw_fishes/cod']),
 ('salmon_dinner', 'pot', ['#forge:raw_fishes/salmon', '#forge:crops/cabbage', '#forge:crops/onion']),
 ('crispy_bass', 'pot', ['#forge:raw_fishes/cod', '#forge:dough', 'minecraft:sunflower']),
 ('spaghetti', 'pot', ['#forge:pasta', '#forge:crops/tomato', '#forge:crops/tomato']),
 ('fried_eel', 'pot', ['#forge:raw_fishes/cod', 'minecraft:sunflower']),
 ('spicy_eel', 'pot', ['#forge:raw_fishes/cod', 'minecraft:blaze_powder']),
 ('red_plate', 'pot', ['#forge:crops/beetroot', '#forge:crops/beetroot', '#forge:crops/cabbage', 'minecraft:apple']),
 ('eggplant_parmesan', 'pot', ['#forge:crops/tomato', '#forge:crops/beetroot', '#forge:milk', '#forge:dough']),
 ('super_meal', 'pot', ['#forge:crops/cabbage', 'minecraft:sweet_berries', 'minecraft:fern']),
 ('roots_platter', 'pot', ['#forge:crops/carrot', '#forge:crops/potato', 'minecraft:glow_berries']),
 ('artichoke_dip', 'pot', ['minecraft:fern', '#forge:milk', '#forge:crops/onion']),
 ('escargot', 'pot', ['minecraft:slime_ball', '#forge:crops/onion', 'minecraft:sunflower']),
 ('squid_ink_ravioli', 'pot', ['minecraft:ink_sac', '#forge:dough', '#forge:crops/tomato']),
 ('dish_o_the_sea', 'craft', ['#forge:cooked_fishes', '#forge:cooked_fishes', 'sd:hashbrowns', 'minecraft:bowl']),
 ('stuffing', 'craft', ['#forge:bread', 'minecraft:sweet_berries', 'sd:roasted_hazelnuts', 'minecraft:bowl']),
 # --- Сладкие блюда в миске ---
 ('cranberry_sauce', 'pot', ['minecraft:sweet_berries', 'minecraft:sweet_berries', 'minecraft:sugar']),
 ('rice_pudding', 'pot', ['#forge:crops/rice', '#forge:milk', 'minecraft:sugar']),
 ('plum_pudding', 'pot', ['minecraft:apple', 'minecraft:apple', '#forge:crops/wheat', 'minecraft:sugar']),
 ('seafoam_pudding', 'pot', ['#forge:raw_fishes', '#forge:raw_fishes', 'minecraft:ink_sac', '#forge:milk']),
 ('banana_pudding', 'pot', ['minecraft:glow_berries', '#forge:milk', 'minecraft:sugar']),
 ('mango_sticky_rice', 'pot', ['minecraft:melon_slice', '#forge:crops/rice', '#forge:milk', 'minecraft:sugar']),
 ('ice_cream', 'craft', ['#forge:milk', 'minecraft:sugar', 'minecraft:snowball', 'minecraft:bowl']),
 # --- Салаты (верстак + миска, как салаты FD) ---
 ('salad', 'craft', ['#forge:salad_ingredients', 'minecraft:dandelion', 'minecraft:apple', 'minecraft:bowl']),
 ('radish_salad', 'craft', ['#forge:crops/beetroot', '#forge:crops/beetroot', '#forge:salad_ingredients', 'minecraft:bowl']),
 ('coleslaw', 'craft', ['#forge:crops/cabbage', '#forge:crops/beetroot', '#forge:eggs', 'minecraft:bowl']),
 ('fruit_salad', 'craft', ['minecraft:sweet_berries', 'minecraft:melon_slice', 'minecraft:apple', 'minecraft:bowl']),
 ('shrimp_cocktail', 'craft', ['#forge:raw_fishes/tropical_fish', '#forge:crops/tomato', '#forge:crops/carrot', 'minecraft:bowl']),
 # --- Снеки: едятся с руки, без тары (как бутерброды и роллы FD) ---
 ('fried_calamari', 'pot', ['minecraft:ink_sac', 'minecraft:ink_sac', '#forge:dough']),
 ('pepper_poppers', 'pot', ['minecraft:blaze_powder', '#forge:milk', '#forge:crops/tomato']),
 ('roasted_hazelnuts', 'pot', ['minecraft:pumpkin_seeds', 'minecraft:pumpkin_seeds', 'minecraft:pumpkin_seeds']),
 ('crab_cakes', 'pot', ['#forge:raw_fishes/tropical_fish', '#forge:dough', '#forge:eggs', 'minecraft:sunflower']),
 ('strange_bun', 'pot', ['#forge:dough', '#forge:raw_fishes', 'minecraft:chorus_fruit']),
 ('lucky_lunch', 'craft', ['minecraft:sea_pickle', 'sd:tortilla', 'minecraft:cornflower']),
 ('tortilla', 'craft', ['#forge:dough', '#forge:dough'], {'count': 3}),
 ('pizza', 'craft', ['#forge:dough', 'fd:tomato_sauce', '#forge:milk']),
 ('fish_taco', 'craft', ['#forge:cooked_fishes', 'sd:tortilla', '#forge:crops/cabbage', '#forge:crops/tomato']),
 ('survival_burger', 'craft', ['#forge:bread', '#forge:crops/carrot', 'minecraft:glow_berries', 'fd:cabbage_leaf']),
 ('bruschetta', 'craft', ['#forge:bread', '#forge:crops/tomato', 'minecraft:sunflower']),
 ('maki_roll', 'craft', ['#forge:raw_fishes', 'minecraft:dried_kelp', 'fd:cooked_rice']),
 # --- Выпечка и десерты (верстак) ---
 ('miners_treat', 'craft', ['minecraft:glow_berries', 'minecraft:glow_berries', 'minecraft:sugar', '#forge:milk']),
 ('chocolate_cake', 'craft', ['#forge:dough', 'minecraft:cocoa_beans', 'minecraft:cocoa_beans', 'minecraft:sugar', '#forge:eggs', '#forge:milk']),
 ('pink_cake', 'craft', ['#forge:dough', 'minecraft:melon_slice', 'minecraft:melon_slice', 'minecraft:sugar', '#forge:eggs']),
 ('rhubarb_pie', 'craft', ['fd:pie_crust', 'minecraft:sugar_cane', 'minecraft:sugar_cane', 'minecraft:sugar']),
 ('pumpkin_pie', 'craft', ['fd:pie_crust', 'fd:pumpkin_slice', 'minecraft:sugar', 'minecraft:honey_bottle']),
 ('blueberry_tart', 'craft', ['fd:pie_crust', 'minecraft:sweet_berries', 'minecraft:sweet_berries', '#forge:eggs']),
 ('blackberry_cobbler', 'craft', ['#forge:dough', 'minecraft:sweet_berries', 'minecraft:sweet_berries', 'minecraft:sweet_berries', 'minecraft:sugar']),
 ('cookie', 'craft', ['#forge:dough', 'minecraft:sugar', '#forge:eggs'], {'count': 4}),
 ('cranberry_candy', 'craft', ['minecraft:sweet_berries', 'minecraft:apple', 'minecraft:sugar', 'minecraft:sugar']),
 ('poppyseed_muffin', 'craft', ['#forge:dough', 'minecraft:poppy', 'minecraft:sugar']),
 ('maple_bar', 'craft', ['#forge:dough', 'minecraft:honey_bottle', 'minecraft:sugar']),
 # --- Разделочная доска ---
 ('sashimi', 'cut', ['minecraft:tropical_fish'], {'count': 2}),
]

# ---------------------------------------------------------------------------------------------------------------
# Версии Minecraft и загрузчики (как в settings.gradle.kts). У каждой — свои теги, формат рецептов Farmer's Delight
# и формат данных Minecraft. Теги проверены по jar-файлам FD, Forge/NeoForge и Fabric API каждой версии:
# все существуют и не пустые. Поле tool — ровно как в рецепте разделочной доски самого FD (cutting/cod.json).
# ---------------------------------------------------------------------------------------------------------------
CROPS = ['potato', 'onion', 'carrot', 'tomato', 'beetroot', 'rice', 'cabbage', 'wheat']
_FORGE_TAGS = ['#forge:eggs', '#forge:milk', '#forge:dough', '#forge:salad_ingredients', '#forge:raw_fishes',
               '#forge:raw_fishes/cod', '#forge:raw_fishes/salmon', '#forge:raw_fishes/tropical_fish',
               '#forge:cooked_fishes', '#forge:pasta', '#forge:bread'] + [f'#forge:crops/{c}' for c in CROPS]
TAGS = {
    # Forge 1.18.2 - 1.20.1: теги forge:*
    'forge': {t: t for t in _FORGE_TAGS},
    # Fabric 1.20.1 (Farmer's Delight Refabricated 2.x): старые общие теги c:*, во множественном числе
    'fab120': {**{f'#forge:crops/{c}': f'#c:crops/{c}' for c in CROPS},
               '#forge:eggs': '#c:eggs', '#forge:milk': '#c:milks', '#forge:dough': '#c:foods/doughs',
               '#forge:salad_ingredients': '#c:salad_ingredients', '#forge:raw_fishes': '#c:foods/raw_fishes',
               '#forge:raw_fishes/cod': '#c:foods/raw_fishes/cod', '#forge:raw_fishes/salmon': '#c:foods/raw_fishes/salmon',
               '#forge:raw_fishes/tropical_fish': '#c:foods/raw_fishes/tropical_fish',
               '#forge:cooked_fishes': '#c:foods/cooked_fishes', '#forge:pasta': '#c:foods/pastas', '#forge:bread': '#c:foods/breads'},
    # NeoForge 1.21.1 и Fabric 1.21.1+: общие теги c:* нового образца. Отдельных тегов для трески, лосося и
    # тропической рыбы нет во всех версиях — там сами предметы. «Любая рыба» — c:foods/safe_raw_fish (без иглобрюха).
    'c': {**{f'#forge:crops/{c}': f'#c:crops/{c}' for c in CROPS},
          '#forge:eggs': '#c:eggs', '#forge:milk': '#c:drinks/milk', '#forge:dough': '#c:foods/dough',
          '#forge:salad_ingredients': '#c:foods/leafy_green', '#forge:raw_fishes': '#c:foods/safe_raw_fish',
          '#forge:raw_fishes/cod': 'minecraft:cod', '#forge:raw_fishes/salmon': 'minecraft:salmon',
          '#forge:raw_fishes/tropical_fish': 'minecraft:tropical_fish',
          '#forge:cooked_fishes': '#c:foods/cooked_fish', '#forge:pasta': '#c:foods/pasta', '#forge:bread': '#c:foods/bread'},
}
# В FD Refabricated для 1.21.5 - 1.21.10 молочная бутылка лежит в c:foods/milk (в остальных версиях — c:drinks/milk)
FOODS_MILK = {'#forge:milk': '#c:foods/milk'}

_TOOL_FORGE_OLD = {'tag': 'forge:tools/knives'}
_TOOL_FORGE = [{'type': 'farmersdelight:tool_action', 'action': 'knife_dig'}, {'tag': 'forge:tools/knives'}]
_TOOL_NEO = [{'type': 'farmersdelight:item_ability', 'action': 'knife_dig'}, {'tag': 'c:tools/knife'}]
_TOOL_FAB121 = {'fabric:type': 'fabric:any', 'ingredients': [{'fabric:type': 'farmersdelight:item_ability', 'action': 'knife_dig'},
                                                             {'tag': 'c:tools/knife'}]}
TARGETS = {
    '1.18.2-forge': dict(tags='forge', tool=_TOOL_FORGE_OLD, pack=(8, 9)),
    '1.19.2-forge': dict(tags='forge', tool=_TOOL_FORGE_OLD, pack=(9, 10)),
    '1.20.1-forge': dict(tags='forge', tool=_TOOL_FORGE, pack=(15, 15)),
    '1.20.1-fabric': dict(tags='fab120', tool={'tag': 'c:tools/knives'}),
    '1.21.1-neoforge': dict(tags='c', tool=_TOOL_NEO),
    '1.21.1-fabric': dict(tags='c', tool=_TOOL_FAB121),
    '1.21.5-fabric': dict(tags='c', extra=FOODS_MILK, tool='#c:tools/knife', tab_key='category'),
    '1.21.8-fabric': dict(tags='c', extra=FOODS_MILK, tool='#c:tools/knife'),
    '1.21.10-fabric': dict(tags='c', extra=FOODS_MILK, tool='#c:tools/knife'),
    '1.21.11-fabric': dict(tags='c', tool='#c:tools/knife'),
    '26.1-fabric': dict(tags='c', tool='#c:tools/knife'),
    '26.2-fabric': dict(tags='c', tool='#c:tools/knife'),
    '26.3-fabric': dict(tags='c', tool='#c:tools/knife'),
}


def ver(s):
    return tuple(int(x) for x in s.split('.'))


class Target:
    """Формат данных одной версии Minecraft + загрузчика."""

    def __init__(self, name, spec):
        self.name = name
        self.mc = ver(name.split('-')[0])
        self.loader = name.split('-')[1]
        self.tags = dict(TAGS[spec['tags']], **spec.get('extra', {}))
        self.tool = spec['tool']
        self.pack = spec.get('pack')
        self.tab_key = spec.get('tab_key', 'recipe_book_tab')
        mc = self.mc
        self.plural = mc < (1, 21)                 # recipes/, advancements/, tags/items/ — до 1.21
        self.result_key = 'item' if mc < (1, 20, 5) else 'id'
        self.string_ingredients = mc >= (1, 21, 2)  # ингредиенты строками "id" / "#тег"
        self.holder_predicates = mc >= (1, 20, 5)   # {"items": "id"} / {"items": "#тег"} в достижениях
        self.craft_category = mc < (26, 2)          # с 26.2 у ванильных рецептов верстака нет поля category
        self.unlock_key = 'recipes' if mc >= (26, 3) else 'recipe'
        self.item_models = mc >= (1, 21, 4)         # assets/<ns>/items/<id>.json
        self.out = os.path.join(ROOT, 'versions', name, 'generated')

    def map(self, s):
        s = self.tags.get(s, s)
        return s.replace('sd:', MOD + ':').replace('fd:', 'farmersdelight:')

    def ingredient(self, s):
        s = self.map(s)
        if self.string_ingredients:
            return s
        return {'tag': s[1:]} if s.startswith('#') else {'item': s}

    def stack(self, item, count=1):
        res = {self.result_key: item}
        if count > 1:
            res['count'] = count
        return res

    def predicate(self, s):
        s = self.map(s)
        if self.holder_predicates:
            return {'items': s}
        return {'tag': s[1:]} if s.startswith('#') else {'items': [s]}

    def dirs(self):
        if self.plural:
            return 'recipes', 'advancements', 'tags/items'
        return 'recipe', 'advancement', 'tags/item'


def wjson(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')


def check(byid):
    """Правила Farmer's Delight, которые легко нарушить при правке таблиц."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import fd_textures
    errors = []
    for it in items:
        i, cat, cont = it['id'], category(it), it['container']
        if cat == 'meals' and cont != 'BOWL':
            errors.append(f'{i}: блюдо из meals должно быть в миске (container BOWL)')
        if cat == 'drinks' and cont != 'GLASS_BOTTLE':
            errors.append(f'{i}: напиток должен быть в бутылке (container GLASS_BOTTLE)')
        if cat == 'snacks' and (cont is not None or i in FD_EXTRA):
            errors.append(f'{i}: снек едят с руки — без тары и без Comfort/Nourishment')
        for e, _, _ in it['effects']:
            if e not in EFFECT_ID:
                errors.append(f'{i}: неизвестный эффект {e} — добавьте его в EFFECT_ID')
        spec = fd_textures.DISHES.get(i)
        want = {'BOWL': ('deep', 'wide'), 'GLASS_BOTTLE': ('glass',), None: (None,)}[cont]
        if spec is None:
            errors.append(f'{i}: нет описания текстуры в tools/fd_textures.py')
        elif spec['cont'] not in want:
            errors.append(f'{i}: на текстуре тара {spec["cont"]}, а у предмета {cont}')
    for r in R:
        name, st, ings = r[0], r[1], r[2]
        cont = byid[name]['container']
        if st == 'craft' and cont == 'BOWL' and 'minecraft:bowl' not in ings:
            errors.append(f'{name}: в рецепт на верстаке нужна миска')
        if st == 'pot' and 'minecraft:bowl' in ings:
            errors.append(f'{name}: кастрюля сама берёт миску как тару — уберите её из ингредиентов')
        for x in ings:
            if x in VANILLA_WITH_TAG:
                errors.append(f'{name}: {x} -> {VANILLA_WITH_TAG[x]}')
            if x.startswith('#') and any(x not in TAGS[k] for k in TAGS):
                errors.append(f'{name}: тег {x} не переведён для всех версий — добавьте его в TAGS')
    if errors:
        sys.exit('Ошибки:\n  ' + '\n  '.join(errors))


def write_dishes():
    """Dishes.java: блюда одинаковы для всех версий — эффекты задаются id, а не полями MobEffects."""
    cont = {'BOWL': 'BOWL', 'GLASS_BOTTLE': 'BOTTLE', None: 'NONE'}
    lines = []
    for it in items:
        effs = list(it['effects'])
        if it['id'] in FD_EXTRA:
            e, d = FD_EXTRA[it['id']]
            effs.insert(0, [e, d, 0])
        s = f'new Dish("{it["id"]}", Dish.Container.{cont[it["container"]]}, {it["nut"]}, {it["sat"]}F)'
        if it['always']:
            s += '.always()'
        if it['drink']:
            s += '.drink()'
        if it['teleport']:
            s += '.teleport()'
        for e, d, a in effs:
            s += f'\n                    .fx("{EFFECT_ID[e]}", {d}, {a})'
        lines.append('            ' + s)
    java = f'''package com.stardewdelight;

// СГЕНЕРИРОВАНО tools/gen.py — правьте tools/items.json или gen.py, а не этот файл.

import java.util.List;

/** Все блюда мода в порядке вкладки творческого режима. */
public final class Dishes {{
    public static final List<Dish> ALL = List.of(
{(",\n").join(lines)});

    private Dishes() {{}}

    public static Dish byId(String id) {{
        for (Dish dish : ALL) if (dish.id.equals(id)) return dish;
        throw new IllegalArgumentException("Unknown dish " + id);
    }}
}}
'''
    with open(DISHES_JAVA, 'w', encoding='utf-8') as f:
        f.write(java)


def write_assets():
    """Модели предметов и языки — общие для всех версий."""
    mdir = os.path.join(RES, 'assets', MOD, 'models', 'item')
    shutil.rmtree(mdir, ignore_errors=True)
    for it in items:
        wjson(os.path.join(mdir, it['id'] + '.json'), {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{MOD}:item/{it["id"]}'}})
    for lang in ('en_us', 'ru_ru'):
        src = json.load(open(os.path.join(ROOT, 'tools', 'lang', lang + '.json'), encoding='utf-8'))
        out = {}
        for k, v in src.items():
            if k in DROP_LANG:
                continue
            k = k.replace('stardewkitchen', MOD)
            if k.startswith('item.') and k.split('.')[-1] in SKIP:
                continue
            out[k] = v
        out['itemGroup.' + MOD] = 'Stardew Delight'
        wjson(os.path.join(RES, 'assets', MOD, 'lang', lang + '.json'), out)


def write_target(t):
    """Рецепты, достижения, теги и прочее для одной версии в versions/<name>/generated."""
    shutil.rmtree(t.out, ignore_errors=True)
    rec_dir, adv_dir, tag_dir = t.dirs()
    data = os.path.join(t.out, 'data')
    for r in R:
        name, st, ings = r[0], r[1], r[2]
        opt = r[3] if len(r) > 3 else {}
        count = opt.get('count', 1)
        res_id = f'{MOD}:{name}'
        if st == 'pot':
            assert len(ings) <= 6
            obj = {'type': 'farmersdelight:cooking', t.tab_key: opt.get('tab', 'meals'),
                   'ingredients': [t.ingredient(x) for x in ings], 'result': t.stack(res_id, count),
                   'experience': 1.0, 'cookingtime': 200}
            sub = 'cooking'
        elif st == 'craft':
            assert len(ings) <= 9
            obj = {'type': 'minecraft:crafting_shapeless'}
            if t.craft_category:
                obj['category'] = 'misc'
            obj.update({'group': MOD, 'ingredients': [t.ingredient(x) for x in ings], 'result': t.stack(res_id, count)})
            sub = 'crafting'
        elif st == 'cut':
            res = t.stack(res_id, count) if t.plural else {'item': t.stack(res_id, count)}
            obj = {'type': 'farmersdelight:cutting', 'ingredients': [t.ingredient(x) for x in ings], 'tool': t.tool, 'result': [res]}
            sub = 'cutting'
        wjson(os.path.join(data, MOD, rec_dir, sub, name + '.json'), obj)

        rec_id = f'{MOD}:{sub}/{name}'
        crit = {'has_the_recipe': {'trigger': 'minecraft:recipe_unlocked', 'conditions': {t.unlock_key: rec_id}}}
        uniq = []
        for x in ings:
            if x not in uniq and x != 'minecraft:bowl':
                uniq.append(x)
        for n, x in enumerate(uniq):
            crit[f'has_ingredient_{n}'] = {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [t.predicate(x)]}}
        wjson(os.path.join(data, MOD, adv_dir, 'recipes', sub, name + '.json'), {
            'parent': 'minecraft:recipes/root', 'criteria': crit, 'requirements': [list(crit.keys())],
            'rewards': {'recipes': [rec_id]}, 'sends_telemetry_event': False})

    # Теги категорий Farmer's Delight
    tags = {'drinks': [], 'meals': [], 'sweets': [], 'snacks': []}
    for it in items:
        tags[category(it)].append(f'{MOD}:{it["id"]}')
    for k, v in tags.items():
        wjson(os.path.join(data, 'farmersdelight', tag_dir, k + '.json'), {'replace': False, 'values': v})

    # Определения предметов (assets/<ns>/items) — с 1.21.4
    if t.item_models:
        for it in items:
            wjson(os.path.join(t.out, 'assets', MOD, 'items', it['id'] + '.json'),
                  {'model': {'type': 'minecraft:model', 'model': f'{MOD}:item/{it["id"]}'}})

    # pack.mcmeta нужен только Forge
    if t.pack:
        resource, datapack = t.pack
        pack = {'description': 'Stardew Delight resources', 'pack_format': datapack}
        if resource != datapack:
            pack['forge:resource_pack_format'] = resource
            pack['forge:data_pack_format'] = datapack
        wjson(os.path.join(t.out, 'pack.mcmeta'), {'pack': pack})


def main():
    byid = {i['id']: i for i in items}
    ids = [r[0] for r in R]
    assert len(ids) == len(set(ids)), 'дубли рецептов'
    assert set(ids) == set(byid), (set(byid) - set(ids), set(ids) - set(byid))
    check(byid)
    if '--check' in sys.argv:
        print(f'OK: {len(items)} блюд, {len(R)} рецептов, {len(TARGETS)} версий')
        return
    write_dishes()
    write_assets()
    for name, spec in TARGETS.items():
        write_target(Target(name, spec))
    print(f'OK: {len(items)} блюд, {len(R)} рецептов, данные для {len(TARGETS)} версий: {", ".join(TARGETS)}')


if __name__ == '__main__':
    main()
