import json
from utils.hashing import hash_algorithm
from pathlib import Path

# Ensures that the program can find users.json, resolve makes DATA_FILE an absolute, full path, .parent goes up directory leves and /data/users.json points to the file
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "users.json"

def load_users():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_user(username, password, client_id, client_secret):
    data = load_users()

    if username in data["users"]:
        raise ValueError("User already exists")

    data["users"][username] = {
        "password": hash_algorithm(password),
        "client_id": client_id,
        "client_secret": client_secret,
        "plants": []
    }

    save_users(data)

def remove_user(username):
    data = load_users()

    if username not in data["users"]:
        return (f"User '{username}' does not exist")

    del data["users"][username]
    save_users(data)

#Admin only (me)
def remove_all_users():
    data = {"users": {}}
    save_users(data)

def list_users():
    data = load_users()
    print(list(data["users"].keys()))

#list_users()
add_user("BoB".lower(), "Bobissuperdupercool123££".lower(), "Jim's clientID", "Jims clientSecret")
#remove_user("jim".lower())
#list_users()

#list_users()
#remove_all_users()
#list_users()

list_users()

list_users()