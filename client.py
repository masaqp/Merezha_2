import socketio

RENDER_SERVER_URL = 'https://merezha-2.onrender.com'
USERNAME = input("Придумай собі прізвисько =)\n ")

sio = socketio.Client()

@sio.event
def connect():
    print("[✔️] Підключений до серверу.")
    sio.emit("set_username", USERNAME)

@sio.on('message')
def on_message(data):
    print(data)

@sio.event
def disconnect():
    print("[❌] Кікнуто.")

try:
    print(f"[...] Йдемо в гості до {RENDER_SERVER_URL} ...")
    sio.connect(RENDER_SERVER_URL)
except Exception as e:
    print("[‼️] Трабли зі з'єднанням:", e)
    exit()

try:
    while True:
        msg = input()
        if msg.lower() == "exit":
            break
        elif msg.lower() == 'randomito':
            sio.emit("random")
            continue
        sio.send(msg)
except KeyboardInterrupt:
    pass
finally:
    sio.disconnect()
