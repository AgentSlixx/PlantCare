import user_store

selected_plant = input("Choose which plant you want to simulate: ")

def add_water(amount):
    print(f"Adding {amount} ml of water to the plant.")
    plant_data = user_store.load_users()
    plant_data["plants"][selected_plant]["water_level"] += amount
    user_store.save_users(plant_data)

def add_sunlight(amount):
    print(f"Adding {amount} lux to the plant.")
    plant_data = user_store.load_users()
    plant_data["plants"][selected_plant]["sunlight_exposure"] += amount
    user_store.save_users(plant_data)    

def add_humidity(amount):
    print(f"Adding {amount}% humidity to the plant.")
    plant_data = user_store.load_users()
    plant_data["plants"][selected_plant]["humidity_level"] += amount
    user_store.save_users(plant_data)

def add_temperature(amount):
    print(f"Adding {amount}°C to the plant's environment.")
    plant_data = user_store.load_users()
    plant_data["plants"][selected_plant]["temperature"] += amount
    user_store.save_users(plant_data)    

    #TO BE CONTINUED MAKE WORK 