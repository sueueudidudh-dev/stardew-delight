package com.stardewdelight;

//? if fabric {
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.entity.FakePlayer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.Item;

// Точка входа Fabric (fabric.mod.json, entrypoints.main). Работает на обеих сторонах: без клиентских классов.
public final class StardewDelightFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        Registry.register(BuiltInRegistries.MOB_EFFECT, StardewDelight.id("magnetism"), ModEffect.magnetism());
        Registry.register(BuiltInRegistries.MOB_EFFECT, StardewDelight.id("immunity"), ModEffect.immunity());
        for (Dish dish : Dishes.ALL) {
            Item item = Registry.register(BuiltInRegistries.ITEM, StardewDelight.id(dish.id), DishItems.create(dish));
            dish.item = () -> item;
        }
        Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, StardewDelight.id("main"), FabricTabs.builder()
                .title(Compat.tr("itemGroup." + StardewDelight.MODID))
                .icon(() -> Dishes.byId("complete_breakfast").item().getDefaultInstance())
                .displayItems((params, output) -> Dishes.ALL.forEach(d -> output.accept(d.item())))
                .build());
        ServerLifecycleEvents.SERVER_STARTED.register(server -> {
            if (SelfTest.enabled()) SelfTest.run(server, FakePlayer.get(server.overworld()));
        });
        StardewDelight.init();
    }
}
//?}
