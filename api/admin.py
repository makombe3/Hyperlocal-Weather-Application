from django.contrib import admin
from .models import WeatherReport

@admin.register(WeatherReport)
class WeatherReportAdmin(admin.ModelAdmin):
    list_display = (
        'datetime', 'location', 'precipitation', 'humidity', 'cloudcover', 'tempmin', 'temp', 'dew',
        'windspeed', 'winddir', 'sealevelpressure', 'precipcover', 'rain', 'comment'
    )
    search_fields = ('location', 'comment')
    list_filter = ('location', 'rain', 'datetime')
