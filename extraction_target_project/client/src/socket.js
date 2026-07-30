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

  // 브라우저 환경인 경우 접속된 프로토콜과 Origin(도메인+프로토콜)을 그대로 활용
  const isHttps = typeof window !== "undefined" && window.location.protocol === "https:";
  
  // REACT_APP_SOCKET_URL이 없을 경우:
  // HTTPS(터널) 환경에서는 현재 origin(https://domain.com)을 그대로 사용 (포트 7605 붙이지 않음)
  // HTTP(로컬) 환경에서는 기존처럼 http://localhost:7605 사용
  const serverUrl = process.env.REACT_APP_SOCKET_URL || 
    (isHttps ? window.location.origin : `http://${typeof window !== "undefined" ? window.location.hostname : "localhost"}:7605`);

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