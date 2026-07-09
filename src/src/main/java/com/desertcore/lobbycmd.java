package com.desertcore;

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import org.bukkit.Bukkit;
import org.bukkit.GameMode;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

public class lobbycmd implements CommandExecutor {

    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String label, @NotNull String[] args) {

        // 1. 명령어를 친 대상이 플레이어인지 확인 (콘솔창 입력 방지)
        if (!(sender instanceof Player)) {
            sender.sendMessage(Component.text("이 명령어는 인게임 플레이어만 사용할 수 있습니다.").color(NamedTextColor.RED));
            return true;
        }

        Player player = (Player) sender;

        // 2. [핵심] 오퍼레이터(OP) 권한이 있는지 체크
        if (!player.isOp()) {
            player.sendMessage(Component.text("❌ 이 명령어를 사용할 권한이 없습니다. (OP 전용)").color(NamedTextColor.RED));
            return true;
        }

        // 3. 로비 월드("world") 정보 가져오기
        World lobbyWorld = Bukkit.getWorld("world");
        if (lobbyWorld != null) {
            // 서바이벌 모드로 안전하게 변경 후 지정된 로비 좌표로 텔레포트
            player.setGameMode(GameMode.SURVIVAL);
            Location lobbyLocation = new Location(lobbyWorld, 0.0, -44.0, 17.0, 180f, 0f);
            player.teleport(lobbyLocation);

            player.sendMessage(Component.text("[!] 관리자 권한으로 로비에 강제 복귀했습니다.").color(NamedTextColor.GREEN));
        } else {
            player.sendMessage(Component.text("❌ 'world' 월드를 찾을 수 없습니다. 월드 이름을 확인해 주세요.").color(NamedTextColor.RED));
        }

        return true;
    }
}