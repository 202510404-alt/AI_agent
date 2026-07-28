# 🏗️ 짭커서 프로젝트 CODEBASE MAP

현재 인덱싱된 총 파일 수: **18개**

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

