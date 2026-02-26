from user_store import add_user, remove_user, list_users, remove_all_users, remove_plant_from_user, save_users, load_users
from utils.hashing import hash_algorithm


def manage_users():
    while True:
        print("\n User Management ")
        print("1. Add user")
        print("2. Remove user")
        print("3. List users")
        print("4. Remove all users (admin only)")
        print("5. Exit user management")

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
            print("Exiting user management")
            break
        
        else:
            print("Invalid option")

def manage_user_data(current_user):
    user_change_data = input("What do you wish to change? \n1. Username \n2. Password \n3. Client ID \n4. Client Secret\n5. Remove Plant\n6. Exit\nSelect an option: ").strip()
    if user_change_data == "1":
        new_username = input("Enter new username: ")  
        data = load_users()
        for i in data["users"]:
            if i == current_user.username:
                data["users"][new_username] = data["users"].pop(i)
                save_users(data)
                print(f"Username changed to '{new_username}'")
    elif user_change_data == "2":
        new_password = input("Enter new password: ")
        data = load_users()
        for i in data["users"]:
            if i == current_user.username:
                data["users"][i]["password"] = hash_algorithm(new_password)
                save_users(data)
                print("Password changed successfully")
    elif user_change_data == "3":
        new_client_id = input("Enter new client ID: ")
        data = load_users()
        for i in data["users"]:
            if i == current_user.username:
                data["users"][i]["client_id"] = new_client_id
                save_users(data)
                print("Client ID changed successfully")
    elif user_change_data == "4":
        new_client_secret = input("Enter new client secret: ")
        data = load_users()
        for i in data["users"]:
            if i == current_user.username:
                data["users"][i]["client_secret"] = new_client_secret
                save_users(data)
                print("Client secret changed successfully")
    elif user_change_data == "5":
        plant_name_input = input("Enter the name of the plant to remove: ")
        plant_names = [plant.name for plant in current_user.plants]
        print(plant_names)
        if plant_name_input in plant_names:
            remove_plant_from_user(current_user.username, plant_name_input)
        else:
            print("Plant not found in user's collection")
    elif user_change_data == "6":
        print("Exiting user data management")                                    