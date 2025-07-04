from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import WeatherReport, NEIGHBORHOODS
from .serializers import WeatherReportSerializer, RainPredictionSerializer
import pandas as pd
import numpy as np
import requests
import joblib
from tensorflow.keras.models import load_model
import os
from django.conf import settings
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

MODEL_PATH = os.path.join(settings.BASE_DIR, 'rain_model.h5')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'scaler.pkl')
CSV_PATH = os.path.join(settings.BASE_DIR, 'Harare, Zimbabwe 2025-06-01 to 2025-06-08.csv')
OPENWEATHERMAP_API_KEY = 'c6aae916795b06e91525f15a178dffe3'

@method_decorator(csrf_exempt, name='dispatch')
class WeatherReportViewSet(viewsets.ModelViewSet):
    queryset = WeatherReport.objects.all().order_by('-datetime')
    serializer_class = WeatherReportSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        # User provides: location, rain flag, (optionally comment)
        user_data = request.data.copy()
        location = user_data.get('location')
        rain = user_data.get('rain')
        comment = user_data.get('comment', '')

        # Fetch weather features from OpenWeatherMap
        owm_url = f'https://api.openweathermap.org/data/2.5/weather?q=Harare,Zimbabwe&appid={OPENWEATHERMAP_API_KEY}&units=metric'
        owm = requests.get(owm_url).json()
        print('OpenWeatherMap API response (report):', owm)
        humidity = owm['main']['humidity']
        cloudcover = owm['clouds']['all']
        windspeed = owm['wind']['speed']
        winddir = owm['wind'].get('deg', 0.0)
        sealevelpressure = owm['main'].get('sea_level', owm['main']['pressure'])
        precipcover = 0.0  # Not directly available
        temp = owm['main']['temp']
        tempmin = owm['main']['temp_min']
        #dew = owm['main'].get('dew_point', 0.0)
        dew= 5.0 #place holder for dew


        # Compose full report data
        report_data = {
            'location': location,
            'precipitation': None,
            'humidity': humidity,
            'cloudcover': cloudcover,
            'tempmin': tempmin,
            'temp': temp,
            'dew': dew,
            'windspeed': windspeed,
            'winddir': winddir,
            'sealevelpressure': sealevelpressure,
            'precipcover': precipcover,
            'rain': rain,
            'comment': comment,
        }
        serializer = self.get_serializer(data=report_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@csrf_exempt
@api_view(['POST'])
def predict_rain(request):
    location = request.data.get('location')
    if location not in dict(NEIGHBORHOODS):
        return Response({'error': 'Invalid location'}, status=400)

    # Load last 7 days from CSV
    df = pd.read_csv(CSV_PATH)
    df = df[df['location'] == location].tail(7)

    # Fetch current weather from OpenWeatherMap
    owm_url = f'https://api.openweathermap.org/data/2.5/weather?q=Harare,Zimbabwe&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    owm = requests.get(owm_url).json()
    print('OpenWeatherMap API response:', owm)  # Debug print
    # Extract features
    features = {
        'precipitation': 0.0,  # OpenWeatherMap may not provide this directly
        'humidity': owm['main']['humidity'],
        'cloudcover': owm['clouds']['all'],
        'tempmin': owm['main']['temp_min'],
        'temp': owm['main']['temp'],
        'dew':  0.0,
        'windspeed': owm['wind']['speed'],
        'winddir': owm['wind'].get('deg', 0.0),
        'sealevelpressure': owm['main'].get('sea_level', owm['main']['pressure']),
        'precipcover': 0.0,  # Not directly available
    }
    today = {**features, 'location': location, 'datetime': datetime.now()}
    df = pd.concat([df, pd.DataFrame([today])], ignore_index=True)

    # Feature engineering
    df['temp_range'] = df['temp'] - df['tempmin']
    df['dew_point_spread'] = df['temp'] - df['dew']
    df['rain_yesterday'] = df['precipitation'].shift(1).fillna(0).apply(lambda x: 1 if x > 0 else 0)
    df['pressure_change'] = df['sealevelpressure'].diff().fillna(0)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['month'] = df['datetime'].dt.month
    df['season_flag'] = df['month'].apply(lambda m: 1 if m in [11,12,1,2,3] else 0)

    # Prepare input for model (include engineered features)
    X = df[['humidity','cloudcover','tempmin','temp','windspeed','winddir','sealevelpressure','precipcover',
            'temp_range','dew_point_spread','rain_yesterday','pressure_change','season_flag']].values
    scaler = joblib.load(SCALER_PATH)
    X_scaled = scaler.transform(X)
    X_scaled = np.expand_dims(X_scaled, axis=0)
    model = load_model(MODEL_PATH)
    y_pred = model.predict(X_scaled)[0][0]
    rain_chance = float(np.clip(y_pred, 0, 1)) * 100
    return Response({'location': location, 'rain_chance': round(rain_chance, 2)})

@csrf_exempt
@api_view(['GET'])
def get_weather_prediction(request):
    location = request.GET.get('location')
    if location not in dict(NEIGHBORHOODS):
        return Response({'error': 'Invalid location'}, status=400)

    # Load last 7 days from CSV
    df = pd.read_csv(CSV_PATH)
    df = df[df['location'] == location].tail(7)

    # Fetch current weather from OpenWeatherMap
    owm_url = f'https://api.openweathermap.org/data/2.5/weather?q=Harare,Zimbabwe&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    owm = requests.get(owm_url).json()
    print('OpenWeatherMap API response:', owm)  # Debug print
    # Extract features
    features = {
        'precipitation': 0.0,  # OpenWeatherMap may not provide this directly
        'humidity': owm['main']['humidity'],
        'cloudcover': owm['clouds']['all'],
        'tempmin': owm['main']['temp_min'],
        'temp': owm['main']['temp'],
        'dew':  0.0,
        'windspeed': owm['wind']['speed'],
        'winddir': owm['wind'].get('deg', 0.0),
        'sealevelpressure': owm['main'].get('sea_level', owm['main']['pressure']),
        'precipcover': 0.0,  # Not directly available
    }
    today = {**features, 'location': location, 'datetime': datetime.now()}
    df = pd.concat([df, pd.DataFrame([today])], ignore_index=True)

    # Feature engineering
    df['temp_range'] = df['temp'] - df['tempmin']
    df['dew_point_spread'] = df['temp'] - df['dew']
    df['rain_yesterday'] = df['precipitation'].shift(1).fillna(0).apply(lambda x: 1 if x > 0 else 0)
    df['pressure_change'] = df['sealevelpressure'].diff().fillna(0)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['month'] = df['datetime'].dt.month
    df['season_flag'] = df['month'].apply(lambda m: 1 if m in [11,12,1,2,3] else 0)

    # Prepare input for model (include engineered features)
    X = df[['humidity','cloudcover','tempmin','temp','windspeed','winddir','sealevelpressure','precipcover',
            'temp_range','dew_point_spread','rain_yesterday','pressure_change','season_flag']].values
    scaler = joblib.load(SCALER_PATH)
    X_scaled = scaler.transform(X)
    X_scaled = np.expand_dims(X_scaled, axis=0)
    model = load_model(MODEL_PATH)
    y_pred = model.predict(X_scaled)[0][0]
    rain_chance = float(np.clip(y_pred, 0, 1)) * 100
    return Response({'location': location, 'rain_chance': round(rain_chance, 2)})
