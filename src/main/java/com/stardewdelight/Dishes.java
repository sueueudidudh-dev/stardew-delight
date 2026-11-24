package com.stardewdelight;

// СГЕНЕРИРОВАНО tools/gen.py — правьте tools/items.json или gen.py, а не этот файл.

import java.util.List;

/** Все блюда мода в порядке вкладки творческого режима. */
public final class Dishes {
    public static final List<Dish> ALL = List.of(
            new Dish("omelet", Dish.Container.NONE, 4, 0.6F),
            new Dish("salad", Dish.Container.BOWL, 5, 0.8F),
            new Dish("cheese_cauliflower", Dish.Container.BOWL, 6, 0.6F)
                    .fx("farmersdelight:nourishment", 3600, 0),
            new Dish("baked_fish", Dish.Container.BOWL, 3, 0.6F)
                    .fx("farmersdelight:nourishment", 1200, 0),
            new Dish("parsnip_soup", Dish.Container.BOWL, 3, 0.8F)
                    .fx("farmersdelight:comfort", 3600, 0),
            new Dish("vegetable_medley", Dish.Container.BOWL, 7, 0.6F)
                    .fx("farmersdelight:comfort", 3600, 0),
            new Dish("complete_breakfast", Dish.Container.BOWL, 8, 1.0F)
                    .fx("farmersdelight:nourishment", 6000, 0)
                    .fx("minecraft:haste", 4200, 1)
                    .fx("minecraft:absorption", 4200, 1),
            new Dish("fried_calamari", Dish.Container.NONE, 3, 0.8F),
            new Dish("strange_bun", Dish.Container.NONE, 4, 0.8F).always().teleport()
                    .fx("minecraft:night_vision", 1200, 0),
            new Dish("lucky_lunch", Dish.Container.NONE, 4, 0.8F)
                    .fx("minecraft:hero_of_the_village", 6600, 2),
            new Dish("fried_mushroom", Dish.Container.BOWL, 5, 0.8F)
                    .fx("farmersdelight:nourishment", 3600, 0)
                    .fx("minecraft:strength", 4200, 1),
            new Dish("pizza", Dish.Container.NONE, 6, 0.8F),
            new Dish("bean_hotpot", Dish.Container.BOWL, 5, 0.3F)
                    .fx("farmersdelight:comfort", 3600, 0)
                    .fx("minecraft:absorption", 4200, 0)
                    .fx("stardewdelight:magnetism", 4200, 0),
            new Dish("glazed_yams", Dish.Container.BOWL, 8, 0.6F)
                    .fx("farmersdelight:nourishment", 3600, 0),
            new Dish("carp_surprise", Dish.Container.BOWL, 4, 0.3F)
                    .fx("farmersdelight:nourishment", 1200, 0)
                    .fx("minecraft:nausea", 100, 0),
            new Dish("hashbrowns", Dish.Container.NONE, 4, 0.6F)
                    .fx("minecraft:haste", 3300, 0),
            new Dish("pancakes", Dish.Container.NONE, 4, 0.6F)
                    .fx("minecraft:jump_boost", 6600, 1),
            new Dish("salmon_dinner", Dish.Container.BOWL, 5, 0.8F)
                    .fx("farmersdelight:nourishment", 3600, 0),
            new Dish("fish_taco", Dish.Container.NONE, 7, 1.0F)
                    .fx("minecraft:luck", 4200, 1),
            new Dish("crispy_bass", Dish.Container.BOWL, 4, 0.8F)
                    .fx("farmersdelight:nourishment", 1200, 0)
                    .fx("stardewdelight:magnetism", 4200, 1),
            new Dish("pepper_poppers", Dish.Container.NONE, 5, 0.6F)
                    .fx("minecraft:haste", 4200, 1)
                    .fx("minecraft:speed", 4200, 0)
                    .fx("minecraft:fire_resistance", 4200, 0),
            new Dish("tom_kha_soup", Dish.Container.BOWL, 7, 0.8F)
                    .fx("farmersdelight:comfort", 3600, 0)
                    .fx("minecraft:haste", 4200, 1)
                    .fx("minecraft:absorption", 4200, 0),
            new Dish("trout_soup", Dish.Container.BOWL, 4, 0.6F)
                    .fx("farmersdelight:comfort", 3600, 0)
                    .fx("minecraft:luck", 2700, 0),
            new Dish("chocolate_cake", Dish.Container.NONE, 6, 1.0F),
            new Dish("pink_cake", Dish.Container.NONE, 10, 1.0F)
                    .fx("minecraft:regeneration", 200, 0),
            new Dish("rhubarb_pie", Dish.Container.NONE, 9, 0.8F),
            new Dish("cookie", Dish.Container.NONE, 4, 0.8F),
            new Dish("spaghetti", Dish.Container.BOWL, 3, 0.6F)
                    .fx("farmersdelight:nourishment", 3600, 0),
            new Dish("fried_eel", Dish.Container.BOWL, 3, 0.6F)
                    .fx("farmersdelight:nourishment", 1200, 0)
                    .fx("minecraft:hero_of_the_village", 4200, 0),
            new Dish("spicy_eel", Dish.Container.BOWL, 5, 0.6F)
                    .fx("farmersdelight:nourishment", 3600, 0)
                    .fx("minecraft:hero_of_the_village", 4200, 0)
                    .fx("minecraft:speed", 4200, 0)
                    .fx("minecraft:fire_resistance", 4200, 0),
            new Dish("sashimi", Dish.Container.NONE, 3, 0.3F),
            new Dish("maki_roll", Dish.Container.NONE, 4, 0.8F),
            new Dish("tortilla", Dish.Container.NONE, 2, 0.3F),
            new Dish("red_plate", Dish.Container.BOWL, 10, 0.6F)
                    .fx("farmersdelight:nourishment", 6000, 0)
                    .fx("minecraft:absorption", 2100, 1),
            new Dish("eggplant_parmesan", Dish.Container.BOWL, 7, 0.6F)
                    .fx("farmersdelight:nourishment", 3600, 0)
                    .fx("minecraft:haste", 2700, 0)
                    .fx("minecraft:resistance", 2700, 1),
            new Dish("rice_pudding", Dish.Container.BOWL, 5, 0.8F),
            new Dish("ice_cream", Dish.Container.BOWL, 4, 0.6F),
            new Dish("blueberry_tart", Dish.Container.NONE, 5, 1.0F),
            new Dish("autumns_bounty", Dish.Container.BOWL, 9, 0.6F)
                    .fx("farmersdelight:comfort", 6000, 0)
                    .fx("minecraft:jump_boost", 4500, 1)
                    .fx("minecraft:resistance", 4500, 1),
            new Dish("pumpkin_soup", Dish.Container.BOWL, 8, 0.6F)
                    .fx("farmersdelight:comfort", 3600, 0)
                    .fx("minecraft:resistance", 4500, 1)
                    .fx("minecraft:hero_of_the_village", 4500, 1),
            new Dish("super_meal", Dish.Container.BOWL, 6, 0.8F)
                    .fx("farmersdelight:nourishment", 3600, 0)
                    .fx("minecraft:absorption", 2100, 0)
                    .fx("minecraft:speed", 2100, 0),
            new Dish("cranberry_sauce", Dish.Container.BOWL, 5, 0.6F)
                    .fx("minecraft:haste", 2100, 1)
                    .fx("minecraft:night_vision", 2100, 0),
            new Dish("stuffing", Dish.Container.BOWL, 7, 0.8F)
                    .fx("farmersdelight:nourishment", 3600, 0)
                    .fx("minecraft:resistance", 3300, 1),
            new Dish("farmers_lunch", Dish.Container.BOWL, 8, 0.6F)
                    .fx("farmersdelight:nourishment", 6000, 0)
                    .fx("minecraft:haste", 3300, 2),
            new Dish("survival_burger", Dish.Container.NONE, 5, 0.8F)
                    .fx("minecraft:jump_boost", 3300, 1),
            new Dish("dish_o_the_sea", Dish.Container.BOWL, 6, 0.6F)
                    .fx("farmersdelight:nourishment", 3600, 0)
                    .fx("minecraft:luck", 3300, 2)
                    .fx("minecraft:water_breathing", 3300, 0),
            new Dish("miners_treat", Dish.Container.NONE, 5, 0.8F)
                    .fx("minecraft:haste", 3300, 2)
                    .fx("minecraft:night_vision", 3300, 0)
                    .fx("stardewdelight:magnetism", 3300, 0),
            new Dish("roots_platter", Dish.Container.BOWL, 5, 0.6F)
                    .fx("farmersdelight:nourishment", 3600, 0)
                    .fx("minecraft:strength", 3300, 1),
            new Dish("triple_shot_espresso", Dish.Container.BOTTLE, 1, 0.6F).always().drink()
                    .fx("minecraft:speed", 2400, 1)
                    .fx("minecraft:haste", 2400, 0),
            new Dish("seafoam_pudding", Dish.Container.BOWL, 7, 0.6F)
                    .fx("minecraft:luck", 2100, 3)
                    .fx("minecraft:water_breathing", 2100, 0)
                    .fx("minecraft:dolphins_grace", 2100, 0),
            new Dish("algae_soup", Dish.Container.BOWL, 3, 0.3F)
                    .fx("farmersdelight:comfort", 3600, 0),
            new Dish("pale_broth", Dish.Container.BOWL, 5, 0.3F)
                    .fx("farmersdelight:comfort", 3600, 0),
            new Dish("plum_pudding", Dish.Container.BOWL, 7, 0.8F),
            new Dish("artichoke_dip", Dish.Container.BOWL, 4, 0.6F),
            new Dish("stir_fry", Dish.Container.BOWL, 8, 1.0F)
                    .fx("farmersdelight:nourishment", 3600, 0),
            new Dish("roasted_hazelnuts", Dish.Container.NONE, 7, 0.3F),
            new Dish("pumpkin_pie", Dish.Container.NONE, 9, 1.0F)
                    .fx("minecraft:regeneration", 200, 0),
            new Dish("radish_salad", Dish.Container.BOWL, 8, 0.8F),
            new Dish("fruit_salad", Dish.Container.BOWL, 11, 0.8F)
                    .fx("minecraft:regeneration", 200, 0),
            new Dish("blackberry_cobbler", Dish.Container.NONE, 7, 0.8F),
            new Dish("cranberry_candy", Dish.Container.NONE, 5, 0.8F),
            new Dish("bruschetta", Dish.Container.NONE, 5, 0.8F),
            new Dish("coleslaw", Dish.Container.BOWL, 9, 0.8F),
            new Dish("fiddlehead_risotto", Dish.Container.BOWL, 9, 0.8F)
                    .fx("farmersdelight:nourishment", 3600, 0)
                    .fx("minecraft:regeneration", 200, 0),
            new Dish("poppyseed_muffin", Dish.Container.NONE, 6, 0.8F),
            new Dish("chowder", Dish.Container.BOWL, 9, 0.8F)
                    .fx("farmersdelight:comfort", 6000, 0)
                    .fx("minecraft:luck", 10200, 0),
            new Dish("lobster_bisque", Dish.Container.BOWL, 9, 0.6F)
                    .fx("farmersdelight:comfort", 6000, 0)
                    .fx("minecraft:luck", 10200, 2)
                    .fx("minecraft:water_breathing", 10200, 0)
                    .fx("minecraft:absorption", 10200, 1),
            new Dish("escargot", Dish.Container.BOWL, 9, 0.6F)
                    .fx("farmersdelight:nourishment", 3600, 0)
                    .fx("minecraft:luck", 10200, 1),
            new Dish("fish_stew", Dish.Container.BOWL, 9, 0.6F)
                    .fx("farmersdelight:comfort", 6000, 0)
                    .fx("minecraft:luck", 10200, 2)
                    .fx("minecraft:water_breathing", 10200, 0),
            new Dish("maple_bar", Dish.Container.NONE, 9, 0.8F)
                    .fx("minecraft:haste", 10200, 0)
                    .fx("minecraft:luck", 10200, 0),
            new Dish("crab_cakes", Dish.Container.NONE, 9, 1.0F)
                    .fx("minecraft:speed", 10200, 0)
                    .fx("minecraft:resistance", 10200, 0),
            new Dish("shrimp_cocktail", Dish.Container.BOWL, 9, 0.8F)
                    .fx("minecraft:luck", 6000, 0)
                    .fx("minecraft:hero_of_the_village", 6000, 0),
            new Dish("ginger_ale", Dish.Container.BOTTLE, 3, 0.8F).always().drink()
                    .fx("minecraft:hero_of_the_village", 3000, 0),
            new Dish("banana_pudding", Dish.Container.BOWL, 5, 0.8F)
                    .fx("minecraft:haste", 3000, 0)
                    .fx("minecraft:hero_of_the_village", 3000, 0)
                    .fx("minecraft:resistance", 3000, 0),
            new Dish("mango_sticky_rice", Dish.Container.BOWL, 5, 0.8F)
                    .fx("minecraft:resistance", 3000, 1),
            new Dish("poi", Dish.Container.BOWL, 3, 0.3F)
                    .fx("farmersdelight:comfort", 3600, 0),
            new Dish("tropical_curry", Dish.Container.BOWL, 6, 0.8F)
                    .fx("farmersdelight:nourishment", 3600, 0)
                    .fx("minecraft:jump_boost", 3000, 1)
                    .fx("minecraft:fire_resistance", 3000, 0),
            new Dish("squid_ink_ravioli", Dish.Container.BOWL, 5, 0.8F)
                    .fx("farmersdelight:nourishment", 3600, 0)
                    .fx("minecraft:haste", 2700, 0)
                    .fx("stardewdelight:immunity", 1800, 0));

    private Dishes() {}

    public static Dish byId(String id) {
        for (Dish dish : ALL) if (dish.id.equals(id)) return dish;
        throw new IllegalArgumentException("Unknown dish " + id);
    }
}
