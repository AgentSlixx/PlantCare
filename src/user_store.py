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
        return (False, f"User '{username}' does not exist")

    if username == "admin":
        return (False, "Cannot remove admin user")
    else:
        del data["users"][username]
        save_users(data)
        return (True, f"User '{username}' removed")

#Admin only (me)
def remove_all_users():
    data = load_users()
    for i in list(data["users"].keys()):
        if i != "admin":
            del data["users"][i]
    save_users(data)

def list_users():
    data = load_users()
    print(list(data["users"].keys()))

#list_users()
#add_user("admin".lower(), "admin", "qOKVybGCvVCFBK7FGdN4RFbnpdgVbNY5RlCv4eWN", "hyYGh11RumoKzPFc9wvD46z6xEtmEVCcR0mqk2XuXDSZRL7ERNUubtO11N6KSxEWiQdMDSLj4Rhnluz3fgTdTf5pmOkZi0nqRjH6tmtCOG3O7xjEmYqvWRYemeLAYupx")
#remove_user("jim".lower())
#list_users()

#list_users()
#remove_all_users()
#remove_user("admin")
#list_users()