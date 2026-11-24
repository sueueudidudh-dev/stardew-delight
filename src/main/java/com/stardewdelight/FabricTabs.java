package com.stardewdelight;

//? if fabric && >=26.1 {
import net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;
import net.minecraft.world.item.CreativeModeTab;

// Конструктор вкладки творческого режима из Fabric API (в 26.1 модуль переименован в creative-tab-api)
final class FabricTabs {
    private FabricTabs() {}

    static CreativeModeTab.Builder builder() {
        return FabricCreativeModeTab.builder();
    }
}
//?}

//? if fabric && <26.1 {
/*import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.world.item.CreativeModeTab;

// Конструктор вкладки творческого режима из Fabric API (item-group-api до 26.1)
final class FabricTabs {
    private FabricTabs() {}

    static CreativeModeTab.Builder builder() {
        return FabricItemGroup.builder();
    }
}
*///?}
