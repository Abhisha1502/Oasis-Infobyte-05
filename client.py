import socket
import threading
import tkinter as tk
import tkinter.messagebox as msgbox
from encryption import encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_socket():
    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        msgbox.showerror("Connection Error", "❌ Unable to connect to the server.\nMake sure the server is running.")
        exit()

def launch_chat(username, room):
    def send_message():
        msg = msg_entry.get()
        if msg:
            encrypted = encrypt_message(msg.encode())
            client.send(encrypted)
            msg_entry.delete(0, tk.END)

    def receive_messages():
        while True:
            try:
                msg = client.recv(4096).decode()
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, msg + "\n")
                chat_area.config(state=tk.DISABLED)
                chat_area.yview(tk.END)
            except:
                break

    connect_socket()
    client.send(f"{username}||{room}".encode())

    win = tk.Toplevel()
    win.title(f"Chat - {username} in #{room}")

    chat_area = tk.Text(win, state=tk.DISABLED)
    chat_area.pack(padx=10, pady=10)

    msg_entry = tk.Entry(win)
    msg_entry.pack(padx=10, pady=5)

    tk.Button(win, text="Send", command=send_message).pack()

    threading.Thread(target=receive_messages, daemon=True).start()
