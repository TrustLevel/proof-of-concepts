import json
import os

from dotenv import load_dotenv

load_dotenv("../.env")
load_dotenv(".env")

import requests

api_key = os.getenv("TRUSTLEVEL_API_KEY")

def get_trustlevel_from_content(content: str):
    url = "https://2q2ffhhelb.execute-api.eu-west-1.amazonaws.com/v1/trustlevels/"
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
            return {"error": f"No trust level key found in response. Response: {response_data}", "status_code": response.status_code}
    else:
        return {"error": f"Failed to get trust level: {response.reason}", "status_code": response.status_code}