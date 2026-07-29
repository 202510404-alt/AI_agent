import { io } from "socket.io-client";

const DEBUG = process.env.NODE_ENV !== "production";

export const initSocket = async () => {
  const options = {
    "force new connection": true,
    reconnectionAttempts: Infinity,
    reconnectionDelay: 1000,
    timeout: 20000,
    transports: ["websocket", "polling"], // 연결 안전성을 위한 폴백 허용
  };

  // 접속한 클라이언트 브라우저의 현재 Host IP/도메인을 우선 추적하여 자동 연결
  const serverUrl =
    process.env.REACT_APP_SOCKET_URL ||
    (typeof window !== "undefined" && window.location.origin
      ? window.location.origin
      : "http://localhost:7605");

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