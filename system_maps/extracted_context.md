# ==========================================================================
# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드
# [SCAN_MODE] EXTRACTION_TARGET_PROJECT
# ==========================================================================
# 📄 [요청 1] TARGET: client/src/App.js (11-20라인)
# ----------------------------------------------------------
```python
function App() {
  
  // const [color,setColor] = useState("#000000");
   
  const [height,setHeight] = useState(700);
  const [width,setWidth] = useState(1200);
  
//  window.onscroll = function (event) {
     
//   if(window.scrollY > 0)
```

# 📄 [요청 2] TARGET: client/src/socket.js (3-19라인)
# ----------------------------------------------------------
```python
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
