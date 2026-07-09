package com.desertcore;

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.event.ClickEvent;
import net.kyori.adventure.text.format.NamedTextColor;
import net.kyori.adventure.text.format.TextDecoration;
import org.bukkit.Bukkit;
import org.bukkit.GameMode;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.PlayerDeathEvent;
import org.bukkit.event.player.PlayerCommandPreprocessEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerMoveEvent;
import org.bukkit.event.player.PlayerRespawnEvent;
import org.bukkit.scheduler.BukkitRunnable;

import java.io.File;
import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.HashMap;
import java.util.HashSet;
import java.util.UUID;

public class deathevent implements Listener {

    private final HashSet<UUID> promptActive = new HashSet<>();
    private final HashMap<UUID, BukkitRunnable> activeTimers = new HashMap<>();

    @EventHandler
    public void onPlayerDeath(PlayerDeathEvent event) {
        Player player = event.getEntity();
        String currentWorld = player.getWorld().getName();

        if (currentWorld.startsWith("desert_")) {
            event.setKeepInventory(true);
            event.getDrops().clear();

            var plugin = Bukkit.getPluginManager().getPlugin("desertcore");
            if (plugin != null) {
                Bukkit.getScheduler().runTaskLater(plugin, () -> player.spigot().respawn(), 1L);
            }
        }
    }

    @EventHandler
    public void onPlayerRespawn(PlayerRespawnEvent event) {
        Player player = event.getPlayer();
        String currentWorld = player.getWorld().getName();

        if (currentWorld.startsWith("desert_")) {
            event.setRespawnLocation(player.getLocation());

            var plugin = Bukkit.getPluginManager().getPlugin("desertcore");
            if (plugin != null) {
                Bukkit.getScheduler().runTaskLater(plugin, () -> {
                    player.setGameMode(GameMode.SPECTATOR);
                    promptActive.remove(player.getUniqueId());
                    cancelTimer(player.getUniqueId());

                    player.sendMessage(Component.text("\n☠️ 전장에서 전사하셨습니다. 관전자 모드로 전환됩니다.").color(NamedTextColor.RED));
                    player.sendMessage(Component.text("💡 [Shift](웅크리기) 키를 3초간 꾹 누르면 로비로 돌아갈 수 있습니다.\n").color(NamedTextColor.GRAY));
                }, 1L);
            }
        }
    }

    @EventHandler
    public void onPlayerMove(PlayerMoveEvent event) {
        Player player = event.getPlayer();
        UUID uuid = player.getUniqueId();
        String currentWorld = player.getWorld().getName();

        if (player.getGameMode() == GameMode.SPECTATOR && currentWorld.startsWith("desert_")) {
            if (player.isSneaking()) {
                if (promptActive.contains(uuid) || activeTimers.containsKey(uuid)) return;

                var plugin = Bukkit.getPluginManager().getPlugin("desertcore");
                if (plugin != null) {
                    BukkitRunnable timer = new BukkitRunnable() {
                        int timeLeft = 3;

                        @Override
                        public void run() {
                            if (!player.isOnline() || player.getGameMode() != GameMode.SPECTATOR) {
                                cancelTimer(uuid);
                                return;
                            }
                            if (!player.isSneaking()) {
                                player.sendMessage(Component.text("❌ Shift 키를 떼어 로비 복귀가 취소되었습니다.").color(NamedTextColor.RED));
                                cancelTimer(uuid);
                                return;
                            }

                            if (timeLeft > 0) {
                                player.sendMessage(Component.text("⏳ 로비 복귀 준비 중... " + timeLeft + "초").color(NamedTextColor.YELLOW));
                                timeLeft--;
                            } else {
                                cancelTimer(uuid);
                                promptActive.add(uuid);

                                player.sendMessage(Component.text("\n[ 시스템 ] 로비로 돌아가시겠습니까?").color(NamedTextColor.GOLD));
                                Component yesButton = Component.text("[ 예 ]").color(NamedTextColor.GREEN).decorate(TextDecoration.BOLD).clickEvent(ClickEvent.runCommand("/lobby_confirm"));
                                Component noButton = Component.text("[ 아니오 ]").color(NamedTextColor.RED).decorate(TextDecoration.BOLD).clickEvent(ClickEvent.runCommand("/lobby_cancel"));
                                player.sendMessage(Component.text("👉 ").append(yesButton).append(Component.text("  |  ")).append(noButton).append(Component.text("\n")));
                            }
                        }
                    };
                    activeTimers.put(uuid, timer);
                    timer.runTaskTimer(plugin, 0L, 20L);
                }
            } else {
                if (activeTimers.containsKey(uuid)) cancelTimer(uuid);
            }
        }
    }

