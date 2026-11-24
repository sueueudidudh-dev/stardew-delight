package com.stardewdelight;

import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
//? if >=1.21.2 {
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.component.Consumable;
import net.minecraft.world.item.component.Consumables;
import net.minecraft.world.item.consume_effects.TeleportRandomlyConsumeEffect;
//?}

/** Свойства предмета-блюда для каждой версии Minecraft. Эффекты накладывает DishLogic при поедании. */
public final class DishItems {
    private DishItems() {}

    /** Новый предмет блюда (вызывается при регистрации). */
    public static Item create(Dish dish) {
        Item.Properties properties = properties(dish);
        return dish.drink ? new StardewDrinkItem(dish, properties) : new StardewFoodItem(dish, properties);
    }

    static Item.Properties properties(Dish dish) {
        FoodProperties.Builder food = new FoodProperties.Builder().nutrition(dish.nutrition);
        //? if >=1.20.5 {
        food.saturationModifier(dish.saturation);
        if (dish.alwaysEdible) food.alwaysEdible();
        //?} else {
        /*food.saturationMod(dish.saturation);
        if (dish.alwaysEdible) food.alwaysEat();
        *///?}

        Item.Properties properties = new Item.Properties();
        //? if >=1.21.2 {
        // С 1.21.2 анимация, звук и телепорт (как у плода хоруса) задаются компонентом Consumable
        Consumable.Builder consumable = dish.drink ? Consumables.defaultDrink() : Consumables.defaultFood();
        if (dish.teleports) consumable.onConsume(new TeleportRandomlyConsumeEffect());
        properties.food(food.build(), consumable.build());
        properties.setId(ResourceKey.create(Registries.ITEM, StardewDelight.id(dish.id)));
        if (dish.teleports) properties.useCooldown(1.0F);
        //?} else {
        /*properties.food(food.build());
        *///?}
        //? if <1.19.3 {
        /*properties.tab(ModTab.TAB);
        *///?}

        // Миска и бутылка возвращаются, как у блюд Farmer's Delight; стак 16
        if (dish.container == Dish.Container.BOWL) properties.craftRemainder(Items.BOWL).stacksTo(16);
        if (dish.container == Dish.Container.BOTTLE) properties.craftRemainder(Items.GLASS_BOTTLE).stacksTo(16);
        return properties;
    }
}
