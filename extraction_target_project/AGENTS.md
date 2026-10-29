# Project Rules & Architecture Guidelines

## 1. Tech Stack & Environment
- **Engine**: Plain HTML5 Canvas + Vanilla JS (ES6 Modules: `import`/`export`).
- **Forbidden**: Do NOT use external heavy game engines or frameworks (No React, Phaser, Pixi, etc.).
- **Server Communication**: WebSocket / Pure HTTP Node.js native server (`server.js`).

## 2. Directory & Module Architecture
All code MUST respect and fit into the following predefined folder structure:
- `index.html`: Canvas container & HUD / Modal overlay.
- `css/style.css`: Custom animations, HUD styling & neon borders.
- `server.js`: Node.js WebSocket/HTTP server handling Room State, Voting, and Sync.
- `js/config/constants.js`: Game constants, colors, AI parameters.
- `js/utils/math.js` & `js/utils/seededRNG.js`: Vector, math helpers, and deterministic PRNG.
- `js/core/`:
  - `sceneManager.js`: Game state manager (LOBBY -> MENU -> GAME -> SCOREBOARD).
  - `gameLoop.js`: Main requestAnimationFrame update/render cycle.
  - `inputManager.js`: Consolidated input controller (Keyboard, Joystick, AI mode toggle).
  - `ui.js`: HUD update, damage stats, game-over modal, voting status overlay.
  - `TeamBuffManager.js`: Shared team buffs (8 types).
- `js/player/`:
  - `basePlayer.js`: Base class for player slots (P1~P4).
  - `playerFactory.js`: Factory for spawning character types.
  - `characters/`: Specific player classes.
- `js/enemy/`:
  - `baseBoss.js` & `bossFactory.js`: Boss logic and spawner.
- `js/ai/`:
  - `aiEngine.js` & `dodgeAlgorithm.js`: AI behavior logic.
- `js/network/`:
  - `networkManager.js`: WebSocket connection, event dispatching, room sync.
  - `scoreSender.js`: HTTP score submission handler.

## 3. Strict Coding Constraints
1. **ES6 Modules**: Always use `import` and `export` statements properly across all JS files.
2. **Comment Language**: Write code comments in Korean (한국어 주석 필수).
3. **Short & Modular**: Keep functions small, single-purpose, and cleanly separated.

## 4. Code Modification Rule (SEARCH / REPLACE Verification)
To prevent code loss or hallucination during file edits, DO NOT rewrite entire files when making small updates.
When presenting or applying code changes, use the following DIFF block format:

<<<<<<< SEARCH
// 기존 파일에 실제로 존재하는 코드 부분
=======
// 변경될 새로운 코드 부분
>>>>>>> REPLACE