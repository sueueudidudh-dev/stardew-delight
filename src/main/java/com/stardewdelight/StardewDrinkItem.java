package com.stardewdelight;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
//? if fabric && >=1.21.2 {
import vectorwing.farmersdelight.common.item.ConsumableItem;
//?} else {
/*import vectorwing.farmersdelight.common.item.DrinkableItem;
*///?}

// Напиток: возвращает стеклянную бутылку. В Farmer's Delight Refabricated для 1.21.2+ нет DrinkableItem:
// там анимацию питья даёт компонент Consumable (см. DishItems), а предмет — обычный ConsumableItem.
//? if fabric && >=1.21.2 {
public class StardewDrinkItem extends ConsumableItem implements StardewDish {
//?} else {
/*public class StardewDrinkItem extends DrinkableItem implements StardewDish {
*///?}
    private final Dish dish;

    public StardewDrinkItem(Dish dish, Properties properties) {
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
