from django.contrib import admin
from django.urls import path, include
from .views import googleMap, processDataWeather, processDataHole, displayHole, searchHole

urlpatterns = [
    path('map',googleMap),
    path('processDataWeather', processDataWeather),
    path('processDataHole', processDataHole),
    path('displayHole',displayHole),
    path('searchHole', searchHole),
]
