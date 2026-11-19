def get_explanation(solar, wind, load, soc, freq, volt, temp, model):
    importances = model.feature_importances_
    features = ["Solar", "Wind", "Load", "Battery SOC", "Frequency", "Voltage", "Temp"]
    values = [solar, wind, load, soc, freq, volt, temp]
    scores = []
    for f, imp, val in zip(features, importances, values):
        scores.append((f, round(float(imp)*100, 1), val))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores