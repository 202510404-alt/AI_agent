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

# 📄 [요청 2] TARGET: client/src/Canvas.js (24-32라인)
# ----------------------------------------------------------
```python
function RemoteAudio({ stream }) {
  const audioRef = useRef(null);
  useEffect(() => {
    if (audioRef.current && stream) {
      audioRef.current.srcObject = stream;
    }
  }, [stream]);
  return <audio ref={audioRef} autoPlay playsInline />;
}
```

# 📄 [요청 3] TARGET: client/src/Canvas.js (61-72라인)
# ----------------------------------------------------------
```python
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
```

# 📄 [요청 4] TARGET: client/src/Home.js (14-39라인)
# ----------------------------------------------------------
```python
   function writeId(event){
    let newId = event.target.value
    setUniqueId(newId);

  }

  function writeUserName(event){
      setUserName(event.target.value);
  }

   function generateUniqueId(event){
     event.preventDefault();
     let id = uuidv4();
     toast.success('새 보드 ID가 생성되었습니다!');
     setUniqueId(id);
    }

    function joinBoard(){
       if(!uniqueId || !userName){
        toast.error("모든 항목을 입력해 주세요");
        return;
       }
       
       navigate(`/whiteboard/${uniqueId}`, {state: {userName: userName}});
       toast.success("보드에 참가했습니다!")
    }
```

# 📄 [요청 5] TARGET: client/src/hooks/useWebRTC.js (11-50라인)
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

    // Add local tracks to peer connection
    if (localStreamRef.current) {
      localStreamRef.current.getTracks().forEach((track) => {
        pc.addTrack(track, localStreamRef.current);
      });
    }

    // Handle incoming ICE candidate
    pc.onicecandidate = (event) => {
      if (event.candidate && socketRef.current) {
        socketRef.current.emit("ice-candidate", {
          targetSocketId,
          candidate: event.candidate,
        });
      }
    };

    // Handle incoming remote stream
    pc.ontrack = (event) => {
      if (event.streams && event.streams[0]) {
```

# 📄 [요청 6] TARGET: index.js (22-28라인)
# ----------------------------------------------------------
```python
function getAllConnectedClients(boardId) {
  const usernames = boardUsersMap[boardId] || [];
  return usernames.map(userName => ({
    socketId: userSocketMap[userName],
    userName,
  }));
}
```

# 📄 [요청 7] TARGET: just_test_tools/main.py (4-22라인)
# ----------------------------------------------------------
```python
def render(board: Board, piece: Tetromino) -> None:
    """보드와 현재 떨어지는 블록을 터미널에 시각화하는 함수"""
    # 임시 보드 복사
    temp_grid = [row[:] for row in board.grid]
    
    # 현재 움직이는 블록 그리기
    for r_idx, row in enumerate(piece.shape):
        for c_idx, val in enumerate(row):
            if val:
                py, px = piece.y + r_idx, piece.x + c_idx
                if 0 <= py < board.height and 0 <= px < board.width:
                    temp_grid[py][px] = 2

    print("\033[H\033[J", end="")  # 화면 갱신 (터미널 클리어)
    print("=" * (board.width * 2 + 2))
    for row in temp_grid:
        line = "|" + "".join("■ " if cell else "  " for cell in row) + "|"
        print(line)
    print("=" * (board.width * 2 + 2))
```

# 📄 [요청 8] TARGET: just_test_tools/tetris_logic.py (15-46라인)
# ----------------------------------------------------------
```python
    def __init__(self, x: int = 3, y: int = 0):
        self.x = x
        self.y = y
        self.shape = random.choice(self.SHAPES)

    def rotate(self) -> None:
        """블록을 시계 방향으로 90도 회전"""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


class Board:
    """테트리스 판 및 이동/충돌 감지 로직"""
    def __init__(self, width: int = 10, height: int = 20):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)]

    def is_valid_position(self, piece: Tetromino, offset_x: int = 0, offset_y: int = 0) -> bool:
        """해당の位置로 이동이 가능한지 확인 (인자: piece 객체, 오프셋 값)"""
        for r_idx, row in enumerate(piece.shape):
            for c_idx, val in enumerate(row):
                if val:
                    new_x = piece.x + c_idx + offset_x
                    new_y = piece.y + r_idx + offset_y
                    
                    # 경계선 체크
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False
                    # 기존에 쌓인 블록과 충돌 체크
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True
```

# 📄 [요청 9] TARGET: just_test_tools/Main.java (10-35라인)
# ----------------------------------------------------------
```python
    public Main() {
        gameModel = new TetrisModel();  // TetrisModel 클래스 호출
        setFocusable(true);

        // 키보드 조작 이벤트 핸들러
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                switch (e.getKeyCode()) {
                    case KeyEvent.VK_LEFT -> gameModel.move(-1, 0);
                    case KeyEvent.VK_RIGHT -> gameModel.move(1, 0);
                    case KeyEvent.VK_DOWN -> gameModel.move(0, 1);
                }
                repaint();
            }
        });

        // 게임 루프 타이머 (400ms마다 아래로 한 칸씩)
        Timer timer = new Timer(400, e -> {
            if (!gameModel.move(0, 1)) {
                gameModel.lockPiece();
            }
            repaint();
        });
        timer.start();
    }
```

# 📄 [요청 10] TARGET: just_test_tools/TetrisModel.java (30-56라인)
# ----------------------------------------------------------
```python
    public boolean move(int dx, int dy) {
        if (canMove(currentShape, currentX + dx, currentY + dy)) {
            currentX += dx;
            currentY += dy;
            return true;
        }
        return false;
    }

    public boolean canMove(int[][] shape, int newX, int newY) {
        for (int r = 0; r < shape.length; r++) {
            for (int c = 0; c < shape[r].length; c++) {
                if (shape[r][c] != 0) {
                    int targetX = newX + c;
                    int targetY = newY + r;

                    if (targetX < 0 || targetX >= WIDTH || targetY >= HEIGHT) {
                        return false;
                    }
                    if (targetY >= 0 && grid[targetY][targetX] != 0) {
                        return false;
                    }
                }
            }
        }
        return true;
    }
```
