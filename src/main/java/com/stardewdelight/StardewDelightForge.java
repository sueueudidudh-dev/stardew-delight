package com.stardewdelight;

//? if forge && >=1.19.3 {
/*import net.minecraft.core.registries.Registries;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.common.util.FakePlayerFactory;
import net.minecraftforge.event.entity.player.ItemTooltipEvent;
import net.minecraftforge.event.server.ServerStartedEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

// Точка входа Forge 1.20.1 (и NeoForge 1.20.1 — тот же jar)
@Mod(StardewDelight.MODID)
public final class StardewDelightForge {
    private static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, StardewDelight.MODID);
    private static final DeferredRegister<MobEffect> EFFECTS = DeferredRegister.create(ForgeRegistries.MOB_EFFECTS, StardewDelight.MODID);
    private static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, StardewDelight.MODID);

    @SuppressWarnings("removal") // FMLJavaModLoadingContext.get() оставлен ради совместимости со старыми Forge 47.x
    public StardewDelightForge() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
        EFFECTS.register("magnetism", ModEffect::magnetism);
        EFFECTS.register("immunity", ModEffect::immunity);
        for (Dish dish : Dishes.ALL) dish.item = ITEMS.register(dish.id, () -> DishItems.create(dish));
        TABS.register("main", () -> CreativeModeTab.builder()
                .title(Compat.tr("itemGroup." + StardewDelight.MODID))
                .withTabsBefore(CreativeModeTabs.FOOD_AND_DRINKS)
                .icon(() -> Dishes.byId("complete_breakfast").item().getDefaultInstance())
                .displayItems((params, output) -> Dishes.ALL.forEach(d -> output.accept(d.item())))
                .build());
        EFFECTS.register(modBus);
        ITEMS.register(modBus);
        TABS.register(modBus);
        MinecraftForge.EVENT_BUS.addListener((ItemTooltipEvent event) -> Tooltips.append(event.getItemStack(), event.getToolTip()));
        MinecraftForge.EVENT_BUS.addListener((ServerStartedEvent event) -> {
            if (SelfTest.enabled()) SelfTest.run(event.getServer(), FakePlayerFactory.getMinecraft(event.getServer().overworld()));
        });
        StardewDelight.init();
    }
}
*///?}

//? if forge && <1.19.3 {
/*import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.item.Item;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.common.util.FakePlayerFactory;
import net.minecraftforge.event.entity.player.ItemTooltipEvent;
import net.minecraftforge.event.server.ServerStartedEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

// Точка входа Forge 1.18.2 / 1.19.2: вкладка творческого режима — ModTab (реестра вкладок ещё нет)
@Mod(StardewDelight.MODID)
public final class StardewDelightForge {
    private static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, StardewDelight.MODID);
    private static final DeferredRegister<MobEffect> EFFECTS = DeferredRegister.create(ForgeRegistries.MOB_EFFECTS, StardewDelight.MODID);

    public StardewDelightForge() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
        EFFECTS.register("magnetism", ModEffect::magnetism);
        EFFECTS.register("immunity", ModEffect::immunity);
        for (Dish dish : Dishes.ALL) dish.item = ITEMS.register(dish.id, () -> DishItems.create(dish));
        EFFECTS.register(modBus);
        ITEMS.register(modBus);
        MinecraftForge.EVENT_BUS.addListener((ItemTooltipEvent event) -> Tooltips.append(event.getItemStack(), event.getToolTip()));
        MinecraftForge.EVENT_BUS.addListener((ServerStartedEvent event) -> {
            if (SelfTest.enabled()) SelfTest.run(event.getServer(), FakePlayerFactory.getMinecraft(event.getServer().overworld()));
        });
        StardewDelight.init();
    }
}
*///?}
