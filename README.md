
# Project 3: Rainfall Prediction Web App

## Description
This project is a full-stack web application that predicts rainfall based on weather data using a machine learning model. The backend is built with Django and exposes a REST API, while the frontend is developed with React for user interaction. The machine learning model (Keras) and scaler are pre-trained and included in the repository. This setup allows users to input weather data and receive rainfall predictions instantly.

### Key Components
- **Django Backend:** Handles API requests, model inference, and data processing.
- **React Frontend:** User interface for submitting data and viewing predictions.
- **Pre-trained Model:** Keras model (`rain_model.h5`) and scaler (`scaler.pkl`) for predictions.

## Features
- Predict rainfall using weather data
- Django REST API backend
- React-based frontend
- Pre-trained ML model (`rain_model.h5`)
- Data scaler (`scaler.pkl`)


## Getting Started & Configuration

To set up and run this project on your PC after downloading:

### 1. Clone the Repository
Clone the project from GitHub:
```sh
git clone <your-repo-url>
cd "project 3 - Copy (2)"
```

### 2. Backend Setup (Django)
1. (Optional but recommended) Create and activate a virtual environment:
   ```sh
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
2. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```sh
   python manage.py migrate
   ```
4. Start the backend server:
   ```sh
   python manage.py runserver
   ```

### 3. Frontend Setup (React)
1. Navigate to the `frontend` folder:
   ```sh
   cd frontend
   ```
2. Install frontend dependencies:
   ```sh
   npm install
   ```
3. Start the frontend server:
   ```sh
   npm start
   ```

### 4. Using the App
- Open your browser and go to `http://localhost:3000` to access the frontend.
- The backend API will be running at `http://localhost:8000`.
- Enter weather data in the form and submit to get rainfall predictions.

### 5. Notes
- If you want to retrain the model, refer to the Google Colab notebook linked below.
- The `db.sqlite3` file is included for convenience; you can delete it to start with a fresh database.

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
