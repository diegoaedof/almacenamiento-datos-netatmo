from django.db import models


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    mail = models.EmailField()
    lang = models.CharField(max_length=255)
    reg_locale = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    windunit = models.IntegerField()
    pressureunit = models.IntegerField()
    feel_like_algo = models.IntegerField()

class Place(models.Model):
    place_id = models.AutoField(primary_key=True)
    altitude = models.IntegerField()
    country = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    _id = models.CharField(max_length=17, unique=True)
    date_setup = models.BigIntegerField()
    last_setup = models.BigIntegerField()
    type_ = models.CharField(max_length=255)
    last_status_store = models.BigIntegerField()
    firmware = models.IntegerField()
    last_upgrade = models.IntegerField()
    wifi_status = models.IntegerField()
    reachable = models.BooleanField()
    co2_calibrating = models.BooleanField()
    station_name = models.CharField(max_length=255)
    read_only = models.BooleanField()
    data_type = models.CharField(max_length=255)
    subtype = models.CharField(max_length=5)


class DashboardData(models.Model):
    data_id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time_utc = models.BigIntegerField()
    temperature = models.FloatField()
    co2 = models.IntegerField()
    humidity = models.IntegerField()
    noise = models.IntegerField()
    pressure = models.FloatField()
    absolutePressure = models.FloatField()
    health_idx = models.IntegerField()
