from django.core.management.base import BaseCommand
from api.models import WeatherReport
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import joblib
import os
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'rain_model.h5')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'scaler.pkl')

class Command(BaseCommand):
    help = 'Retrain the LSTM rainfall prediction model using all WeatherReport entries.'

    def handle(self, *args, **kwargs):
        qs = WeatherReport.objects.all().order_by('datetime')
        if qs.count() < 8:
            self.stdout.write(self.style.ERROR('Not enough data to retrain (need at least 8 records).'))
            return
        df = pd.DataFrame(list(qs.values()))
        features = ['precipitation','humidity','cloudcover','tempmin','temp','dew','windspeed','winddir','sealevelpressure','precipcover']
        X = df[features].values
        y = df['rain'].astype(float).values
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        X_seq = []
        y_seq = []
        seq_len = 7
        for i in range(len(X_scaled) - seq_len):
            X_seq.append(X_scaled[i:i+seq_len])
            y_seq.append(y[i+seq_len])
        X_seq = np.array(X_seq)
        y_seq = np.array(y_seq)
        model = Sequential([
            LSTM(32, input_shape=(seq_len, X_seq.shape[2])),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model.fit(X_seq, y_seq, epochs=10, batch_size=8, verbose=1)
        model.save(MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)
        self.stdout.write(self.style.SUCCESS('Model and scaler retrained and saved.'))
