import requests


class Oauth:
    def __init__(self):
        f = open('.userconfig.txt', 'r')
        contents = f.readline().split(',')
        f.close()
        self._secret = contents[0]
        self._client = contents[1]
        self._username = contents[2]
        self._password = contents[3]
        self.access_token_url = 'https://www.reddit.com/api/v1/access_token'

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
        return headers