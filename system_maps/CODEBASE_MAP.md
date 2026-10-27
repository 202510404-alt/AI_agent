# 🏗️ 짭커서 프로젝트 CODEBASE MAP

현재 인덱싱된 총 파일 수: **41개**

## 🗂️ [Module Index]
- `extraction_target_project/AGENTS.md`
- `extraction_target_project/css/style.css`
- `extraction_target_project/index.html`
- `extraction_target_project/js/ai/aiEngine.js`
- `extraction_target_project/js/ai/dodgeAlgorithm.js`
- `extraction_target_project/js/config/constants.js`
- `extraction_target_project/js/core/gameLoop.js`
- `extraction_target_project/js/core/input.js`
- `extraction_target_project/js/core/sceneManager.js`
- `extraction_target_project/js/core/ui.js`
- `extraction_target_project/js/enemy/baseBoss.js`
- `extraction_target_project/js/enemy/bossFactory.js`
- `extraction_target_project/js/enemy/bosses/neonDragon/neonDragon.js`
- `extraction_target_project/js/enemy/bosses/neonDragon/neonDragonBullet.js`
- `extraction_target_project/js/enemy/bosses/neonDragon/neonDragonParticle.js`
- `extraction_target_project/js/enemy/bosses/neonDragon/neonDragonPattern.js`
- `extraction_target_project/js/main.js`
- `extraction_target_project/js/minian/ally/bannerMinion.js`
- `extraction_target_project/js/minian/ally/baseAllyMinion.js`
- `extraction_target_project/js/minian/ally/berserkerMinion.js`
- `extraction_target_project/js/minian/ally/shooterMinion.js`
- `extraction_target_project/js/minian/baseMinion.js`
- `extraction_target_project/js/minian/enemy/neonDragonHatchling/neonDragonHatchling.js`
- `extraction_target_project/js/minian/minionBullet.js`
- `extraction_target_project/js/network/networkManager.js`
- `extraction_target_project/js/network/scoreSender.js`
- `extraction_target_project/js/player/basePlayer.js`
- `extraction_target_project/js/player/characters/bufferPlayer.js`
- `extraction_target_project/js/player/characters/defaultPlayer.js`
- `extraction_target_project/js/player/characters/empPlayer.js`
- `extraction_target_project/js/player/characters/index.js`
- `extraction_target_project/js/player/characters/shielderPlayer.js`
- `extraction_target_project/js/player/characters/summonerPlayer.js`
- `extraction_target_project/js/player/particle.js`
- `extraction_target_project/js/player/playerBullet.js`
- `extraction_target_project/js/player/playerFactory.js`
- `extraction_target_project/js/utils/math.js`
- `extraction_target_project/package-lock.json`
- `extraction_target_project/package.json`
- `extraction_target_project/run_server.bat`
- `extraction_target_project/server.js`

## 💀 [Skeleton & Dependency 명세서]
### 📄 extraction_target_project/AGENTS.md
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 extraction_target_project/css/style.css
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 extraction_target_project/index.html
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 extraction_target_project/js/ai/aiEngine.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../config/constants.js, ../utils/math.js, ./dodgeAlgorithm.js
🧬 class AIEngine [L9~L245]
```

--------------------------------------------------

### 📄 extraction_target_project/js/ai/dodgeAlgorithm.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../config/constants.js, ../utils/math.js
🧬 class DodgeAlgorithm [L8~L294]
```

--------------------------------------------------

### 📄 extraction_target_project/js/config/constants.js
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 extraction_target_project/js/core/gameLoop.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../ai/aiEngine.js, ../config/constants.js, ../enemy/bossFactory.js, ../network/scoreSender.js, ../player/particle.js, ../player/playerFactory.js, ../utils/math.js, ./sceneManager.js
🧬 class GameLoop [L14~L23]
```

--------------------------------------------------

### 📄 extraction_target_project/js/core/input.js
#### 🧱 Code Skeleton:
```python
🧬 class InputHandler [L6~L145]
🎯 def endTouch() [L104~L109]
```

--------------------------------------------------

### 📄 extraction_target_project/js/core/sceneManager.js
#### 🧱 Code Skeleton:
```python
🧬 class SceneManager [L13~L80]
```

--------------------------------------------------

### 📄 extraction_target_project/js/core/ui.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../player/characters/index.js
🧬 class UIManager [L8~L407]
🎯 def updateSlotLockStatus() [L69~L87]
🎯 def triggerSkill() [L235~L265]
```

