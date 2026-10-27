# Project Rules & Architecture Guidelines

## 1. Tech Stack & Environment
- **Engine**: Plain HTML5 Canvas + Vanilla JS (ES6 Modules: `import`/`export`).
- **Forbidden**: Do NOT use external heavy game engines or frameworks (No React, Phaser, Pixi, etc.).
- **Server Communication**: Pure HTTP `fetch` POST to remote Leaderboard Server on match completion.

## 2. Directory & Module Architecture
All code MUST respect and fit into the following predefined folder structure:
- `index.html`: Canvas container & HUD / Modal overlay.
- `css/style.css`: Custom animations, HUD styling & neon borders.
- `js/config/constants.js`: Game constants, colors, AI parameters.
- `js/utils/math.js`: Vector, angle, distance, and Lerp helper functions.
- `js/core/`:
  - `sceneManager.js`: Game state manager (MENU -> PLAY -> GAMEOVER).
  - `gameLoop.js`: Main requestAnimationFrame update/render cycle.
  - `input.js`: Keyboard, mouse & touch joystick handlers.
  - `ui.js`: HUD update, damage stats, game-over modal.
- `js/player/`:
  - `basePlayer.js`: Base class for player slots.
  - `playerFactory.js`: Factory for spawning character types.
  - `characters/speedster/`: Specific character code, bullets, and particles.
- `js/enemy/`:
  - `baseBoss.js`: Base class for boss entities.
  - `bossFactory.js`: Boss spawner.
  - `bosses/neonDragon/`: Specific boss patterns, bullets, and particles.
- `js/ai/`:
  - `aiEngine.js`: 0.08s reaction cycle & FSM (IDLE/DODGE/REPOSITION).
  - `dodgeAlgorithm.js`: Angle Offset error angle + Fatigue mistake calculation.
- `js/network/scoreSender.js`: Single `fetch` POST handler for score submission.

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