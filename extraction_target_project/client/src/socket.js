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
