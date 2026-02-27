import requests
from plant_classes import Plant
import json

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
        response = requests.post(
            f"{Base_URL}token/",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def search_plant(self, plant_name):
        response = requests.get(
            f"{Base_URL}plant/search",
            params={"alias": plant_name},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json().get("results", [])

    def get_plant_detail(self, pid):
        response = requests.get(
            f"{Base_URL}plant/detail/{pid}",
            headers=self.headers
        )
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
        plant_name = input("Enter the plant name to search: ")

        api = PlantbookAPI(client_id=logged_in_user.client_id, client_secret=logged_in_user.client_secret)

        # get the plant max and min light, temperature, humidity, moisture and save to a Plant object
        search_results = api.search_plant(plant_name)
        if not search_results:
            print("No plants found with that name.")
        else:
            plant_light_limits = api.get_plant_light_limits(search_results[0]['pid'])
            plant_temperature_limits = api.get_plant_temperature_limits(search_results[0]['pid'])
            plant_humidity_limits = api.get_plant_humidity_limits(search_results[0]['pid'])
            plant_moisture_limits = api.get_plant_moisture_limits(search_results[0]['pid'])

            print(f"Plant '{plant_name}' added with the following limits:")
            print(f"Light limits: {plant_light_limits}")
            print(f"Temperature limits: {plant_temperature_limits}")
            print(f"Humidity limits: {plant_humidity_limits}")
            print(f"Moisture limits: {plant_moisture_limits}")

            user_plant = Plant(plant_name, plant_light_limits, plant_temperature_limits, plant_humidity_limits, plant_moisture_limits)

        
            # send plant data to users.json in the logged in user's plants list
            with open("data/users.json", "r") as g:
                users_data = json.load(g)
            username = logged_in_user.username
            if username in users_data.get("users", {}):
                users_data["users"][username].setdefault("plants", [])
                users_data["users"][username]["plants"].append({
                    "name": user_plant.plant_name,
                    "light_limits": user_plant.light_limits,
                    "temperature_limits": user_plant.temperature_limits,
                    "humidity_limits": user_plant.humidity_limits,
                    "moisture_limits": user_plant.moisture_limits
                })
                with open("data/users.json", "w") as g:
                    json.dump(users_data, g, indent=4)
                print(f"Plant '{user_plant.plant_name}' saved to user '{username}'.")
            else:
                print("Username not found. Plant not saved.")    

                    

#if __name__ == "__main__":
    #PlantbookAPI.class_run()