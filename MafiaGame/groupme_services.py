import requests
import json


# Sends a message to a Groupme group and returns response
def send_message(botid, message, image_url = None) :
    url = "https://api.groupme.com/v3/bots/post"
    data = {"text": message, "bot_id": botid}
    if (image_url != None) :
        data["attachments"] = [{"type" : "image", "url" : image_url }]

    json_data = json.dumps(data);
    print(json_data)
    return requests.post(url, json_data)

# Returns URL of uploaded image on success
def upload_image(auth_token, filepath) :
    url = "https://image.groupme.com/pictures"
    header = {"X-Access-Token":auth_token, "Content-Type":"image/jpeg"}
    with open(filepath,"rb") as data:
        data = data.read()
        #header = json.dumps(header)
        response = requests.post(url = url, data = data, headers = header)
        if response.status_code == 200:
            content = response.json()
            return(content["payload"]["url"])
        return(response) 
    return("failure")

def create_group(auth_token, name):
    url = "https://api.groupme.com/v3/groups"
    header = {"X-Access-Token":auth_token}
    data = {"name": name, "share": False}
    response = requests.post(url = url, data = json.dumps(data), headers = header)
    if response.status_code == 201:
        content = response.json()
        return content["response"]["id"]
    return response

# Members should be an array of dictionaries containing "nickname" and "phone_number" entries
def add_members(auth_token, groupid, members):
    url = f"https://api.groupme.com/v3/groups/{groupid}/members/add"
    header = {"X-Access-Token":auth_token}
    data = {"members":members}

    response = requests.post(url = url, data = json.dumps(data), headers = header)
    return response

# Retrieves metadata for a given group
def get_metadata(auth_token, groupid):
    url = f"https://api.groupme.com/v3/groups/{groupid}"
    header = {"X-Access-Token":auth_token}
    response = requests.get(url = url, headers = header)
    if response.status_code == 200:
        content = response.json()
        return content["response"]
    return response 

# Wrapper function for get_metadata that gets a dict of (id, name) pairs
def get_user_ids(auth_token, groupid):
    response = get_metadata(auth_token, groupid)
    # Makes sure request succeeded
    if type(response) != dict:
        return None
    
    members = response["members"]

    # Formats response nicely, but destroys avatar and muted data
    members = {member["user_id"]:member["nickname"] for member in members}
    return members

   
# Sends a get request for one set of messages
def get_messages(auth_token, group_id, before_id = None):
    url = f"https://api.groupme.com/v3/groups/{group_id}/messages"
    header = {"X-Access-Token":auth_token}
    data = {"limit":100}
    if before_id != None:
        data["before_id"] = before_id

    response = requests.get(url = url, headers = header, params = data)
    if response.status_code == 200:
        content = response.json()
        return content["response"]["messages"]
    return response 


def create_bot(auth_token, groupid, callback=None):
    url = "https://api.groupme.com/v3/bots"
    header = {"X-Access-Token":auth_token}
    data = {"bot": {"name":"Narrator", "group_id":groupid}}
    if callback is not  None:
        data["bot"]["callback_url"]=callback
    print(data)
    response = requests.post(url = url, data = json.dumps(data), headers = header)
    if response.status_code == 201:
        content = response.json()
        print("callback: "+content["response"]["bot"]["callback_url"])
        return content["response"]["bot"]["bot_id"]
    return response


