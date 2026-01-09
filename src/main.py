from user_controller import manage_users
from ui_main import ui_run
from plantbook_api import PlantbookAPI
from plantbook_api import class_run

if __name__ == "__main__":
    print("Welcome to the Plant Management System")
    while True:
        print("\n Main Menu ")
        print("1. Manage Users")
        print("2. Manage Plants")
        print("3. Run UI")
        print("4. Exit")

        main_choice = input("Select an option: ").strip()

        if main_choice == "1":
            manage_users()
        elif main_choice == "2": #TEST AND FIX
            class_run()
        elif main_choice == "3":
            ui_run()
        elif main_choice == "4":
            print("Exiting the program")
            break
        else:
            print("Invalid option")

#TO DO:
# Improve error handling in user management
# Finalize the Plantbook API integration
# Finalize UI and connect to real sensor data and other functions
# Add raspberry pi everything
# Figure out what to do with plant class and how to use inheritance with the json file