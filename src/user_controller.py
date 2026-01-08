from user_store import add_user, remove_user, list_users


def manage_users():
    while True:
        print("\n User Management ")
        print("1. Add user")
        print("2. Remove user")
        print("3. List users")
        print("4. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            username = input(("Enter username: ").strip()).lower()
            password = input("Enter password: ").strip()
            client_id = input("Enter client ID: ").strip()
            client_secret = input("Enter client secret: ").strip()

            try:
                add_user(username, password, client_id, client_secret)
                print(f"User '{username.strip()}' added successfully")
            except ValueError as error:
                print(error)

        elif choice == "2":
            username = input("Enter username to remove: ").strip().lower()

            if remove_user(username):
                print(f"User '{username}' removed")
            elif username == "admin":
                print("Cannot remove admin user")
            else:
                print("User not found")

        elif choice == "3":
            data = list_users()
            
            if data == []:
                print("No users found")

        elif choice == "4":
            print("Exiting user management")
            break

        else:
            print("Invalid option")

