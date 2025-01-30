from pathlib import Path
import requests
import json


fhir_api = "http://BLAZE_SRC_APP:8080/fhir"

if __name__ == "__main__":
    count_success = 0
    for item in Path('./data/fhir').iterdir():
        if item.is_file():

            with open(item, 'r') as resource_file:
                resource = json.load(resource_file)

            response = requests.post(fhir_api, json=resource)
            if response.status_code == 200:
                count_success += 1
    print(f"{count_success} resource(s) were successfully inserted.")