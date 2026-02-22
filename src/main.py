from user_controller import manage_users, manage_user_data
from ui_main import main_ui_run
from plantbook_api import PlantbookAPI
from user_logins import user_login


logged_in = False
current_user = None
running = True

def logged_out_menu():
    print("Login to access Plant Management System")
    global logged_in, current_user
    logged_in, current_user = user_login()
    if logged_in:
        print(f"Welcome, {current_user.username}!")
    else:
        print("Login failed. Please try again.")    

def logged_in_menu():
    global running
    if __name__ == "__main__":
        print("Welcome to the Plant Management System")
        while running:
            print("\n Main Menu ")
            print("1. Manage Users")
            print("2. Manage your data") 
            print("3. Add Plants")
            print("4. Run UI")
            print("5. Exit")

            main_choice = input("Select an option: ").strip()

            if main_choice == "1":
                manage_users()
            elif main_choice == "2":
                print("Testing current user info:")
                print(f"Username: {current_user.username}")
                print(f"Client ID: {current_user.client_id}")
                print(f"Client Secret: {current_user.client_secret}")
                print(f"Plants: {current_user.plants}")
                manage_user_data(current_user)
            elif main_choice == "3": #RE-ORDER
                user_plant_search_decision = input("Do you want to search for a new plant to add to your collection? (y/n): ").strip().lower()
                if user_plant_search_decision == "y":
                    PlantbookAPI.plant_class_run(current_user)
                elif user_plant_search_decision == "n":
                    print("Returning to main menu") 
                    break
                else:
                    print("Invalid option, returning to main menu")
                    break        
            elif main_choice == "4":
                main_ui_run()
            elif main_choice == "5":
                print("Exiting the program")
                running = False
            else:
                print("Invalid option")

            
while running:
    if not logged_in:
        logged_out_menu()      #Bugs in exiting main program, and basically every other option, need to fix
    elif logged_in:
        logged_in_menu()
    elif running == False:
        print("Exiting the program")
        break       


#TO DO:
# Improve error handling in user management
# Finalize the Plantbook API integration
# Finalize UI and connect to real sensor data and other functions
# Add raspberry pi everything
# Figure out what to do with plant class and how to use inheritance with the json file