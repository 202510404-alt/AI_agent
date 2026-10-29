# 🏗️ 짭커서 프로젝트 CODEBASE MAP

현재 인덱싱된 총 파일 수: **44개**

## 🗂️ [Module Index]
- `extraction_target_project/AGENTS.md`
- `extraction_target_project/css/style.css`
- `extraction_target_project/index.html`
- `extraction_target_project/js/ai/aiEngine.js`
- `extraction_target_project/js/ai/dodgeAlgorithm.js`
- `extraction_target_project/js/config/constants.js`
- `extraction_target_project/js/core/InputManager.js`
- `extraction_target_project/js/core/audioManager.js`
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
- `extraction_target_project/js/utils/seededRNG.js`
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
💡 📦 imp: ../config/constants.js, ../utils/math.js, ../utils/seededRNG.js, ./dodgeAlgorithm.js
🧬 class AIEngine [L10~L255]
```

--------------------------------------------------

### 📄 extraction_target_project/js/ai/dodgeAlgorithm.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../config/constants.js, ../utils/math.js, ../utils/seededRNG.js
🧬 class DodgeAlgorithm [L9~L306]
```

--------------------------------------------------

### 📄 extraction_target_project/js/config/constants.js
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 extraction_target_project/js/core/InputManager.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./input.js
🧬 class InputManager [L9~L35]
```

--------------------------------------------------

### 📄 extraction_target_project/js/core/audioManager.js
#### 🧱 Code Skeleton:
```python
🧬 class AudioManager [L2~L82]
```

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
💡 📦 imp: ../utils/seededRNG.js
🧬 class InputHandler [L12~L298]
🎯 def updateJoystick(clientX, clientY) [L144~L162]
🎯 def endJoystick(e) [L179~L186]
```

--------------------------------------------------

### 📄 extraction_target_project/js/core/sceneManager.js
#### 🧱 Code Skeleton:
```python
🧬 class SceneManager [L16~L95]
```

--------------------------------------------------

### 📄 extraction_target_project/js/core/ui.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../player/characters/index.js
🧬 class UIManager [L8~L17]
🎯 def updateSlotLockStatus() [L69~L87]
🎯 def triggerSkill() [L248~L281]
🧬 class truncate [L480~L492]
🧬 class truncate [L518~L527]
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
💡 📦 imp: ../utils/seededRNG.js, ./bosses/neonDragon/neonDragon.js
🧬 class BossFactory [L8~L31]
```

--------------------------------------------------

### 📄 extraction_target_project/js/enemy/bosses/neonDragon/neonDragon.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../../../minian/enemy/neonDragonHatchling/neonDragonHatchling.js, ../../../utils/seededRNG.js, ../../baseBoss.js, ./neonDragonPattern.js
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
💡 📦 imp: ../../../utils/seededRNG.js, ./neonDragonBullet.js
🧬 class NeonDragonPattern [L8~L59]
```

--------------------------------------------------

### 📄 extraction_target_project/js/main.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./core/InputManager.js, ./core/audioManager.js, ./core/gameLoop.js, ./core/sceneManager.js, ./core/ui.js, ./network/networkManager.js, ./player/particle.js
🎯 def resizeCanvas() [L43~L53]
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
💡 📦 imp: ../../utils/seededRNG.js, ./baseAllyMinion.js
🧬 class ShooterMinion [L9~L109]
```

--------------------------------------------------

### 📄 extraction_target_project/js/minian/baseMinion.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../utils/seededRNG.js, ./minionBullet.js
🧬 class BaseMinion [L14~L254]
```

--------------------------------------------------

### 📄 extraction_target_project/js/minian/enemy/neonDragonHatchling/neonDragonHatchling.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../../../utils/seededRNG.js, ../../baseMinion.js
🧬 class NeonDragonHatchling [L8~L114]
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
💡 📦 imp: ../utils/seededRNG.js
🧬 class NetworkManager [L14~L423]
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
💡 📦 imp: ../config/constants.js, ../utils/seededRNG.js, ./playerBullet.js
🧬 class BasePlayer [L15~L462]
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
🧬 class ShielderPlayer [L11~L255]
```

--------------------------------------------------

### 📄 extraction_target_project/js/player/characters/summonerPlayer.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ../../minian/ally/berserkerMinion.js, ../../minian/ally/shooterMinion.js, ../basePlayer.js
🧬 class SummonerPlayer [L12~L84]
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
💡 📦 imp: ./seededRNG.js
🎯 def setGameSeed(seed) [L18~L23]
🎯 def seededRandom() [L25~L27]
🎯 def getDistance(x1, y1, x2, y2) [L29~L31]
🎯 def getAngle(fromX, fromY, toX, toY) [L41~L43]
🎯 def lerp(start, end, factor) [L52~L54]
🎯 def degToRad(deg) [L61~L63]
🎯 def radToDeg(rad) [L70~L72]
🧬 class Vector2D [L77~L108]
```

--------------------------------------------------

### 📄 extraction_target_project/js/utils/seededRNG.js
#### 🧱 Code Skeleton:
```python
🎯 def hashSeed(seed) [L14~L28]
🧬 class Mulberry32PRNG [L34~L78]
🧬 class SeededRNGManager [L83~L142]
```

--------------------------------------------------

### 📄 extraction_target_project/package-lock.json
#### 🔍 내부 심볼 및 의존성 관계:
- **[JSON_KEY]** `name` (Line: 2~2)
- **[JSON_KEY]** `lockfileVersion` (Line: 3~3)
- **[JSON_KEY]** `requires` (Line: 4~4)
- **[JSON_KEY]** `packages` (Line: 5~5)
  - 🔗 *Calls (호출하는 것)*: `ipaddr.js, node_modules/ipaddr.js`

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
🎯 def ensureModule(moduleName) [L20~L28]
🎯 def generateMasterSeed() [L73~L75]
🎯 def broadcast(payloadObj) [L80~L87]
🎯 def broadcastRoomState() [L92~L119]
🎯 def broadcastVoteStatus() [L124~L136]
🎯 def changePhase(nextPhase) [L142~L166]
🎯 def checkReadyUnanimity() [L171~L181]
🎯 def checkScoreboardVoting() [L186~L209]
🎯 def getLocalIpAddress() [L212~L222]
```

--------------------------------------------------

