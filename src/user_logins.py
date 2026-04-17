# user_logins.py
from user_store import load_users, add_user
from utils.hashing import hash_algorithm

current_user = None  # global variable for currently logged-in user

class logged_in_user_class:
    def __init__(self, username, password_hash, client_id, client_secret, plants):
        self.username = username
        self.password_hash = password_hash
        self.client_id = client_id
        self.client_secret = client_secret
        self.plants = plants

def user_login():
    global current_user
    username = input("Enter username: ").strip().lower()
    password = input("Enter password: ")
    if not username:
        print("Username cannot be blank")
        return False, None
    if not password:
        print("Password cannot be blank")
        return False, None

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

def create_account():
    global current_user
    print("\n--- Create New Account ---")
    username = input("Enter desired username: ").strip().lower()
    password = input("Enter password: ")
    client_id = input("Enter client ID: ")
    client_secret = input("Enter client secret: ")
    if not username:
        print("Username cannot be blank")
        return False, None
    if not password:
        print("Password cannot be blank")
        return False, None
    
    try:
        add_user(username, password, client_id, client_secret)
        print(f"Account '{username}' created successfully!")
        
        data = load_users()
        user_data = data["users"][username]
        current_user = logged_in_user_class(
            username,
            user_data.get("password"),
            user_data.get("client_id"),
            user_data.get("client_secret"),
            user_data.get("plants"),
        )
        return True, current_user
    except ValueError as error:
        print(f"Error creating account: {error}")
        return False, None

def login_menu():
    global current_user
    while True:
        print("\n--- Plant Care System Login ---")
        print("1. Login to existing account")
        print("2. Create new account")
        print("3. Exit")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            logged_in, current_user = user_login()
            if logged_in:
                return True, current_user
        elif choice == "2":
            logged_in, current_user = create_account()
            if logged_in:
                return True, current_user
        elif choice == "3":
            print("Exiting...")
            return False, None
        else:
            print("Invalid option. Please try again.")