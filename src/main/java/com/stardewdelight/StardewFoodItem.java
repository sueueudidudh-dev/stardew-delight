package com.stardewdelight;

import vectorwing.farmersdelight.common.item.ConsumableItem;

/** Обычное блюдо. ConsumableItem из Farmer's Delight сам возвращает миску и показывает эффекты в подсказке. */
public class StardewFoodItem extends ConsumableItem {
    public StardewFoodItem(Properties properties) {
        super(properties, true, false);
    }
}
