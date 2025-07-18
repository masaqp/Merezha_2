import socket
import threading

HOST = 'your-render-server-url'  # e.g. 'my-app-name.onrender.com'
PORT = 10000

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message)
        except:
            print("Connection closed.")
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.start()

    print("Connected to the chat server. Type messages below:")
    try:
        while True:
            msg = input()
            if msg.lower() == "exit":
                break
            sock.sendall(msg.encode())
    finally:
        sock.close()

if __name__ == "__main__":
    main()
