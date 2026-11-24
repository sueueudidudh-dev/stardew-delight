package com.stardewdelight;

//? if neoforge {
/*import net.minecraft.core.registries.Registries;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.common.util.FakePlayerFactory;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.registries.DeferredRegister;

// Точка входа NeoForge 1.21.1 (NeoForge 1.20.1 загружает Forge-версию мода)
@Mod(StardewDelight.MODID)
public final class StardewDelightNeoForge {
    private static final DeferredRegister<Item> ITEMS = DeferredRegister.create(Registries.ITEM, StardewDelight.MODID);
    private static final DeferredRegister<MobEffect> EFFECTS = DeferredRegister.create(Registries.MOB_EFFECT, StardewDelight.MODID);
    private static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, StardewDelight.MODID);

    public StardewDelightNeoForge(IEventBus modBus) {
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
        NeoForge.EVENT_BUS.addListener((ItemTooltipEvent event) -> Tooltips.append(event.getItemStack(), event.getToolTip()));
        NeoForge.EVENT_BUS.addListener((ServerStartedEvent event) -> {
            if (SelfTest.enabled()) SelfTest.run(event.getServer(), FakePlayerFactory.getMinecraft(event.getServer().overworld()));
        });
        StardewDelight.init();
    }
}
*///?}
