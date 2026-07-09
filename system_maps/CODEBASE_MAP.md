# 🏗️ 짭커서 프로젝트 CODEBASE MAP

현재 인덱싱된 총 파일 수: **5개**

## 🗂️ [Module Index]
- `src/main/java/com/desertcore/DesertCore.java`
- `src/main/java/com/desertcore/deathevent.java`
- `src/main/java/com/desertcore/lobbycmd.java`
- `src/main/java/com/desertcore/marendumbul.java`
- `src/main/java/com/desertcore/samakportal.java`

## 💀 [Skeleton & Dependency 명세서]
### 📄 src/main/java/com/desertcore/DesertCore.java
#### 🧱 Code Skeleton:
```python
public void onEnable() { // L8-14
getServer().getPluginManager().registerEvents(new marendumbul(), this); // L9-17
getLogger().info("desertcore 플러그인이 성공적으로 켜졌습니다!"); // L10-17
getServer().getPluginManager().registerEvents(new samakportal(), this); // L11-17
getServer().getPluginManager().registerEvents(new deathevent(), this); // L12-17
getCommand("로비").setExecutor(new lobbycmd()); // L13-17
public void onDisable() { // L17-18
```

--------------------------------------------------

### 📄 src/main/java/com/desertcore/deathevent.java
#### 🧱 Code Skeleton:
```python
class deathevent { // L32-223
    public void onPlayerDeath(PlayerDeathEvent event) { // L38-51
    public void onPlayerRespawn(PlayerRespawnEvent event) { // L54-73
    cancelTimer(player.getUniqueId()); // L66-76
    public void onPlayerMove(PlayerMoveEvent event) { // L76-123
    public void run() { // L91-114
    cancelTimer(uuid); // L93-96
    cancelTimer(uuid); // L98-102
    cancelTimer(uuid); // L106-119
    private void cancelTimer(UUID uuid) { // L125-130
    public void onPlayerJoin(PlayerJoinEvent event) { // L133-148
    cancelTimer(player.getUniqueId()); // L139-146
    unloadAndDeleteInstance(previousWorldName); // L145-151
    public void onPlayerCommand(PlayerCommandPreprocessEvent event) { // L151-178
    cancelTimer(player.getUniqueId()); // L161-170
    unloadAndDeleteInstance(currentWorldName); // L169-172
    cancelTimer(player.getUniqueId()); // L175-181
    private void unloadAndDeleteInstance(String instanceName) { // L181-205
    deleteDirectoryNative(instanceDir.toPath()); // L196-197
    private void deleteDirectoryNative(Path path) throws IOException { // L208-222
    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException { // L211-214
    public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException { // L217-220
```

--------------------------------------------------

### 📄 src/main/java/com/desertcore/lobbycmd.java
#### 🧱 Code Skeleton:
```python
class lobbycmd { // L15-49
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String label, @NotNull String[] args) { // L18-48
```

--------------------------------------------------

### 📄 src/main/java/com/desertcore/marendumbul.java
#### 🧱 Code Skeleton:
```python
class marendumbul { // L13-62
    public void onPlayerJoin(PlayerJoinEvent event) { // L19-61
```

--------------------------------------------------

### 📄 src/main/java/com/desertcore/samakportal.java
#### 🧱 Code Skeleton:
```python
class samakportal { // L22-133
    public void onVillagerClick(PlayerInteractEntityEvent event) { // L25-95
    deleteDirectoryNative(instanceDir.toPath()); // L61-69
    copyDirectoryNative(templateDir.toPath(), instanceDir.toPath()); // L65-74
    private void copyDirectoryNative(Path source, Path target) throws IOException { // L98-115
    public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException { // L101-107
    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException { // L110-113
    private void deleteDirectoryNative(Path path) throws IOException { // L118-132
    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException { // L121-124
    public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException { // L127-130
```

--------------------------------------------------

