package com.stardewdelight;

import com.mojang.logging.LogUtils;
import net.minecraft.resources.Identifier;
import org.slf4j.Logger;

/**
 * Общие константы мода. Точки входа загрузчиков: StardewDelightForge, StardewDelightNeoForge, StardewDelightFabric.
 * Код для разных версий Minecraft размечен комментариями Stonecutter (//? if ...).
 */
public final class StardewDelight {
    public static final String MODID = "stardewdelight";
    public static final Logger LOGGER = LogUtils.getLogger();

    private StardewDelight() {}

    /** stardewdelight:path */
    public static Identifier id(String path) {
        //? if >=1.21 {
        return Identifier.fromNamespaceAndPath(MODID, path);
        //?} else {
        /*return new Identifier(MODID, path);
        *///?}
    }

    /** Полный id вида namespace:path. */
    public static Identifier parse(String id) {
        //? if >=1.21 {
        return Identifier.parse(id);
        //?} else {
        /*return new Identifier(id);
        *///?}
    }

    static void init() {
        LOGGER.info("Stardew Delight: {} dishes loaded", Dishes.ALL.size());
    }
}
