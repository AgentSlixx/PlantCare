import requests

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
    
while __name__ == "__main__":
    
    user_Client_ID = input("Enter your Plantbook Client ID: ")
    user_client_secret = input("Enter your Plantbook Client Secret: ")
    plant_name = input("Enter the plant name to search: ")

    Client_ID = user_Client_ID 
    Client_SECRET = user_client_secret

    api = PlantbookAPI(Client_ID, Client_SECRET)

    # Search for Aloe Vera
    results = api.search_plant(plant_name)
    if not results:
        print(f"No plant found for '{plant_name}'")
        exit()

    pid = results[0]["pid"]

    # Get plant detail
    detail = api.get_plant_detail(pid)

    print([detail.get("min_light_lux"), detail.get("max_light_lux")])    