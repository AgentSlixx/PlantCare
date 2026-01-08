from user_controller import manage_users
from ui_main import ui_run
from plantbook_api import PlantbookAPI

if __name__ == "__main__":
    print("Welcome to the Plant Management System")
    while True:
        print("\n Main Menu ")
        print("1. Manage Users")
        print("2. Run UI")
        print("3. Exit")

        main_choice = input("Select an option: ").strip()

        if main_choice == "1":
            manage_users()
        elif main_choice == "2":
            ui_run()
        elif main_choice == "3":
            print("Exiting the program")
            break
        else:
            print("Invalid option")