import threading
import time
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import requests
from .models import DashboardData, Device, Place, Users
from .services.netatmo_client import NetatmoClient
from datetime import datetime


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
from django.db import transaction


@transaction.atomic
def deserialize(request):
    token = request.session['access_token']

    response_json = client.get_homecoach_data(token)

    usuario_data = response_json['body']['user']['administrative']

    usuario, created = Users.objects.get_or_create(
        mail=response_json['body']['user']['mail'],
        defaults={
            'lang': usuario_data['lang'],
            'reg_locale': usuario_data['reg_locale'],
            'country': usuario_data['country'],
            'unit': usuario_data['unit'],
            'windunit': usuario_data['windunit'],
            'pressureunit': usuario_data['pressureunit'],
            'feel_like_algo': usuario_data['feel_like_algo'],
        }
    )

    for data in response_json['body']['devices']:
        lugar_data = data['place']
        lugar, _ = Place.objects.get_or_create(
            altitude=lugar_data['altitude'],
            country=lugar_data['country'],
            timezone=lugar_data['timezone'],
            location=str(lugar_data['location']),
        )


        try: 
            dispositivo = Device.objects.get(_id=data['_id'])
        except Device.DoesNotExist:
                 
            lugar = Place.objects.create(
                altitude= data['place']['altitude'],
                country = data['place']['country'],
                timezone= data['place']['timezone'],
                location= str(data['place']['location']),
            )
        
            id=data['_id']
            if id == Device:
                pass
            else:
                dispositivo = Device.objects.create(
                    user = usuario,
                    place = lugar,
                    _id = data['_id'],
                    date_setup = data['date_setup'],
                    last_setup = data['last_setup'],
                    device_type= data['type'],
                    last_status_store = data['last_status_store'],
                    firmware = data['firmware'],
                    last_upgrade = data['wifi_status'],
                    wifi_status = data['wifi_status'],
                    reachable = data['reachable'],
                    co2_calibrating = data['co2_calibrating'],
                    station_name = data['station_name'],
                    read_only = True,
                    data_type = str(data['data_type']),
                    subtype = data['subtype'],
                )

    timestamp = data['dashboard_data']['time_utc'] #se guardael dato entregado en formato time_utc, ej:1706403169
    time_utc_datetime = datetime.utcfromtimestamp(timestamp) #se importa el modulo datetime para realizar la transformación con el metodo correspondiente
    DashboardData.objects.create(
            device=dispositivo,
            time_utc=time_utc_datetime, # se almacena dato transformado
            temperature=data['dashboard_data']['Temperature'],
            co2=data['dashboard_data']['CO2'],
            humidity=data['dashboard_data']['Humidity'],
            noise=data['dashboard_data']['Noise'],
            pressure=data['dashboard_data']['Pressure'],
            absolutePressure=data['dashboard_data']['AbsolutePressure'],
            health_idx=data['dashboard_data']['health_idx']
        )
                

    return HttpResponse('datos almacenados')

