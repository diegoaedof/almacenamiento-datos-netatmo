import requests
from ..credentials import credentials
import time


class NetatmoClient:

    def __init__(self):
        self.client_id = credentials.client_id
        self.client_secret = credentials.client_secret
        self.scope = "read_homecoach"
        self.access_token = None
        self.refresh_token_ = None
        self.expires_in = None
        self.redirect_uri = "localhost:8000"  # cambiar por la url de la vista que corresponda.
        self.data = None

    def login(self):
        url = "https://api.netatmo.com/oauth2/authorize?"
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope,
            'state': "sd1dfs2dfdg12154dfs"  # cambiar por un generador random de strings
        }

        headers = {}

        return requests.post(url, headers=headers, params=params)

    def get_access_token(self, code):
        headers = {
            'Host': 'api.netatmo.com',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope,
        }

        response_json = requests.post('/oauth2/token', headers=headers, data=data).json()

        self.access_token = response_json['access_token']
        self.refresh_token_ = response_json['refresh_token']
        self.expires_in = int(response_json['expires_in']) + time.time()

        return

    def refresh_token(self):

        if self.expires_in < time.time():
            headers = {
                'Host': 'api.netatmo.com',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            }

            data = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token_,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }

            response = requests.post('/oauth2/token', headers=headers, data=data).json()

            self.access_token = response['access_token']
            self.refresh_token_ = response['refresh_token']
            self.expires_in = int(response['expires_in']) + time.time()

            print("Se ha actualizado el token")

            return response

        return

