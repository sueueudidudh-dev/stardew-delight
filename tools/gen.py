"""Генератор кода и данных для Stardew Delight.
Читает tools/items.json (параметры блюд, перенесённые из Stardew Kitchen) и таблицу рецептов ниже,
создаёт ModItems.java, рецепты, достижения-разблокировки, модели, теги и языковые файлы.
Заодно проверяет, что всё устроено как в Farmer's Delight: блюда из meals — в миске, снеки — в руках,
у рецептов на верстаке есть миска, тара на текстуре (tools/fd_textures.py) совпадает с тарой предмета."""
import json, os, re, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = 'stardewdelight'
RES = os.path.join(ROOT, 'src/main/resources')
JAVA = os.path.join(ROOT, 'src/main/java/com/stardewdelight/ModItems.java')

SKIP = {'fried_egg', 'bread'}  # уже есть: farmersdelight:fried_egg и minecraft:bread
items = [i for i in json.load(open(os.path.join(ROOT, 'tools/items.json'))) if i['id'] not in SKIP]

EFFECT_MAP = {  # имена 26.x -> 1.20.1 (official mappings)
    'HASTE': 'MobEffects.DIG_SPEED', 'SPEED': 'MobEffects.MOVEMENT_SPEED', 'JUMP_BOOST': 'MobEffects.JUMP',
    'RESISTANCE': 'MobEffects.DAMAGE_RESISTANCE', 'STRENGTH': 'MobEffects.DAMAGE_BOOST', 'NAUSEA': 'MobEffects.CONFUSION',
    'ABSORPTION': 'MobEffects.ABSORPTION', 'NIGHT_VISION': 'MobEffects.NIGHT_VISION', 'LUCK': 'MobEffects.LUCK',
    'HERO_OF_THE_VILLAGE': 'MobEffects.HERO_OF_THE_VILLAGE', 'WATER_BREATHING': 'MobEffects.WATER_BREATHING',
    'DOLPHINS_GRACE': 'MobEffects.DOLPHINS_GRACE', 'FIRE_RESISTANCE': 'MobEffects.FIRE_RESISTANCE',
    'REGENERATION': 'MobEffects.REGENERATION',
    'SK_MAGNETISM': 'ModEffects.MAGNETISM.get()', 'SK_IMMUNITY': 'ModEffects.IMMUNITY.get()',
    'FD_COMFORT': 'vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get()',
    'FD_NOURISHMENT': 'vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get()',
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
# Ванильные продукты с общим тегом Forge: в рецептах — только тег (как у самого FD), чтобы подходили культуры других модов.
VANILLA_WITH_TAG = {'minecraft:carrot': '#forge:crops/carrot', 'minecraft:potato': '#forge:crops/potato',
                    'minecraft:beetroot': '#forge:crops/beetroot', 'minecraft:wheat': '#forge:crops/wheat',
                    'minecraft:cod': '#forge:raw_fishes/cod'}


def category(it):
    i = it['id']
    return 'drinks' if it['drink'] else 'sweets' if i in SWEETS else 'snacks' if i in SNACKS else 'meals'

# ---------------------------------------------------------------------------------------------------------------
# Рецепты. pot = кастрюля FD (cooking pot), craft = верстак (shapeless), cut = разделочная доска с ножом.
# "#тег" — тег предмета, иначе id предмета. Префикс "sd:" = наш мод, "fd:" = farmersdelight.
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

def rid(s):
    return s.replace('sd:', MOD + ':').replace('fd:', 'farmersdelight:')

def ing(s):
    s = rid(s)
    return {'tag': s[1:]} if s.startswith('#') else {'item': s}

def wjson(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False); f.write('\n')

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
    if errors:
        sys.exit('Ошибки:\n  ' + '\n  '.join(errors))


def main():
    byid = {i['id']: i for i in items}
    ids = [r[0] for r in R]
    assert len(ids) == len(set(ids)), 'дубли рецептов'
    assert set(ids) == set(byid), (set(byid) - set(ids), set(ids) - set(byid))
    check(byid)

    # ---------- ModItems.java ----------
    lines = []
    for it in items:
        effs = list(it['effects'])
        if it['id'] in FD_EXTRA:
            e, d = FD_EXTRA[it['id']]; effs.insert(0, [e, d, 0])
        b = f'food({it["nut"]}, {it["sat"]}F)'
        if it['always']: b += '.alwaysEat()'
        for e, d, a in effs:
            b += f'\n                .effect(() -> new MobEffectInstance({EFFECT_MAP[e]}, {d}, {a}), 1.0F)'
        props = {'BOWL': 'bowl', 'GLASS_BOTTLE': 'bottle', None: 'plate'}[it['container']]
        cls = 'StardewDrinkItem' if it['drink'] else ('StrangeBunItem' if it['teleport'] else 'StardewFoodItem')
        lines.append(f'    public static final RegistryObject<Item> {it["id"].upper()} = reg("{it["id"]}", () -> new {cls}({props}({b}\n                .build())));')
    java = f'''package com.stardewdelight;

// СГЕНЕРИРОВАНО tools/gen.py — правьте tools/items.json или gen.py, а не этот файл.

import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public final class ModItems {{
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, StardewDelight.MODID);
    public static final List<RegistryObject<Item>> ALL = new ArrayList<>();

    private ModItems() {{}}

    private static RegistryObject<Item> reg(String id, Supplier<Item> sup) {{
        RegistryObject<Item> ro = ITEMS.register(id, sup);
        ALL.add(ro);
        return ro;
    }}

    private static FoodProperties.Builder food(int nutrition, float saturation) {{
        return new FoodProperties.Builder().nutrition(nutrition).saturationMod(saturation);
    }}

    /** Блюдо на тарелке / в руках. */
    private static Item.Properties plate(FoodProperties food) {{
        return new Item.Properties().food(food);
    }}

    /** Блюдо в миске: возвращает миску, стак 16 (как миски Farmer's Delight). */
    private static Item.Properties bowl(FoodProperties food) {{
        return new Item.Properties().food(food).craftRemainder(Items.BOWL).stacksTo(16);
    }}

    /** Напиток в стеклянной бутылке. */
    private static Item.Properties bottle(FoodProperties food) {{
        return new Item.Properties().food(food).craftRemainder(Items.GLASS_BOTTLE).stacksTo(16);
    }}

{chr(10).join(lines)}
}}
'''
    open(JAVA, 'w', encoding='utf-8').write(java)

    # ---------- рецепты + достижения ----------
    rdir = os.path.join(RES, 'data', MOD, 'recipes'); adir = os.path.join(RES, 'data', MOD, 'advancements', 'recipes')
    for d in (rdir, adir):
        shutil.rmtree(d, ignore_errors=True)
    for r in R:
        name, st, ings = r[0], r[1], r[2]; opt = r[3] if len(r) > 3 else {}
        res = {'item': f'{MOD}:{name}'}
        if opt.get('count'): res['count'] = opt['count']
        if st == 'pot':
            assert len(ings) <= 6
            obj = {'type': 'farmersdelight:cooking', 'recipe_book_tab': opt.get('tab', 'meals'),
                   'ingredients': [ing(x) for x in ings], 'result': res, 'experience': 1.0, 'cookingtime': 200}
            sub = 'cooking'
        elif st == 'craft':
            assert len(ings) <= 9
            obj = {'type': 'minecraft:crafting_shapeless', 'category': 'misc', 'group': MOD,
                   'ingredients': [ing(x) for x in ings], 'result': res}
            sub = 'crafting'
        elif st == 'cut':
            obj = {'type': 'farmersdelight:cutting', 'ingredients': [ing(x) for x in ings],
                   'tool': [{'type': 'farmersdelight:tool_action', 'action': 'knife_dig'}, {'tag': 'forge:tools/knives'}],
                   'result': [res]}
            sub = 'cutting'
        wjson(os.path.join(rdir, sub, name + '.json'), obj)
        rec_id = f'{MOD}:{sub}/{name}'
        crit = {'has_the_recipe': {'trigger': 'minecraft:recipe_unlocked', 'conditions': {'recipe': rec_id}}}
        uniq = []
        for x in ings:
            if x not in uniq and x != 'minecraft:bowl': uniq.append(x)
        for n, x in enumerate(uniq):
            i = ing(x)
            pred = {'tag': i['tag']} if 'tag' in i else {'items': [i['item']]}
            crit[f'has_ingredient_{n}'] = {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [pred]}}
        wjson(os.path.join(adir, sub, name + '.json'), {
            'parent': 'minecraft:recipes/root', 'criteria': crit, 'requirements': [list(crit.keys())],
            'rewards': {'recipes': [rec_id]}, 'sends_telemetry_event': False})

    # ---------- модели ----------
    mdir = os.path.join(RES, 'assets', MOD, 'models', 'item'); shutil.rmtree(mdir, ignore_errors=True)
    for it in items:
        wjson(os.path.join(mdir, it['id'] + '.json'), {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{MOD}:item/{it["id"]}'}})

    # ---------- теги (категории Farmer's Delight) ----------
    tags = {'drinks': [], 'meals': [], 'sweets': [], 'snacks': []}
    for it in items:
        tags[category(it)].append(f'{MOD}:{it["id"]}')
    for k, v in tags.items():
        wjson(os.path.join(RES, 'data', 'farmersdelight', 'tags', 'items', k + '.json'), {'replace': False, 'values': v})

    # ---------- языки ----------
    for lang in ('en_us', 'ru_ru'):
        src = json.load(open(os.path.join(ROOT, 'tools', 'lang', lang + '.json'), encoding='utf-8'))
        out = {}
        for k, v in src.items():
            if k in DROP_LANG: continue
            k = k.replace('stardewkitchen', MOD)
            if k.startswith('item.') and k.split('.')[-1] in SKIP: continue
            out[k] = v
        out['itemGroup.' + MOD] = 'Stardew Delight'
        wjson(os.path.join(RES, 'assets', MOD, 'lang', lang + '.json'), out)
    print(f'OK: {len(items)} блюд, {len(R)} рецептов')

if __name__ == '__main__':
    main()
