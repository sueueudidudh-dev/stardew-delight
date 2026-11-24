package com.stardewdelight;

import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;
//? if <1.21.2 {
/*import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.Vec3;
*///?}

/** Что происходит, когда блюдо съедено: эффекты Stardew и Farmer's Delight, телепорт странной булочки. */
final class DishLogic {
    private DishLogic() {}

    static void eaten(Item item, Dish dish, Level level, LivingEntity consumer) {
        if (level.isClientSide()) return;
        // Эффекты ищутся по id в момент поедания: так не важен порядок загрузки модов
        for (Dish.Fx fx : dish.effects()) {
            MobEffectInstance instance = Compat.instance(fx);
            if (instance != null) consumer.addEffect(instance);
        }
        //? if <1.21.2 {
        /*if (dish.teleports) teleport(item, level, consumer);
        *///?}
    }

    //? if <1.21.2 {
    /*// Как у плода хоруса: до 16 попыток найти место в радиусе 8 блоков, потом секундная перезарядка
    private static void teleport(Item item, Level level, LivingEntity entity) {
        if (!(level instanceof ServerLevel server)) return;
        double x0 = entity.getX(), y0 = entity.getY(), z0 = entity.getZ();
        for (int i = 0; i < 16; ++i) {
            double x = entity.getX() + (entity.getRandom().nextDouble() - 0.5D) * 16.0D;
            double y = Mth.clamp(entity.getY() + (entity.getRandom().nextInt(16) - 8),
                    level.getMinBuildHeight(), level.getMinBuildHeight() + server.getLogicalHeight() - 1);
            double z = entity.getZ() + (entity.getRandom().nextDouble() - 0.5D) * 16.0D;
            if (entity.isPassenger()) entity.stopRiding();
            Vec3 from = entity.position();
            double[] target = Compat.chorusTarget(entity, x, y, z);
            if (target == null) return;
            if (entity.randomTeleport(target[0], target[1], target[2], true)) {
                Compat.teleported(level, from, entity);
                level.playSound((Player) null, x0, y0, z0, SoundEvents.CHORUS_FRUIT_TELEPORT, SoundSource.PLAYERS, 1.0F, 1.0F);
                entity.playSound(SoundEvents.CHORUS_FRUIT_TELEPORT, 1.0F, 1.0F);
                break;
            }
        }
        if (entity instanceof Player player) player.getCooldowns().addCooldown(item, 20);
    }
    *///?}
}
