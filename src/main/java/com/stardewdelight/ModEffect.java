package com.stardewdelight;

import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;

/**
 * Свои эффекты мода. Сами по себе ничего не делают: их действие описано в {@link EffectLogic}
 * и вызывается из миксина на LivingEntity, одинаково для всех загрузчиков и версий.
 */
public final class ModEffect extends MobEffect {
    public ModEffect(MobEffectCategory category, int color) {
        super(category, color);
    }

    /** Магнетизм: притягивает выпавшие предметы и опыт. Радиус 5 / 8 / 11 блоков. */
    public static MobEffect magnetism() {
        return new ModEffect(MobEffectCategory.BENEFICIAL, 0xD62F30);
    }

    /** Иммунитет к дебаффам: снимает и блокирует все негативные эффекты. */
    public static MobEffect immunity() {
        return new ModEffect(MobEffectCategory.BENEFICIAL, 0x3CAA5A);
    }
}
