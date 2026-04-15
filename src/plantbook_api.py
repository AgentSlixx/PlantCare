import requests
from plant_classes import Plant
from user_store import load_users, save_users

Base_URL = "https://open.plantbook.io/api/v1/"

class PlantbookAPI:
    def __init__(self, client_id=None, client_secret=None, current_user=None):
        if current_user is not None:
            client_id = getattr(current_user, "client_id", None)
            client_secret = getattr(current_user, "client_secret", None)
        if not client_id or not client_secret:
            raise ValueError("client_id and client_secret must be provided")
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.get_access_token()
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def get_access_token(self):
        response = requests.post(f"{Base_URL}token/",data={"grant_type": "client_credentials","client_id": self.client_id,"client_secret": self.client_secret})
        response.raise_for_status()
        return response.json()["access_token"]

    def search_plant(self, plant_name):
        response = requests.get(f"{Base_URL}plant/search",params={"alias": plant_name},headers=self.headers)
        response.raise_for_status()
        return response.json().get("results", [])

    def get_plant_detail(self, pid):
        response = requests.get(f"{Base_URL}plant/detail/{pid}",headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_plant_light_limits(self, pid):
        plant_detail = self.get_plant_detail(pid)
        return plant_detail.get("min_light_lux"), plant_detail.get("max_light_lux")

    def get_plant_temperature_limits(self, pid):
        plant_detail = self.get_plant_detail(pid)
        return plant_detail.get("min_temp"), plant_detail.get("max_temp")
    
    def get_plant_humidity_limits(self, pid):
        plant_detail = self.get_plant_detail(pid)
        return plant_detail.get("min_env_humid"), plant_detail.get("max_env_humid")

    def get_plant_moisture_limits(self, pid):
        plant_detail = self.get_plant_detail(pid)
        return plant_detail.get("min_soil_moist"), plant_detail.get("max_soil_moist")

    def plant_class_run(logged_in_user):
        if logged_in_user is None:
            print("No logged-in user provided")
            return
        plant_name = input("Enter the plant name to search: ").strip()
        if not plant_name:
            print("Plant name cannot be blank")
            return

        try:
            api = PlantbookAPI(client_id=logged_in_user.client_id, client_secret=logged_in_user.client_secret)
        except requests.RequestException as error:
            print(f"Could not connect to PlantBook API: {error}")
            return
        except ValueError as error:
            print(error)
            return

        users_data = load_users()
        username = logged_in_user.username
        if username not in users_data.get("users", {}):
            print("Username not found. Plant not saved.")
            return

        user_plants = users_data["users"][username].setdefault("plants", [])
        # Duplicate checking prevents the same user storing the same plant twice.
        if any(plant.get("name", "").lower() == plant_name.lower() for plant in user_plants):
            print(f"Plant '{plant_name}' is already saved for user '{username}'.")
            return

        # Validate API results before using the first result's pid.
        try:
            search_results = api.search_plant(plant_name)
        except requests.RequestException as error:
            print(f"Plant search failed: {error}")
            return

        if not search_results:
            print("No plants found with that name.")
        else:
            plant_id = search_results[0].get("pid")
            if plant_id is None:
                print("Plant result did not include a plant ID.")
                return

            try:
                plant_light_limits = api.get_plant_light_limits(plant_id)
                plant_temperature_limits = api.get_plant_temperature_limits(plant_id)
                plant_humidity_limits = api.get_plant_humidity_limits(plant_id)
                plant_moisture_limits = api.get_plant_moisture_limits(plant_id)
            except requests.RequestException as error:
                print(f"Plant details could not be loaded: {error}")
                return

            print(f"Plant '{plant_name}' added with the following limits:")
            print(f"Light limits: {plant_light_limits}")
            print(f"Temperature limits: {plant_temperature_limits}")
            print(f"Humidity limits: {plant_humidity_limits}")
            print(f"Moisture limits: {plant_moisture_limits}")

            user_plant = Plant(plant_name, plant_light_limits, plant_temperature_limits, plant_humidity_limits, plant_moisture_limits)

            # Plant.to_dict keeps the JSON format in one place.
            user_plants.append(user_plant.to_dict())
            save_users(users_data)
            print(f"Plant '{user_plant.plant_name}' saved to user '{username}'.")

                    

#if __name__ == "__main__":
    #PlantbookAPI.class_run()
