package com.stardewdelight;

import com.mojang.logging.LogUtils;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;
import org.slf4j.Logger;

@Mod(StardewDelight.MODID)
public final class StardewDelight {
    public static final String MODID = "stardewdelight";
    public static final Logger LOGGER = LogUtils.getLogger();

    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MODID);
    public static final RegistryObject<CreativeModeTab> TAB = TABS.register("main", () -> CreativeModeTab.builder()
            .title(Component.translatable("itemGroup." + MODID))
            .withTabsBefore(CreativeModeTabs.FOOD_AND_DRINKS)
            .icon(() -> ModItems.COMPLETE_BREAKFAST.get().getDefaultInstance())
            .displayItems((params, output) -> ModItems.ALL.forEach(item -> output.accept(item.get())))
            .build());

    @SuppressWarnings("removal") // get() оставлен ради совместимости со старыми Forge 47.x
    public StardewDelight() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
        ModEffects.EFFECTS.register(modBus);
        ModItems.ITEMS.register(modBus);
        TABS.register(modBus);
        LOGGER.info("Stardew Delight: {} dishes loaded", ModItems.ALL.size());
    }
}
