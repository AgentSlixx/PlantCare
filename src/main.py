from user_controller import manage_users
from ui_main import ui_run
from plantbook_api import PlantbookAPI
from user_logins import user_login, logged_in_user

logged_in = False
current_user = None
 

def logged_out_menu():
    print("Login to access Plant Management System")
    global logged_in, current_user
    logged_in, current_user = user_login()
    if logged_in:
        print(f"Welcome, {current_user.username}!")
    else:
        print("Login failed. Please try again.")    

def logged_in_menu():
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
                PlantbookAPI.class_run()
            elif main_choice == "3":
                ui_run()
            elif main_choice == "4":
                print("Exiting the program")
                break
            else:
                print("Invalid option")

if not logged_in:
    logged_out_menu()
    if logged_in:
        logged_in_menu()
else:
    logged_in_menu()    


#TO DO:
# Improve error handling in user management
# Finalize the Plantbook API integration
# Finalize UI and connect to real sensor data and other functions
# Add raspberry pi everything
# Figure out what to do with plant class and how to use inheritance with the json file