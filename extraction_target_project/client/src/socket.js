import { io } from "socket.io-client";

const DEBUG = process.env.NODE_ENV !== "production";

export const initSocket = async () => {
  const options = {
    forceNew: true,
    reconnectionAttempts: Infinity,
    reconnectionDelay: 1000,
    timeout: 20000,
    transports: ["websocket", "polling"],
  };

  // [수정점] 현재 브라우저의 Host IP를 가져오되, 소켓 서버 포트(7605)로 정확히 타겟팅
  const hostname = typeof window !== "undefined" ? window.location.hostname : "localhost";
  const serverUrl = process.env.REACT_APP_SOCKET_URL || `http://${hostname}:7605`;

  if (DEBUG) {
    console.log(`[socket.js] initSocket() -> Connecting Socket Server: ${serverUrl}`);
  }

  try {
    return io(serverUrl, options);
  } catch (error) {
    if (DEBUG) {
      console.error(`[socket.js] initSocket() -> Connection Error:`, error);
    }
    throw error;
  }
};