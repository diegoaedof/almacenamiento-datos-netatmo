from django.http import HttpRequest
from django.shortcuts import render, redirect
import requests
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

    return redirect()

def deserializer(request):

    data = client.get_homecoach_data(request.session['access_token'])
