import user_logins

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
    global selected_plant
    user = user_logins.current_user

    if not user or not user.plants: # Check if user has plants
        print("No plants found for the current user.")
        selected_plant = None
        return None

    user_plants = user.plants

    while True:
        print("\nYour Plants:")
        for i, plant in enumerate(user_plants, 1): # Lists the plants on the users account
            print(f"{i}. {plant['name']}")

        choice = input("Select a plant by number: ").strip()

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(user_plants):
                selected_plant = user_plants[choice - 1]['name']
                print(f"Selected plant: {selected_plant}")
                return selected_plant

        print("Invalid selection. Please try again.")

