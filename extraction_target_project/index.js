const DEBUG = process.env.NODE_ENV !== "production";

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
const io = new Server(httpServer);
const userSocketMap = {};
const boardUsersMap = {};
const voiceUsersMap = {};

app.use(express.static(clientBuildPath));

function getAllConnectedClients(boardId) {
  const usernames = boardUsersMap[boardId] || [];
  return usernames.map(userName => ({
    socketId: userSocketMap[userName],
    userName,
  }));
}

io.on("connection", (socket) => {
  if (DEBUG) {
    console.log(`[index.js] connection() -> Socket Connected: ${socket.id}`);
  }

  socket.on("join", ({ boardId, userName }) => {
    if (boardUsersMap[boardId]?.includes(userName)) {
      return;
    }

    userSocketMap[userName] = socket.id;
    boardUsersMap[boardId] = boardUsersMap[boardId] || [];
    boardUsersMap[boardId].push(userName);

    if (DEBUG) {
      console.log(`[index.js] join() -> User Joined Board: (userName: ${userName}, socketId: ${socket.id}, boardId: ${boardId})`);
    }
    socket.join(boardId);

    const clients = getAllConnectedClients(boardId);

    clients.forEach(({ socketId }) => {
      io.to(socketId).emit("joined", {
        clients,
        userName,
        socketId: socket.id,
      });
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

    // Send existing voice users list to the joining user
    const voiceUsersList = Object.keys(voiceUsersMap[boardId]).map((sid) => ({
      socketId: sid,
      userName: voiceUsersMap[boardId][sid].userName,
      isMuted: voiceUsersMap[boardId][sid].isMuted,
    }));
    socket.emit("voice-users", voiceUsersList);

    // Notify other users in the board about the new voice user
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
    const rooms = [...socket.rooms];
    rooms.forEach((boardId) => {
      if (voiceUsersMap[boardId] && voiceUsersMap[boardId][socket.id]) {
        delete voiceUsersMap[boardId][socket.id];
        if (Object.keys(voiceUsersMap[boardId]).length === 0) {
          delete voiceUsersMap[boardId];
        }
        socket.in(boardId).emit("user-left-voice", { socketId: socket.id });
      }

      const userName = boardUsersMap[boardId]?.find(
        (name) => userSocketMap[name] === socket.id
      );

      if (userName) {
        socket.in(boardId).emit("disconnected", {
          socketId: socket.id,
          userName,
        });
        boardUsersMap[boardId] = boardUsersMap[boardId]?.filter(
          (name) => name !== userName
        );
        delete userSocketMap[userName];
      }
    });

    socket.leave();
  });
});

app.get("*", (req, res) => {
  res.sendFile(path.join(clientBuildPath, "index.html"));
});

httpServer.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});