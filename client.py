import socket
import threading
import tkinter as tk
from tkinter import messagebox
import time
import psutil

from crypto_utils import *
from login_system import login, register
from dashboard import show_dashboard

# ================= SOCKET =================
client = socket.socket()
client.connect(("localhost", 12345))

# ================= DATA =================
username_global = ""
selected_user = ""
selected_algo = ""

# ================= PERFORMANCE =================
times = {
    "AES": [],
    "DES": [],
    "HYBRID": []
}

cpu_usage = {
    "AES": [],
    "DES": [],
    "HYBRID": []
}

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Secure Chat 💜")
root.geometry("750x650")
root.configure(bg="#E6E6FA")

# =========================================================
# LOGIN FRAME
# =========================================================
login_frame = tk.Frame(root, bg="#E6E6FA")
login_frame.pack(expand=True)

title = tk.Label(
    login_frame,
    text="💜 Secure Chat Login 💜",
    font=("Segoe UI", 20, "bold"),
    bg="#E6E6FA",
    fg="#6A0DAD"
)

title.pack(pady=20)

username_entry = tk.Entry(
    login_frame,
    width=30,
    font=("Segoe UI", 12)
)

username_entry.pack(pady=10)

password_entry = tk.Entry(
    login_frame,
    width=30,
    font=("Segoe UI", 12),
    show="*"
)

password_entry.pack(pady=10)

# =========================================================
# SETUP FRAME
# =========================================================
setup_frame = tk.Frame(root, bg="#E6E6FA")

setup_title = tk.Label(
    setup_frame,
    text="💜 Setup Chat 💜",
    font=("Segoe UI", 18, "bold"),
    bg="#E6E6FA",
    fg="#6A0DAD"
)

setup_title.pack(pady=20)

# USER SELECT
receiver_var = tk.StringVar()

receiver_menu = tk.OptionMenu(
    setup_frame,
    receiver_var,
    ""
)

receiver_menu.config(
    bg="#C8A2C8",
    width=20
)

receiver_menu.pack(pady=10)

# ALGORITHM SELECT
algo_var = tk.StringVar(value="AES")

algo_menu = tk.OptionMenu(
    setup_frame,
    algo_var,
    "AES",
    "DES",
    "HYBRID"
)

algo_menu.config(
    bg="#B57EDC",
    width=20
)

algo_menu.pack(pady=10)

# =========================================================
# CHAT FRAME
# =========================================================
chat_frame = tk.Frame(root, bg="#E6E6FA")

chat_title = tk.Label(
    chat_frame,
    text="💜 Secure Chat Room 💜",
    font=("Segoe UI", 18, "bold"),
    bg="#E6E6FA",
    fg="#6A0DAD"
)

chat_title.pack(pady=10)

# CHAT BOX
chat_box = tk.Text(
    chat_frame,
    width=75,
    height=25,
    font=("Segoe UI", 11),
    bg="#F8F0FF",
    fg="#4B0082"
)

chat_box.pack(padx=10, pady=10)

chat_box.tag_config("you", foreground="#6A0DAD")
chat_box.tag_config("friend", foreground="#2E8B57")

# MESSAGE FRAME
message_frame = tk.Frame(chat_frame, bg="#E6E6FA")
message_frame.pack(pady=10)

message_entry = tk.Entry(
    message_frame,
    width=45,
    font=("Segoe UI", 12)
)

message_entry.grid(row=0, column=0, padx=10)

# =========================================================
# UPDATE USERS
# =========================================================
def update_users(users):

    online_users = [
        u for u in users
        if u != username_global and u != ""
    ]

    menu = receiver_menu["menu"]

    menu.delete(0, "end")

    for user in online_users:

        menu.add_command(
            label=user,
            command=lambda value=user:
            receiver_var.set(value)
        )

    if online_users:
        receiver_var.set(online_users[0])

# =========================================================
# PROCESS SERVER PACKETS
# =========================================================
def process_packet(packet):

    global selected_user

    # ONLINE USERS
    if packet.startswith("USERS|"):

        users = packet.replace("USERS|", "").split(",")

        root.after(
            0,
            update_users,
            users
        )

        return

    # MESSAGE
    parts = packet.split("|", 4)

    if len(parts) < 5:
        return

    packet_type = parts[0]

    if packet_type != "MSG":
        return

    sender = parts[1]
    receiver = parts[2]
    algorithm = parts[3]
    encrypted_message = parts[4]

    try:

        if algorithm == "AES":
            message = decrypt_aes(encrypted_message)

        elif algorithm == "DES":
            message = decrypt_des(encrypted_message)

        else:
            message = decrypt_hybrid(encrypted_message)

        def show():

            chat_box.insert(
                tk.END,
                f"\n💚 {sender} ({algorithm})\n{message}\n",
                "friend"
            )

            chat_box.see(tk.END)

        root.after(0, show)

    except Exception as e:
        print("Decrypt Error:", e)

