package com.desertcore;

import org.bukkit.plugin.java.JavaPlugin;

public final class DesertCore extends JavaPlugin {

    @Override
    public void onEnable() {
        getServer().getPluginManager().registerEvents(new marendumbul(), this);
        getLogger().info("desertcore 플러그인이 성공적으로 켜졌습니다!");
        getServer().getPluginManager().registerEvents(new samakportal(), this);
        getServer().getPluginManager().registerEvents(new deathevent(), this);
        getCommand("로비").setExecutor(new lobbycmd());
    }

    @Override
    public void onDisable() {
    }
}