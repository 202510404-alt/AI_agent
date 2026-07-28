# 🏗️ 짭커서 프로젝트 CODEBASE MAP

현재 인덱싱된 총 파일 수: **22개**

## 🗂️ [Module Index]
- `extraction_target_project/client/package-lock.json`
- `extraction_target_project/client/package.json`
- `extraction_target_project/client/public/manifest.json`
- `extraction_target_project/client/src/App.js`
- `extraction_target_project/client/src/App.test.js`
- `extraction_target_project/client/src/Button.js`
- `extraction_target_project/client/src/Canvas.js`
- `extraction_target_project/client/src/Home.js`
- `extraction_target_project/client/src/Input.js`
- `extraction_target_project/client/src/UploadFile.js`
- `extraction_target_project/client/src/hooks/useWebRTC.js`
- `extraction_target_project/client/src/index.js`
- `extraction_target_project/client/src/reportWebVitals.js`
- `extraction_target_project/client/src/setupTests.js`
- `extraction_target_project/client/src/socket.js`
- `extraction_target_project/index.js`
- `extraction_target_project/just_test_tools/Main.java`
- `extraction_target_project/just_test_tools/TetrisModel.java`
- `extraction_target_project/just_test_tools/main.py`
- `extraction_target_project/just_test_tools/tetris_logic.py`
- `extraction_target_project/package-lock.json`
- `extraction_target_project/package.json`

## 💀 [Skeleton & Dependency 명세서]
### 📄 extraction_target_project/client/package-lock.json
#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "name": str (val: whiteboard)
  ├── "version": str (val: 0.1.0)
  ├── "lockfileVersion": int (val: 3)
  ├── "requires": bool (val: True)
  ├── "packages": Dict (keys: ['', 'node_modules/@aashutoshrathi/word-wrap', 'node_modules/@adobe/css-tools']...)
```

--------------------------------------------------

### 📄 extraction_target_project/client/package.json
#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "name": str (val: whiteboard)
  ├── "version": str (val: 0.1.0)
  ├── "private": bool (val: True)
  ├── "dependencies": Dict (keys: ['@testing-library/jest-dom', '@testing-library/react', '@testing-library/user-event']...)
  ├── "scripts": Dict (keys: ['start', 'build', 'test']...)
  ├── "eslintConfig": Dict (keys: ['extends']...)
  ├── "browserslist": Dict (keys: ['production', 'development']...)
```

--------------------------------------------------

