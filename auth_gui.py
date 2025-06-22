import tkinter as tk
from tkinter import messagebox
import db
import client

def open_chat(username, room):
    client.launch_chat(username, room)

def attempt_login():
    user = username_entry.get()
    pwd = password_entry.get()
    room = room_entry.get()
    if db.validate_user(user, pwd):
        root.destroy()
        open_chat(user, room)
    else:
        messagebox.showerror("Error", "Invalid credentials.")

def attempt_register():
    user = username_entry.get()
    pwd = password_entry.get()
    room = room_entry.get()
    if db.register_user(user, pwd):
        root.destroy()
        open_chat(user, room)
    else:
        messagebox.showerror("Error", "Username already exists.")

root = tk.Tk()
root.title("Login / Register")
root.geometry("400x300")  # ⬅️ Increased window size

tk.Label(root, text="Username", font=("Arial", 12)).pack(pady=(15, 5))
username_entry = tk.Entry(root, font=("Arial", 12), width=30)
username_entry.pack()

tk.Label(root, text="Password", font=("Arial", 12)).pack(pady=(10, 5))
password_entry = tk.Entry(root, show="*", font=("Arial", 12), width=30)
password_entry.pack()

tk.Label(root, text="Room", font=("Arial", 12)).pack(pady=(10, 5))
room_entry = tk.Entry(root, font=("Arial", 12), width=30)
room_entry.insert(0, "General")
room_entry.pack()

tk.Button(root, text="Login", font=("Arial", 12), command=attempt_login).pack(pady=10)
tk.Button(root, text="Register", font=("Arial", 12), command=attempt_register).pack()

root.mainloop()
