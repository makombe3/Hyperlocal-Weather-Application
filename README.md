# Project 3: Rainfall Prediction Web App

This project is a full-stack web application for rainfall prediction using a machine learning model. It includes a Django backend, a React frontend, and a pre-trained Keras model.

## Features
- Predict rainfall using weather data
- Django REST API backend
- React-based frontend
- Pre-trained ML model (`rain_model.h5`)
- Data scaler (`scaler.pkl`)

## Getting Started

### Backend (Django)
1. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```sh
   python manage.py migrate
   ```
3. Start the backend server:
   ```sh
   python manage.py runserver
   ```

### Frontend (React)
1. Navigate to the `frontend` folder:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the frontend server:
   ```sh
   npm start
   ```

## Model Training
- The model was trained and evaluated in Google Colab. See the notebook link in `Google colab Model training-evaluating.md`.

## Files
- `requirements.txt` — Python dependencies
- `rain_model.h5` — Trained Keras model
- `scaler.pkl` — Data scaler for preprocessing
- `db.sqlite3` — SQLite database (can be deleted for a fresh start)
- `frontend/package.json` — Frontend dependencies

## License
Specify your license here.
