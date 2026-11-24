package com.stardewdelight;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import vectorwing.farmersdelight.common.item.ConsumableItem;

/** Блюдо. ConsumableItem из Farmer's Delight сам возвращает миску; эффекты и подсказку добавляет мод. */
public class StardewFoodItem extends ConsumableItem implements StardewDish {
    private final Dish dish;

    public StardewFoodItem(Dish dish, Properties properties) {
        super(properties, false, false);
        this.dish = dish;
    }

    @Override
    public Dish dish() {
        return dish;
    }

    @Override
    public void affectConsumer(ItemStack stack, Level level, LivingEntity consumer) {
        DishLogic.eaten(this, dish, level, consumer);
    }
}