    private void cancelTimer(UUID uuid) {
        if (activeTimers.containsKey(uuid)) {
            activeTimers.get(uuid).cancel();
            activeTimers.remove(uuid);
        }
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        Player player = event.getPlayer();
        World lobbyWorld = Bukkit.getWorld("world");
        String previousWorldName = player.getWorld().getName();

        if (lobbyWorld != null) {
            cancelTimer(player.getUniqueId());
            player.setGameMode(GameMode.SURVIVAL);
            Location lobbyLocation = new Location(lobbyWorld, 0.0, -43.0, 0.0, 0f, 0f);
            player.teleport(lobbyLocation);

            if (previousWorldName.startsWith("desert_")) {
                unloadAndDeleteInstance(previousWorldName);
            }
        }
    }

    @EventHandler
    public void onPlayerCommand(PlayerCommandPreprocessEvent event) {
        Player player = event.getPlayer();
        String message = event.getMessage();
        String currentWorldName = player.getWorld().getName();

        if (message.equalsIgnoreCase("/lobby_confirm")) {
            event.setCancelled(true);
            World lobbyWorld = Bukkit.getWorld("world");
            if (lobbyWorld != null) {
                promptActive.remove(player.getUniqueId());
                cancelTimer(player.getUniqueId());
                player.setGameMode(GameMode.SURVIVAL);

                Location lobbyLocation = new Location(lobbyWorld, 0.0, -43.0, 0.0, 0f, 0f);
                player.teleport(lobbyLocation);
                player.sendMessage(Component.text("[!] 안전하게 로비로 복귀했습니다.").color(NamedTextColor.GREEN));

                if (currentWorldName.startsWith("desert_")) {
                    unloadAndDeleteInstance(currentWorldName);
                }
            }
        } else if (message.equalsIgnoreCase("/lobby_cancel")) {
            event.setCancelled(true);
            promptActive.remove(player.getUniqueId());
            cancelTimer(player.getUniqueId());
            player.sendMessage(Component.text("[!] 전장을 계속 관전합니다. (다시 나가려면 Shift를 3초간 유지)").color(NamedTextColor.GRAY));
        }
    }

    // ★ [오류 해결] FileUtils 대신 자바 순정 내장 API로 월드 사본 폴더 제거
    private void unloadAndDeleteInstance(String instanceName) {
        var plugin = Bukkit.getPluginManager().getPlugin("desertcore");
        if (plugin == null) return;

        Bukkit.getScheduler().runTaskLater(plugin, () -> {
            World instanceWorld = Bukkit.getWorld(instanceName);
            if (instanceWorld != null) {
                if (instanceWorld.getPlayers().isEmpty()) {
                    Bukkit.unloadWorld(instanceWorld, false);

                    // 비동기로 폴더 트리 삭제 수행
                    Bukkit.getScheduler().runTaskAsynchronously(plugin, () -> {
                        File instanceDir = new File(Bukkit.getWorldContainer(), instanceName);
                        if (instanceDir.exists()) {
                            try {
                                deleteDirectoryNative(instanceDir.toPath());
                            } catch (IOException e) {
                                plugin.getLogger().warning(instanceName + " 사본 월드 폴더 삭제 중 예외 발생");
                            }
                        }
                    });
                }
            }
        }, 20L);
    }

    // 자바 내장 폴더 삭제용 헬퍼 메소드
    private void deleteDirectoryNative(Path path) throws IOException {
        Files.walkFileTree(path, new SimpleFileVisitor<>() {
            @Override
            public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                Files.delete(file);
                return FileVisitResult.CONTINUE;
            }

            @Override
            public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
                Files.delete(dir);
                return FileVisitResult.CONTINUE;
            }
        });
    }
}