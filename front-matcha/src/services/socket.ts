import { io } from "socket.io-client";

const SOCKET_URL =
  import.meta.env.VITE_SOCKET_URL ?? "http://localhost:5000";

export const socket = io(SOCKET_URL, {
  autoConnect: false,
  transports: ["polling"],
  upgrade: false,
  reconnection: true,
  reconnectionAttempts: 10,
  reconnectionDelay: 1000,
  timeout: 10000,
  auth: (callback) => {
    callback({ token: localStorage.getItem("token") });
  },
});

socket.on("connect", () => {
  console.log("[SOCKET] Connected :", socket.id);
  console.log("[SOCKET] Transport :", socket.io.engine.transport.name);
});

socket.on("connect_error", (error) => {
  console.error("[SOCKET] Erreur :", error.message);
});