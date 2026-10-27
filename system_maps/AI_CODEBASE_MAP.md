# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)

> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.
> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.

```markdown
extraction_target_project/
├── AGENTS.md [📂 AGENTS.md] -> [General File (45 lines)]
├── css/
│   ├── style.css [📂 css/style.css] -> [General File (32 lines)]
├── index.html [📂 index.html] -> [General File (253 lines)]
├── js/
│   ├── ai/
│   │   ├── aiEngine.js [📂 js/ai/aiEngine.js] -> [💡 📦 imp: ../config/constants.js, ../utils/math.js, ./dodgeAlgorithm.js | 🧬 class AIEngine [L9~L245]]
│   │   │   ├── 🧬 class AIEngine [L9-L245]
│   │   ├── dodgeAlgorithm.js [📂 js/ai/dodgeAlgorithm.js] -> [💡 📦 imp: ../config/constants.js, ../utils/math.js | 🧬 class DodgeAlgorithm [L8~L294]]
│   │   │   ├── 🧬 class DodgeAlgorithm [L8-L294]
│   ├── config/
│   │   ├── constants.js [📂 js/config/constants.js]
│   ├── core/
│   │   ├── gameLoop.js [📂 js/core/gameLoop.js] -> [💡 📦 imp: ../ai/aiEngine.js, ../config/constants.js, ../enemy/bossFactory.js, ../network/scoreSender.js, ../player/particle.js, ../player/playerFactory.js, ../utils/math.js, ./sceneManager.js | 🧬 class GameLoop [L14~L23]]
│   │   │   ├── 🧬 class GameLoop [L14-L23]
│   │   ├── input.js [📂 js/core/input.js] -> [🧬 class InputHandler [L6~L145] | 🎯 def endTouch() [L104~L109]]
│   │   │     ├── 🔑 [REGISTRY]: "InputHandler"
│   │   │   ├── 🧬 class InputHandler [L6-L145]
│   │   │   ├── 🎯 def endTouch() [L104-L109]
│   │   ├── sceneManager.js [📂 js/core/sceneManager.js] -> [🧬 class SceneManager [L13~L80]]
│   │   │   ├── 🧬 class SceneManager [L13-L80]
│   │   ├── ui.js [📂 js/core/ui.js] -> [💡 📦 imp: ../player/characters/index.js | 🧬 class UIManager [L8~L407] | 🎯 def updateSlotLockStatus() [L69~L87] | 🎯 def triggerSkill() [L235~L265]]
│   │   │   ├── 🧬 class UIManager [L8-L407]
│   │   │   ├── 🎯 def updateSlotLockStatus() [L69-L87]
│   │   │   ├── 🎯 def triggerSkill() [L235-L265]
│   ├── enemy/
│   │   ├── baseBoss.js [📂 js/enemy/baseBoss.js] -> [🧬 class BaseBoss [L6~L61]]
│   │   │   ├── 🧬 class BaseBoss [L6-L61]
│   │   ├── bosses/
│   │   │   ├── neonDragon/
│   │   │   │   ├── neonDragon.js [📂 js/enemy/bosses/neonDragon/neonDragon.js] -> [💡 📦 imp: ../../../minian/enemy/neonDragonHatchling/neonDragonHatchling.js, ../../../utils/math.js, ../../baseBoss.js, ./neonDragonPattern.js | 🧬 class NeonDragon [L10~L226]]
│   │   │   │   │   ├── 🧬 class NeonDragon [L10-L226]
│   │   │   │   ├── neonDragonBullet.js [📂 js/enemy/bosses/neonDragon/neonDragonBullet.js] -> [🧬 class BossBullet [L6~L181]]
│   │   │   │   │   ├── 🧬 class BossBullet [L6-L181]
│   │   │   │   ├── neonDragonParticle.js [📂 js/enemy/bosses/neonDragon/neonDragonParticle.js] -> [💡 📦 imp: ../../../player/particle.js | 🎯 def createBossExplosionParticles(particlesContainer, x, y, color = '#f43f5e', count = 30) [L15~L19]]
│   │   │   │   │   ├── 🎯 def createBossExplosionParticles() [L15-L19]
│   │   │   │   ├── neonDragonPattern.js [📂 js/enemy/bosses/neonDragon/neonDragonPattern.js] -> [💡 📦 imp: ./neonDragonBullet.js | 🧬 class NeonDragonPattern [L7~L58]]
│   │   │   │   │   ├── 🧬 class NeonDragonPattern [L7-L58]
│   │   ├── bossFactory.js [📂 js/enemy/bossFactory.js] -> [💡 📦 imp: ./bosses/neonDragon/neonDragon.js | 🧬 class BossFactory [L7~L22]]
│   │   │   ├── 🧬 class BossFactory [L7-L22]
│   ├── main.js [📂 js/main.js] -> [💡 📦 imp: ./core/gameLoop.js, ./core/input.js, ./core/sceneManager.js, ./core/ui.js, ./network/networkManager.js, ./player/particle.js]
│   ├── minian/
│   │   ├── ally/
│   │   │   ├── bannerMinion.js [📂 js/minian/ally/bannerMinion.js] -> [💡 📦 imp: ./baseAllyMinion.js | 🧬 class BannerMinion [L8~L85]]
│   │   │   │   ├── 🧬 class BannerMinion [L8-L85]
│   │   │   ├── baseAllyMinion.js [📂 js/minian/ally/baseAllyMinion.js] -> [🧬 class BaseAllyMinion [L5~L55]]
│   │   │   │   ├── 🧬 class BaseAllyMinion [L5-L55]
│   │   │   ├── berserkerMinion.js [📂 js/minian/ally/berserkerMinion.js] -> [💡 📦 imp: ./baseAllyMinion.js | 🧬 class BerserkerMinion [L7~L241]]
│   │   │   │   ├── 🧬 class BerserkerMinion [L7-L241]
│   │   │   ├── shooterMinion.js [📂 js/minian/ally/shooterMinion.js] -> [💡 📦 imp: ./baseAllyMinion.js | 🧬 class ShooterMinion [L8~L108]]
│   │   │   │   ├── 🧬 class ShooterMinion [L8-L108]
│   │   ├── baseMinion.js [📂 js/minian/baseMinion.js] -> [💡 📦 imp: ./minionBullet.js | 🧬 class BaseMinion [L13~L253]]
│   │   │   ├── 🧬 class BaseMinion [L13-L253]
│   │   ├── enemy/
│   │   │   ├── neonDragonHatchling/
│   │   │   │   ├── neonDragonHatchling.js [📂 js/minian/enemy/neonDragonHatchling/neonDragonHatchling.js] -> [💡 📦 imp: ../../baseMinion.js | 🧬 class NeonDragonHatchling [L7~L113]]
│   │   │   │   │   ├── 🧬 class NeonDragonHatchling [L7-L113]
│   │   ├── minionBullet.js [📂 js/minian/minionBullet.js] -> [🧬 class MinionBullet [L6~L58]]
│   │   │   ├── 🧬 class MinionBullet [L6-L58]
│   ├── network/
│   │   ├── networkManager.js [📂 js/network/networkManager.js] -> [🧬 class NetworkManager [L6~L116]]
│   │   │   ├── 🧬 class NetworkManager [L6-L116]
│   │   ├── scoreSender.js [📂 js/network/scoreSender.js] -> [💡 📦 imp: ../config/constants.js | 🎯 def sendScoreToServer(payload) [L16~L49]]
│   │   │   ├── 🎯 def sendScoreToServer() [L16-L49]
│   ├── player/
│   │   ├── basePlayer.js [📂 js/player/basePlayer.js] -> [💡 📦 imp: ../config/constants.js, ./playerBullet.js | 🧬 class BasePlayer [L9~L18]]
│   │   │   ├── 🧬 class BasePlayer [L9-L18]
│   │   ├── characters/
│   │   │   ├── bufferPlayer.js [📂 js/player/characters/bufferPlayer.js] -> [💡 📦 imp: ../basePlayer.js | 🧬 class BufferPlayer [L7~L142]]
│   │   │   │   ├── 🧬 class BufferPlayer [L7-L142]
│   │   │   ├── defaultPlayer.js [📂 js/player/characters/defaultPlayer.js] -> [💡 📦 imp: ../basePlayer.js | 🧬 class DefaultPlayer [L7~L19]]
│   │   │   │   ├── 🧬 class DefaultPlayer [L7-L19]
│   │   │   ├── empPlayer.js [📂 js/player/characters/empPlayer.js] -> [💡 📦 imp: ../basePlayer.js | 🧬 class EmpPlayer [L3~L132]]
│   │   │   │   ├── 🧬 class EmpPlayer [L3-L132]
│   │   │   ├── index.js [📂 js/player/characters/index.js] -> [💡 📦 imp: ./bufferPlayer.js, ./defaultPlayer.js, ./empPlayer.js, ./shielderPlayer.js, ./summonerPlayer.js | 🎯 def getAutoDiscoveredClasses() [L23~L33]]
│   │   │   │   ├── 🎯 def getAutoDiscoveredClasses() [L23-L33]
│   │   │   ├── shielderPlayer.js [📂 js/player/characters/shielderPlayer.js] -> [💡 📦 imp: ../basePlayer.js | 🧬 class ShielderPlayer [L7~L272]]
│   │   │   │   ├── 🧬 class ShielderPlayer [L7-L272]
│   │   │   ├── summonerPlayer.js [📂 js/player/characters/summonerPlayer.js] -> [💡 📦 imp: ../../minian/ally/berserkerMinion.js, ../../minian/ally/shooterMinion.js, ../basePlayer.js | 🧬 class SummonerPlayer [L9~L68]]
│   │   │   │   ├── 🧬 class SummonerPlayer [L9-L68]
│   │   ├── particle.js [📂 js/player/particle.js] -> [🧬 class Particle [L9~L47] | 🎯 def createImpactParticles(particlesContainer, x, y, color, count = 6) [L57~L61] | 🎯 def createFloatingText(x, y, text, color = '#ec4899') [L71~L81]]
│   │   │   ├── 🧬 class Particle [L9-L47]
│   │   │   ├── 🎯 def createImpactParticles() [L57-L61]
│   │   │   ├── 🎯 def createFloatingText() [L71-L81]
│   │   ├── playerBullet.js [📂 js/player/playerBullet.js] -> [🧬 class PlayerBullet [L6~L70]]
│   │   │   ├── 🧬 class PlayerBullet [L6-L70]
│   │   ├── playerFactory.js [📂 js/player/playerFactory.js] -> [💡 📦 imp: ./characters/defaultPlayer.js, ./characters/index.js | 🧬 class PlayerFactory [L8~L19]]
│   │   │   ├── 🧬 class PlayerFactory [L8-L19]
│   ├── utils/
│   │   ├── math.js [📂 js/utils/math.js] -> [🎯 def setGameSeed(seed) [L17~L21] | 🎯 def seededRandom() [L23~L28] | 🎯 def getDistance(x1, y1, x2, y2) [L30~L32] | 🎯 def getAngle(fromX, fromY, toX, toY) [L42~L44] | 🎯 def lerp(start, end, factor) [L53~L55] | 🎯 def degToRad(deg) [L62~L64] | 🎯 def radToDeg(rad) [L71~L73] | 🧬 class Vector2D [L78~L109]]
│   │   │   ├── 🎯 def setGameSeed() [L17-L21]
│   │   │   ├── 🎯 def seededRandom() [L23-L28]
│   │   │   ├── 🎯 def getDistance() [L30-L32]
│   │   │   ├── 🎯 def getAngle() [L42-L44]
│   │   │   ├── 🎯 def lerp() [L53-L55]
│   │   │   ├── 🎯 def degToRad() [L62-L64]
│   │   │   ├── 🎯 def radToDeg() [L71-L73]
│   │   │   ├── 🧬 class Vector2D [L78-L109]
├── package-lock.json [📂 package-lock.json] -> [💡 📦 json_keys: 4개 포착 | 🔑 "name" [str] | 🔑 "lockfileVersion" [int] | 🔑 "requires" [bool] | 🔑 "packages" [dict]]
│   ├── 🔑 key "name" [L2]
│   ├── 🔑 key "lockfileVersion" [L3]
│   ├── 🔑 key "requires" [L4]
│   ├── 🔑 key "packages" [L5]
│   │   ├── 📞 [CALLS]: node_modules/ipaddr.js, ipaddr.js
├── package.json [📂 package.json] -> [💡 📦 json_keys: 1개 포착 | 🔑 "dependencies" [dict]]
│   ├── 🔑 key "dependencies" [L2]
├── run_server.bat [📂 run_server.bat] -> [General File (16 lines)]
├── server.js [📂 server.js] -> [💡 📦 imp: child_process, fs, http, os, path | 🎯 def ensureModule(moduleName) [L15~L23] | 🎯 def getLocalIpAddress() [L53~L63] | 🎯 def sendRoomState() [L97~L103]]
│   ├── 🎯 def ensureModule() [L15-L23]
│   ├── 🎯 def getLocalIpAddress() [L53-L63]
│   ├── 🎯 def sendRoomState() [L97-L103]
