import os
import csv
import json
import base64
import requests
import pandas as pd

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


# method to request freshdesk and download data on csv file
@app.get("/hello_world")
def hello_world():
    """
    hello world! post.
    """
    url = 'https://ocasasupport.freshdesk.com/api/v2/agents?per_page=100'
    apikey = "SXWwkGJZcbTKibkjiv"
    encodedBytes = base64.b64encode(apikey.encode("utf-8"))
    encodedStr = str(encodedBytes,"utf-8")
    
    headers = { 
        "Accept": "application/json", 
        "Authorization": "Basic "+ encodedStr
    }
    
    response = requests.get(url, headers=headers)

    json_response = []
    for freshdesk_user in response.json():
        freshdesk_user.pop("signature")
        json_response.append(freshdesk_user)


    # response to json file
    with open("freshdesk_users.json", "w") as json_file:
        json.dump(json_response, json_file)

    # json file to csv
    json_file = pd.read_json("freshdesk_users.json")
    json_file.to_csv("freshdeskUsers.csv", index = None)

    return response.json()