--------------------------------------------------

### 📄 extraction_target_project/js/enemy/baseBoss.js
#### 🧱 Code Skeleton:
```python
🧬 class BaseBoss [L6~L61]
```

--------------------------------------------------

### 📄 extraction_target_project/js/enemy/bossFactory.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./bosses/neonDragon/neonDragon.js
🧬 class BossFactory [L7~L22]
```

--------------------------------------------------

### 📄 extraction_target_project/js/enemy/bosses/neonDragon/neonDragon.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../../../minian/enemy/neonDragonHatchling/neonDragonHatchling.js, ../../../utils/math.js, ../../baseBoss.js, ./neonDragonPattern.js
🧬 class NeonDragon [L10~L226]
```

--------------------------------------------------

### 📄 extraction_target_project/js/enemy/bosses/neonDragon/neonDragonBullet.js
#### 🧱 Code Skeleton:
```python
🧬 class BossBullet [L6~L181]
```

--------------------------------------------------

### 📄 extraction_target_project/js/enemy/bosses/neonDragon/neonDragonParticle.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../../../player/particle.js
🎯 def createBossExplosionParticles(particlesContainer, x, y, color = '#f43f5e', count = 30) [L15~L19]
```

--------------------------------------------------

### 📄 extraction_target_project/js/enemy/bosses/neonDragon/neonDragonPattern.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./neonDragonBullet.js
🧬 class NeonDragonPattern [L7~L58]
```

--------------------------------------------------

### 📄 extraction_target_project/js/main.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./core/gameLoop.js, ./core/input.js, ./core/sceneManager.js, ./core/ui.js, ./network/networkManager.js, ./player/particle.js
```

--------------------------------------------------

### 📄 extraction_target_project/js/minian/ally/bannerMinion.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./baseAllyMinion.js
🧬 class BannerMinion [L8~L85]
```

--------------------------------------------------

### 📄 extraction_target_project/js/minian/ally/baseAllyMinion.js
#### 🧱 Code Skeleton:
```python
🧬 class BaseAllyMinion [L5~L55]
```

--------------------------------------------------

### 📄 extraction_target_project/js/minian/ally/berserkerMinion.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./baseAllyMinion.js
🧬 class BerserkerMinion [L7~L241]
```

--------------------------------------------------

### 📄 extraction_target_project/js/minian/ally/shooterMinion.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./baseAllyMinion.js
🧬 class ShooterMinion [L8~L108]
```

--------------------------------------------------

### 📄 extraction_target_project/js/minian/baseMinion.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./minionBullet.js
🧬 class BaseMinion [L13~L253]
```

--------------------------------------------------

### 📄 extraction_target_project/js/minian/enemy/neonDragonHatchling/neonDragonHatchling.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../../baseMinion.js
🧬 class NeonDragonHatchling [L7~L113]
```

--------------------------------------------------

### 📄 extraction_target_project/js/minian/minionBullet.js
#### 🧱 Code Skeleton:
```python
🧬 class MinionBullet [L6~L58]
```

--------------------------------------------------

### 📄 extraction_target_project/js/network/networkManager.js
#### 🧱 Code Skeleton:
```python
🧬 class NetworkManager [L6~L116]
```

--------------------------------------------------

### 📄 extraction_target_project/js/network/scoreSender.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../config/constants.js
🎯 def sendScoreToServer(payload) [L16~L49]
```

--------------------------------------------------

### 📄 extraction_target_project/js/player/basePlayer.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../config/constants.js, ./playerBullet.js
🧬 class BasePlayer [L9~L18]
```

