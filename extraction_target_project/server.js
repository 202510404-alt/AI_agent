/**
 * server.js
 * 방장(Host) 노트북 전용 Node.js 웹소켓 & 정적 파일 서버
 * 
 * [실행 방법]
 * 1. 터미널/CMD 열기: npm install ws express
 * 2. 서버 실행: node server.js
 */

const { execSync } = require('child_process');
const path = require('path');
const os = require('os');

// 💡 [자동 라이브러리 감지 & 설치 구역]
function ensureModule(moduleName) {
    try {
        return require(moduleName);
    } catch (e) {
        console.log(`📦 [Auto Setup] 필수 모듈 '${moduleName}'을(를) 찾을 수 없습니다. 자동으로 설치 중...`);
        execSync(`npm install ${moduleName}`, { stdio: 'inherit' });
        return require(moduleName);
    }
}

const express = ensureModule('express');
const WebSocket = ensureModule('ws');
const http = require('http');

const app = express();
const PORT = 3000;
const WS_PORT = 8080;

const fs = require('fs');

// 💡 [실행 경로 자동 추적]: 어느 위치에서 실행되어도 extraction_target_project 내부 경로 자동 조준
let targetStaticPath = __dirname;

if (fs.existsSync(path.join(__dirname, 'extraction_target_project'))) {
    targetStaticPath = path.join(__dirname, 'extraction_target_project');
} else if (fs.existsSync(path.join(__dirname, 'AI_agent', 'extraction_target_project'))) {
    targetStaticPath = path.join(__dirname, 'AI_agent', 'extraction_target_project');
}

app.use(express.static(targetStaticPath));
console.log(`📂 [Static Directory] 게임 정적 경로 자동 로드 완료: ${targetStaticPath}`);

const server = http.createServer(app);

// 웹소켓 서버 인스턴스 생성 (포트 8080)
const wss = new WebSocket.Server({ port: WS_PORT });

// 현재 호스트 노트북의 로컬 IP 주소 추출
function getLocalIpAddress() {
    const interfaces = os.networkInterfaces();
    for (const name of Object.keys(interfaces)) {
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal) {
                return iface.address;
            }
        }
    }
    return 'localhost';
}

const localIp = getLocalIpAddress();

console.log('====================================================');
console.log(`🚀 [Bullet Hell Host Server] 오프라인 LAN 서버 가동 중`);
console.log(`📱 폰/클라이언트 접속 주소: http://${localIp}:${PORT}?client=true`);
console.log(`⚡ 웹소켓 포트: ${WS_PORT}`);
console.log('====================================================');

// 연결된 모든 클라이언트 패킷 중계 및 슬롯 관리
const connectedSlots = {}; // { wsId: slotIndex }

wss.on('connection', (ws) => {
    // 1~4 중 사용 가능한 빈 슬롯 찾기
    const assignedSlots = Object.values(connectedSlots);
    let mySlot = 1;
    for (let i = 1; i <= 4; i++) {
        if (!assignedSlots.includes(i)) {
            mySlot = i;
            break;
        }
    }
    const socketId = Math.random();
    ws.socketId = socketId;
    ws.slotIndex = mySlot;
    connectedSlots[socketId] = mySlot;

    console.log(`🌐 [WebSocket] 노드 연결됨 - 슬롯 P${mySlot} 할당`);

    // 새로 들어온 클라이언트에게 할당된 슬롯 전달
    ws.send(JSON.stringify({ type: 'SLOT_ASSIGNED', slotIndex: mySlot }));

    // 접속한 전원에게 현재 연결된 슬롯 상태 전파
    const sendRoomState = () => {
        const activeSlots = Object.values(connectedSlots);
        const payload = JSON.stringify({ type: 'ROOM_STATE', activeSlots });
        wss.clients.forEach(c => {
            if (c.readyState === WebSocket.OPEN) c.send(payload);
        });
    };
    sendRoomState();

    ws.on('message', (message) => {
        // 💡 송신자를 포함한 연결된 모든 클라이언트 노드에 조작 및 방 상태 공유
        wss.clients.forEach((client) => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(message.toString());
            }
        });
    });

    ws.on('close', () => {
        delete connectedSlots[ws.socketId];
        console.log(`❌ [WebSocket] P${ws.slotIndex} 연결 해제됨`);
        sendRoomState();
    });
});

server.listen(PORT, () => {
    console.log(`🌐 웹 서버가 포트 ${PORT}에서 정상 대기 중입니다.`);
});