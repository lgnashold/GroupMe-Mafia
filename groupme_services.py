import requests
import json


# Sends a message to a Groupme group and returns response
def send_message(botid, message) :
    url = "https://api.groupme.com/v3/bots/post"
    data = {"text": message, "bot_id": botid}
    json_data = json.dumps(data);
    return requests.post(url, json_data)

def upload_image(auth_token, filepath) :
    url = "https://image.groupme.com/pictures"
    unencodedJSON = {"X-Access-Token":auth_token, "Content-Type":"image/jpeg"}
    with open(filepath,"rb").read() as data:
        response = requests.post(url=url, data = data)
        if response.status_code == 200:
            content = response.json()
            return(content)
        return(response) 
