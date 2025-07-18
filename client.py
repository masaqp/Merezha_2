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

@sio.on("private_message")
def send_message_private(data):
    print("[CLIENT] Received list of users for private message:", data)

    user_sid = ""

    receiver = input('Введіть прізвисько отримувача:\n')
    forwarded_msg = input('Лист отримувачу пишіть тут:\n')
    for sid in data.get('clients'):
        user = data.get('clients')[sid]
        if user == receiver:
            user_sid = sid
            break

    if not user_sid:
        print("[CLIENT] No such user found.")
        return

    rcv_info = {"msg": forwarded_msg, 'rcver': user_sid}
    print("[CLIENT] Sending message:", rcv_info)
    sio.emit("send_dm", rcv_info)

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
        elif msg.lower() == '/users':
            sio.emit("users")
            continue
        elif msg.lower() == '/private':
            sio.emit("users", 'start')
            continue
        sio.send(msg)
except KeyboardInterrupt:
    pass
finally:
    sio.disconnect()
