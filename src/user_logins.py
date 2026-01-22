from user_store import load_all_user_info
from utils.hashing import hash_algorithm

class logged_in_user:
    def __init__(self, username, password_hash, client_id, client_secret, plants):
        self.username = username
        self.password_hash = password_hash
        self.client_id = client_id
        self.client_secret = client_secret
        self.plants = plants

logged_in = False
current_user = None

def user_login():
    global logged_in, current_user
    username = input("Enter username: ").strip().lower()
    password = input("Enter password: ")
    data = load_all_user_info()
    if username in data["users"]:
        login_hashes_password = hash_algorithm(password)
        if login_hashes_password == data["users"][username]["password"]:
            print(f"User '{username}' logged in successfully")
            logged_in = True
            current_user = logged_in_user(
                username,
                data["users"][username]["password"],
                data["users"][username]["client_id"],
                data["users"][username]["client_secret"],
                data["users"][username]["plants"]
            )
        else:
            print("Incorrect password")
            logged_in = False
    else:
        print(f"User '{username}' does not exist")   
        logged_in = False

#GO OVER AND TEST, LINK TO API PLANT DATA AND ID AND SECRET GOING INTO NECESSARY USER JSON 

user_login()
print(current_user.username, current_user.client_id, current_user.client_secret, current_user.plants)