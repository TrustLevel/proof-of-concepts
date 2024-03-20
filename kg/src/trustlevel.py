import json
import os

from dotenv import load_dotenv

load_dotenv("../.env")
load_dotenv(".env")

import requests

api_key = os.getenv("TRUSTLEVEL_API_KEY")

def get_trustlevel_from_content(content: str):
    url = "https://powr86cuh9.execute-api.eu-west-1.amazonaws.com/v1/trustlevels/"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    data = json.dumps({"text": content})
    response = requests.post(url, headers=headers, data=data)
    if response.ok:
        response_data = response.json()
        if 'trustlevel' in response_data:
            return response_data['trustlevel']
        else:
            raise ValueError(f"No trust level key found in response. Response: {response_data}")
    else:
        raise ConnectionError(f"Failed to get trust level: {response.reason}, Status Code: {response.status_code}")


if __name__ == "__main__":
    print(get_trustlevel_from_content("Israel’s deadly bombardm"))