import os
import requests

def hit_api_coin_asset_by_id(target_url:str):
    url = f"{os.getenv("COIN_CAP_URL")}{target_url}"
    response = requests.get(url)


    if response.status_code == 200:
        data =  response.json()

        return data
    else:
        print('Failed to fetch third-party data')

        return False