### 📄 extraction_target_project/client/public/manifest.json
#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "short_name": str (val: 화이트보드)
  ├── "name": str (val: 실시간 협업 화이트보드)
  ├── "icons": List (len: 4)
  ├── "start_url": str (val: .)
  ├── "display": str (val: standalone)
  ├── "theme_color": str (val: #243b55)
  ├── "background_color": str (val: #141e30)
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/App.js
#### 🧱 Code Skeleton:
```python
import React from "react";
import Canvas from "./Canvas";
import {useState} from "react";
import { Toaster } from "react-hot-toast";
import { BrowserRouter,Routes,Route } from "react-router-dom";
import Home from "./Home";




function App() {
  
  // const [color,setColor] = useState("#000000");
   
  const [height,setHeight] = useState(700);
  const [width,setWidth] = useState(1200);
  
//  window.onscroll = function (event) {
     
//   if(window.scrollY > 0)
//     setHeight(height + 10);

/
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/App.test.js
#### 🧱 Code Skeleton:
```python
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/Button.js
#### 🧱 Code Skeleton:
```python
import React from "react";
import './style.css';

function Button({ value, name, buttonFunction }) {
  return (
    <button
      value={value}
      title={name}
      style={{
        backgroundColor: value,
        width: "22px",
        height: "22px",
        borderRadius: "50%",
        border: "2px solid rgba(255, 255, 255, 0.4)",
        cursor: "pointer",
        padding: 0,
        margin: "2px",
        boxShadow: "0 2px 4px rgba(0,0,0,0.3)"
      }}
      onClick={(event) => { button
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/Canvas.js
#### 🧱 Code Skeleton:
```python
import React, { useRef, useEffect, useState } from "react";
import UploadFile from './UploadFile';
import './style.css';
import './styleCanvas.css';
import { initSocket } from "./socket";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import toast from "react-hot-toast";
import Button from "./Button";
import { AiOutlineClear } from "react-icons/ai";
import { FaImage, FaRegSquareMinus } from "react-icons/fa6";
import {
  FaRegPlusSquare,
  FaMicrophone,
  FaMicrophoneSlas
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/Home.js
#### 🧱 Code Skeleton:
```python
import React from 'react';
import { useState } from 'react';
import {v4 as uuidv4} from 'uuid';
import toast from 'react-hot-toast';
import {useNavigate} from "react-router-dom";
import './style.css';

function Home(){
    const navigate = useNavigate();
    
   const [uniqueId,setUniqueId] = useState("");
   const [userName,setUserName] = useState("");

   function writeId(event){
    let newId = event.target.value
    setUniqueId(newId);

  }

  function writeUserName(event){
      setUserName
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/Input.js
#### 🧱 Code Skeleton:
```python
import React from "react";

function Input(props){

    
    return (
        <input type="text" placeholder={props.placeholder} value={props.value} onChange={props.changeFunction}/>
    )
}

export default Input;
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/UploadFile.js
#### 🧱 Code Skeleton:
```python
import React, { useState } from "react";
import './style.css';
import { FaImage } from "react-icons/fa6";

function UploadFile(props) {
  const [imageFile, uploadImageFile] = useState();

  function upload(event) {
    const file = event.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      uploadImageFile(url);
      props.imageSource(url);
    }
  }

  return (
    <div>
      <label htmlFor={props.id || "uploadedImage"} className="tool-btn" title="이미지 업로드" style=
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/hooks/useWebRTC.js
#### 🧱 Code Skeleton:
```python
import { useState, useRef, useCallback, useEffect } from "react";
import toast from "react-hot-toast";

const ICE_SERVERS = {
  iceServers: [
    { urls: "stun:stun.l.google.com:19302" },
    { urls: "stun:stun1.l.google.com:19302" },
  ],
};

export function useWebRTC(socketRef, boardId, userName) {
  const [localStream, setLocalStream] = useState(null);
  const [remoteStreams, setRemoteStreams] = useState({}); // { [socketId]: MediaStream }
  const [voiceUsers, setVoiceUsers] = useState([]); /
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/index.js
#### 🧱 Code Skeleton:
```python
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bi
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/reportWebVitals.js
#### 🧱 Code Skeleton:
```python
const reportWebVitals = onPerfEntry => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

export default reportWebVitals;
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/setupTests.js
#### 🧱 Code Skeleton:
```python
// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/socket.js
#### 🧱 Code Skeleton:
```python
import { io } from "socket.io-client";

export const initSocket = async () => {
  const options = {
    "force new connection": true,
    reconnectionAttempt: "infinity",
    timeout: 10000,
    transports: ["websocket"],
  };

  // 개발: React(3000) → 서버(7605) / 빌드 후: 같은 서버 origin 사용
  const serverUrl =
    process.env.REACT_APP_SOCKET_URL ||
    (process.env.NODE_ENV === "production"
      ? window.location.origin
      : "http://localhost:7605");

  return io(serverUrl, options);
};
```

--------------------------------------------------

### 📄 extraction_target_project/index.js
#### 🧱 Code Skeleton:
```python
import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";
import path from "path";
import { extractDate } from "dateuuidv2";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const clientBuildPath = path.join(__dirname, "client", "build");
const PORT = process.env.PORT || 7605;

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServ
```

--------------------------------------------------

### 📄 extraction_target_project/just_test_tools/Main.java
#### 🧱 Code Skeleton:
```python
class Main { // L6-76
    public Main() { // L10-35
    setFocusable(true); // L12-25
    addKeyListener(new KeyAdapter() { // L15-25
    public void keyPressed(KeyEvent e) { // L17-24
    repaint(); // L23-28
    repaint(); // L32-38
    protected void paintComponent(Graphics g) { // L38-64
    public static void main(String[] args) { // L66-75
```

--------------------------------------------------

### 📄 extraction_target_project/just_test_tools/TetrisModel.java
#### 🧱 Code Skeleton:
```python
class TetrisModel { // L3-73
    public TetrisModel() { // L19-21
    spawnPiece(); // L20-23
    public void spawnPiece() { // L23-28
    public boolean move(int dx, int dy) { // L30-37
    public boolean canMove(int[][] shape, int newX, int newY) { // L39-56
    public void lockPiece() { // L58-67
    spawnPiece(); // L66-69
    public int[][] getGrid() { return grid; } // L69-69
    public int[][] getCurrentShape() { return currentShape; } // L70-70
    public int getCurrentX() { return currentX; } // L71-71
    public int getCurrentY() { return currentY; } // L72-72
```

--------------------------------------------------

### 📄 extraction_target_project/just_test_tools/main.py
#### 🧱 Code Skeleton:
```python
def render(board: Board, piece: Tetromino) -> None:
    """보드와 현재 떨어지는 블록을 터미널에 시각화하는 함수"""
    # 임시 보드 복사
    temp_grid = [row[:] for row in board.grid]
    
    # 현재 움직이는 블록 그리기
    for r_idx, row in enumerate(piece.shape):
        for c_idx, val in enumerate(row):
            if val:
                py, px = piece.y + r_idx, piece.x + c_idx
                if 0 <= py < board.height and 0 <= px < board.width:
                    temp_grid[py][px] = 2

    print("\033[H\033[J", end="")  # 화면 갱신 (터미널 클리어)
    print("=" * (board.width * 2 + 2))
    for row in temp_grid:
        line = "|" + "".join("■ " if cell else "  " for cell in row) + "|"
        print(line)
    print("=" * (board.width * 2 + 2))

def start_game() -> None:
    board = Board(width=10, height=15)
    current_piece = Tetromino()
    score = 0

    while True:
        render(board, current_piece)
        time.sleep(0.3)  # 블록이 내려오는 속도 조절

        # 아래로 1칸 이동 시도
        if board.is_valid_position(current_piece, offset_x=0, offset_y=1):
            current_piece.y += 1
        else:
            # 더 이상 못 내려가면 고정
            board.lock_piece(current_piece)
            cleared = board.clear_lines()
            score += cleared * 100
            
            # 새 블록 생성
            current_piece = Tetromino()
            
            # 새 블록 생성 위치가 겹치면 게임 오버
            if not board.is_valid_position(current_piece):
                render(board, current_piece)
                print(f"GAME OVER! 최종 점수: {score}")
                break
```

--------------------------------------------------

### 📄 extraction_target_project/just_test_tools/tetris_logic.py
#### 🧱 Code Skeleton:
```python
class Tetromino:
    """테트리스 블록 데이터 및 회전 로직 관리"""
    SHAPES = [
        [[1, 1, 1, 1]],                  # I
        [[1, 1], [1, 1]],                # O
        [[0, 1, 0], [1, 1, 1]],          # T
        [[1, 0, 0], [1, 1, 1]],          # L
        [[0, 0, 1], [1, 1, 1]],          # J
        [[0, 1, 1], [1, 0, 0]],          # S
        [[1, 1, 0], [0, 1, 1]]           # Z
    ]

    def __init__(self, x: int = 3, y: int = 0):
        self.x = x
        self.y = y
        self.shape = random.choice(self.SHAPES)

    def rotate(self) -> None:
        """블록을 시계 방향으로 90도 회전"""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Board:
    """테트리스 판 및 이동/충돌 감지 로직"""
    def __init__(self, width: int = 10, height: int = 20):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)]

    def is_valid_position(self, piece: Tetromino, offset_x: int = 0, offset_y: int = 0) -> bool:
        """해당の位置로 이동이 가능한지 확인 (인자: piece 객체, 오프셋 값)"""
        for r_idx, row in enumerate(piece.shape):
            for c_idx, val in enumerate(row):
                if val:
                    new_x = piece.x + c_idx + offset_x
                    new_y = piece.y + r_idx + offset_y
                    
                    # 경계선 체크
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False
                    # 기존에 쌓인 블록과 충돌 체크
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def lock_piece(self, piece: Tetromino) -> None:
        """블록을 보드판에 고정"""
        for r_idx, row in enumerate(piece.shape):
            for c_idx, val in enumerate(row):
                if val:
                    self.grid[piece.y + r_idx][piece.x + c_idx] = 1

    def clear_lines(self) -> int:
        """꽉 찬 줄을 지우고 획득한 줄 수를 반환"""
        lines_cleared = 0
        new_grid = []
        for row in self.grid:
            if all(cell == 1 for cell in row):
                lines_cleared += 1
            else:
                new_grid.append(row)
        
        # 지워진 줄만큼 위에 빈 줄 추가
        for _ in range(lines_cleared):
            new_grid.insert(0, [0] * self.width)
            
        self.grid = new_grid
        return lines_cleared
```

--------------------------------------------------

### 📄 extraction_target_project/package-lock.json
#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "name": str (val: real-time-collaborat)
  ├── "version": str (val: 1.0.0)
  ├── "lockfileVersion": int (val: 3)
  ├── "requires": bool (val: True)
  ├── "packages": Dict (keys: ['', 'node_modules/@socket.io/component-emitter', 'node_modules/@types/cors']...)
```

--------------------------------------------------

### 📄 extraction_target_project/package.json
#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "name": str (val: real-time-collaborat)
  ├── "version": str (val: 1.0.0)
  ├── "description": str (val: Real-time collaborat)
  ├── "type": str (val: module)
  ├── "main": str (val: index.js)
  ├── "scripts": Dict (keys: ['start', 'dev', 'dev:client']...)
  ├── "license": str (val: ISC)
  ├── "dependencies": Dict (keys: ['express', 'nodemon', 'dateuuidv2']...)
```

--------------------------------------------------

