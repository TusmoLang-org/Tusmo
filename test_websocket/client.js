const WebSocket = require('ws');

const wsUrl = process.argv[2] || 'ws://localhost:8080';

console.log('Connecting to:', wsUrl);

const ws = new WebSocket(wsUrl);

ws.on('open', () => {
    console.log('Connected to WebSocket server');
    ws.send(JSON.stringify({ type: 'hello', message: 'Connected from Node.js client' }));
});

ws.on('message', (data) => {
    try {
        const json = JSON.parse(data.toString());
        console.log('Received JSON:', JSON.stringify(json, null, 2));
    } catch (e) {
        console.log('Received (non-JSON):', data.toString());
    }
});

ws.on('error', (err) => {
    console.error('WebSocket error:', err.message);
});

ws.on('close', () => {
    console.log('Disconnected from WebSocket server');
});

process.stdin.on('data', (input) => {
    const msg = input.toString().trim();
    if (msg && ws.readyState === WebSocket.OPEN) {
        ws.send(msg);
    }
});

console.log('Ready. Type messages and press Enter to send. Press Ctrl+C to exit.');