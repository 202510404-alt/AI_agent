const DEBUG = process.env.NODE_ENV !== "production";

import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";
import path from "path";
import { fileURLToPath } from "url";
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const clientBuildPath = path.join(__dirname, "client", "build");
const PORT = process.env.PORT || 7605;

const app = express();
const httpServer = createServer(app);

// CORS 설정 및 소켓 서버 생성
const io = new Server(httpServer, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  },
  pingTimeout: 60000,
  pingInterval: 25000
});

// socketId -> { userName, boardId } 매핑으로 관리 체계 일원화
const socketUserMap = {};
const boardUsersMap = {};
const voiceUsersMap = {};

app.use(express.static(clientBuildPath));

function getAllConnectedClients(boardId) {
  const socketIds = Array.from(io.sockets.adapter.rooms.get(boardId) || []);
  return socketIds.map((sid) => ({
    socketId: sid,
    userName: socketUserMap[sid]?.userName || "Unknown",
  }));
}

io.on("connection", (socket) => {
  if (DEBUG) {
    console.log(`[index.js] connection() -> Socket Connected: ${socket.id}`);
  }

  socket.on("join", ({ boardId, userName }) => {
    // 소켓 ID 기준으로 사용자 및 보드 정보 저장
    socketUserMap[socket.id] = { userName, boardId };

    if (!boardUsersMap[boardId]) {
      boardUsersMap[boardId] = new Set();
    }
    boardUsersMap[boardId].add(userName);

    if (DEBUG) {
      console.log(`[index.js] join() -> User Joined Board: (userName: ${userName}, socketId: ${socket.id}, boardId: ${boardId})`);
    }
    socket.join(boardId);

    const clients = getAllConnectedClients(boardId);

    // 해당 방 전체에 업데이트 브로드캐스트
    io.in(boardId).emit("joined", {
      clients,
      userName,
      socketId: socket.id,
    });
  });

  socket.on("board_change", ({ boardId, code }) => {
    socket.in(boardId).emit("board_change", { code });
  });

  socket.on("image_update", ({ boardId, imageUrl }) => {
    socket.in(boardId).emit("image_update", { imageUrl });
  });

  // WebRTC Voice Signaling Events
  socket.on("join-voice", ({ boardId, userName }) => {
    if (!voiceUsersMap[boardId]) {
      voiceUsersMap[boardId] = {};
    }
    voiceUsersMap[boardId][socket.id] = { userName, isMuted: false };

    if (DEBUG) {
      console.log(`[index.js] join-voice() -> Voice Joined: (socketId: ${socket.id}, userName: ${userName}, boardId: ${boardId})`);
    }

    const voiceUsersList = Object.keys(voiceUsersMap[boardId]).map((sid) => ({
      socketId: sid,
      userName: voiceUsersMap[boardId][sid].userName,
      isMuted: voiceUsersMap[boardId][sid].isMuted,
    }));
    socket.emit("voice-users", voiceUsersList);

    socket.in(boardId).emit("user-joined-voice", {
      socketId: socket.id,
      userName,
      isMuted: false,
    });
  });

  socket.on("leave-voice", ({ boardId }) => {
    if (voiceUsersMap[boardId] && voiceUsersMap[boardId][socket.id]) {
      delete voiceUsersMap[boardId][socket.id];
      if (Object.keys(voiceUsersMap[boardId]).length === 0) {
        delete voiceUsersMap[boardId];
      }
    }
    if (DEBUG) {
      console.log(`[index.js] leave-voice() -> Voice Left: (socketId: ${socket.id}, boardId: ${boardId})`);
    }
    socket.in(boardId).emit("user-left-voice", { socketId: socket.id });
  });

  socket.on("offer", ({ targetSocketId, offer }) => {
    if (DEBUG) {
      console.log(`[index.js] offer() -> Relaying Offer: (from: ${socket.id} -> to: ${targetSocketId})`);
    }
    io.to(targetSocketId).emit("offer", {
      callerSocketId: socket.id,
      offer,
    });
  });

  socket.on("answer", ({ targetSocketId, answer }) => {
    if (DEBUG) {
      console.log(`[index.js] answer() -> Relaying Answer: (from: ${socket.id} -> to: ${targetSocketId})`);
    }
    io.to(targetSocketId).emit("answer", {
      responderSocketId: socket.id,
      answer,
    });
  });

  socket.on("ice-candidate", ({ targetSocketId, candidate }) => {
    if (DEBUG) {
      console.log(`[index.js] ice-candidate() -> Relaying ICE Candidate: (from: ${socket.id} -> to: ${targetSocketId})`);
    }
    io.to(targetSocketId).emit("ice-candidate", {
      senderSocketId: socket.id,
      candidate,
    });
  });

  socket.on("mute-changed", ({ boardId, isMuted }) => {
    if (voiceUsersMap[boardId] && voiceUsersMap[boardId][socket.id]) {
      const prevMuted = voiceUsersMap[boardId][socket.id].isMuted;
      voiceUsersMap[boardId][socket.id].isMuted = isMuted;

      if (DEBUG) {
        console.log(`[index.js] mute-changed() -> Mute State Changed: (socketId: ${socket.id}, isMuted: ${prevMuted} -> ${isMuted})`);
      }
    }
    socket.in(boardId).emit("user-mute-changed", {
      socketId: socket.id,
      isMuted,
    });
  });

  socket.on("disconnecting", () => {
    if (DEBUG) {
      console.log(`[index.js] disconnecting() -> Cleaning Up Disconnected Socket: ${socket.id}`);
    }

    const userInfo = socketUserMap[socket.id];
    const rooms = [...socket.rooms];

    rooms.forEach((boardId) => {
      // 음성 채널 정리
      if (voiceUsersMap[boardId] && voiceUsersMap[boardId][socket.id]) {
        delete voiceUsersMap[boardId][socket.id];
        if (Object.keys(voiceUsersMap[boardId]).length === 0) {
          delete voiceUsersMap[boardId];
        }
        socket.in(boardId).emit("user-left-voice", { socketId: socket.id });
      }

      // 화이트보드 접속자 알림 및 정리
      if (userInfo) {
        socket.in(boardId).emit("disconnected", {
          socketId: socket.id,
          userName: userInfo.userName,
        });
      }
    });

    // 메모리 정리
    if (userInfo && boardUsersMap[userInfo.boardId]) {
      boardUsersMap[userInfo.boardId].delete(userInfo.userName);
      if (boardUsersMap[userInfo.boardId].size === 0) {
        delete boardUsersMap[userInfo.boardId];
      }
    }
    delete socketUserMap[socket.id];

    socket.leave();
  });
});

// React Client Fallback Route
app.get("*", (req, res) => {
  res.sendFile(path.join(clientBuildPath, "index.html"));
});

// 로컬 IPv4 주소 자동 탐색
function getLocalExternalIP() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const net of interfaces[name]) {
      if (net.family === 'IPv4' && !net.internal) {
        return net.address;
      }
    }
  }
  return 'localhost';
}

httpServer.listen(PORT, '0.0.0.0', () => {
  const localIP = getLocalExternalIP();
  
  console.log('\n========================================================');
  console.log('🚀 화이트보드 서버가 정상적으로 시작되었습니다!');
  console.log('========================================================');
  console.log(`🏠 내 PC 접속 주소   : http://localhost:${PORT}`);
  console.log(`🌐 다른 사람 접속 주소: http://${localIP}:${PORT}`);
  console.log('========================================================\n');
});