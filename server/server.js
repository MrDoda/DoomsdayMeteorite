const WebSocket = require("ws");

const wss = new WebSocket.Server({ port: 6789 });

const clients = new Map();
let clientIdCounter = 0;

wss.on("connection", function connection(ws) {
  const clientId = clientIdCounter++; // Assign an ID and increment the counter
  clients.set(clientId, ws);
  console.log(`Client connected: ${clientId}`);

  ws.on("message", function incoming(message) {
    console.log(`incoming msg from ${clientId}:`, message.toString());

    for (let [otherClientId, client] of clients) {
      if (otherClientId !== clientId && client.readyState === WebSocket.OPEN) {
        // console.log(`outgoing to ${otherClientId}:`, message);
        client.send(message);
      }
    }
  });

  ws.on("error", function error(err) {
    console.error("WebSocket error:", err);
  });

  ws.on("close", function close() {
    console.log(`Client disconnected: ${clientId}`);
    clients.delete(clientId);
  });
});

console.log("WebSocket server started on ws://localhost:6789");
