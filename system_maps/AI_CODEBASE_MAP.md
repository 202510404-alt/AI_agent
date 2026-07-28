# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)

> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.
> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.

```markdown
extraction_target_project/
├── .gitignore [📂 .gitignore]
├── client/
│   ├── .gitignore [📂 client/.gitignore]
│   ├── package-lock.json [📂 client/package-lock.json] -> [💡 📦 json_keys: 5개 포착 | 🔑 "name" [str] | 🔑 "version" [str] | 🔑 "lockfileVersion" [int] | 🔑 "requires" [bool] | 🔑 "packages" [dict]]
│   ├── package.json [📂 client/package.json] -> [💡 📦 json_keys: 7개 포착 | 🔑 "name" [str] | 🔑 "version" [str] | 🔑 "private" [bool] | 🔑 "dependencies" [dict] | 🔑 "scripts" [dict] | ...외 2개]
│   ├── public/
│   │   ├── favicon.ico [📂 client/public/favicon.ico]
│   │   ├── favicon.svg [📂 client/public/favicon.svg]
│   │   ├── index.html [📂 client/public/index.html]
│   │   ├── logo.svg [📂 client/public/logo.svg]
│   │   ├── logo192.png [📂 client/public/logo192.png]
│   │   ├── logo512.png [📂 client/public/logo512.png]
│   │   ├── manifest.json [📂 client/public/manifest.json] -> [💡 📦 json_keys: 7개 포착 | 🔑 "short_name" [str] | 🔑 "name" [str] | 🔑 "icons" [list] | 🔑 "start_url" [str] | 🔑 "display" [str] | ...외 2개]
│   ├── src/
│   │   ├── App.css [📂 client/src/App.css]
│   │   ├── App.js [📂 client/src/App.js] -> [💡 📦 imp: ./Canvas, ./Home, react, react-hot-toast, react-router-dom | 🎯 def App() [L11~L20]]
│   │   ├── App.test.js [📂 client/src/App.test.js] -> [💡 📦 imp: ./App, @testing-library/react]
│   │   ├── Button.js [📂 client/src/Button.js] -> [💡 📦 imp: react | 🎯 def Button({ value, name, buttonFunction }) [L4~L24]]
│   │   ├── Canvas.js [📂 client/src/Canvas.js] -> [💡 📦 imp: ./Button, ./UploadFile, ./hooks/useWebRTC, ./socket, react, react-hot-toast, react-icons/ai, react-icons/fa6, react-router-dom | 🎯 def RemoteAudio({ stream }) [L24~L32] | 🎯 def Canvas(props) [L34~L433] | 🎯 def changeColour(event) [L61~L64] | 🎯 def lineWidth(event) [L66~L72] | 🎯 def handleImageUploadSuccess(imageUrl) [L74~L82] | 🎯 def init() [L85~L133] | 🎯 def handleError(err) [L96~L100] | 🎯 def handleDraw(e) [L165~L175] | 🎯 def handleMoveDraw(e) [L177~L191] | 🎯 def handleNotDraw() [L193~L200] | 🎯 def undo() [L202~L210] | 🎯 def redrawCanvas(context) [L212~L230] | 🎯 def handleCanvasChange() [L236~L241] | 🎯 def clearCanvas() [L250~L257] | 🎯 def copyBoardId() [L259~L262] | 🎯 def leaveBoard() [L264~L266]]
│   │   ├── Home.js [📂 client/src/Home.js] -> [💡 📦 imp: react, react-hot-toast, react-router-dom, uuid | 🎯 def Home() [L8~L63] | 🎯 def writeId(event) [L14~L18] | 🎯 def writeUserName(event) [L20~L22] | 🎯 def generateUniqueId(event) [L24~L29] | 🎯 def joinBoard() [L31~L39]]
│   │   ├── hooks/
│   │   │   ├── useWebRTC.js [📂 client/src/hooks/useWebRTC.js] -> [💡 📦 imp: react, react-hot-toast | 🎯 def useWebRTC(socketRef, boardId, userName) [L11~L278]]
│   │   ├── index.css [📂 client/src/index.css]
│   │   ├── index.js [📂 client/src/index.js] -> [💡 📦 imp: ./App, ./reportWebVitals, react, react-dom/client]
│   │   ├── Input.js [📂 client/src/Input.js] -> [💡 📦 imp: react | 🎯 def Input(props) [L3~L9]]
│   │   ├── reportWebVitals.js [📂 client/src/reportWebVitals.js]
│   │   ├── setupTests.js [📂 client/src/setupTests.js]
│   │   ├── socket.js [📂 client/src/socket.js] -> [💡 📦 imp: socket.io-client | 🎯 def initSocket() [L3~L19]]
│   │   ├── style.css [📂 client/src/style.css]
│   │   ├── styleCanvas.css [📂 client/src/styleCanvas.css]
│   │   ├── UploadFile.js [📂 client/src/UploadFile.js] -> [💡 📦 imp: react, react-icons/fa6 | 🎯 def UploadFile(props) [L5~L31] | 🎯 def upload(event) [L8~L15]]
├── index.js [📂 index.js] -> [💡 📦 imp: dateuuidv2, express, http, path, socket.io, url | 🎯 def getAllConnectedClients(boardId) [L22~L28]]
├── just_test_tools/
│   ├── Main.java [📂 just_test_tools/Main.java] -> [💡 📦 imp: java.awt.*, java.awt.event.KeyAdapter, java.awt.event.KeyEvent, javax.swing.* | 🧬 class Main [L6-76] | 🎯 def Main() [L10-35] | 🎯 def setFocusable(true) [L12-25] | 🎯 def addKeyListener(new) [L15-25] | 🎯 def keyPressed(KeyEvent) [L17-24] | 🎯 def repaint() [L23-28] | 🎯 def repaint() [L32-38] | 🎯 def paintComponent(Graphics) [L38-64] | 🎯 def main(String[]) [L66-75]]
│   ├── main.py [📂 just_test_tools/main.py] -> [💡 📦 imp: tetris_logic, time | 🎯 def render(board, piece) [L4-22] | 🎯 def start_game() [L24-49]]
│   ├── tetris_logic.py [📂 just_test_tools/tetris_logic.py] -> [💡 📦 imp: random | 🧬 class Tetromino [L3-22] |     └─ def __init__(x, y) [L15-18] |     └─ def rotate() [L20-22] | 🧬 class Board [L25-70] |     └─ def __init__(width, height) [L27-30] |     └─ def is_valid_position(piece, offset_x, offset_y) [L32-46] |     └─ def lock_piece(piece) [L48-53] |     └─ def clear_lines() [L55-70]]
│   ├── TetrisModel.java [📂 just_test_tools/TetrisModel.java] -> [💡 📦 imp: java.util.Random | 🧬 class TetrisModel [L3-73] | 🎯 def TetrisModel() [L19-21] | 🎯 def spawnPiece() [L20-23] | 🎯 def spawnPiece() [L23-28] | 🎯 def move(int, int) [L30-37] | 🎯 def canMove(int[][], int, int) [L39-56] | 🎯 def lockPiece() [L58-67] | 🎯 def spawnPiece() [L66-69] | 🎯 def getGrid() [L69-69] | 🎯 def getCurrentShape() [L70-70] | 🎯 def getCurrentX() [L71-71] | 🎯 def getCurrentY() [L72-72]]
├── package-lock.json [📂 package-lock.json] -> [💡 📦 json_keys: 5개 포착 | 🔑 "name" [str] | 🔑 "version" [str] | 🔑 "lockfileVersion" [int] | 🔑 "requires" [bool] | 🔑 "packages" [dict]]
├── package.json [📂 package.json] -> [💡 📦 json_keys: 8개 포착 | 🔑 "name" [str] | 🔑 "version" [str] | 🔑 "description" [str] | 🔑 "type" [str] | 🔑 "main" [str] | ...외 3개]
├── prompt.md [📂 prompt.md]
├── README.md [📂 README.md]
├── start.bat [📂 start.bat]
