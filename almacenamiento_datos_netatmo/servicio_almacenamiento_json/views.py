import threading
import time
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import requests
from .models import DashboardData, Device, Place, Users
from .services.netatmo_client import NetatmoClient

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
<<<<<<< HEAD
        
    try:
        usuario = Users.objects.get(mail=response_json['body']['user']['mail'])
    except Users.DoesNotExist:
        usuario = Users.objects.create(
            mail = response_json['body']['user']['mail'],
            lang = response_json['body']['user']['administrative']['lang'],
            reg_locale = response_json['body']['user']['administrative']['reg_locale'],
            country = response_json['body']['user']['administrative']['country'],
            unit = response_json['body']['user']['administrative']['unit'],
            windunit = response_json['body']['user']['administrative']['windunit'],
            pressureunit = response_json['body']['user']['administrative']['pressureunit'],
            feel_like_algo = response_json['body']['user']['administrative']['feel_like_algo']
        )

=======

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
>>>>>>> mario

    for data in response_json['body']['devices']:
        lugar_data = data['place']
        lugar, _ = Place.objects.get_or_create(
            altitude=lugar_data['altitude'],
            country=lugar_data['country'],
            timezone=lugar_data['timezone'],
            location=str(lugar_data['location']),
        )

<<<<<<< HEAD
        try: 
            dispositivo = Device.objects.get(_id=data['_id'])

            lugar = Place.objects.create(
                altitude= data['place']['altitude'],
                country = data['place']['country'],
                timezone= data['place']['timezone'],
                location= str(data['place']['location']),
            )
        except Device.DoesNotExist:
    
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

        if DashboardData.DoesNotExist:
            return HttpResponse('Dispocitivo no existe')
        else:
            DashboardData.objects.create(
                device = dispositivo,
                time_utc = data['dashboard_data']['time_utc'],
                temperature = data['dashboard_data']['Temperature'],
                co2 = data['dashboard_data']['CO2'],
                humidity = data['dashboard_data']['Humidity'],
                noise = data['dashboard_data']['Noise'],
                pressure = data['dashboard_data']['Pressure'],
                absolutePressure = data['dashboard_data']['AbsolutePressure'],
                health_idx = data['dashboard_data']['health_idx']
            )

=======
        dispositivo, created = Device.objects.get_or_create(
            _id=data['_id'],
            defaults={
                'user': usuario,
                'place': lugar,
                'date_setup': data.get('date_setup'),
                'last_setup': data.get('last_setup'),
                'device_type': data.get('type'),
                'last_status_store': data.get('last_status_store'),
                'firmware': data.get('firmware'),
                'last_upgrade': data.get('wifi_status'),
                'wifi_status': data.get('wifi_status'),
                'reachable': data.get('reachable'),
                'co2_calibrating': data.get('co2_calibrating'),
                'station_name': data.get('station_name'),
                'read_only': True,
                'data_type': str(data.get('data_type')),
                'subtype': data.get('subtype'),
            }
        )

        # Verifica si 'dashboard_data' está presente antes de intentar acceder a las claves específicas
        if 'dashboard_data' in data:
            dashboard_data = data['dashboard_data']
            
            # Verifica si los datos del dashboard son diferentes a los existentes
            if not DashboardData.objects.filter(
                device=dispositivo,
                time_utc=dashboard_data.get('time_utc'),
                temperature=dashboard_data.get('Temperature'),
                co2=dashboard_data.get('CO2'),
                humidity=dashboard_data.get('Humidity'),
                noise=dashboard_data.get('Noise'),
                pressure=dashboard_data.get('Pressure'),
                absolutePressure=dashboard_data.get('AbsolutePressure'),
                health_idx=dashboard_data.get('health_idx')
            ).exists():
                DashboardData.objects.create(
                    device=dispositivo,
                    time_utc=dashboard_data.get('time_utc'),
                    temperature=dashboard_data.get('Temperature'),
                    co2=dashboard_data.get('CO2'),
                    humidity=dashboard_data.get('Humidity'),
                    noise=dashboard_data.get('Noise'),
                    pressure=dashboard_data.get('Pressure'),
                    absolutePressure=dashboard_data.get('AbsolutePressure'),
                    health_idx=dashboard_data.get('health_idx')
                )

>>>>>>> mario
    return HttpResponse('datos almacenados')

