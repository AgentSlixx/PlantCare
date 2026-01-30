from user_store import add_user, remove_user, list_users, remove_all_users
from utils.hashing import hash_algorithm

def manage_users():
    while True:
        print("\n User Management ")
        print("1. Add user")
        print("2. Remove user")
        print("3. List users")
        print("4. Remove all users (admin only)")
        print("5. Manage your data")
        print("6. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            client_id = input("Enter client ID: ")
            client_secret = input("Enter client Secret: ")

            try:
                add_user(username.lower().strip(), password, client_id, client_secret)
                print(f"User '{username.strip()}' added successfully")
            except ValueError as error:
                print(error)

        elif choice == "2":
            username = input("Enter username to remove: ").strip().lower()
            success, message = remove_user(username)
            if success:
                print(message)
            else:
                print(message)

        elif choice == "3":
            data = list_users()
            if data == []:
                print("No users found")

        elif choice == "4":
            password = input("Enter admin password to confirm: ")
            hashed_password = hash_algorithm(password)
            if hashed_password == hash_algorithm("admin"):
                remove_all_users()
                print("All users removed except admin")
            else:
                print("Incorrect admin password")

        elif choice == "5":
            #allow user to change their name, password, client id and client secret
            user_change_data = input("What do you wish to change? \n1. Username \n2. Password \n3. Client ID \n4. Client Secret\n")
            if user_change_data == "1":
                username = input("Enter username: ")
                
                #FINISH THIS

        elif choice == "6":
            print("Exiting user management")
            break
        
        else:
            print("Invalid option")

manage_users()            