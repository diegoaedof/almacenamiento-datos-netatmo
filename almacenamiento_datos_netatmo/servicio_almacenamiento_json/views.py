from django.shortcuts import render, redirect
from django.http import HttpRequest
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




