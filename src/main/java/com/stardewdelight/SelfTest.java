package com.stardewdelight;

import java.util.List;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

/**
 * Самопроверка для тестового сервера: с -Dstardewdelight.selftest=true после старта сервера
 * считает рецепты мода, съедает каждое блюдо ненастоящим игроком (эффекты и возврат тары)
 * и проверяет «Иммунитет к дебаффам» (то есть что миксин встроен). Итог — строка SELFTEST DONE в логе.
 */
public final class SelfTest {
    private SelfTest() {}

    public static boolean enabled() {
        return Boolean.getBoolean("stardewdelight.selftest");
    }

    public static void run(MinecraftServer server, ServerPlayer player) {
        ServerLevel level = server.overworld();
        int ok = 0;
        int fail = 0;

        // Рецепты: по одному на блюдо, все из данных этой версии
        List<String> ids = Compat.recipeIds(server).stream().filter(id -> id.startsWith(StardewDelight.MODID + ":")).toList();
        for (Dish dish : Dishes.ALL) {
            boolean found = ids.stream().anyMatch(id -> id.endsWith("/" + dish.id));
            if (found) ok++;
            else {
                fail++;
                StardewDelight.LOGGER.error("SELFTEST FAIL recipe for {} not loaded", dish.id);
            }
        }
        if (ids.size() != Dishes.ALL.size()) {
            fail++;
            StardewDelight.LOGGER.error("SELFTEST FAIL {} recipes loaded, {} dishes", ids.size(), Dishes.ALL.size());
        }

        // Блюда: эффекты (Stardew + Farmer's Delight) и тара
        for (Dish dish : Dishes.ALL) {
            player.removeAllEffects();
            ItemStack left = new ItemStack(dish.item()).finishUsingItem(level, player);
            int effects = player.getActiveEffects().size();
            boolean container = switch (dish.container) {
                case BOWL -> left.is(Items.BOWL);
                case BOTTLE -> left.is(Items.GLASS_BOTTLE);
                case NONE -> left.isEmpty();
            };
            if (effects == dish.effects().size() && container) ok++;
            else {
                fail++;
                StardewDelight.LOGGER.error("SELFTEST FAIL {}: {} effects (want {}), left {}", dish.id, effects, dish.effects().size(), left);
            }
        }

        // Иммунитет: не даёт наложить дебафф и снимает уже наложенный
        MobEffectInstance poison = Compat.instance(new Dish.Fx("minecraft:poison", 200, 0));
        MobEffectInstance immunity = Compat.instance(new Dish.Fx(StardewDelight.MODID + ":immunity", 200, 0));
        player.removeAllEffects();
        player.addEffect(immunity);
        boolean blocked = !player.addEffect(poison) && player.getActiveEffects().size() == 1;
        player.removeAllEffects();
        player.addEffect(Compat.instance(new Dish.Fx("minecraft:poison", 200, 0)));
        player.addEffect(Compat.instance(new Dish.Fx(StardewDelight.MODID + ":immunity", 200, 0)));
        EffectLogic.tick(player);
        boolean removed = player.getActiveEffects().size() == 1;
        player.removeAllEffects();
        for (boolean passed : new boolean[] {blocked, removed}) {
            if (passed) ok++;
            else fail++;
        }
        if (!blocked) StardewDelight.LOGGER.error("SELFTEST FAIL immunity does not block poison");
        if (!removed) StardewDelight.LOGGER.error("SELFTEST FAIL immunity does not remove poison");

        StardewDelight.LOGGER.info("SELFTEST DONE: {} ok, {} failed", ok, fail);
    }
}
