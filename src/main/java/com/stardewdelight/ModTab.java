package com.stardewdelight;

//? if <1.19.3 {
/*import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;

// Вкладка творческого режима для Minecraft до 1.19.3, где у вкладок ещё нет реестра (только Forge 1.18.2 / 1.19.2)
public final class ModTab {
    public static final CreativeModeTab TAB = new CreativeModeTab(StardewDelight.MODID) {
        @Override
        public ItemStack makeIcon() {
            return new ItemStack(Dishes.byId("complete_breakfast").item());
        }
    };

    private ModTab() {}
}
*///?}
