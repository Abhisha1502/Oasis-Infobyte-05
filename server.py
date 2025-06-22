import socket
import threading
from encryption import decrypt_message
from db import save_message

HOST = '127.0.0.1'
PORT = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

clients = []
usernames = {}
rooms = {}

def broadcast(message, room, sender_conn=None):
    for client in clients:
        if rooms.get(client) == room and client != sender_conn:
            try:
                client.send(message)
            except:
                remove_client(client)

def handle_client(conn):
    try:
        user_info = conn.recv(1024).decode().split("||")
        username, room = user_info[0], user_info[1]
        usernames[conn] = username
        rooms[conn] = room
        print(f"[CONNECTED] {username} joined #{room}")
        broadcast(f"{username} joined the room.".encode(), room, conn)

        while True:
            data = conn.recv(4096)
            if not data:
                break
            message = decrypt_message(data).decode()
            print(f"[{username}] #{room}: {message}")
            save_message(username, room, message)
            broadcast(f"{username}: {message}".encode(), room, conn)

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        remove_client(conn)

def remove_client(conn):
    username = usernames.get(conn, "Unknown")
    room = rooms.get(conn, "Unknown")
    print(f"[DISCONNECTED] {username} from #{room}")
    if conn in clients:
        clients.remove(conn)
    usernames.pop(conn, None)
    rooms.pop(conn, None)
    broadcast(f"{username} left the room.".encode(), room, conn)
    conn.close()

def receive_connections():
    while True:
        conn, _ = server.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

receive_connections()
