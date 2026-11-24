package com.stardewdelight;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.ExperienceOrb;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.living.MobEffectEvent;
import net.minecraftforge.eventbus.api.Event;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

@Mod.EventBusSubscriber(modid = StardewDelight.MODID)
public final class ModEffects {
    public static final DeferredRegister<MobEffect> EFFECTS = DeferredRegister.create(ForgeRegistries.MOB_EFFECTS, StardewDelight.MODID);
    /** Притягивает выпавшие предметы и опыт. */
    public static final RegistryObject<MobEffect> MAGNETISM = EFFECTS.register("magnetism", MagnetismEffect::new);
    /** Снимает и блокирует все негативные эффекты. */
    public static final RegistryObject<MobEffect> IMMUNITY = EFFECTS.register("immunity", ImmunityEffect::new);

    private ModEffects() {}

    private static boolean hasImmunity(LivingEntity entity) {
        return IMMUNITY.isPresent() && entity.hasEffect(IMMUNITY.get());
    }

    @SubscribeEvent
    public static void onEffectApplicable(MobEffectEvent.Applicable event) {
        if (hasImmunity(event.getEntity()) && event.getEffectInstance().getEffect().getCategory() == MobEffectCategory.HARMFUL) {
            event.setResult(Event.Result.DENY);
        }
    }

    @SubscribeEvent
    public static void onPlayerTick(TickEvent.PlayerTickEvent event) {
        if (event.phase != TickEvent.Phase.END) return;
        Player player = event.player;
        if (player.level().isClientSide() || !hasImmunity(player)) return;
        List<MobEffect> toRemove = new ArrayList<>();
        for (MobEffectInstance inst : player.getActiveEffects()) {
            if (inst.getEffect().getCategory() == MobEffectCategory.HARMFUL) toRemove.add(inst.getEffect());
        }
        toRemove.forEach(player::removeEffect);
    }

    static final class ImmunityEffect extends MobEffect {
        ImmunityEffect() { super(MobEffectCategory.BENEFICIAL, 0x3CAA5A); }
    }

    static final class MagnetismEffect extends MobEffect {
        MagnetismEffect() { super(MobEffectCategory.BENEFICIAL, 0xD62F30); }

        @Override
        public boolean isDurationEffectTick(int duration, int amplifier) { return true; }

        @Override
        public void applyEffectTick(LivingEntity mob, int amplifier) {
            if (mob.level().isClientSide() || !(mob instanceof Player player) || player.isSpectator()) return;
            double radius = 5.0 + 3.0 * amplifier;
            Vec3 target = player.position().add(0.0, player.getBbHeight() * 0.5, 0.0);
            AABB box = player.getBoundingBox().inflate(radius);
            for (ItemEntity item : player.level().getEntitiesOfClass(ItemEntity.class, box, e -> e.isAlive() && !e.hasPickUpDelay())) {
                pull(item, target);
            }
            for (ExperienceOrb orb : player.level().getEntitiesOfClass(ExperienceOrb.class, box, Entity::isAlive)) {
                pull(orb, target);
            }
        }

        private static void pull(Entity e, Vec3 target) {
            Vec3 dir = target.subtract(e.position());
            double dist = dir.length();
            if (dist < 0.6) return;
            e.setDeltaMovement(dir.normalize().scale(Math.min(0.45, 0.12 + dist * 0.03)));
            e.hurtMarked = true;
        }
    }
}
