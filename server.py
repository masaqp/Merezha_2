from flask import Flask, request
from flask_socketio import SocketIO, send, disconnect
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

# Store usernames by session ID
users = {}

@app.route('/')
def index():
    return 'WebSocket server with usernames is running.'

@socketio.on('connect')
def handle_connect():
    print(f"[CONNECTED] Client: {request.sid}")

@socketio.on('set_username')
def handle_set_username(username):
    users[request.sid] = username
    print(f"[USERNAME SET] {request.sid} is now '{username}'")
    send(f"{username} has joined the chat.", broadcast=True)

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, "Anonymous")
    full_msg = f"{username}: {msg}"
    print(f"[MESSAGE] {full_msg}")
    send(full_msg, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = users.pop(request.sid, "Anonymous")
    print(f"[DISCONNECTED] {username} ({request.sid})")
    send(f"{username} has left the chat.", broadcast=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
