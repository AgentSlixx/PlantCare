import csv
from datetime import datetime
from pathlib import Path
import time
import user_logins
import user_store
from plant_classes import Plant

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
simulation_speed = 1  # Default simulation speed
time_counter = 0  # Time counter for simulation cycles
last_history_log = 0
current_health_score = 100
HISTORY_FILE = Path(__file__).resolve().parent.parent / "data" / "sample_readings.csv"
# Sets a file path for the history log under a constant variable 

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
    
def speed_of_simulation():
    global simulation_speed
    user_time_input = input("Enter a number (1-10) to set the simulation speed: ")
    try:
        speed = int(user_time_input)
        if 1 <= speed <= 10:
            simulation_speed = speed
            print(f"Simulation speed set to {speed}")
            return speed
        else:
            print("Invalid input. Please enter a number between 1 and 10.")
            return None
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None
    
starting_plant_data = {
    "humidity": 50.0,
    "temperature": 20.0,
    "moisture": 50.0,
    "sunlight": 10000.0,
}

def show_message(message, output_callback=None):
    print(message)
    if output_callback:
        output_callback(message)

def add_water_command(amount, output_callback=None):
    global selected_plant
    if amount < 0:
        show_message("Water amount cannot be negative", output_callback)
        return
    if selected_plant:
        show_message(f"Adding {amount} units of water to the plant...", output_callback)
        for i in range(5):
            time.sleep(0.5)  # Simulate time taken to add water
            selected_plant["moisture"] += amount / 5  # Gradually increase moisture
            if selected_plant["moisture"] > Physical_bounds["moisture"][1]:
                selected_plant["moisture"] = Physical_bounds["moisture"][1]  # Cap at max moisture
            show_message(f"Current moisture level: {selected_plant['moisture']:.2f}%", output_callback)

def add_sunlight_command(amount, output_callback=None):
    global selected_plant
    if amount < 0:
        show_message("Sunlight amount cannot be negative", output_callback)
        return
    if selected_plant:
        show_message(f"Adding {amount} units of sunlight to the plant...", output_callback)
        for i in range(5):
            time.sleep(0.5)  # Simulate time taken to add sunlight
            selected_plant["sunlight"] += amount / 5  # Gradually increase sunlight
            if selected_plant["sunlight"] > Physical_bounds["sunlight"][1]:
                selected_plant["sunlight"] = Physical_bounds["sunlight"][1]  # Cap at max sunlight
            show_message(f"Current sunlight level: {selected_plant['sunlight']:.2f} lux", output_callback)

def add_humidity_command(amount, output_callback=None):
    global selected_plant
    if amount < 0:
        show_message("Humidity amount cannot be negative", output_callback)
        return
    if selected_plant:
        show_message(f"Adding {amount} units of humidity to the plant...", output_callback)
        for i in range(5):
            time.sleep(0.5)  # Simulate time taken to add humidity
            selected_plant["humidity"] += amount / 5  # Gradually increase humidity
            if selected_plant["humidity"] > Physical_bounds["humidity"][1]:
                selected_plant["humidity"] = Physical_bounds["humidity"][1]  # Cap at max humidity
            show_message(f"Current humidity level: {selected_plant['humidity']:.2f}%", output_callback)

def add_temperature_command(amount, output_callback=None):
    global selected_plant
    if amount < 0:
        show_message("Temperature amount cannot be negative", output_callback)
        return
    if selected_plant:
        show_message(f"Adding {amount} units of temperature to the plant...", output_callback)
        for i in range(5):
            time.sleep(0.5)  # Simulate time taken to add temperature
            selected_plant["temperature"] += amount / 5  # Gradually increase temperature
            if selected_plant["temperature"] > Physical_bounds["temperature"][1]:
                selected_plant["temperature"] = Physical_bounds["temperature"][1]  # Cap at max temperature
            print(f"Current temperature level: {selected_plant['temperature']:.2f}°C") # 2 decimal places
            show_message(f"Current temperature level: {selected_plant['temperature']:.2f}C", output_callback)

def water_change():
    # Simulate water level change over time until it reaches 0
    global selected_plant, time_counter
    if selected_plant and selected_plant["moisture"] > 0:
        evaporation_rate = 0.05 * simulation_speed  # Slower evaporation
        selected_plant["moisture"] -= evaporation_rate
        if selected_plant["moisture"] < 0:
            selected_plant["moisture"] = 0

