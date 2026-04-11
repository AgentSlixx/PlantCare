import time
import user_logins
import user_store

Graph_keys = ["humidity", "temperature", "moisture", "sunlight"]
Graph_labels = {
    "humidity": "Humidity",
    "temperature": "Temperature",
    "moisture": "Moisture",
    "sunlight": "Sunlight",
}
Graph_units = {
    "humidity": "%",
    "temperature": "C",
    "moisture": "%",
    "sunlight": "lux",
}
Physical_bounds = {
    "humidity": (0.0, 100.0),
    "temperature": (-30.0, 80.0),
    "moisture": (0.0, 100.0),
    "sunlight": (0.0, 200000.0),
}

selected_plant = None

def user_choose_plant():
    data = user_store.load_users()
    users_plants = data["users"][user_logins.current_user.username]["plants"]
    print("Your Plants:\n")
    for i in range(len(users_plants)):
        print(f"{i + 1}. {users_plants[i]['name']}")
    chosen_plant_number = input("Select one of your plants to simulate by selecting its corresponding number, or type 'esc' to go back: ")
    if chosen_plant_number.lower() == 'esc':
        return 'back'
    try:
        chosen_plant_number = int(chosen_plant_number)
        if 1 <= chosen_plant_number <= len(users_plants):
            return users_plants[chosen_plant_number - 1]
        else:
            print("Invalid selection. Please select a valid plant number.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number corresponding to the plant.")
        return None