package com.stardewdelight;

//? if fabric && >=1.20.5 {
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.item.v1.ItemTooltipCallback;

// Клиентская точка входа Fabric (entrypoints.client): ItemTooltipCallback нельзя загружать на выделенном сервере
public final class StardewDelightFabricClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        ItemTooltipCallback.EVENT.register((stack, context, flag, lines) -> Tooltips.append(stack, lines));
    }
}
//?}

//? if fabric && <1.20.5 {
/*import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.item.v1.ItemTooltipCallback;

// Клиентская точка входа Fabric (entrypoints.client): ItemTooltipCallback нельзя загружать на выделенном сервере
public final class StardewDelightFabricClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        ItemTooltipCallback.EVENT.register((stack, flag, lines) -> Tooltips.append(stack, lines));
    }
}
*///?}
