import socketio

RENDER_SERVER_URL = 'https://merezha-2.onrender.com'
USERNAME = input("Choose your username: ")

sio = socketio.Client()

@sio.event
def connect():
    print("[✔️] Connected to server.")
    sio.emit("set_username", USERNAME)

@sio.on('message')
def on_message(data):
    print(data)

@sio.event
def disconnect():
    print("[❌] Disconnected.")

try:
    print(f"[...] Connecting to {RENDER_SERVER_URL} ...")
    sio.connect(RENDER_SERVER_URL)
except Exception as e:
    print("[‼️] Connection failed:", e)
    exit()

try:
    while True:
        msg = input()
        if msg.lower() == "exit":
            break
        sio.send(msg)
except KeyboardInterrupt:
    pass
finally:
    sio.disconnect()
