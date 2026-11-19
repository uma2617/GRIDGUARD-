import pandas as pd
import numpy as np
import os

np.random.seed(42)
os.makedirs("data/raw", exist_ok=True)

n = 5000
dates = pd.date_range("2024-01-01", periods=n, freq="h")

df = pd.DataFrame({
    "timestamp": dates,
    "solar_kw": np.clip(np.random.normal(50, 20, n) * np.sin(np.linspace(0, 100, n))**2 + 30, 0, 100),
    "wind_kw": np.clip(np.random.normal(40, 15, n), 0, 90),
    "load_kw": np.clip(np.random.normal(80, 20, n), 30, 140),
    "battery_soc": np.clip(np.random.normal(60, 15, n), 10, 95),
    "grid_freq": np.random.normal(50.0, 0.05, n),
    "voltage": np.random.normal(230, 5, n),
    "temperature": np.random.normal(28, 5, n),
})

# fault label: 1 if voltage low or freq off
df["fault"] = ((df["voltage"] < 220) | (df["grid_freq"] < 49.9) | (df["grid_freq"] > 50.1)).astype(int)

df.to_csv("data/raw/gpvs_data.csv", index=False)
print(f"Created {len(df)} rows")
print(df.head())