from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
import requests
from .models import DashboardData, Device, Place, Users
from services.netatmo_client import NetatmoClient

client = NetatmoClient()


def index(request):
    return redirect(client.login())


def authorize(request: HttpRequest):
    state = request.GET.get('state')
    code = request.GET.get('code')

    if request.GET.get('error') is not None:
        return redirect('index')  # configurar urls.py

    client.get_access_token(code)

    request.session['access_token'] = client.access_token
    request.session['refresh_token'] = client.refresh_token_

    return redirect('deserialize')


'''BENJA DEBE TRABAJAR EN DESERIALIZE'''
def deserialize(request):
    token = request.session['access_token']

    response_json = client.get_homecoach_data(token)

    usuario = Users.objects.create(
        mail = data['mail'],
        lang = data['lang'],
        reg_locale = data['reg_locale'],
        country = data['country'],
        unit = data['unit'],
        windunit = data['windunit'],
        pressureunit = data['pressureunit'],
        feel_like_algo = data['feel_like_algo']
    )



    for data in response_json['body']['devices']:

        lugar = Place.objects.create(
            altitude= data['place']['altitude'],
            country = data['place']['country'],
            timezone= data['place']['timezone'],
            location= ,#transformr a texto
        )

        dispositivo = Device.objects.create(
            user = usuario,
            place = lugar,
            _id = data['_id'],
            date_setup = data['date_setup'],
            last_setup = data['last_setup'],
            type_ = data['type'],
            last_status_store = data['last_status_store'],
            firmware = data['firmware'],
            last_upgrade = data[''],
            wifi_status = data['wifi_status'],
            reachable = data['reachable'],
            co2_calibrating = data['co2_calibrating'],
            station_name = data['station_name'],
            read_only = True,
            data_type = ,#transformar texto
            subtype = data['subtype'],
        )


        DashboardData.objects.create(
            data_id = data['_id'],
            device = dispositivo,
            time_utc = data['time_utc'],
            temperature = data['Temperature'],
            co2 = data['CO2'],
            humidity = data['Humidity'],
            noise = data['Noise'],
            pressure = data['Pressure'],
            absolutePressure = data['AbsolutePressure'],
            health_idx = data['health_idx']
        )


