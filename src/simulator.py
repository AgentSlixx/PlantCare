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
_simulation_speed = 5

_simulator_state = {
    "humidity": {"value": 50.0, "base": 50.0, "amp": 12.0, "period": 24 * 3600.0, "last_update": None},
    "temperature": {"value": 22.0, "base": 22.0, "amp": 8.0, "period": 24 * 3600.0, "last_update": None},
    "moisture": {"value": 40.0, "base": 40.0, "amp": 10.0, "period": 48 * 3600.0, "last_update": None},
    "sunlight": {"value": 30000.0, "base": 30000.0, "amp": 30000.0, "period": 24 * 3600.0, "last_update": None},
}

# Utility to keep values inside physical bounds
def _clamp(key, value):
    low, high = Physical_bounds.get(key, (None, None))
    if low is not None:
        value = max(low, value)
    if high is not None:
        value = min(high, value)
    return value


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

def user_set_simulation_speed():
    speed = 1
    while True:
        speed = input("Enter the simulation speed in seconds (e.g., 1 for regular-speed, 2 for double speed): ").strip()
        if speed and speed.isdigit() and int(speed):
            if int(speed) <= 0:
                print("Simulation speed must be a positive integer.")
            elif int(speed) > 10:
                print("Simulation speed is too high. Please enter a value between 1 and 10.")
            else:
                return int(speed)
        else: 
            print("Invalid input. Please enter a positive integer for the simulation speed.")

def set_simulation_speed(speed):
    global _simulation_speed
    if not isinstance(speed, int):
        raise TypeError("Simulation speed must be an integer")
    if speed < 1 or speed > 10:
        raise ValueError("Simulation speed must be between 1 and 10")
    _simulation_speed = speed


def get_simulation_speed():
    return _simulation_speed


def simulation_speed():
    while True:
        speed_input = input("Enter simulation speed (1-10, where 1 is slowest and 10 is fastest): ").strip()
        if speed_input.isdigit():
            speed = int(speed_input)
            if 1 <= speed <= 10:
                set_simulation_speed(speed)
                print(f"Simulation speed set to {speed}")
                return speed
        print("Invalid input. Please enter a number between 1 and 10.")


def _simulate_metric(key, dt_seconds=None):
    import math
    import random
    import time

    state = _simulator_state[key]
    now = time.time()
    last = state.get("last_update")

    if dt_seconds is None:
        dt = 1.0 if last is None else max(0.001, now - last)
    else:
        dt = max(0.001, dt_seconds)

    state["last_update"] = now

    # Speed factor: 1 is slowest, 10 is fastest
    effective_dt = dt * get_simulation_speed()

    phase = (now % state["period"]) / state["period"]
    target = state["base"] + math.sin(2 * math.pi * phase) * state["amp"]
    noise = (random.random() - 0.5) * 2.0 * 0.02 * effective_dt * (state["amp"] / 20.0)

    current = state["value"]
    smoothing = 0.015 * effective_dt
    next_value = current + (target - current) * smoothing + noise
    next_value = _clamp(key, next_value)

    state["value"] = next_value
    return next_value


def humidity_change(dt_seconds=None):
    return _simulate_metric("humidity", dt_seconds)


def temperature_change(dt_seconds=None):
    return _simulate_metric("temperature", dt_seconds)


def moisture_change(dt_seconds=None):
    return _simulate_metric("moisture", dt_seconds)


def sunlight_change(dt_seconds=None):
    return _simulate_metric("sunlight", dt_seconds)


def get_current_environment(dt_seconds=None):
    return {
        "humidity": humidity_change(dt_seconds),
        "temperature": temperature_change(dt_seconds),
        "moisture": moisture_change(dt_seconds),
        "sunlight": sunlight_change(dt_seconds),
    }


def add_water(amount):
    """Add water to increase moisture level."""
    global _simulator_state
    _simulator_state["moisture"]["value"] = _clamp("moisture", _simulator_state["moisture"]["value"] + amount)


def add_humidity(amount):
    """Add humidity to increase humidity level."""
    global _simulator_state
    _simulator_state["humidity"]["value"] = _clamp("humidity", _simulator_state["humidity"]["value"] + amount)


def set_sunlight(amount):
    """Add percentage to sunlight level."""
    global _simulator_state
    current = _simulator_state["sunlight"]["value"]
    increase = current * (amount / 100.0)
    _simulator_state["sunlight"]["value"] = _clamp("sunlight", current + increase)


def set_temperature(amount):
    """Set temperature level."""
    global _simulator_state
    _simulator_state["temperature"]["value"] = _clamp("temperature", amount)


def time_of_day():
    speed = user_set_simulation_speed()
    time_of_day = 12
    while True:
        time_of_day += 0.5 * speed
        if time_of_day >= 24:
            time_of_day -= 24
        time.sleep(1)   

def water_change():
    #get the plant data from user.json and make the starting water level the midpoint of the plant's water limits
    # then slowly decrease the water over time based on the simulation speed, and if the water level goes below the plant's minimum water limit, log a warning message
    pass
