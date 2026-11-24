package com.stardewdelight;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.item.ItemStack;

/**
 * Строки подсказки блюда: «Голод +N, Насыщение +M», эффекты (как у блюд Farmer's Delight) и телепорт.
 * Вызывается из обработчика подсказок загрузчика (ItemTooltipEvent / ItemTooltipCallback).
 */
public final class Tooltips {
    private Tooltips() {}

    public static void append(ItemStack stack, List<Component> tooltip) {
        if (!(stack.getItem() instanceof StardewDish item)) return;
        Dish dish = item.dish();
        String id = StardewDelight.MODID;
        List<Component> lines = new ArrayList<>();
        lines.add(Compat.tr("tooltip." + id + ".food", dish.nutrition, String.format("%.1f", dish.saturationPoints()))
                .withStyle(ChatFormatting.GOLD));
        for (Dish.Fx fx : dish.effects()) {
            var holder = Compat.effect(StardewDelight.parse(fx.effect()));
            if (holder == null) continue;
            MobEffect effect = Compat.value(holder);
            MutableComponent line = Compat.tr(effect.getDescriptionId());
            if (fx.amplifier() > 0) line = Compat.tr("potion.withAmplifier", line, Compat.tr("potion.potency." + fx.amplifier()));
            if (fx.duration() > 20) line = Compat.tr("potion.withDuration", line, duration(fx.duration()));
            lines.add(line.withStyle(effect.getCategory().getTooltipFormatting()));
        }
        if (dish.teleports()) {
            lines.add(Compat.tr("tooltip." + id + ".teleport").withStyle(ChatFormatting.DARK_PURPLE));
        }
        // Сразу под названием предмета
        tooltip.addAll(Math.min(1, tooltip.size()), lines);
    }

    private static String duration(int ticks) {
        int seconds = ticks / 20;
        return String.format("%d:%02d", seconds / 60, seconds % 60);
    }
}
