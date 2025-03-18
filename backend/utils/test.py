import requests, json
from backend.api import Cycle

BASE = "http://127.0.0.1:5000/"

# Define query parameters
params = {
    # "cycle_code": "some_code",
    "name": "Roland",
    #"cardText": "some text",
    # "factions": "Guardian"
}

response = requests.get(BASE + "cards/", params)
print(response.json())
