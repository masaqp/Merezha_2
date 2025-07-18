import socket
import threading

HOST = '0.0.0.0'  # For external access on Render
PORT = 10000      # You can choose any open port

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = f"{addr}: {data.decode()}"
            print(message)

            # Broadcast to all clients
            for client in clients:
                if client != conn:
                    client.sendall(message.encode())
    finally:
        print(f"[DISCONNECTED] {addr}")
        clients.remove(conn)
        conn.close()

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is running on port {PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start()
