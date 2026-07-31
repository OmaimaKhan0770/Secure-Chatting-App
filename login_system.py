import hashlib
import os

FILE = "users.txt"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register(username, password):
    if not os.path.exists(FILE):
        open(FILE, 'w').close()

    with open(FILE, "r") as f:
        for line in f:
            if username == line.split(":", 1)[0]:
                return False

    with open(FILE, "a") as f:
        f.write(f"{username}:{hash_password(password)}\n")

    return True


def login(username, password):
    if not os.path.exists(FILE):
        return False

    hashed = hash_password(password)

    with open(FILE, "r") as f:
        for line in f:
            user, pwd = line.strip().split(":", 1)
            if user == username and pwd == hashed:
                return True

    return False


def get_all_users():
    users = []

    if not os.path.exists(FILE):
        return users

    with open(FILE, "r") as f:
        for line in f:
            user = line.split(":", 1)[0]
            users.append(user)

    return users