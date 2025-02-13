import requests
import json
import base64
import os

CLIENT_ID = os.getenv('CLIENT_ID', 'CIC_E_REST_APPS')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = "https://cic-apps-dev.datascience.columbia.edu/v1"
OAUTH_TOKEN_URL = os.getenv('OAUTH_URL')

def refresh_token():
    '''refresh existing token for a new one'''
    with open('creds.json', 'r') as f:
        creds = json.load(f)

    refresh_token = creds.get('refresh_token', os.getenv('REFRESH_TOKEN'))
    base64_encoded_clientid_clientsecret = base64.b64encode(str.encode(f'{CLIENT_ID}:{CLIENT_SECRET}'))  # concatenate with : and encode in base64
    base64_encoded_clientid_clientsecret = base64_encoded_clientid_clientsecret.decode('ascii')  # turn bytes object into ascii string

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': f'Basic {base64_encoded_clientid_clientsecret}'
    }

    data = {
        'grant_type': 'refresh_token',
        'redirect_uri': REDIRECT_URI,
        'refresh_token': refresh_token
    }

    r = requests.post(OAUTH_TOKEN_URL, headers=headers, data=data)
    response = r.json()

    if response.get('access_token'):
        os.environ["ACCESS_TOKEN"] = response.get('access_token')
        os.environ["REFRESH_TOKEN"] = response.get('refresh_token')

        with open('creds.json', 'w') as f:
            json.dump(response, f, indent=4)
    else:
        print('There was an error refreshing your access token')
        print(r.text)


if __name__ == '__main__':
    refresh_token()  # refresh an existing token (assuming you have one stored in creds.json)
