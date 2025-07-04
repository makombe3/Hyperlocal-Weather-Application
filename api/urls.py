from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherReportViewSet, predict_rain, get_weather_prediction

router = DefaultRouter()
router.register(r'weather-reports', WeatherReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('predict/', predict_rain, name='predict-rain'),
    path('weather-prediction/', get_weather_prediction, name='weather-prediction'),
]
