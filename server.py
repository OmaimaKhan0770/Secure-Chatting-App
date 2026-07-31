import socket
import threading

clients = {}

# ================= SEND ONLINE USERS =================
def broadcast_users():

    users = ",".join(clients.keys())

    packet = f"USERS|{users}\n"

    for conn in clients.values():

        try:
            conn.send(packet.encode())

        except:
            pass

# ================= HANDLE CLIENT =================
def handle_client(conn, username):

    while True:

        try:

            data = conn.recv(8192).decode()

            if not data:
                break

            packets = data.split("\n")

            for packet in packets:

                if packet.strip() == "":
                    continue

                # MESSAGE FORMAT:
                # MSG|sender|receiver|algo|encrypted

                parts = packet.split("|", 4)

                if len(parts) < 5:
                    continue

                packet_type = parts[0]

                if packet_type != "MSG":
                    continue

                sender = parts[1]
                receiver = parts[2]
                algo = parts[3]
                encrypted_message = parts[4]

                print(f"{sender} → {receiver} ({algo})")

                # SEND ONLY TO RECEIVER
                if receiver in clients:

                    try:
                        clients[receiver].send(
                            (packet + "\n").encode()
                        )

                    except:
                        pass

        except Exception as e:
            print("Error:", e)
            break

    conn.close()

    if username in clients:
        del clients[username]

    print(username, "disconnected")

    broadcast_users()

# ================= SERVER =================
def start_server():

    server = socket.socket()

    server.bind(("localhost", 12345))

    server.listen(5)

    print("✅ Server Started")

    while True:

        conn, addr = server.accept()

        try:

            login_packet = conn.recv(1024).decode().strip()

            # LOGIN|username
            parts = login_packet.split("|")

            if len(parts) != 2:
                conn.close()
                continue

            if parts[0] != "LOGIN":
                conn.close()
                continue

            username = parts[1]

            clients[username] = conn

            print(username, "connected")

            broadcast_users()

            thread = threading.Thread(
                target=handle_client,
                args=(conn, username),
                daemon=True
            )

            thread.start()

        except Exception as e:
            print("Connection Error:", e)

# ================= MAIN =================
if __name__ == "__main__":
    start_server()