package com.stardewdelight;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.event.ForgeEventFactory;
import net.minecraftforge.event.entity.EntityTeleportEvent;

/** Странная булочка: случайный телепорт как у плода хоруса + секундная перезарядка. */
public class StrangeBunItem extends StardewFoodItem {
    public StrangeBunItem(Properties properties) {
        super(properties);
    }

    @Override
    public void affectConsumer(ItemStack stack, Level level, LivingEntity entity) {
        if (!(level instanceof ServerLevel server)) return;
        double x0 = entity.getX(), y0 = entity.getY(), z0 = entity.getZ();
        for (int i = 0; i < 16; ++i) {
            double x = entity.getX() + (entity.getRandom().nextDouble() - 0.5D) * 16.0D;
            double y = Mth.clamp(entity.getY() + (entity.getRandom().nextInt(16) - 8),
                    level.getMinBuildHeight(), level.getMinBuildHeight() + server.getLogicalHeight() - 1);
            double z = entity.getZ() + (entity.getRandom().nextDouble() - 0.5D) * 16.0D;
            if (entity.isPassenger()) entity.stopRiding();
            Vec3 from = entity.position();
            EntityTeleportEvent.ChorusFruit event = ForgeEventFactory.onChorusFruitTeleport(entity, x, y, z);
            if (event.isCanceled()) return;
            if (entity.randomTeleport(event.getTargetX(), event.getTargetY(), event.getTargetZ(), true)) {
                level.gameEvent(GameEvent.TELEPORT, from, GameEvent.Context.of(entity));
                level.playSound(null, x0, y0, z0, SoundEvents.CHORUS_FRUIT_TELEPORT, SoundSource.PLAYERS, 1.0F, 1.0F);
                entity.playSound(SoundEvents.CHORUS_FRUIT_TELEPORT, 1.0F, 1.0F);
                break;
            }
        }
        if (entity instanceof Player player) player.getCooldowns().addCooldown(this, 20);
    }
}
