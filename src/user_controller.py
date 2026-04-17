from user_store import add_user, remove_user, list_users, remove_all_users, remove_plant_from_user, save_users, load_users
from utils.hashing import hash_algorithm
from user_logins import logged_in_user_class


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
            data = load_users()
            if hashed_password == data["users"]["admin"]["password"]:
                remove_all_users()
                print("All users removed except admin")
            else:
                print("Incorrect admin password")

        elif choice == "5":
            print("Exiting user management")
            break
        
        else:
            print("Invalid option")

def confirm_user_password(current_user, data):
    # Reused by account changes so password checks are consistent.
    confirmation = input("Enter current password to confirm change: ")
    stored_password = data["users"][current_user.username]["password"]
    return hash_algorithm(confirmation) == stored_password

def manage_user_data(current_user):
    user_change_data = input("What do you wish to change? \n1. Username \n2. Password \n3. Client ID \n4. Client Secret\n5. Remove Plant\n6. Exit\nSelect an option: ").strip()
    if user_change_data == "1":
        new_username = input("Enter new username: ").strip().lower()
        if not new_username:
            print("Username cannot be blank")
            return
        data = load_users()
        if new_username in data["users"]:
            print("Username already exists")
            return
        for i in list(data["users"]):
            if i == current_user.username:
                if i == "admin":
                    print("Cannot change admin username")
                    return
                else:
                    if confirm_user_password(current_user, data):
                        data["users"][new_username] = data["users"].pop(i)
                        save_users(data)
                        print(f"Username changed to '{new_username}'")
                        current_user = load_users()["users"][new_username]
                    else:
                        print("Incorrect password")
    elif user_change_data == "2":
        new_password = input("Enter new password: ")
        if not new_password:
            print("Password cannot be blank")
            return
        data = load_users()
        for i in list(data["users"]):
            if i == current_user.username:
                if i == "admin":
                    print("Cannot change admin password")
                    return
                else:
                    if confirm_user_password(current_user, data):
                        data["users"][i]["password"] = hash_algorithm(new_password)
                        save_users(data)
                        print("Password changed successfully")
                        current_user = load_users()["users"][current_user.username]
                    else:
                        print("Incorrect password")
    elif user_change_data == "3":
        new_client_id = input("Enter new client ID: ").strip()
        data = load_users()
        for i in list(data["users"]):
            if i == current_user.username:
                if i == "admin":
                    print("Cannot change admin client ID")
                    return
                else:
                    if confirm_user_password(current_user, data):
                        data["users"][i]["client_id"] = new_client_id
                        save_users(data)
                        print("Client ID changed successfully")
                        current_user = load_users()["users"][current_user.username]
                    else:
                        print("Incorrect password")
    elif user_change_data == "4":
        new_client_secret = input("Enter new client secret: ").strip()
        data = load_users()
        for i in list(data["users"]):
            if i == current_user.username:
                if i == "admin":
                    print("Cannot change admin client secret")
                    return
                else:
                    if confirm_user_password(current_user, data):
                        data["users"][i]["client_secret"] = new_client_secret
                        save_users(data)
                        print("Client secret changed successfully")
                        current_user = load_users()["users"][current_user.username]
                    else:
                        print("Incorrect password")
    elif user_change_data == "5":
        plant_name_input = input("Enter the name of the plant to remove: ")
        user_data = load_users()["users"][current_user.username]
        current_user = logged_in_user_class(
            current_user.username,
            user_data.get("password"),
            user_data.get("client_id"),
            user_data.get("client_secret"),
            user_data.get("plants")
        )
        plant_names = [current_user.plants[i]["name"] for i in range(len(current_user.plants))]
        print(f"Current plants: {plant_names}")
        if any(plant_name_input.lower() == name.lower() for name in plant_names):
            remove_plant_from_user(current_user.username, plant_name_input)
            user_data = load_users()["users"][current_user.username]
            current_user = logged_in_user_class(
                current_user.username,
                user_data.get("password"),
                user_data.get("client_id"),
                user_data.get("client_secret"),
                user_data.get("plants")
            )
            plant_names = [current_user.plants[i]["name"] for i in range(len(current_user.plants))]
            print(f"New plants: {plant_names}")
        else:
            print("Plant not found in user's collection")
    elif user_change_data == "6":
        print("Exiting user data management")