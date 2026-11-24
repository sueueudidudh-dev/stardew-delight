package com.stardewdelight;

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

public final class ModItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, StardewDelight.MODID);
    public static final List<RegistryObject<Item>> ALL = new ArrayList<>();

    private ModItems() {}

    private static RegistryObject<Item> reg(String id, Supplier<Item> sup) {
        RegistryObject<Item> ro = ITEMS.register(id, sup);
        ALL.add(ro);
        return ro;
    }

    private static FoodProperties.Builder food(int nutrition, float saturation) {
        return new FoodProperties.Builder().nutrition(nutrition).saturationMod(saturation);
    }

    /** Блюдо на тарелке / в руках. */
    private static Item.Properties plate(FoodProperties food) {
        return new Item.Properties().food(food);
    }

    /** Блюдо в миске: возвращает миску, стак 16 (как миски Farmer's Delight). */
    private static Item.Properties bowl(FoodProperties food) {
        return new Item.Properties().food(food).craftRemainder(Items.BOWL).stacksTo(16);
    }

    /** Напиток в стеклянной бутылке. */
    private static Item.Properties bottle(FoodProperties food) {
        return new Item.Properties().food(food).craftRemainder(Items.GLASS_BOTTLE).stacksTo(16);
    }

    public static final RegistryObject<Item> OMELET = reg("omelet", () -> new StardewFoodItem(plate(food(4, 0.6F)
                .build())));
    public static final RegistryObject<Item> SALAD = reg("salad", () -> new StardewFoodItem(bowl(food(5, 0.8F)
                .build())));
    public static final RegistryObject<Item> CHEESE_CAULIFLOWER = reg("cheese_cauliflower", () -> new StardewFoodItem(bowl(food(6, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> BAKED_FISH = reg("baked_fish", () -> new StardewFoodItem(bowl(food(3, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 1200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> PARSNIP_SOUP = reg("parsnip_soup", () -> new StardewFoodItem(bowl(food(3, 0.8F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 3600, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> VEGETABLE_MEDLEY = reg("vegetable_medley", () -> new StardewFoodItem(bowl(food(7, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 3600, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> COMPLETE_BREAKFAST = reg("complete_breakfast", () -> new StardewFoodItem(bowl(food(8, 1.0F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 6000, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 4200, 1), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.ABSORPTION, 4200, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> FRIED_CALAMARI = reg("fried_calamari", () -> new StardewFoodItem(plate(food(3, 0.8F)
                .build())));
    public static final RegistryObject<Item> STRANGE_BUN = reg("strange_bun", () -> new StrangeBunItem(plate(food(4, 0.8F).alwaysEat()
                .effect(() -> new MobEffectInstance(MobEffects.NIGHT_VISION, 1200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> LUCKY_LUNCH = reg("lucky_lunch", () -> new StardewFoodItem(plate(food(4, 0.8F)
                .effect(() -> new MobEffectInstance(MobEffects.HERO_OF_THE_VILLAGE, 6600, 2), 1.0F)
                .build())));
    public static final RegistryObject<Item> FRIED_MUSHROOM = reg("fried_mushroom", () -> new StardewFoodItem(bowl(food(5, 0.8F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DAMAGE_BOOST, 4200, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> PIZZA = reg("pizza", () -> new StardewFoodItem(plate(food(6, 0.8F)
                .build())));
    public static final RegistryObject<Item> BEAN_HOTPOT = reg("bean_hotpot", () -> new StardewFoodItem(bowl(food(5, 0.3F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.ABSORPTION, 4200, 0), 1.0F)
                .effect(() -> new MobEffectInstance(ModEffects.MAGNETISM.get(), 4200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> GLAZED_YAMS = reg("glazed_yams", () -> new StardewFoodItem(bowl(food(8, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> CARP_SURPRISE = reg("carp_surprise", () -> new StardewFoodItem(bowl(food(4, 0.3F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 1200, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.CONFUSION, 100, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> HASHBROWNS = reg("hashbrowns", () -> new StardewFoodItem(plate(food(4, 0.6F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 3300, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> PANCAKES = reg("pancakes", () -> new StardewFoodItem(plate(food(4, 0.6F)
                .effect(() -> new MobEffectInstance(MobEffects.JUMP, 6600, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> SALMON_DINNER = reg("salmon_dinner", () -> new StardewFoodItem(bowl(food(5, 0.8F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> FISH_TACO = reg("fish_taco", () -> new StardewFoodItem(plate(food(7, 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.LUCK, 4200, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> CRISPY_BASS = reg("crispy_bass", () -> new StardewFoodItem(bowl(food(4, 0.8F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 1200, 0), 1.0F)
                .effect(() -> new MobEffectInstance(ModEffects.MAGNETISM.get(), 4200, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> PEPPER_POPPERS = reg("pepper_poppers", () -> new StardewFoodItem(plate(food(5, 0.6F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 4200, 1), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 4200, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 4200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> TOM_KHA_SOUP = reg("tom_kha_soup", () -> new StardewFoodItem(bowl(food(7, 0.8F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 4200, 1), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.ABSORPTION, 4200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> TROUT_SOUP = reg("trout_soup", () -> new StardewFoodItem(bowl(food(4, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.LUCK, 2700, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> CHOCOLATE_CAKE = reg("chocolate_cake", () -> new StardewFoodItem(plate(food(6, 1.0F)
                .build())));
    public static final RegistryObject<Item> PINK_CAKE = reg("pink_cake", () -> new StardewFoodItem(plate(food(10, 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.REGENERATION, 200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> RHUBARB_PIE = reg("rhubarb_pie", () -> new StardewFoodItem(plate(food(9, 0.8F)
                .build())));
    public static final RegistryObject<Item> COOKIE = reg("cookie", () -> new StardewFoodItem(plate(food(4, 0.8F)
                .build())));
    public static final RegistryObject<Item> SPAGHETTI = reg("spaghetti", () -> new StardewFoodItem(bowl(food(3, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> FRIED_EEL = reg("fried_eel", () -> new StardewFoodItem(bowl(food(3, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 1200, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.HERO_OF_THE_VILLAGE, 4200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> SPICY_EEL = reg("spicy_eel", () -> new StardewFoodItem(bowl(food(5, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.HERO_OF_THE_VILLAGE, 4200, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 4200, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 4200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> SASHIMI = reg("sashimi", () -> new StardewFoodItem(plate(food(3, 0.3F)
                .build())));
    public static final RegistryObject<Item> MAKI_ROLL = reg("maki_roll", () -> new StardewFoodItem(plate(food(4, 0.8F)
                .build())));
    public static final RegistryObject<Item> TORTILLA = reg("tortilla", () -> new StardewFoodItem(plate(food(2, 0.3F)
                .build())));
    public static final RegistryObject<Item> RED_PLATE = reg("red_plate", () -> new StardewFoodItem(bowl(food(10, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 6000, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.ABSORPTION, 2100, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> EGGPLANT_PARMESAN = reg("eggplant_parmesan", () -> new StardewFoodItem(bowl(food(7, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 2700, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 2700, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> RICE_PUDDING = reg("rice_pudding", () -> new StardewFoodItem(bowl(food(5, 0.8F)
                .build())));
    public static final RegistryObject<Item> ICE_CREAM = reg("ice_cream", () -> new StardewFoodItem(bowl(food(4, 0.6F)
                .build())));
    public static final RegistryObject<Item> BLUEBERRY_TART = reg("blueberry_tart", () -> new StardewFoodItem(plate(food(5, 1.0F)
                .build())));
    public static final RegistryObject<Item> AUTUMNS_BOUNTY = reg("autumns_bounty", () -> new StardewFoodItem(bowl(food(9, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 6000, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.JUMP, 4500, 1), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 4500, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> PUMPKIN_SOUP = reg("pumpkin_soup", () -> new StardewFoodItem(bowl(food(8, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 4500, 1), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.HERO_OF_THE_VILLAGE, 4500, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> SUPER_MEAL = reg("super_meal", () -> new StardewFoodItem(bowl(food(6, 0.8F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.ABSORPTION, 2100, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 2100, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> CRANBERRY_SAUCE = reg("cranberry_sauce", () -> new StardewFoodItem(bowl(food(5, 0.6F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 2100, 1), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.NIGHT_VISION, 2100, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> STUFFING = reg("stuffing", () -> new StardewFoodItem(bowl(food(7, 0.8F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 3300, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> FARMERS_LUNCH = reg("farmers_lunch", () -> new StardewFoodItem(bowl(food(8, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 6000, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 3300, 2), 1.0F)
                .build())));
    public static final RegistryObject<Item> SURVIVAL_BURGER = reg("survival_burger", () -> new StardewFoodItem(plate(food(5, 0.8F)
                .effect(() -> new MobEffectInstance(MobEffects.JUMP, 3300, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> DISH_O_THE_SEA = reg("dish_o_the_sea", () -> new StardewFoodItem(bowl(food(6, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.LUCK, 3300, 2), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.WATER_BREATHING, 3300, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> MINERS_TREAT = reg("miners_treat", () -> new StardewFoodItem(plate(food(5, 0.8F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 3300, 2), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.NIGHT_VISION, 3300, 0), 1.0F)
                .effect(() -> new MobEffectInstance(ModEffects.MAGNETISM.get(), 3300, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> ROOTS_PLATTER = reg("roots_platter", () -> new StardewFoodItem(bowl(food(5, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DAMAGE_BOOST, 3300, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> TRIPLE_SHOT_ESPRESSO = reg("triple_shot_espresso", () -> new StardewDrinkItem(bottle(food(1, 0.6F).alwaysEat()
                .effect(() -> new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 2400, 1), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 2400, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> SEAFOAM_PUDDING = reg("seafoam_pudding", () -> new StardewFoodItem(bowl(food(7, 0.6F)
                .effect(() -> new MobEffectInstance(MobEffects.LUCK, 2100, 3), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.WATER_BREATHING, 2100, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DOLPHINS_GRACE, 2100, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> ALGAE_SOUP = reg("algae_soup", () -> new StardewFoodItem(bowl(food(3, 0.3F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 3600, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> PALE_BROTH = reg("pale_broth", () -> new StardewFoodItem(bowl(food(5, 0.3F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 3600, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> PLUM_PUDDING = reg("plum_pudding", () -> new StardewFoodItem(bowl(food(7, 0.8F)
                .build())));
    public static final RegistryObject<Item> ARTICHOKE_DIP = reg("artichoke_dip", () -> new StardewFoodItem(bowl(food(4, 0.6F)
                .build())));
    public static final RegistryObject<Item> STIR_FRY = reg("stir_fry", () -> new StardewFoodItem(bowl(food(8, 1.0F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> ROASTED_HAZELNUTS = reg("roasted_hazelnuts", () -> new StardewFoodItem(plate(food(7, 0.3F)
                .build())));
    public static final RegistryObject<Item> PUMPKIN_PIE = reg("pumpkin_pie", () -> new StardewFoodItem(plate(food(9, 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.REGENERATION, 200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> RADISH_SALAD = reg("radish_salad", () -> new StardewFoodItem(bowl(food(8, 0.8F)
                .build())));
    public static final RegistryObject<Item> FRUIT_SALAD = reg("fruit_salad", () -> new StardewFoodItem(bowl(food(11, 0.8F)
                .effect(() -> new MobEffectInstance(MobEffects.REGENERATION, 200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> BLACKBERRY_COBBLER = reg("blackberry_cobbler", () -> new StardewFoodItem(plate(food(7, 0.8F)
                .build())));
    public static final RegistryObject<Item> CRANBERRY_CANDY = reg("cranberry_candy", () -> new StardewFoodItem(plate(food(5, 0.8F)
                .build())));
    public static final RegistryObject<Item> BRUSCHETTA = reg("bruschetta", () -> new StardewFoodItem(plate(food(5, 0.8F)
                .build())));
    public static final RegistryObject<Item> COLESLAW = reg("coleslaw", () -> new StardewFoodItem(bowl(food(9, 0.8F)
                .build())));
    public static final RegistryObject<Item> FIDDLEHEAD_RISOTTO = reg("fiddlehead_risotto", () -> new StardewFoodItem(bowl(food(9, 0.8F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.REGENERATION, 200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> POPPYSEED_MUFFIN = reg("poppyseed_muffin", () -> new StardewFoodItem(plate(food(6, 0.8F)
                .build())));
    public static final RegistryObject<Item> CHOWDER = reg("chowder", () -> new StardewFoodItem(bowl(food(9, 0.8F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 6000, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.LUCK, 10200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> LOBSTER_BISQUE = reg("lobster_bisque", () -> new StardewFoodItem(bowl(food(9, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 6000, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.LUCK, 10200, 2), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.WATER_BREATHING, 10200, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.ABSORPTION, 10200, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> ESCARGOT = reg("escargot", () -> new StardewFoodItem(bowl(food(9, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.LUCK, 10200, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> FISH_STEW = reg("fish_stew", () -> new StardewFoodItem(bowl(food(9, 0.6F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 6000, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.LUCK, 10200, 2), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.WATER_BREATHING, 10200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> MAPLE_BAR = reg("maple_bar", () -> new StardewFoodItem(plate(food(9, 0.8F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 10200, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.LUCK, 10200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> CRAB_CAKES = reg("crab_cakes", () -> new StardewFoodItem(plate(food(9, 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 10200, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 10200, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> SHRIMP_COCKTAIL = reg("shrimp_cocktail", () -> new StardewFoodItem(bowl(food(9, 0.8F)
                .effect(() -> new MobEffectInstance(MobEffects.LUCK, 6000, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.HERO_OF_THE_VILLAGE, 6000, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> GINGER_ALE = reg("ginger_ale", () -> new StardewDrinkItem(bottle(food(3, 0.8F).alwaysEat()
                .effect(() -> new MobEffectInstance(MobEffects.HERO_OF_THE_VILLAGE, 3000, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> BANANA_PUDDING = reg("banana_pudding", () -> new StardewFoodItem(bowl(food(5, 0.8F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 3000, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.HERO_OF_THE_VILLAGE, 3000, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 3000, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> MANGO_STICKY_RICE = reg("mango_sticky_rice", () -> new StardewFoodItem(bowl(food(5, 0.8F)
                .effect(() -> new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 3000, 1), 1.0F)
                .build())));
    public static final RegistryObject<Item> POI = reg("poi", () -> new StardewFoodItem(bowl(food(3, 0.3F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.COMFORT.get(), 3600, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> TROPICAL_CURRY = reg("tropical_curry", () -> new StardewFoodItem(bowl(food(6, 0.8F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.JUMP, 3000, 1), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 3000, 0), 1.0F)
                .build())));
    public static final RegistryObject<Item> SQUID_INK_RAVIOLI = reg("squid_ink_ravioli", () -> new StardewFoodItem(bowl(food(5, 0.8F)
                .effect(() -> new MobEffectInstance(vectorwing.farmersdelight.common.registry.ModEffects.NOURISHMENT.get(), 3600, 0), 1.0F)
                .effect(() -> new MobEffectInstance(MobEffects.DIG_SPEED, 2700, 0), 1.0F)
                .effect(() -> new MobEffectInstance(ModEffects.IMMUNITY.get(), 1800, 0), 1.0F)
                .build())));
}
