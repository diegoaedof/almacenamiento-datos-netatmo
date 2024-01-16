from django.shortcuts import render, redirect
from .netatmo.NetatmoClient import NetatmoClient

netatmo = NetatmoClient()


def index(request):
    return redirect(netatmo.login())




# Create your views here.
