package com.stardewdelight;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.event.entity.player.ItemTooltipEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.ForgeRegistries;

/** Добавляет к подсказке строку «Голод +N, Насыщение +M». Эффекты выводит сам Farmer's Delight. */
@Mod.EventBusSubscriber(modid = StardewDelight.MODID, value = Dist.CLIENT)
public final class ClientTooltips {
    private ClientTooltips() {}

    @SubscribeEvent
    public static void onTooltip(ItemTooltipEvent event) {
        ItemStack stack = event.getItemStack();
        var key = ForgeRegistries.ITEMS.getKey(stack.getItem());
        if (key == null || !StardewDelight.MODID.equals(key.getNamespace())) return;
        FoodProperties food = stack.getFoodProperties(event.getEntity());
        if (food == null) return;
        List<Component> tip = event.getToolTip();
        float saturation = food.getNutrition() * food.getSaturationModifier() * 2.0F;
        tip.add(1, Component.translatable("tooltip." + StardewDelight.MODID + ".food", food.getNutrition(), String.format("%.1f", saturation))
                .withStyle(ChatFormatting.GOLD));
        if (stack.getItem() instanceof StrangeBunItem) {
            tip.add(Component.translatable("tooltip." + StardewDelight.MODID + ".teleport").withStyle(ChatFormatting.DARK_PURPLE));
        }
    }
}
