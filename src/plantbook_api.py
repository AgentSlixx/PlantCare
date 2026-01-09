import requests
from plant_class import Plant

Base_URL = "https://open.plantbook.io/api/v1/"
MY_CLIENT_ID = "qOKVybGCvVCFBK7FGdN4RFbnpdgVbNY5RlCv4eWN" #MY CLIENT ID AND SECRET, MAKE USER INPUT THEIRS
MY_CLIENT_SECRET = "hyYGh11RumoKzPFc9wvD46z6xEtmEVCcR0mqk2XuXDSZRL7ERNUubtO11N6KSxEWiQdMDSLj4Rhnluz3fgTdTf5pmOkZi0nqRjH6tmtCOG3O7xjEmYqvWRYemeLAYupx" 

class PlantbookAPI:
    def __init__(self, client_id, client_secret):
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

while __name__ == "__main__":
    
    user_Client_ID = input("Enter your Plantbook Client ID: ")
    user_client_secret = input("Enter your Plantbook Client Secret: ")
    plant_name = input("Enter the plant name to search: ")

    Client_ID = user_Client_ID 
    Client_SECRET = user_client_secret

    api = PlantbookAPI(Client_ID, Client_SECRET)

    #get the plant max and min light, temperature, humidity, moisture and save to a Plant object
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

        
        # add plant info to users.json under the user's plants list
        # WORK IN PROGRESS