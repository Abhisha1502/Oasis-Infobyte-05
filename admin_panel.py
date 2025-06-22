import tkinter as tk
from tkinter import messagebox
import db

def view_history():
    room = room_entry.get()
    messages = db.get_message_history(room)
    chat_box.delete("1.0", tk.END)
    for user, msg in messages:
        chat_box.insert(tk.END, f"{user}: {msg}\n")

def validate_admin():
    user = user_entry.get()
    pwd = pass_entry.get()
    if db.is_admin(user, pwd):
        login_win.destroy()
        launch_panel()
    else:
        messagebox.showerror("Access Denied", "Invalid admin credentials.")

def launch_panel():
    win = tk.Tk()
    win.title("Admin Panel")
    win.geometry("600x400")  # ⬅️ Larger window

    tk.Label(win, text="Room Name", font=("Arial", 12)).pack(pady=(10, 5))
    global room_entry
    room_entry = tk.Entry(win, font=("Arial", 12), width=40)
    room_entry.pack()

    tk.Button(win, text="View Messages", font=("Arial", 12), command=view_history).pack(pady=10)

    global chat_box
    chat_box = tk.Text(win, font=("Courier New", 11), wrap="word")
    chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    win.mainloop()

# --- Admin Login Window ---
login_win = tk.Tk()
login_win.title("Admin Login")
login_win.geometry("400x250")  # ⬅️ Larger login window

tk.Label(login_win, text="Admin Username", font=("Arial", 12)).pack(pady=(15, 5))
user_entry = tk.Entry(login_win, font=("Arial", 12), width=30)
user_entry.pack()

tk.Label(login_win, text="Password", font=("Arial", 12)).pack(pady=(10, 5))
pass_entry = tk.Entry(login_win, show="*", font=("Arial", 12), width=30)
pass_entry.pack()

tk.Button(login_win, text="Login", font=("Arial", 12), command=validate_admin).pack(pady=15)

login_win.mainloop()
