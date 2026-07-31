# ==========================================================================
# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드
# [SCAN_MODE] EXTRACTION_TARGET_PROJECT
# ==========================================================================
# 📄 [요청 1] TARGET: extraction_target_project/index.js (160-194라인)
# ----------------------------------------------------------
```python
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

app.get("*", (req, res) => {
  res.sendFile(path.join(clientBuildPath, "index.html"));
});

httpServer.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
```
