# src/models/train.py
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
import joblib

# 1. Load - YOUR real file
df = pd.read_csv("data/raw/gpvs_data.csv")
df = df.sort_values("timestamp")  # TIME split, NOT random

split = int(len(df) * 0.8)
train, test = df.iloc[:split].copy(), df.iloc[split:].copy()

# 2. Features - YOUR real column names
for d in [train, test]:
    d["load_lag_1"] = d["load_kw"].shift(1)
    d["load_rolling_3h"] = d["load_kw"].rolling(3).mean()
    d["solar_ramp"] = d["solar_kw"].diff()
    d["load_minus_solar"] = d["load_kw"] - d["solar_kw"]
train = train.dropna()
test = test.dropna()

features = ["load_kw", "solar_kw", "wind_kw", "temperature", "voltage",
            "battery_soc", "grid_freq",
            "load_lag_1", "load_rolling_3h", "solar_ramp", "load_minus_solar"]

X_train, y_train = train[features], train["fault"]
X_test, y_test = test[features], test["fault"]

# 3. Train - handles imbalance
model = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42)
model.fit(X_train, y_train)

# 4. Evaluate - NOT just Accuracy
pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]
print(f"Precision: {precision_score(y_test, pred):.3f}")
print(f"Recall: {recall_score(y_test, pred):.3f}")
print(f"F1: {f1_score(y_test, pred):.3f}")
print(f"ROC-AUC: {roc_auc_score(y_test, proba):.3f}")

# 5. Save - overwrite your old model
Path("artifacts").mkdir(exist_ok=True)
joblib.dump(model, "models/gridguard_model.pkl")
joblib.dump(features, "models/features.pkl")

# 6. Anomaly - train on NORMAL only
normal = train[train["fault"] == 0]
iso = IsolationForest(contamination=0.05, random_state=42)
iso.fit(normal[features])
joblib.dump(iso, "models/anomaly.pkl")

# 7. Leaderboard
pd.DataFrame([{
    "model": "RandomForest",
    "precision": precision_score(y_test, pred),
    "recall": recall_score(y_test, pred),
    "f1": f1_score(y_test, pred),
    "roc_auc": roc_auc_score(y_test, proba)
}]).to_csv("artifacts/leaderboard.csv", index=False)
print("Saved: models/gridguard_model.pkl + models/anomaly.pkl + artifacts/leaderboard.csv")