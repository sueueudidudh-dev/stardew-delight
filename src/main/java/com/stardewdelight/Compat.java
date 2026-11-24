package com.stardewdelight;

import java.util.List;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
//? if >=1.20.5 {
import net.minecraft.core.Holder;
//?}
//? if >=1.19.3 {
import net.minecraft.core.registries.BuiltInRegistries;
//?} else {
/*import net.minecraft.core.Registry;
*///?}
//? if >=1.19 {
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.gameevent.GameEvent;
//?} else {
/*import net.minecraft.network.chat.TranslatableComponent;
*///?}

/**
 * Обёртки над API, которое отличается между версиями Minecraft и загрузчиками.
 * Внутри условных блоков Stonecutter — только однострочные комментарии.
 */
final class Compat {
    private Compat() {}

    // ---- эффекты: до 1.20.5 это MobEffect, с 1.20.5 — Holder<MobEffect>. effect(id) — эффект по id или null ----

    //? if >=1.21.2 {
    static Holder<MobEffect> effect(Identifier id) {
        return BuiltInRegistries.MOB_EFFECT.get(id).orElse(null);
    }
    //?}

    //? if >=1.20.5 <1.21.2 {
    /*static Holder<MobEffect> effect(Identifier id) {
        return BuiltInRegistries.MOB_EFFECT.getHolder(id).orElse(null);
    }
    *///?}

    //? if >=1.19.3 <1.20.5 {
    /*static MobEffect effect(Identifier id) {
        return BuiltInRegistries.MOB_EFFECT.get(id);
    }
    *///?}

    //? if <1.19.3 {
    /*static MobEffect effect(Identifier id) {
        return Registry.MOB_EFFECT.get(id);
    }
    *///?}

    //? if >=1.20.5 {
    static MobEffect value(Holder<MobEffect> effect) {
        return effect.value();
    }
    //?} else {
    /*static MobEffect value(MobEffect effect) {
        return effect;
    }
    *///?}

    /** Экземпляр эффекта блюда или null, если такого эффекта нет (например, мод эффекта не установлен). */
    static MobEffectInstance instance(Dish.Fx fx) {
        var effect = effect(StardewDelight.parse(fx.effect()));
        return effect == null ? null : new MobEffectInstance(effect, fx.duration(), fx.amplifier());
    }

    // ---- текст ----

    //? if >=1.19 {
    static MutableComponent tr(String key, Object... args) {
        return Component.translatable(key, args);
    }
    //?} else {
    /*static MutableComponent tr(String key, Object... args) {
        return new TranslatableComponent(key, args);
    }
    *///?}

    // ---- мир ----

    static Level level(Entity entity) {
        //? if >=1.20 {
        return entity.level();
        //?} else {
        /*return entity.level;
        *///?}
    }

    /** Отправить клиентам новую скорость сущности (в 26.3 hurtMarked переименован в syncVelocity). */
    static void syncVelocity(Entity entity) {
        //? if >=26.3 {
        entity.syncVelocity = true;
        //?} else {
        /*entity.hurtMarked = true;
        *///?}
    }

    // ---- рецепты сервера (для SelfTest): id всех загруженных рецептов ----

    //? if >=1.21.11 {
    static List<String> recipeIds(MinecraftServer server) {
        return server.getRecipeManager().getRecipes().stream().map(h -> h.id().identifier().toString()).toList();
    }
    //?}

    //? if >=1.21.2 <1.21.11 {
    /*static List<String> recipeIds(MinecraftServer server) {
        return server.getRecipeManager().getRecipes().stream().map(h -> h.id().location().toString()).toList();
    }
    *///?}

    //? if >=1.20.2 <1.21.2 {
    /*static List<String> recipeIds(MinecraftServer server) {
        return server.getRecipeManager().getRecipes().stream().map(h -> h.id().toString()).toList();
    }
    *///?}

    //? if <1.20.2 {
    /*static List<String> recipeIds(MinecraftServer server) {
        return server.getRecipeManager().getRecipes().stream().map(r -> r.getId().toString()).toList();
    }
    *///?}

    // ---- телепорт странной булочки до 1.21.2 (с 1.21.2 его делает компонент Consumable) ----

    //? if forge {
    /*// Событие Forge, как у плода хоруса: другие моды могут отменить или изменить телепорт
    static double[] chorusTarget(LivingEntity entity, double x, double y, double z) {
        net.minecraftforge.event.entity.EntityTeleportEvent.ChorusFruit event =
                net.minecraftforge.event.ForgeEventFactory.onChorusFruitTeleport(entity, x, y, z);
        return event.isCanceled() ? null : new double[] {event.getTargetX(), event.getTargetY(), event.getTargetZ()};
    }
    *///?}

    //? if neoforge && <1.21.2 {
    /*// Событие NeoForge, как у плода хоруса: другие моды могут отменить или изменить телепорт
    static double[] chorusTarget(LivingEntity entity, double x, double y, double z) {
        net.neoforged.neoforge.event.entity.EntityTeleportEvent.ChorusFruit event =
                net.neoforged.neoforge.event.EventHooks.onChorusFruitTeleport(entity, x, y, z);
        return event.isCanceled() ? null : new double[] {event.getTargetX(), event.getTargetY(), event.getTargetZ()};
    }
    *///?}

    //? if fabric && <1.21.2 {
    /*static double[] chorusTarget(LivingEntity entity, double x, double y, double z) {
        return new double[] {x, y, z};
    }
    *///?}

    //? if >=1.19 <1.21.2 {
    /*static void teleported(Level level, Vec3 from, LivingEntity entity) {
        level.gameEvent(GameEvent.TELEPORT, from, GameEvent.Context.of(entity));
    }
    *///?}

    //? if <1.19 {
    /*static void teleported(Level level, Vec3 from, LivingEntity entity) {
    }
    *///?}
}
