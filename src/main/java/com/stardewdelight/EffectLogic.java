package com.stardewdelight;

import java.util.ArrayList;
import net.minecraft.resources.Identifier;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.ExperienceOrb;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/** Действие эффектов «Магнетизм» и «Иммунитет к дебаффам». Вызывается из LivingEntityMixin. */
public final class EffectLogic {
    private static final Identifier MAGNETISM = StardewDelight.id("magnetism");
    private static final Identifier IMMUNITY = StardewDelight.id("immunity");

    private EffectLogic() {}

    /** Не даём наложить негативный эффект, пока действует иммунитет. */
    public static boolean blocks(LivingEntity entity, MobEffectInstance instance) {
        if (entity.getActiveEffects().isEmpty()) return false;
        var immunity = Compat.effect(IMMUNITY);
        return immunity != null && entity.hasEffect(immunity)
                && Compat.value(instance.getEffect()).getCategory() == MobEffectCategory.HARMFUL;
    }

    /** Вызывается в начале LivingEntity.tick(), до обработки эффектов, поэтому снимать их здесь безопасно. */
    public static void tick(LivingEntity entity) {
        if (entity.getActiveEffects().isEmpty()) return;
        Level level = Compat.level(entity);
        if (level.isClientSide()) return;

        var immunity = Compat.effect(IMMUNITY);
        if (immunity != null && entity.hasEffect(immunity)) {
            for (MobEffectInstance instance : new ArrayList<>(entity.getActiveEffects())) {
                if (Compat.value(instance.getEffect()).getCategory() == MobEffectCategory.HARMFUL) {
                    entity.removeEffect(instance.getEffect());
                }
            }
        }

        if (entity instanceof Player player && !player.isSpectator()) {
            var magnetism = Compat.effect(MAGNETISM);
            if (magnetism == null) return;
            MobEffectInstance instance = player.getEffect(magnetism);
            if (instance != null) pullItems(level, player, instance.getAmplifier());
        }
    }

    private static void pullItems(Level level, Player player, int amplifier) {
        double radius = 5.0 + 3.0 * amplifier;
        Vec3 target = player.position().add(0.0, player.getBbHeight() * 0.5, 0.0);
        AABB box = player.getBoundingBox().inflate(radius);
        for (ItemEntity item : level.getEntitiesOfClass(ItemEntity.class, box, e -> e.isAlive() && !e.hasPickUpDelay())) {
            pull(item, target);
        }
        for (ExperienceOrb orb : level.getEntitiesOfClass(ExperienceOrb.class, box, Entity::isAlive)) {
            pull(orb, target);
        }
    }

    private static void pull(Entity entity, Vec3 target) {
        Vec3 dir = target.subtract(entity.position());
        double dist = dir.length();
        if (dist < 0.6) return;
        entity.setDeltaMovement(dir.normalize().scale(Math.min(0.45, 0.12 + dist * 0.03)));
        Compat.syncVelocity(entity);
    }
}
