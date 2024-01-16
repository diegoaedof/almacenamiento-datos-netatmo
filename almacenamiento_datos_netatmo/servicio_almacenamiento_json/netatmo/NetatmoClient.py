import os
from pprint import pprint
import requests
from main.utils.utils import get_random_string, Device, DashboardData, mensajes, update_ago, health_index_state_color, \
    wifi_status, id_format
import time
import urllib.parse, urllib.request
import json
from ..credentials import credentials
from main.models import DeviceModel, Patient


# This class is to manage the Netatmo API
class NetatmoClient:
    def __init__(self):
        self.client_id = credentials.client_id
        self.client_secret = credentials.client_secret
        self.token = None
        self.refresh_token = None
        self.expires_in = None
        self.data = None
        self.redirect_uri = 'http://127.0.0.1:8000/autorize'

    def login(self):
        payload = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'read_homecoach',
            'state': get_random_string(),
        }

        headers = {}
        return requests.post('https://api.netatmo.com/oauth2/authorize', headers=headers, params=payload).url

    def access_token(self, code):

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;chartset=UTF-8'}

        params = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'scope': 'read_homecoach',
        }

        response = requests.post('https://api.netatmo.com/oauth2/token', headers=headers, data=params)

        rjson = response.json()
        self.token = rjson['access_token']
        self.refresh_token = rjson['refresh_token']
        self.expires_in = int(rjson['expires_in'] + time.time())

        return rjson

    def refresh_token(self):
        if self.expires_in < time.time():  # Token should be renewed
            print("token should be renewed")
            postParams = {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }

            def postRequest(url, params):
                req = urllib.request.Request(url)
                req.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
                params = urllib.parse.urlencode(params)
                resp = urllib.request.urlopen(req, params).read()

                return json.loads(resp)

            resp = postRequest('https://api.netatmo.com/oauth2/token', postParams)
            self.access_token = resp['access_token']
            self.refresh_token = resp['refresh_token']
            self.expiration = int(resp['expire_in'] + time.time())

            print(self.access_token)
        return self.access_token

    def get_data(self, token):
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.get('https://api.netatmo.com/api/gethomecoachsdata', headers=headers, )
        rjson = response.json()
        self.data = rjson

        return rjson

    '''
    def deserialize_devices(self, j):
        # pprint(j)
        devices = []
        for device in j:
            # pprint(device)
            if device['reachable']:
                dashboardata = DashboardData(json.dumps(device['dashboard_data']))
            else:
                dashboardata = DashboardData(json.dumps({
                    "time_utc": 1555677739,
                    "Temperature": 23.7,
                    "CO2": 967,
                    "Humidity": 41,
                    "Noise": 42,
                    "Pressure": 45,
                    "AbsolutePressure": 1022.9,
                    "health_idx": 1,
                    "min_temp": 21.2,
                    "max_temp": 27.4,
                    "date_max_temp": 1555662436,
                    "date_min_temp": 1555631374
                }))
            print(dashboardata)
            deviceObj = Device(json.dumps(device))
            deviceObj.dashboard_data = dashboardata

            deviceObj.id = deviceObj._id
            deviceObj.id_front = id_format(deviceObj.id)
            deviceObj.last_status_store = update_ago(deviceObj.last_status_store)
            deviceObj.health_state, deviceObj.health_color = health_index_state_color(
                deviceObj.dashboard_data.health_idx)
            deviceObj.wifi_message, deviceObj.wifi_idx, deviceObj.wifi_color = wifi_status(deviceObj.wifi_status)
            # ----------------------------------------------------------------------
            deviceObj.relato = mensajes(deviceObj.dashboard_data)
            deviceObj.patients = list(Patient.objects.filter(device=deviceObj._id).values().all())
            print(vars(deviceObj))

            print('sssssssssssssss')
            print(deviceObj.station_name)
            print(deviceObj.patients)
            # print(qs_patients)
            # print(qs_list)
            print('sssssssssssssss')

            model_devices = DeviceModel.objects.all()
            mac_adds = []
            for device in model_devices:
                mac_adds.append(device.mac_ad)

            if deviceObj.id not in mac_adds:
                DeviceModel.objects.create(mac_ad=deviceObj.id, station_name=deviceObj.station_name)
            # -----------------------------------------------------------------------
            devices.append(deviceObj)
            # print(vars(deviceObj))
            # print(vars(deviceObj.dashboard_data))
        return devices
'''