def humidity_change():
    # Simulate humidity change, affected by temperature and moisture
    global selected_plant
    if selected_plant:
        # Humidity decreases over time but is impacted by moisture
        drying_rate = 0.02 * simulation_speed
        selected_plant["humidity"] -= drying_rate
        # If moisture is high, humidity increases slightly
        if selected_plant["moisture"] > 30:
            selected_plant["humidity"] += 0.01 * simulation_speed
        if selected_plant["humidity"] < Physical_bounds["humidity"][0]:
            selected_plant["humidity"] = Physical_bounds["humidity"][0]
        if selected_plant["humidity"] > Physical_bounds["humidity"][1]:
            selected_plant["humidity"] = Physical_bounds["humidity"][1]

def temperature_change():
    # Simulate daily temperature cycle
    global selected_plant, time_counter
    if selected_plant:
        import math
        # 1440 minutes in a day, cycle every 24 hours
        cycle = (time_counter % 1440) / 1440 * 2 * math.pi
        ambient_temp = 20 + 10 * math.sin(cycle)  # Varies between 10-30°C
        # Temperature approaches ambient
        diff = ambient_temp - selected_plant["temperature"]
        selected_plant["temperature"] += diff * 0.01 * simulation_speed  # Gradual change
        if selected_plant["temperature"] < Physical_bounds["temperature"][0]:
            selected_plant["temperature"] = Physical_bounds["temperature"][0]
        if selected_plant["temperature"] > Physical_bounds["temperature"][1]:
            selected_plant["temperature"] = Physical_bounds["temperature"][1]

def sunlight_change():
    # Simulate daily sunlight cycle
    global selected_plant, time_counter
    if selected_plant:
        import math
        cycle = (time_counter % 1440) / 1440  # 0 to 1 over day
        if cycle < 0.5:  # Morning to noon
            target_sunlight = 200000 * (cycle / 0.5)
        else:  # Noon to night
            target_sunlight = 200000 * ((1 - cycle) / 0.5)
        diff = target_sunlight - selected_plant["sunlight"]
        selected_plant["sunlight"] += diff * 0.1 * simulation_speed  # Gradual change
        if selected_plant["sunlight"] < Physical_bounds["sunlight"][0]:
            selected_plant["sunlight"] = Physical_bounds["sunlight"][0]
        if selected_plant["sunlight"] > Physical_bounds["sunlight"][1]:
            selected_plant["sunlight"] = Physical_bounds["sunlight"][1]

def current_readings():
    if not selected_plant:
        return {}
    return {
        "humidity": selected_plant.get("humidity"),
        "temperature": selected_plant.get("temperature"),
        "moisture": selected_plant.get("moisture"),
        "sunlight": selected_plant.get("sunlight"),
    }

def selected_plant_object():
    if not selected_plant:
        return None
    return Plant.from_dict(selected_plant)

def reset_health_score():
    global current_health_score
    plant = selected_plant_object()
    if plant is None:
        current_health_score = 100
    else:
        current_health_score = plant.overall_health(current_readings())

def update_health_score():
    global current_health_score
    plant = selected_plant_object()
    if plant is None:
        return current_health_score

    # Long-term health changes a little each update, so repeated bad readings keep hurting.
    current_health_score += plant.health_change(current_readings()) * simulation_speed
    current_health_score = max(0, min(100, current_health_score))
    return current_health_score

def current_health_category():
    return Plant.category_from_score(current_health_score)

def log_simulation_reading(plant_name, readings, health_score=None, health_category=None):
    # append the current reading to the history log CSV file, creating it if it doesn't exist
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    plant = selected_plant_object()
    if health_score is None and plant is not None:
        health_score = current_health_score
    if health_category is None:
        health_category = current_health_category()

    file_is_empty = not HISTORY_FILE.exists() or HISTORY_FILE.stat().st_size == 0
    with open(HISTORY_FILE, "a", newline="") as history_file:
        fieldnames = [
            "timestamp",
            "plant_name",
            "humidity",
            "temperature",
            "moisture",
            "sunlight",
            "health_score",
            "health_category",
        ]
        writer = csv.DictWriter(history_file, fieldnames=fieldnames)
        if file_is_empty:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "plant_name": plant_name,
            "humidity": readings.get("humidity"),
            "temperature": readings.get("temperature"),
            "moisture": readings.get("moisture"),
            "sunlight": readings.get("sunlight"),
            "health_score": health_score,
            "health_category": health_category,
        })