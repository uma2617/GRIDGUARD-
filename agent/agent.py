def grid_agent(solar, wind, load, soc, freq, volt, temp, pred):
    solutions = []
    actions = []
    risk = "LOW"
    reasoning = "Grid is stable. No action needed."

    if pred == 1:
        risk = "HIGH"
        reasoning = "Fault detected! AI Agent has created a recovery plan below."

        # SOLUTION 1 - Voltage Issue
        if volt < 220:
            actions.append("⚡ Voltage Low - Switch to Battery Backup")
            solutions.append({
                "problem": "⚡ Voltage Low (%.0fV) - Below 220V" % volt,
                "cause": "High load + Low solar generation",
                "solution": "1. Switch to Battery Backup within 2 sec | 2. Reduce non-critical load by 30% | 3. Start Diesel Generator as backup | 4. Check Solar Inverter connection"
            })

        # SOLUTION 2 - Frequency Issue
        if freq < 49.9 or freq > 50.1:
            actions.append("🔄 Frequency Unstable - Reduce Load")
            solutions.append({
                "problem": "🔄 Frequency Unstable (%.2f Hz)" % freq,
                "cause": "Generation != Load - Imbalance",
                "solution": "1. Shed 20% load immediately | 2. Increase Wind/Solar output | 3. Activate Battery to balance frequency | 4. Sync with main grid"
            })

        # SOLUTION 3 - Overload
        if load > 110:
            actions.append("🔥 Overload - Load Shedding Required")
            solutions.append({
                "problem": "🔥 Overload - Load %.0f kW too high" % load,
                "cause": "Peak hour demand exceeds generation",
                "solution": "1. Turn OFF AC / Heater for 15 min | 2. Shift load to off-peak | 3. Discharge Battery to support load | 4. Send alert to consumers"
            })

        # SOLUTION 4 - Battery Low
        if soc < 30:
            actions.append("🔋 Battery Low - Charge Battery")
            solutions.append({
                "problem": "🔋 Battery Low (%.0f%%)" % soc,
                "cause": "Battery drained, no charging source",
                "solution": "1. Charge battery from Solar on priority | 2. Stop battery discharge | 3. Connect to Grid charging | 4. Limit backup usage"
            })

        # SOLUTION 5 - Overheating
        if temp > 35:
            actions.append("🌡️ Overheating - Cool System")
            solutions.append({
                "problem": "🌡️ High Temperature (%.0fC)" % temp,
                "cause": "Inverter / Transformer overheating",
                "solution": "1. Turn ON cooling fans | 2. Reduce load by 15% | 3. Check ventilation | 4. Schedule maintenance"
            })

        if not solutions:
            actions.append("⚠️ General Fault - Isolate & Inspect")
            solutions.append({
                "problem": "⚠️ General Grid Fault Detected",
                "cause": "Multiple parameters abnormal",
                "solution": "1. Isolate faulty section | 2. Switch to backup | 3. Notify maintenance team | 4. Run diagnostic scan"
            })
    else:
        actions.append("✅ No action needed - Grid Healthy")
        solutions.append({
            "problem": "✅ Grid Healthy - No Fault",
            "cause": "All parameters in normal range",
            "solution": "1. Continue monitoring | 2. Keep Battery charging | 3. Log data for forecasting"
        })

    return risk, actions, reasoning, solutions