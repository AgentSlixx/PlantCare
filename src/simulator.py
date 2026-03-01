import user_store
import user_logins
selected_plant = None

def user_choose_plant(user=None):
    global selected_plant

    if user is None:
        user = user_logins.current_user
    if not user or not user.plants:
        print("No plants found for the current user.")
        selected_plant = None
        return None

    user_plants = user.plants

    while True:
        print("\nYour Plants:")
        for i, plant in enumerate(user_plants, 1):
            print(f"{i}. {plant['name']}")

        choice = input("Select a plant by number: ").strip()

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(user_plants):
                selected_plant = user_plants[choice - 1]['name']
                print(f"Selected plant: {selected_plant}")
                return selected_plant

        print("Invalid selection. Please try again.")


def add_water(amount):
    if selected_plant is None:
        print("No plant selected. Please choose a plant first.")
        return
    print(f"Adding {amount} ml of water to the plant.")
    plant_data = user_store.load_users()
    plant_data["plants"][selected_plant]["water_level"] += amount
    user_store.save_users(plant_data)

def add_sunlight(amount):
    if selected_plant is None:
        print("No plant selected. Please choose a plant first.")
        return
    print(f"Adding {amount} lux to the plant.")
    plant_data = user_store.load_users()
    plant_data["plants"][selected_plant]["sunlight_exposure"] += amount
    user_store.save_users(plant_data)    

def add_humidity(amount):
    if selected_plant is None:
        print("No plant selected. Please choose a plant first.")
        return
    print(f"Adding {amount}% humidity to the plant.")
    plant_data = user_store.load_users()
    plant_data["plants"][selected_plant]["humidity_level"] += amount
    user_store.save_users(plant_data)

def add_temperature(amount):
    if selected_plant is None:
        print("No plant selected. Please choose a plant first.")
        return
    print(f"Adding {amount}°C to the plant's environment.")
    plant_data = user_store.load_users()
    plant_data["plants"][selected_plant]["temperature"] += amount
    user_store.save_users(plant_data)    

    #TO BE CONTINUED MAKE WORK