--------------------------------------------------

### 📄 extraction_target_project/js/player/characters/bufferPlayer.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../basePlayer.js
🧬 class BufferPlayer [L7~L142]
```

--------------------------------------------------

### 📄 extraction_target_project/js/player/characters/defaultPlayer.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../basePlayer.js
🧬 class DefaultPlayer [L7~L19]
```

--------------------------------------------------

### 📄 extraction_target_project/js/player/characters/empPlayer.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../basePlayer.js
🧬 class EmpPlayer [L3~L132]
```

--------------------------------------------------

### 📄 extraction_target_project/js/player/characters/index.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./bufferPlayer.js, ./defaultPlayer.js, ./empPlayer.js, ./shielderPlayer.js, ./summonerPlayer.js
🎯 def getAutoDiscoveredClasses() [L23~L33]
```

--------------------------------------------------

### 📄 extraction_target_project/js/player/characters/shielderPlayer.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../basePlayer.js
🧬 class ShielderPlayer [L7~L272]
```

--------------------------------------------------

### 📄 extraction_target_project/js/player/characters/summonerPlayer.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../../minian/ally/berserkerMinion.js, ../../minian/ally/shooterMinion.js, ../basePlayer.js
🧬 class SummonerPlayer [L9~L68]
```

--------------------------------------------------

### 📄 extraction_target_project/js/player/particle.js
#### 🧱 Code Skeleton:
```python
🧬 class Particle [L9~L47]
🎯 def createImpactParticles(particlesContainer, x, y, color, count = 6) [L57~L61]
🎯 def createFloatingText(x, y, text, color = '#ec4899') [L71~L81]
```

--------------------------------------------------

### 📄 extraction_target_project/js/player/playerBullet.js
#### 🧱 Code Skeleton:
```python
🧬 class PlayerBullet [L6~L70]
```

--------------------------------------------------

### 📄 extraction_target_project/js/player/playerFactory.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./characters/defaultPlayer.js, ./characters/index.js
🧬 class PlayerFactory [L8~L19]
```

--------------------------------------------------

### 📄 extraction_target_project/js/utils/math.js
#### 🧱 Code Skeleton:
```python
🎯 def setGameSeed(seed) [L17~L21]
🎯 def seededRandom() [L23~L28]
🎯 def getDistance(x1, y1, x2, y2) [L30~L32]
🎯 def getAngle(fromX, fromY, toX, toY) [L42~L44]
🎯 def lerp(start, end, factor) [L53~L55]
🎯 def degToRad(deg) [L62~L64]
🎯 def radToDeg(rad) [L71~L73]
🧬 class Vector2D [L78~L109]
```

--------------------------------------------------

### 📄 extraction_target_project/package-lock.json
#### 🔍 내부 심볼 및 의존성 관계:
- **[JSON_KEY]** `name` (Line: 2~2)
- **[JSON_KEY]** `lockfileVersion` (Line: 3~3)
- **[JSON_KEY]** `requires` (Line: 4~4)
- **[JSON_KEY]** `packages` (Line: 5~5)
  - 🔗 *Calls (호출하는 것)*: `node_modules/ipaddr.js, ipaddr.js`

#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "name": str (val: extraction_target_project)
  ├── "lockfileVersion": int (val: 3)
  ├── "requires": bool (val: True)
  ├── "packages": Dict (keys: ['', 'node_modules/accepts', 'node_modules/body-parser']...)
```

--------------------------------------------------

### 📄 extraction_target_project/package.json
#### 🔍 내부 심볼 및 의존성 관계:
- **[JSON_KEY]** `dependencies` (Line: 2~2)

#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "dependencies": Dict (keys: ['express', 'ws']...)
```

--------------------------------------------------

### 📄 extraction_target_project/run_server.bat
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 extraction_target_project/server.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: child_process, fs, http, os, path
🎯 def ensureModule(moduleName) [L15~L23]
🎯 def getLocalIpAddress() [L53~L63]
🎯 def sendRoomState() [L97~L103]
```

--------------------------------------------------

