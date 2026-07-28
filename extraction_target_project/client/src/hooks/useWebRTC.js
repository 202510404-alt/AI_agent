import { useState, useRef, useCallback, useEffect } from "react";
import toast from "react-hot-toast";

const ICE_SERVERS = {
  iceServers: [
    { urls: "stun:stun.l.google.com:19302" },
    { urls: "stun:stun1.l.google.com:19302" },
  ],
};

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
        const stream = event.streams[0];
        setRemoteStreams((prev) => ({
          ...prev,
          [targetSocketId]: stream,
        }));
      }
    };

    pc.onconnectionstatechange = () => {
      if (
        pc.connectionState === "disconnected" ||
        pc.connectionState === "failed" ||
        pc.connectionState === "closed"
      ) {
        // Handle disconnect if needed
      }
    };

    return pc;
  }, [socketRef]);

  // Clean up a specific peer connection
  const closePeerConnection = useCallback((targetSocketId) => {
    const pc = peerConnections.current.get(targetSocketId);
    if (pc) {
      pc.onicecandidate = null;
      pc.ontrack = null;
      pc.close();
      peerConnections.current.delete(targetSocketId);
    }
    setRemoteStreams((prev) => {
      const next = { ...prev };
      delete next[targetSocketId];
      return next;
    });
  }, []);

  // Leave Voice Call & Cleanup
  const leaveVoice = useCallback(() => {
    if (socketRef.current && isVoiceConnected) {
      socketRef.current.emit("leave-voice", { boardId });
    }

    // Stop local stream tracks
    if (localStreamRef.current) {
      localStreamRef.current.getTracks().forEach((track) => track.stop());
      localStreamRef.current = null;
    }
    setLocalStream(null);

    // Close all PeerConnections
    peerConnections.current.forEach((pc, sid) => {
      pc.onicecandidate = null;
      pc.ontrack = null;
      pc.close();
    });
    peerConnections.current.clear();

    setRemoteStreams({});
    setVoiceUsers([]);
    setIsVoiceConnected(false);
    setIsMuted(false);
    isMutedRef.current = false;

    // Remove socket listeners
    if (socketRef.current) {
      socketRef.current.off("voice-users");
      socketRef.current.off("user-joined-voice");
      socketRef.current.off("offer");
      socketRef.current.off("answer");
      socketRef.current.off("ice-candidate");
      socketRef.current.off("user-left-voice");
      socketRef.current.off("user-mute-changed");
    }
  }, [socketRef, boardId, isVoiceConnected]);

  // Join Voice Call
  const joinVoice = useCallback(async () => {
    if (!socketRef.current) {
      toast.error("소켓 연결이 완료되지 않았습니다.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
        video: false,
      });
      localStreamRef.current = stream;
      setLocalStream(stream);
      setIsVoiceConnected(true);
      toast.success("음성 채널에 연결되었습니다.");

      const socket = socketRef.current;

      // Socket Listeners for Signaling
      socket.on("voice-users", async (users) => {
        setVoiceUsers(users);

        // Initiate connection to existing users
        for (const user of users) {
          if (user.socketId !== socket.id) {
            const pc = createPeerConnection(user.socketId);
            try {
              const offer = await pc.createOffer();
              await pc.setLocalDescription(offer);
              socket.emit("offer", {
                targetSocketId: user.socketId,
                offer,
              });
            } catch (err) {
              console.error("Error creating offer:", err);
            }
          }
        }
      });

      socket.on("user-joined-voice", ({ socketId, userName: remoteName, isMuted: remoteMuted }) => {
        toast.info(`${remoteName}님이 음성 채널에 입장하셨습니다.`);
        setVoiceUsers((prev) => [
          ...prev.filter((u) => u.socketId !== socketId),
          { socketId, userName: remoteName, isMuted: remoteMuted },
        ]);
      });

      socket.on("offer", async ({ callerSocketId, offer }) => {
        const pc = createPeerConnection(callerSocketId);
        try {
          await pc.setRemoteDescription(new RTCSessionDescription(offer));
          const answer = await pc.createAnswer();
          await pc.setLocalDescription(answer);
          socket.emit("answer", {
            targetSocketId: callerSocketId,
            answer,
          });
        } catch (err) {
          console.error("Error handling offer:", err);
        }
      });

      socket.on("answer", async ({ responderSocketId, answer }) => {
        const pc = peerConnections.current.get(responderSocketId);
        if (pc) {
          try {
            await pc.setRemoteDescription(new RTCSessionDescription(answer));
          } catch (err) {
            console.error("Error setting remote description from answer:", err);
          }
        }
      });

      socket.on("ice-candidate", async ({ senderSocketId, candidate }) => {
        const pc = peerConnections.current.get(senderSocketId);
        if (pc) {
          try {
            await pc.addIceCandidate(new RTCIceCandidate(candidate));
          } catch (err) {
            console.error("Error adding ice candidate:", err);
          }
        }
      });

      socket.on("user-left-voice", ({ socketId }) => {
        closePeerConnection(socketId);
        setVoiceUsers((prev) => prev.filter((u) => u.socketId !== socketId));
      });

      socket.on("user-mute-changed", ({ socketId, isMuted: remoteMuted }) => {
        setVoiceUsers((prev) =>
          prev.map((u) => (u.socketId === socketId ? { ...u, isMuted: remoteMuted } : u))
        );
      });

      // Join voice channel on server
      socket.emit("join-voice", { boardId, userName });

    } catch (err) {
      console.error("Mic permission error:", err);
      toast.error("마이크 접근 권한이 없거나 마이크를 찾을 수 없습니다.");
      leaveVoice();
    }
  }, [socketRef, boardId, userName, createPeerConnection, closePeerConnection, leaveVoice]);

  // Toggle Mute
  const toggleMute = useCallback(() => {
    if (!localStreamRef.current) return;
    const audioTracks = localStreamRef.current.getAudioTracks();
    const newMutedState = !isMuted;

    audioTracks.forEach((track) => {
      track.enabled = !newMutedState;
    });

    setIsMuted(newMutedState);
    isMutedRef.current = newMutedState;

    if (socketRef.current) {
      socketRef.current.emit("mute-changed", {
        boardId,
        isMuted: newMutedState,
      });
    }

    if (newMutedState) {
      toast.success("음소거 처리되었습니다.");
    } else {
      toast.success("음소거가 해제되었습니다.");
    }
  }, [socketRef, boardId, isMuted]);

  // Cleanup on component unmount
  useEffect(() => {
    return () => {
      leaveVoice();
    };
  }, [leaveVoice]);

  return {
    localStream,
    remoteStreams,
    voiceUsers,
    isVoiceConnected,
    isMuted,
    joinVoice,
    leaveVoice,
    toggleMute,
  };
}
