import requests
import json


# Sends a message to a Groupme group and returns response
def send_message(message, botid) :
    url = "https://api.groupme.com/v3/bots/post"
    data = {"text": message, "bot_id": botid}
    json_data = json.dumps(data);
    return requests.post(url, json_data)
