package com.desertcore;

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import org.bukkit.Bukkit;
import org.bukkit.GameMode;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.WorldCreator;
import org.bukkit.entity.Player;
import org.bukkit.entity.Villager;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerInteractEntityEvent;

import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.logging.Level;

public class samakportal implements Listener {

    @EventHandler
    public void onVillagerClick(PlayerInteractEntityEvent event) {
        if (!(event.getRightClicked() instanceof Villager villager)) {
            return;
        }

        if (villager.getScoreboardTags().contains("desert_npc")) {
            event.setCancelled(true);
            Player player = event.getPlayer();

            if (player.getWorld().getName().startsWith("desert_")) {
                player.sendMessage(Component.text("[!] 이미 전장 월드에 진입한 상태입니다.").color(NamedTextColor.RED));
                return;
            }

            player.sendMessage(Component.text("⏳ 새로운 전장(사본)을 생성하고 있습니다. 잠시만 기다려주세요...").color(NamedTextColor.YELLOW));

            String templateName = "desert_template";
            String instanceName = "desert_" + player.getUniqueId().toString().substring(0, 8);

            File serverDir = Bukkit.getWorldContainer();
            File templateDir = new File(serverDir, templateName);
            File instanceDir = new File(serverDir, instanceName);

            if (!templateDir.exists()) {
                player.sendMessage(Component.text("❌ 서버에 '" + templateName + "' 원본 폴더가 없습니다! 관리자에게 문의하세요.").color(NamedTextColor.RED));
                return;
            }

            var plugin = Bukkit.getPluginManager().getPlugin("desertcore");
            if (plugin == null) return;

            // 비동기로 자바 순정 기능을 활용해 폴더 복사 및 청소 진행
            Bukkit.getScheduler().runTaskAsynchronously(plugin, () -> {
                try {
                    // 1. 기존 잔재 폴더가 있다면 자바 순정 방식으로 트리 삭제
                    if (instanceDir.exists()) {
                        deleteDirectoryNative(instanceDir.toPath());
                    }

                    // 2. 템플릿 폴더 복사 (자바 NIO 사용)
                    copyDirectoryNative(templateDir.toPath(), instanceDir.toPath());

                    // 3. uid.dat 파일 제거 및 결과 확인(경고 제거)
                    File uidFile = new File(instanceDir, "uid.dat");
                    if (uidFile.exists()) {
                        boolean deleted = uidFile.delete();
                        if (!deleted) {
                            plugin.getLogger().warning("uid.dat 파일을 삭제하지 못했습니다.");
                        }
                    }

                    // 4. 메인 스레드 복귀 후 월드 로드 및 이동
                    Bukkit.getScheduler().runTask(plugin, () -> {
                        World copiedWorld = Bukkit.createWorld(new WorldCreator(instanceName));
                        if (copiedWorld != null) {
                            Location desertLocation = new Location(copiedWorld, 0.0, -43.0, 0.0, 180f, 0f);
                            player.teleport(desertLocation);
                            player.setGameMode(GameMode.SURVIVAL);
                            player.sendMessage(Component.text("[!] 전장(사막 맵)으로 이동했습니다!").color(NamedTextColor.YELLOW));
                        } else {
                            player.sendMessage(Component.text("❌ 월드 로딩 중 오류가 발생했습니다.").color(NamedTextColor.RED));
                        }
                    });

                } catch (IOException e) {
                    player.sendMessage(Component.text("❌ 전장 맵 데이터 복사 중 오류가 발생했습니다.").color(NamedTextColor.RED));
                    plugin.getLogger().log(Level.SEVERE, "전장 복사 중 예외 발생: ", e); // 더 강력한 로깅 경고 해결
                }
            });
        }
    }

    // 자바 순정 폴더 복사 편의 메소드
    private void copyDirectoryNative(Path source, Path target) throws IOException {
        Files.walkFileTree(source, new SimpleFileVisitor<>() {
            @Override
            public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
                Path targetDir = target.resolve(source.relativize(dir));
                if (!Files.exists(targetDir)) {
                    Files.createDirectories(targetDir);
                }
                return FileVisitResult.CONTINUE;
            }

            @Override
            public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                Files.copy(file, target.resolve(source.relativize(file)), StandardCopyOption.REPLACE_EXISTING);
                return FileVisitResult.CONTINUE;
            }
        });
    }

    // 자바 순정 폴더 삭제 편의 메소드
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