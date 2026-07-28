# ==========================================================================
# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드
# [SCAN_MODE] EXTRACTION_TARGET_PROJECT
# ==========================================================================
# 📄 [요청 1] TARGET: client/package.json (1-15라인)
# ----------------------------------------------------------
```python
{
  "name": "whiteboard",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "fabric": "^5.3.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-hot-toast": "^2.4.1",
    "react-icons": "^5.2.0",
    "react-router-dom": "^6.23.0",
    "react-scripts": "^5.0.1",
```

# 📄 [요청 2] TARGET: client/src/App.js (10-20라인)
# ----------------------------------------------------------
```python

function App() {
  
  // const [color,setColor] = useState("#000000");
   
  const [height,setHeight] = useState(700);
  const [width,setWidth] = useState(1200);
  
//  window.onscroll = function (event) {
     
//   if(window.scrollY > 0)
```

# 📄 [요청 3] TARGET: client/src/Canvas.js (34-80라인)
# ----------------------------------------------------------
```python
function Canvas(props) {
  const [clients, setClients] = useState([]);
  const socketRef = useRef(null);
  const location = useLocation();
  const { boardId } = useParams();
  const navigate = useNavigate();

  const [width, setWidth] = useState(1.0);
  const [drawing, setDrawing] = useState(false);
  const canvasRef = useRef(null);
  const [imageDraw, setImageDraw] = useState(null);
  const [shapeColor, setShapeColor] = useState("#000000");
  const [linesHistory, setLinesHistory] = useState([]);
  const [currentLine, setCurrentLine] = useState([]);

  // WebRTC Hook Integration
  const userName = location.state?.userName || "익명 유저";
  const {
    remoteStreams,
    voiceUsers,
    isVoiceConnected,
    isMuted,
    joinVoice,
    leaveVoice,
    toggleMute,
  } = useWebRTC(socketRef, boardId, userName);

  function changeColour(event) {
    let color = event.target.value;
    setShapeColor(color);
  }

  function lineWidth(event) {
    let name = event.target.name;
    if (name === 'increase')
      setWidth((prev) => (prev < 10 ? prev + 1 : prev));
    else if (name === 'decrease')
      setWidth((prev) => (prev > 1 ? prev - 1 : prev));
  }

  const handleImageUploadSuccess = (imageUrl) => {
    setImageDraw(imageUrl);
    if (socketRef.current) {
      socketRef.current.emit("image_update", {
        boardId,
        imageUrl,
      });
```

# 📄 [요청 4] TARGET: client/src/Home.js (30-40라인)
# ----------------------------------------------------------
```python

    function joinBoard(){
       if(!uniqueId || !userName){
        toast.error("모든 항목을 입력해 주세요");
        return;
       }
       
       navigate(`/whiteboard/${uniqueId}`, {state: {userName: userName}});
       toast.success("보드에 참가했습니다!")
    }
```

# 📄 [요청 5] TARGET: client/src/hooks/useWebRTC.js (10-30라인)
# ----------------------------------------------------------
```python

export function useWebRTC(socketRef, boardId, userName) {
  const [localStream, setLocalStream] = useState(null);
  const [remoteStreams, setRemoteStreams] = useState({}); // { [socketId]: MediaStream }
  const [voiceUsers, setVoiceUsers] = useState([]); // [{ socketId, userName, isMuted }]
  const [isVoiceConnected, setIsVoiceConnected] = useState(false);
  const [isMuted, setIsMuted] = useState(false);

  const peerConnections = useRef(new Map()); // Map<socketId, RTCPeerConnection>
  const localStreamRef = useRef(null);
  const isMutedRef = useRef(false);

  // Helper to create RTCPeerConnection for a remote peer
  const createPeerConnection = useCallback((targetSocketId) => {
    if (peerConnections.current.has(targetSocketId)) {
      return peerConnections.current.get(targetSocketId);
    }

    const pc = new RTCPeerConnection(ICE_SERVERS);
    peerConnections.current.set(targetSocketId, pc);
```

# 📄 [요청 6] TARGET: index.js (20-28라인)
# ----------------------------------------------------------
```python
app.use(express.static(clientBuildPath));

function getAllConnectedClients(boardId) {
  const usernames = boardUsersMap[boardId] || [];
  return usernames.map(userName => ({
    socketId: userSocketMap[userName],
    userName,
  }));
}
```

# 📄 [요청 7] TARGET: just_test_tools/Main.java (1-10라인)
# ----------------------------------------------------------
```python
import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class Main extends JPanel {
    private TetrisModel gameModel;
    private static final int CELL_SIZE = 30;

    public Main() {
```

# 📄 [요청 8] TARGET: just_test_tools/tetris_logic.py (1-15라인)
# ----------------------------------------------------------
```python
import random

class Tetromino:
    """테트리스 블록 데이터 및 회전 로직 관리"""
    SHAPES = [
        [[1, 1, 1, 1]],                  # I
        [[1, 1], [1, 1]],                # O
        [[0, 1, 0], [1, 1, 1]],          # T
        [[1, 0, 0], [1, 1, 1]],          # L
        [[0, 0, 1], [1, 1, 1]],          # J
        [[0, 1, 1], [1, 0, 0]],          # S
        [[1, 1, 0], [0, 1, 1]]           # Z
    ]

    def __init__(self, x: int = 3, y: int = 0):
```
