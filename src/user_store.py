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
        print("User already exists")
    else:
        data["users"][username] = {
            "password": hash_algorithm(password),
            "client_id": client_id,
            "client_secret": client_secret,
            "plants": []
        }
        print(f"User '{username}' added successfully")
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

def load_all_user_info():
    with open(DATA_FILE, "r") as f: #NOT USED YET, DELETE IF NEVER USED
        return json.load(f)

def list_password_hash(username):
    users = load_users()
    user_found = False
    for i in users["users"]:
        if i == username:
            user_found = True
            return users["users"][i]["password"]
    if user_found == False:
        print(f"User '{username}' not found")
        return None
            
def remove_plant_from_user(username, plant_name):
    data = load_users()
    plant_found = False

    if username not in data["users"]:
        return False, f"User '{username}' does not exist"
    else:
        plants = data["users"][username]["plants"]
        for plant in plants:
            if plant["name"].lower() == plant_name.lower():
                plants.remove(plant)
                save_users(data)
                print(f"Plant '{plant_name}' removed from user '{username}'")
                plant_found = True
                return True
        if plant_found == False:
            print(f"Plant '{plant_name}' not found for user '{username}'")
            return False
            
        

#list_users()
#add_user("admin".lower(), "admin", "qOKVybGCvVCFBK7FGdN4RFbnpdgVbNY5RlCv4eWN", "hyYGh11RumoKzPFc9wvD46z6xEtmEVCcR0mqk2XuXDSZRL7ERNUubtO11N6KSxEWiQdMDSLj4Rhnluz3fgTdTf5pmOkZi0nqRjH6tmtCOG3O7xjEmYqvWRYemeLAYupx")
#remove_user("jim".lower())
#list_users()

#list_users()
#remove_all_users()
#remove_user("admin")
#list_users()

#remove_plant_from_user("admin", "aloe vera")
#add_user("edward ford".lower(), "password123", "ClientIDExample", "ClientSecretExample")
#list_password_hash("edward ford")

remove_all_users()