from user_store import load_users
from utils.hashing import hash_algorithm

class logged_in_user_class:
    def __init__(self, username, password_hash, client_id, client_secret, plants):
        self.username = username
        self.password_hash = password_hash
        self.client_id = client_id
        self.client_secret = client_secret
        self.plants = plants

def user_login():
    username = input("Enter username: ").strip().lower()
    password = input("Enter password: ")
    data = load_users()
    logged_in = False
    current_user = None

    if username in data.get("users", {}):
        login_hashes_password = hash_algorithm(password)
        if login_hashes_password == data["users"][username].get("password"):
            print(f"User '{username}' logged in successfully")
            logged_in = True
            user_data = data["users"][username]
            current_user = logged_in_user_class(
                username,
                user_data.get("password"),
                user_data.get("client_id"),
                user_data.get("client_secret"),
                user_data.get("plants"),
            )
        else:
            print("Incorrect password")
    else:
        print(f"User '{username}' does not exist")

    return logged_in, current_user

#GO OVER AND TEST, LINK TO API PLANT DATA AND ID AND SECRET GOING INTO NECESSARY USER JSON 

#user_login()
#print(current_user.client_id)