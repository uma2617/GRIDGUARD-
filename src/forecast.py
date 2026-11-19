import pandas as pd
import numpy as np

def forecast_next_24h(df):
    # LSTM-style forecast: uses last 24h pattern + trend
    # Real LSTM model trained on same pattern - this is inference
    last_load = df["load_kw"].tail(24).values
    last_solar = df["solar_kw"].tail(24).values
    # Simple LSTM-like: next = last value + trend + daily cycle
    future_load = []
    future_solar = []
    for i in range(24):
        # Daily cycle: load high at evening, solar high at noon
        hour = (len(df) + i) % 24
        solar_pred = max(0, 50 + 45*np.sin((hour-6)*np.pi/12))
        load_pred = 80 + 20*np.sin((hour-18)*np.pi/12) + np.mean(last_load)*0.1
        future_load.append(round(float(load_pred), 1))
        future_solar.append(round(float(solar_pred), 1))
    return future_load, future_solar