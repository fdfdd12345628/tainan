from django.contrib import admin
from .models import hole, weather, examination, modelResult

# Register your models here.
admin.site.register(hole)
admin.site.register(weather)
admin.site.register(examination)
admin.site.register(modelResult)