# =========================================================
# RECEIVE THREAD
# =========================================================
def receive_messages():

    buffer = ""

    while True:

        try:

            data = client.recv(8192).decode()

            if not data:
                break

            buffer += data

            while "\n" in buffer:

                line, buffer = buffer.split("\n", 1)

                line = line.strip()

                if line:
                    process_packet(line)

        except Exception as e:
            print("Receive Error:", e)
            break

# =========================================================
# SEND MESSAGE
# =========================================================
def send_message():

    msg = message_entry.get()

    if msg == "":
        return

    cpu_before = psutil.cpu_percent(interval=None)

    start = time.time()

    # AES
    if selected_algo == "AES":

        encrypted = encrypt_aes(msg)

    # DES
    elif selected_algo == "DES":

        encrypted = encrypt_des(msg)

    # HYBRID
    else:

        encrypted = encrypt_hybrid(msg)

    end = time.time()

    cpu_after = psutil.cpu_percent(interval=None)

    times[selected_algo].append(end - start)

    cpu_usage[selected_algo].append(
        abs(cpu_after - cpu_before)
    )

    # FINAL PACKET
    packet = (
        f"MSG|"
        f"{username_global}|"
        f"{selected_user}|"
        f"{selected_algo}|"
        f"{encrypted}\n"
    )

    client.send(packet.encode())

    chat_box.insert(
        tk.END,
        f"\n💜 You → {selected_user} ({selected_algo})\n{msg}\n",
        "you"
    )

    chat_box.see(tk.END)

    message_entry.delete(0, tk.END)

# =========================================================
# START CHAT BUTTON
# =========================================================
def start_chat():

    global selected_user
    global selected_algo

    selected_user = receiver_var.get()
    selected_algo = algo_var.get()

    if selected_user == "":

        messagebox.showerror(
            "Error",
            "No User Selected"
        )

        return

    setup_frame.pack_forget()

    chat_frame.pack(fill="both", expand=True)


# =========================================================
# BACK TO SETUP
# =========================================================
def go_back():

    chat_frame.pack_forget()

    setup_frame.pack(expand=True)

    chat_box.delete(1.0, tk.END)


# =========================================================
# DASHBOARD
# =========================================================
def open_dashboard():

    show_dashboard(
        times,
        cpu_usage
    )

# =========================================================
# LOGIN
# =========================================================
def do_login():

    global username_global

    username = username_entry.get()
    password = password_entry.get()

    if login(username, password):

        username_global = username

        # LOGIN PACKET
        client.send(
            f"LOGIN|{username}\n".encode()
        )

        login_frame.pack_forget()

        setup_frame.pack(expand=True)

        # START RECEIVER
        threading.Thread(
            target=receive_messages,
            daemon=True
        ).start()

    else:

        messagebox.showerror(
            "Error",
            "Invalid Login"
        )

# =========================================================
# REGISTER
# =========================================================
def do_register():

    username = username_entry.get()
    password = password_entry.get()

    if register(username, password):

        messagebox.showinfo(
            "Success",
            "Registered Successfully"
        )

    else:

        messagebox.showerror(
            "Error",
            "User Already Exists"
        )

# =========================================================
# BUTTONS
# =========================================================
login_btn = tk.Button(
    login_frame,
    text="Login 💜",
    bg="#B57EDC",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    width=15,
    command=do_login
)

login_btn.pack(pady=10)

# BACK BUTTON
back_btn = tk.Button(
    chat_frame,
    text="⬅ Back",
    bg="#D8BFD8",
    fg="black",
    font=("Segoe UI", 11, "bold"),
    width=12,
    command=go_back
)

back_btn.pack(pady=5)


register_btn = tk.Button(
    login_frame,
    text="Register ✨",
    bg="#C8A2C8",
    font=("Segoe UI", 12, "bold"),
    width=15,
    command=do_register
)

register_btn.pack(pady=10)

# START CHAT BUTTON
start_chat_btn = tk.Button(
    setup_frame,
    text="Start Chat 💜",
    bg="#B57EDC",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    width=20,
    command=start_chat
)

start_chat_btn.pack(pady=20)

# SEND BUTTON
send_btn = tk.Button(
    message_frame,
    text="Send 💜",
    bg="#B57EDC",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    padx=20,
    command=send_message
)

send_btn.grid(row=0, column=1)

# DASHBOARD BUTTON
dashboard_btn = tk.Button(
    chat_frame,
    text="Open Dashboard 📊",
    bg="#C8A2C8",
    font=("Segoe UI", 11, "bold"),
    command=open_dashboard
)

dashboard_btn.pack(pady=10)

# ================= START =================
root.mainloop()