from rest_framework import serializers
from .models import WeatherReport, NEIGHBORHOODS

class WeatherReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherReport
        fields = '__all__'

class RainPredictionSerializer(serializers.Serializer):
    location = serializers.ChoiceField(choices=NEIGHBORHOODS)
    rain_chance = serializers.FloatField()
