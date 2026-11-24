package com.stardewdelight.mixin;

import com.stardewdelight.EffectLogic;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Эффекты мода для всех загрузчиков сразу: иммунитет к дебаффам и магнетизм. */
@Mixin(LivingEntity.class)
public abstract class LivingEntityMixin {
    @Inject(method = "canBeAffected", at = @At("HEAD"), cancellable = true)
    private void stardewdelight$blockHarmful(MobEffectInstance instance, CallbackInfoReturnable<Boolean> cir) {
        // Начало LivingEntity.canBeAffected(MobEffectInstance): иммунитет не даёт наложить дебафф
        if (EffectLogic.blocks((LivingEntity) (Object) this, instance)) cir.setReturnValue(false);
    }

    @Inject(method = "tick", at = @At("HEAD"))
    private void stardewdelight$tick(CallbackInfo ci) {
        // Начало LivingEntity.tick(), до обработки эффектов
        EffectLogic.tick((LivingEntity) (Object) this);
    }
}
