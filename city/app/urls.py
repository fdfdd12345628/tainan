from django.contrib import admin
from django.urls import path, include
from .views import googleMap, processDataWeather, processDataHole, displayHole, searchHole, searchHoleDetail, processDataWeatherPredict, downloadSplitData, showingPath, pastMap, showingPathAuto, statistic
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('map',googleMap),
    path('processDataWeather', processDataWeather),
    path('processDataHole', processDataHole),
    path('processDataWeatherPredict', processDataWeatherPredict),
    path('displayHole',displayHole),
    path('searchHole', searchHole),
    path('searchHoleDetail', searchHoleDetail),
    path('showingPath/<int:date>', showingPath),
    path('showingPath', showingPathAuto),
    path('statistic',statistic),
    path('downloadSplitData/<int:id>', downloadSplitData),
    path('pastMap',pastMap),
    path('serviceworker', (TemplateView.as_view(
      template_name="serviceworker.js",
      content_type='application/javascript',)),
      name='serviceworker'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
