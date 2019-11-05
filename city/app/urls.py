from django.contrib import admin
from django.urls import path, include
from .views import googleMap, processDataWeather, processDataHole, displayHole, searchHole, searchHoleDetail, processDataWeatherPredict

urlpatterns = [
    path('map',googleMap),
    path('processDataWeather', processDataWeather),
    path('processDataHole', processDataHole),
    path('processDataWeatherPredict', processDataWeatherPredict),
    path('displayHole',displayHole),
    path('searchHole', searchHole),
    path('searchHoleDetail', searchHoleDetail),
]
