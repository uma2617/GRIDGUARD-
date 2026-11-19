# app/api/main.py
from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI(title="GridGuard API")

model = joblib.load("models/gridguard_model.pkl")
features = joblib.load("models/features.pkl")

@app.get("/")
def home():
    return {"status": "GridGuard API running"}

@app.post("/predict")
def predict(data: dict):
    # data = {"load_kw": 38, "solar_kw": 10, "wind_kw": 7, "temperature": 18, "voltage": 214, "battery_soc": 16, "grid_freq": 49.85}
    # For single point, lag/rolling = current value, ramp = 0
    row = {
        "load_kw": data["load_kw"],
        "solar_kw": data["solar_kw"],
        "wind_kw": data["wind_kw"],
        "temperature": data["temperature"],
        "voltage": data["voltage"],
        "battery_soc": data["battery_soc"],
        "grid_freq": data["grid_freq"],
        "load_lag_1": data["load_kw"],
        "load_rolling_3h": data["load_kw"],
        "solar_ramp": 0,
        "load_minus_solar": data["load_kw"] - data["solar_kw"],
    }
    X = pd.DataFrame([row])[features]
    proba = float(model.predict_proba(X)[0, 1])
    pred = int(proba > 0.7)
    return {
        "fault": pred,
        "fault_probability": round(proba, 3),
        "risk": "HIGH" if proba > 0.7 else "LOW" if proba < 0.3 else "MEDIUM"
    }

@app.get("/forecast")
def forecast(hours: int = 24):
    return {"hours": hours, "message": "Forecast endpoint - connect to forecast.py in Step 3.2"}

@app.get("/report")
def report():
    return {"message": "Report endpoint - connect to report.py in Step 3.2"}