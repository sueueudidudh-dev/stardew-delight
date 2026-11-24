package com.stardewdelight;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.world.item.Item;

/**
 * Описание блюда: тара, сытость и эффекты. Одинаково для всех версий и загрузчиков.
 * Сами блюда перечислены в {@link Dishes} — его генерирует tools/gen.py из tools/items.json.
 */
public final class Dish {
    /** Тара: NONE — едят с руки, BOWL — миска возвращается, BOTTLE — стеклянная бутылка. */
    public enum Container { NONE, BOWL, BOTTLE }

    /** Эффект при поедании: id эффекта (minecraft:haste, farmersdelight:comfort, ...), длительность в тиках, уровень с 0. */
    public record Fx(String effect, int duration, int amplifier) {}

    public final String id;
    public final Container container;
    public final int nutrition;
    /** Множитель насыщения, как в FoodProperties.Builder. */
    public final float saturation;
    boolean alwaysEdible;
    boolean drink;
    boolean teleports;
    private final List<Fx> effects = new ArrayList<>();
    /** Предмет; ставит загрузчик при регистрации. */
    Supplier<Item> item;

    Dish(String id, Container container, int nutrition, float saturation) {
        this.id = id;
        this.container = container;
        this.nutrition = nutrition;
        this.saturation = saturation;
    }

    /** Можно съесть и на полный желудок. */
    Dish always() {
        alwaysEdible = true;
        return this;
    }

    /** Напиток: анимация питья. */
    Dish drink() {
        drink = true;
        return this;
    }

    /** Случайный телепорт, как у плода хоруса. */
    Dish teleport() {
        teleports = true;
        return this;
    }

    Dish fx(String effect, int duration, int amplifier) {
        effects.add(new Fx(effect, duration, amplifier));
        return this;
    }

    public List<Fx> effects() {
        return Collections.unmodifiableList(effects);
    }

    public boolean teleports() {
        return teleports;
    }

    public Item item() {
        return item.get();
    }

    /** Насыщение в единицах шкалы, как его считает Minecraft. */
    public float saturationPoints() {
        return nutrition * saturation * 2.0F;
    }
}
