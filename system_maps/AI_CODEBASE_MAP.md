# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)

> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.
> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.

```markdown
project_root/
├── .gitignore [📂 .gitignore]
├── .vscode/
│   ├── settings.json [📂 .vscode/settings.json] -> [💡 📦 json_keys: 17개 포착 | 🔑 "terminal.integrated.sendKeybindingsToShell" [bool] | 🔑 "accessibility.verbosity.terminal" [bool] | 🔑 "git.autofetch" [bool] | 🔑 "explorer.confirmDelete" [bool] | 🔑 "git.openRepositoryInParentFolders" [str] | ...외 12개]
├── agent_core/
│   ├── __init__.py [📂 agent_core/__init__.py]
│   ├── execution/
│   │   ├── __init__.py [📂 agent_core/execution/__init__.py]
│   ├── memory/
│   │   ├── __init__.py [📂 agent_core/memory/__init__.py]
│   ├── plan/
│   │   ├── __init__.py [📂 agent_core/plan/__init__.py]
│   │   ├── gemini_client.py [📂 agent_core/plan/gemini_client.py]
│   │   ├── planner.py [📂 agent_core/plan/planner.py]
│   │   ├── prompt_builder.py [📂 agent_core/plan/prompt_builder.py]
│   │   ├── schemas.py [📂 agent_core/plan/schemas.py]
│   ├── validation/
│   │   ├── __init__.py [📂 agent_core/validation/__init__.py]
├── agent_plan.md [📂 agent_plan.md]
├── oldplan/
│   ├── agent_plan1.md [📂 oldplan/agent_plan1.md]
│   ├── agent_plan2.md [📂 oldplan/agent_plan2.md]
│   ├── agent_plan3.md [📂 oldplan/agent_plan3.md]
├── prompt.md [📂 prompt.md]
├── scan_debug.txt [📂 scan_debug.txt]
├── src/
│   ├── .gitignore [📂 src/.gitignore]
│   ├── .gradle/
│   │   ├── 9.4.0/
│   │   │   ├── checksums/
│   │   │   │   ├── checksums.lock [📂 src/.gradle/9.4.0/checksums/checksums.lock]
│   │   │   ├── fileChanges/
│   │   │   │   ├── last-build.bin [📂 src/.gradle/9.4.0/fileChanges/last-build.bin]
│   │   │   ├── fileHashes/
│   │   │   │   ├── fileHashes.bin [📂 src/.gradle/9.4.0/fileHashes/fileHashes.bin]
│   │   │   │   ├── fileHashes.lock [📂 src/.gradle/9.4.0/fileHashes/fileHashes.lock]
│   │   │   ├── gc.properties [📂 src/.gradle/9.4.0/gc.properties]
│   │   ├── buildOutputCleanup/
│   │   │   ├── buildOutputCleanup.lock [📂 src/.gradle/buildOutputCleanup/buildOutputCleanup.lock]
│   │   │   ├── cache.properties [📂 src/.gradle/buildOutputCleanup/cache.properties]
│   │   ├── vcs-1/
│   │   │   ├── gc.properties [📂 src/.gradle/vcs-1/gc.properties]
│   ├── .idea/
│   │   ├── .gitignore [📂 src/.idea/.gitignore]
│   │   ├── compiler.xml [📂 src/.idea/compiler.xml]
│   │   ├── gradle.xml [📂 src/.idea/gradle.xml]
│   │   ├── misc.xml [📂 src/.idea/misc.xml]
│   │   ├── modules/
│   │   │   ├── desertcore.main.iml [📂 src/.idea/modules/desertcore.main.iml]
│   │   ├── modules.xml [📂 src/.idea/modules.xml]
│   │   ├── vcs.xml [📂 src/.idea/vcs.xml]
│   ├── build.gradle.kts [📂 src/build.gradle.kts]
│   ├── gradle/
│   │   ├── wrapper/
│   │   │   ├── gradle-wrapper.properties [📂 src/gradle/wrapper/gradle-wrapper.properties]
│   ├── gradle.properties [📂 src/gradle.properties]
│   ├── plan.md [📂 src/plan.md]
│   ├── settings.gradle.kts [📂 src/settings.gradle.kts]
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/
│   │   │   │   ├── com/
│   │   │   │   │   ├── desertcore/
│   │   │   │   │   │   ├── deathevent.java [📂 src/src/main/java/com/desertcore/deathevent.java] -> [💡 📦 imp: java.io.File, java.io.IOException, java.nio.file.FileVisitResult, java.nio.file.Files, java.nio.file.Path, java.nio.file.SimpleFileVisitor, java.nio.file.attribute.BasicFileAttributes, java.util.HashMap, java.util.HashSet, java.util.UUID, net.kyori.adventure.text.Component, net.kyori.adventure.text.event.ClickEvent, net.kyori.adventure.text.format.NamedTextColor, net.kyori.adventure.text.format.TextDecoration, org.bukkit.Bukkit, org.bukkit.GameMode, org.bukkit.Location, org.bukkit.World, org.bukkit.entity.Player, org.bukkit.event.EventHandler, org.bukkit.event.Listener, org.bukkit.event.entity.PlayerDeathEvent, org.bukkit.event.player.PlayerCommandPreprocessEvent, org.bukkit.event.player.PlayerJoinEvent, org.bukkit.event.player.PlayerMoveEvent, org.bukkit.event.player.PlayerRespawnEvent, org.bukkit.scheduler.BukkitRunnable | 🧬 class deathevent [L32-223] | 🎯 def onPlayerDeath(PlayerDeathEvent) [L38-51] | 🎯 def onPlayerRespawn(PlayerRespawnEvent) [L54-73] | 🎯 def cancelTimer(player.getUniqueId() [L66-76] | 🎯 def onPlayerMove(PlayerMoveEvent) [L76-123] | 🎯 def run() [L91-114] | 🎯 def cancelTimer(uuid) [L93-96] | 🎯 def cancelTimer(uuid) [L98-102] | 🎯 def cancelTimer(uuid) [L106-119] | 🎯 def cancelTimer(UUID) [L125-130] | 🎯 def onPlayerJoin(PlayerJoinEvent) [L133-148] | 🎯 def cancelTimer(player.getUniqueId() [L139-146] | 🎯 def unloadAndDeleteInstance(previousWorldName) [L145-151] | 🎯 def onPlayerCommand(PlayerCommandPreprocessEvent) [L151-178] | 🎯 def cancelTimer(player.getUniqueId() [L161-170] | 🎯 def unloadAndDeleteInstance(currentWorldName) [L169-172] | 🎯 def cancelTimer(player.getUniqueId() [L175-181] | 🎯 def unloadAndDeleteInstance(String) [L181-205] | 🎯 def deleteDirectoryNative(instanceDir.toPath() [L196-197] | 🎯 def deleteDirectoryNative(Path) [L208-222] | 🎯 def visitFile(Path, BasicFileAttributes) [L211-214] | 🎯 def postVisitDirectory(Path, IOException) [L217-220]]
│   │   │   │   │   │   ├── DesertCore.java [📂 src/src/main/java/com/desertcore/DesertCore.java] -> [💡 📦 imp: org.bukkit.plugin.java.JavaPlugin | 🎯 def onEnable() [L8-14] | 🎯 def getServer() [L9-17] | 🎯 def getLogger() [L10-17] | 🎯 def getServer() [L11-17] | 🎯 def getServer() [L12-17] | 🎯 def getCommand("로비") [L13-17] | 🎯 def onDisable() [L17-18]]
│   │   │   │   │   │   ├── lobbycmd.java [📂 src/src/main/java/com/desertcore/lobbycmd.java] -> [💡 📦 imp: net.kyori.adventure.text.Component, net.kyori.adventure.text.format.NamedTextColor, org.bukkit.Bukkit, org.bukkit.GameMode, org.bukkit.Location, org.bukkit.World, org.bukkit.command.Command, org.bukkit.command.CommandExecutor, org.bukkit.command.CommandSender, org.bukkit.entity.Player, org.jetbrains.annotations.NotNull | 🧬 class lobbycmd [L15-49] | 🎯 def onCommand(@NotNull, @NotNull, @NotNull, @NotNull) [L18-48]]
│   │   │   │   │   │   ├── marendumbul.java [📂 src/src/main/java/com/desertcore/marendumbul.java] -> [💡 📦 imp: java.util.Random, org.bukkit.Bukkit, org.bukkit.Material, org.bukkit.World, org.bukkit.block.Block, org.bukkit.entity.Player, org.bukkit.event.EventHandler, org.bukkit.event.Listener, org.bukkit.event.player.PlayerJoinEvent | 🧬 class marendumbul [L13-62] | 🎯 def onPlayerJoin(PlayerJoinEvent) [L19-61]]
│   │   │   │   │   │   ├── samakportal.java [📂 src/src/main/java/com/desertcore/samakportal.java] -> [💡 📦 imp: java.io.File, java.io.IOException, java.nio.file.*, java.nio.file.attribute.BasicFileAttributes, java.util.logging.Level, net.kyori.adventure.text.Component, net.kyori.adventure.text.format.NamedTextColor, org.bukkit.Bukkit, org.bukkit.GameMode, org.bukkit.Location, org.bukkit.World, org.bukkit.WorldCreator, org.bukkit.entity.Player, org.bukkit.entity.Villager, org.bukkit.event.EventHandler, org.bukkit.event.Listener, org.bukkit.event.player.PlayerInteractEntityEvent | 🧬 class samakportal [L22-133] | 🎯 def onVillagerClick(PlayerInteractEntityEvent) [L25-95] | 🎯 def deleteDirectoryNative(instanceDir.toPath() [L61-69] | 🎯 def copyDirectoryNative(templateDir.toPath() [L65-74] | 🎯 def copyDirectoryNative(Path, Path) [L98-115] | 🎯 def preVisitDirectory(Path, BasicFileAttributes) [L101-107] | 🎯 def visitFile(Path, BasicFileAttributes) [L110-113] | 🎯 def deleteDirectoryNative(Path) [L118-132] | 🎯 def visitFile(Path, BasicFileAttributes) [L121-124] | 🎯 def postVisitDirectory(Path, IOException) [L127-130]]
│   │   │   ├── resources/
│   │   │   │   ├── plugin.yml [📂 src/src/main/resources/plugin.yml]
├── start.py [📂 start.py] -> [💡 📦 imp: os, pathlib, shutil, stat, subprocess, sys, time | 🎯 def get_best_python() [L34-50] | 🎯 def auto_install_dependencies() [L59-80] | 🎯 def main() [L82-202]]
├── System Prompt.md [📂 System Prompt.md]
├── tools/
│   ├── universal_indexer/
│   │   ├── agent_navigator.py [📂 tools/universal_indexer/agent_navigator.py] -> [💡 📦 imp: json, pathlib, re, sys, tkinter, traceback | 🧬 class SemanticNavigator [L11-208] |     └─ def __init__() [L12-16] |     └─ def _load_database() [L18-25] |     └─ def extract_multi_slices() [L30-208] | 🧬 class JjapCursorNavigatorGUI [L213-339] |     └─ def __init__() [L214-263] |     └─ def execute_slicing_pipeline() [L265-320] |     └─ def manual_export_file() [L322-339]]
│   │   │     ├── 🔑 [REGISTRY]: "JjapCursorNavigatorGUI"
│   │   │     ├── 🔑 [REGISTRY]: "SemanticNavigator"
│   │   ├── context_builder.py [📂 tools/universal_indexer/context_builder.py] -> [💡 📦 imp: os, pathlib | 🧬 class ContextBuilder [L13-107] |     └─ def __init__() [L16-18] |     └─ def read_and_clean_file() [L20-78] |     └─ def assemble_ai_prompt() [L80-107]]
│   │   ├── core_parsers/
│   │   │   ├── __init__.py [📂 tools/universal_indexer/core_parsers/__init__.py]
│   │   │   ├── cs_parser.py [📂 tools/universal_indexer/core_parsers/cs_parser.py]
│   │   │   ├── java_parser.py [📂 tools/universal_indexer/core_parsers/java_parser.py] -> [💡 📦 imp: hashlib, pathlib, re | 🎯 def log() [L8-10] | 🎯 def _find_matching_curly_brace() [L12-34] | 🎯 def extract_symbols() [L36-193]]
│   │   │   ├── js_parser.py [📂 tools/universal_indexer/core_parsers/js_parser.py]
│   │   │   ├── json_parser.py [📂 tools/universal_indexer/core_parsers/json_parser.py] -> [💡 📦 imp: hashlib, json, pathlib | 🎯 def extract_symbols() [L5-97]]
│   │   │   ├── py_parser.py [📂 tools/universal_indexer/core_parsers/py_parser.py] -> [💡 📦 imp: ast, hashlib, pathlib | 🎯 def extract_symbols() [L5-158]]
│   │   ├── create_ai_map.py [📂 tools/universal_indexer/create_ai_map.py] -> [💡 📦 imp: ast, json, os, pathlib, tools.universal_indexer.switch | 🎯 def load_jjap_context() [L41-60] | 🎯 def collect_target_files() [L63-121] | 🎯 def load_registry() [L124-161] | 🎯 def load_protocols() [L164-186] | 🎯 def parse_protocols_and_registries() [L193-246] | 🎯 def main() [L249-339] | 🎯 def generate_ai_optimized_map() [L345-347]]
│   │   ├── indexer.py [📂 tools/universal_indexer/indexer.py] -> [💡 📦 imp: ast, hashlib, importlib.util, json, os, pathlib, switch, typing | 🎯 def log() [L18-20] | 🧬 class AdvancedIndexerV2 [L32-198] |     └─ def __init__() [L37-47] |     └─ def _auto_load_parsers() [L49-80] |     └─ def scan_project() [L82-120] |     └─ def index_file() [L122-161] |     └─ def save_index_data() [L163-198]]
│   │   │     ├── 🔑 [REGISTRY]: "AdvancedIndexerV2"
│   │   ├── jjap_lookup.py [📂 tools/universal_indexer/jjap_lookup.py] -> [💡 📦 imp: argparse, json, pathlib, sys | 🎯 def load_json() [L17-22] | 🎯 def lookup_symbol() [L24-51] | 🎯 def show_skeleton() [L53-69]]
│   │   ├── jjap_retriever.py [📂 tools/universal_indexer/jjap_retriever.py] -> [💡 📦 imp: json, os, pathlib, sys, typing | 🧬 class JjapRetriever [L9-129] |     └─ def __init__() [L16-21] |     └─ def _load_symbols() [L23-37] |     └─ def retrieve_symbol() [L39-98] |     └─ def _find_best_match() [L100-117] |     └─ def _safe_truncate() [L119-129] | 🎯 def main() [L132-140]]
│   │   │     ├── 🔑 [REGISTRY]: "JjapRetriever"
│   │   ├── jjap_watcher.py [📂 tools/universal_indexer/jjap_watcher.py] -> [💡 📦 imp: importlib.util, os, pathlib, sys, time, traceback, watchdog.observers, watchdog.observers.polling | 🎯 def import_file_directly() [L25-33] | 🎯 def run_pipeline() [L35-78] | 🧬 class CodeChangeHandler [L81-104] |     └─ def __init__() [L82-84] |     └─ def dispatch() [L86-104] | 🎯 def main() [L106-132]]
│   │   │     ├── 🔑 [REGISTRY]: "CodeChangeHandler"
│   │   ├── README.md [📂 tools/universal_indexer/README.md]
│   │   ├── rule.txt [📂 tools/universal_indexer/rule.txt]
│   │   ├── switch.py [📂 tools/universal_indexer/switch.py]
│   │   ├── update_map.py [📂 tools/universal_indexer/update_map.py] -> [💡 📦 imp: json, pathlib | 🎯 def update_map() [L4-94]]
