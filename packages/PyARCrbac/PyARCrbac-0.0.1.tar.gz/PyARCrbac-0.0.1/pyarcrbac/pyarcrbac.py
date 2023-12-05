import requests

URL = "http://127.0.0.1:40342/metadata/identity/oauth2/token?api-version=2019-11-01&resource=https%3A%2F%2Fmanagement.azure.com"

def get_challenge_token():
    """
    Retrieves the challenge token from the metadata service.
    """
    headers = {"Metadata": "true"}
    response = requests.get(URL, headers=headers)
    
    for item, data in response.headers.items():
        if item == "Www-Authenticate":
            return data.split("=")[1]
    
    raise Exception("Failed to retrieve challenge token")
        
def get_access_token(challenge_token_path):
    """
    Retrieves the access token using the challenge token.
    """
    with open(challenge_token_path, "r") as file:
        header = {"Metadata": "true", "Authorization": f"Basic {file.read()}"}
    response = requests.get(URL, headers=header)
    return response.json()['access_token']

def retrieve_token():
    """
    Retrieves the access token by first getting the challenge token and then using it to get the access token.
    If failed returns no date
    """
    challenge_token = get_challenge_token()
    return get_access_token(challenge_token)