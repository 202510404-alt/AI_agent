import React, { useRef, useEffect, useState } from "react";
import UploadFile from './UploadFile';
import './style.css';
import './styleCanvas.css';
import { initSocket } from "./socket";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import toast from "react-hot-toast";
import Button from "./Button";
import { AiOutlineClear } from "react-icons/ai";
import { FaImage, FaRegSquareMinus } from "react-icons/fa6";
import {
  FaRegPlusSquare,
  FaMicrophone,
  FaMicrophoneSlash,
  FaUndoAlt,
  FaPhone,
  FaPhoneSlash,
  FaCopy,
  FaSignOutAlt,
  FaUserFriends
} from "react-icons/fa";
import { useWebRTC } from "./hooks/useWebRTC";

function RemoteAudio({ stream }) {
  const audioRef = useRef(null);

  useEffect(() => {
    const audioEl = audioRef.current;
    if (audioEl && stream) {
      audioEl.srcObject = stream;
      
      const playAudio = async () => {
        try {
          await audioEl.play();
        } catch (err) {
          console.warn("[RemoteAudio] 자동 재생 차단됨. 유저 클릭 시 재생을 대기합니다.", err);
          // 브라우저 차단 시, 사용자가 화면을 클릭할 때 소리가 즉시 재생되도록 리스너 등록
          const handleUserInteraction = () => {
            audioEl.play().then(() => {
              window.removeEventListener("click", handleUserInteraction);
              window.removeEventListener("keydown", handleUserInteraction);
            }).catch(e => console.error(e));
          };
          window.addEventListener("click", handleUserInteraction);
          window.addEventListener("keydown", handleUserInteraction);
        }
      };

      playAudio();
    }
  }, [stream]);

  return <audio ref={audioRef} autoPlay playsInline controls={false} />;
}

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

  function changeColour(e) {
    const newColor = e.target ? e.target.value : e;
    setShapeColor(newColor);
    console.log(`[DEBUG_LOG] Step=COLOR_CHANGE | SelectedColor='${newColor}'`);
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
    }
  };

  useEffect(() => {
    const init = async () => {
      if (!location.state?.userName) {
        toast.error("사용자 이름이 필요합니다.");
        navigate("/");
        return;
      }

      socketRef.current = await initSocket();
      socketRef.current.on('connect_error', (err) => handleError(err));
      socketRef.current.on('connect_failed', (err) => handleError(err));

      const handleError = (err) => {
        console.log('socket error', err);
        toast.error("소켓 연결에 실패했습니다");
        navigate("/");
      };

      socketRef.current.emit('join', {
        boardId,
        userName: location.state.userName,
      });

      socketRef.current.on('joined', ({ clients, userName, socketId }) => {
        if (userName !== location.state.userName) {
          toast.success(`${userName}님이 참가했습니다`);
        }
        setClients(clients);
      });

      socketRef.current.on("disconnected", ({ socketId, userName }) => {
        toast.success(`${userName}님이 보드를 나갔습니다`);
        setClients((prev) => prev.filter((client) => client.socketId !== socketId));
      });

      socketRef.current.on("board_change", ({ code }) => {
        if (code !== null) {
          if (canvasRef.current) {
            const context = canvasRef.current.getContext('2d');
            const image = new Image();
            image.src = code;
            image.onload = () => context.drawImage(image, 0, 0);
          }
        }
      });

      socketRef.current.on("image_update", ({ imageUrl }) => {
        setImageDraw(imageUrl);
      });
    };

    init();

    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
        socketRef.current.off("joined");
        socketRef.current.off("disconnected");
      }
    };
  }, [boardId, location.state, navigate]);

  useEffect(() => {
    const imageContext = canvasRef.current?.getContext('2d');
    if (imageContext && imageDraw) {
      const image = new Image();
      image.src = imageDraw;
      image.onload = () => {
        imageContext.drawImage(image, 90, 90, 650, 500);
      };
    }
  }, [imageDraw]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const context = canvas.getContext('2d');
      redrawCanvas(context);
    }
  }, []);

  const handleDraw = (e) => {
    try {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const context = canvas.getContext('2d');
      if (!context) return;
      const rect = canvas.getBoundingClientRect();
      setDrawing(true);
      const startPoint = { x: e.clientX - rect.left, y: e.clientY - rect.top, color: shapeColor, size: width };
      setCurrentLine([startPoint]);
      context.beginPath();
      context.moveTo(startPoint.x, startPoint.y);
      canvas.dispatchEvent(new CustomEvent('canvasChange'));
    } catch (err) {
      console.error("[Canvas.js] handleDraw() -> Exception Caught:", err);
    }
  };

  const handleMoveDraw = (e) => {
    if (!drawing) return;
    try {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const context = canvas.getContext('2d');
      if (!context) return;
      const rect = canvas.getBoundingClientRect();
      const newPoint = { x: e.clientX - rect.left, y: e.clientY - rect.top, color: shapeColor, size: width };
      setCurrentLine((prev) => [...prev, newPoint]);

      context.lineTo(newPoint.x, newPoint.y);
      context.strokeStyle = shapeColor;
      context.lineWidth = width;
      context.stroke();
      canvas.dispatchEvent(new CustomEvent('canvasChange'));
    } catch (err) {
      console.error("[Canvas.js] handleMoveDraw() -> Exception Caught:", err);
    }
  };

  const handleNotDraw = () => {
    try {
      const canvas = canvasRef.current;
      if (!canvas) return;
      setDrawing(false);
      if (currentLine.length > 0) {
        setLinesHistory((prev) => [...prev, currentLine]);
        setCurrentLine([]);
      }
      canvas.dispatchEvent(new CustomEvent('canvasChange'));
    } catch (err) {
      console.error("[Canvas.js] handleNotDraw() -> Exception Caught:", err);
    }
  };

  const undo = () => {
    try {
      if (linesHistory.length > 0) {
        const newHistory = linesHistory.slice(0, -1);
        setLinesHistory(newHistory);
        if (canvasRef.current) {
          const context = canvasRef.current.getContext('2d');
          if (context) redrawCanvas(context, newHistory);
        }
      }
    } catch (err) {
      console.error("[Canvas.js] undo() -> Exception Caught:", err);
    }
  };

  const redrawCanvas = (context, history = linesHistory) => {
    if (!canvasRef.current || !context) return;
    try {
      context.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      history.forEach((line) => {
        if (!line || line.length === 0) return;
        context.beginPath();
        line.forEach((point, index) => {
          if (!point) return;
          if (index === 0) {
            context.moveTo(point.x, point.y);
          } else {
            context.lineTo(point.x, point.y);
          }
        });
        context.strokeStyle = line[0]?.color || "#000000";
        context.lineWidth = line[0]?.size || 1;
        context.stroke();
      });
    } catch (err) {
      console.error("[Canvas.js] redrawCanvas() -> Exception Caught:", err);
    }
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const handleCanvasChange = () => {
      const code = canvas.toDataURL();
      if (socketRef.current) {
        socketRef.current.emit('board_change', { boardId, code });
      }
    };

    canvas.addEventListener('canvasChange', handleCanvasChange);

    return () => {
      canvas.removeEventListener('canvasChange', handleCanvasChange);
    };
  }, [boardId]);

  function clearCanvas() {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
    setLinesHistory([]);
    canvas.dispatchEvent(new CustomEvent('canvasChange'));
  }

  const copyBoardId = () => {
    navigator.clipboard.writeText(boardId);
    toast.success("보드 ID가 클립보드에 복사되었습니다!");
  };

  const leaveBoard = () => {
    navigate("/");
  };

  return (
    <div className="canvasPage">
      {/* Remote Audio Players */}
      {Object.entries(remoteStreams).map(([sid, stream]) => (
        <RemoteAudio key={sid} stream={stream} />
      ))}

      {/* Top Header Bar */}
      <header className="canvas-header">
        <div className="header-left">
          <div className="brand-logo">Collaborative Canvas</div>
          <div className="room-info">
            <span className="room-label">Room:</span>
            <span className="room-id">{boardId}</span>
            <button className="icon-btn copy-btn" title="보드 ID 복사" onClick={copyBoardId}>
              <FaCopy size="14" />
            </button>
          </div>
        </div>

        <div className="header-right">
          <div className="client-badges">
            <span className="badge-item">
              <FaUserFriends size="14" /> {clients.length}명 접속 중
            </span>
          </div>
          <button className="button leave-btn" onClick={leaveBoard}>
            <FaSignOutAlt size="16" style={{ marginRight: "6px" }} /> 나가기
          </button>
        </div>
      </header>

      {/* Main Canvas Area */}
      <main className="canvas-viewport">
        <canvas
          ref={canvasRef}
          className="canvas"
          height={props.height || 800}
          width={props.width || 1400}
          onMouseDown={handleDraw}
          onMouseMove={handleMoveDraw}
          onMouseUp={handleNotDraw}
        />
      </main>

      {/* Left Floating Toolbar */}
      <aside className="floating-toolbar left-toolbar">
        <div className="toolbar-section">
          <UploadFile imageSource={handleImageUploadSuccess} id="uploadedImage" />
        </div>
        <div className="toolbar-divider" />
        <div className="toolbar-section colors-grid">
          <input
            type="color"
            id="colorPicker"
            value={shapeColor}
            onChange={changeColour}
            style={{ width: '40px', height: '40px', border: 'none', cursor: 'pointer', padding: 0, background: 'none' }}
          />
        </div>
        <div className="toolbar-divider" />
        <div className="toolbar-section stroke-controls">
          <button
            className="tool-btn"
            value={width}
            name="decrease"
            onClick={lineWidth}
            title="선 굵기 감소"
          >
            <FaRegSquareMinus size="18" />
          </button>
          <span className="width-indicator">{width}px</span>
          <button
            className="tool-btn"
            value={width}
            name="increase"
            onClick={lineWidth}
            title="선 굵기 증가"
          >
            <FaRegPlusSquare size="18" />
          </button>
        </div>
        <div className="toolbar-divider" />
        <div className="toolbar-section actions-group">
          <button className="tool-btn" onClick={undo} title="되돌리기 (Undo)">
            <FaUndoAlt size="18" />
          </button>
          <button className="tool-btn danger-btn" onClick={clearCanvas} title="전체 지우기">
            <AiOutlineClear size="20" />
          </button>
        </div>
      </aside>

      {/* Right Floating Voice Panel */}
      <aside className="floating-panel right-voice-panel">
        <div className="voice-header">
          <h3>음성 채널 (WebRTC)</h3>
          <span className={`status-dot ${isVoiceConnected ? "connected" : "disconnected"}`} />
        </div>

        <div className="voice-controls">
          {!isVoiceConnected ? (
            <button className="voice-action-btn join-voice-btn" onClick={joinVoice}>
              <FaPhone size="14" /> 음성 연결
            </button>
          ) : (
            <div className="voice-btn-group">
              <button
                className={`voice-action-btn mute-btn ${isMuted ? "muted" : ""}`}
                onClick={toggleMute}
              >
                {isMuted ? (
                  <>
                    <FaMicrophoneSlash size="14" /> 음소거 해제
                  </>
                ) : (
                  <>
                    <FaMicrophone size="14" /> 음소거
                  </>
                )}
              </button>
              <button className="voice-action-btn leave-voice-btn" onClick={leaveVoice}>
                <FaPhoneSlash size="14" /> 끊기
              </button>
            </div>
          )}
        </div>

        <div className="voice-members">
          <h4>참가자 목록 ({clients.length})</h4>
          <ul className="member-list">
            {clients.map((client) => {
              const voiceUser = voiceUsers.find((v) => v.socketId === client.socketId);
              const isInVoice = !!voiceUser;
              const isUserMuted = voiceUser?.isMuted;
              const isSelf = client.userName === location.state?.userName;

              return (
                <li key={client.socketId} className={`member-item ${isInVoice ? "in-voice" : ""}`}>
                  <div className="member-avatar">
                    {client.userName.charAt(0).toUpperCase()}
                  </div>
                  <div className="member-info">
                    <span className="member-name">
                      {client.userName} {isSelf && "(나)"}
                    </span>
                    <span className="member-status">
                      {isInVoice ? (isUserMuted ? "음소거 상태" : "음성 참가 중") : "대기 중"}
                    </span>
                  </div>
                  {isInVoice && (
                    <div className="member-voice-icon">
                      {isUserMuted ? (
                        <FaMicrophoneSlash size="14" className="icon-muted" />
                      ) : (
                        <FaMicrophone size="14" className="icon-active" />
                      )}
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      </aside>
    </div>
  );
}

export default Canvas;
