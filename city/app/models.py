from django.db import models

# Create your models here.

class weather(models.Model):
    '''
    溫度、最高溫、最低溫、露點溫度、相對濕度、最小相對濕度、降雨量、最大十分鐘降雨量、最大六十分鐘降雨量
    '''
    date = models.DateTimeField()
    temperature = models.FloatField()
    relativeHumidity = models.FloatField()
    rainfall = models.FloatField()
    maxTenMinuteRainFall = models.FloatField()
    maxSixtyMinuteRainFall = models.FloatField()

class hole(models.Model):
    '''
    區、經度、緯度、時間、原因、住址、淹水潛勢
    '''
    town = models.CharField(max_length=5)
    positionLon = models.FloatField()
    positionLat = models.FloatField()
    occurTime = models.DateTimeField()
    reason = models.CharField(max_length=50,blank=True)
    address = models.CharField(max_length=100,blank=True)
    flood = models.IntegerField()

class examination(models.Model):
    '''
    巡視結果
    '''
    positionLon = models.FloatField()
    positionLat = models.FloatField()
    examinationTime = models.DateTimeField(auto_now=True)
    photoURL = models.CharField(max_length=100,blank=True)

