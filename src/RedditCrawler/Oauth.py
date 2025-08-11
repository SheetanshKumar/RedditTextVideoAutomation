import requests

from dotenv import load_dotenv
import os



class Oauth:
    def __init__(self):
        load_dotenv()
        self._client = os.getenv('REDDIT_CLIENT_ID')
        self._secret = os.getenv('REDDIT_CLIENT_SECRET')
        self._username = os.getenv('REDDIT_USERNAME')
        self._password = os.getenv('REDDIT_PASSWORD')
        self.access_token_url = 'https://www.reddit.com/api/v1/access_token'

    def get_auth_details(self):
        return {
            "client_id": self._client,
            "client_secret": self._secret,
            "username": self._username,
            "password": self._password
        }

    def get_headers_after_auth(self):
        # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
        auth = requests.auth.HTTPBasicAuth(self._client,  self._secret)
        # here we pass our login method (password), username, and password
        data = {'grant_type': 'password',
                'username': self._username,
                'password': self._password}

        # setup our header info, which gives reddit a brief description of our app
        headers = {'User-Agent': 'MyBot/0.0.1'}

        # send our request for an OAuth token
        res = requests.post(self.access_token_url, auth=auth, data=data, headers=headers)
        # convert response to JSON and pull access_token value
        TOKEN = res.json()['access_token']

        # add authorization to our headers dictionary
        headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
        # print(headers)
        return headers