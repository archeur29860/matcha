import { io } from "socket.io-client";

const SOCKET_URL =
  import.meta.env.VITE_SOCKET_URL ?? "http://localhost:5000";

export const socket = io(SOCKET_URL, {
  autoConnect: false,
  reconnection: true,
  reconnectionAttempts: 10,
  reconnectionDelay: 1000,
  timeout: 10000,
  auth: (callback) => {
    const token = localStorage.getItem("token");
    callback({ token });
  }
});

// to remove after test
socket.on("connect", () => {
  console.log("[SOCKET] Connecté :", socket.id);
});

socket.on("disconnect", (reason) => {
  console.log("[SOCKET] Déconnecté :", reason);
});

socket.on("connect_error", (error) => {
  console.error("[SOCKET] Erreur :", error.message);
});