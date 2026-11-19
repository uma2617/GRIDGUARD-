import streamlit as st
import pandas as pd
import pickle
import sys
sys.path.append(".")
from agent.agent import grid_agent
from src.report import generate_report
from src.explain import get_explanation
from src.digital_twin import digital_twin_sim
from src.forecast import forecast_next_24h

st.set_page_config(page_title="GridGuard - Smart Grid AI", layout="wide")
st.title("⚡ GridGuard - Smart Grid Fault Prediction")
st.markdown("GPVS Dataset | Agentic AI + LSTM + SHAP + Digital Twin")

df = pd.read_csv("data/raw/gpvs_data.csv")
FEATURES = ["solar_kw","wind_kw","load_kw","battery_soc","grid_freq","voltage","temperature"]

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(df[FEATURES], df["fault"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", len(df))
col2.metric("Faults Detected", int(df["fault"].sum()))
col3.metric("Avg Solar (kW)", round(df["solar_kw"].mean(), 1))
col4.metric("Avg Load (kW)", round(df["load_kw"].mean(), 1))

st.subheader("📊 Live Grid Data")
st.line_chart(df[["solar_kw", "wind_kw", "load_kw"]].head(200))

# --- DIGITAL TWIN ---
st.subheader("🧊 Digital Twin - Live Simulation")
solar = st.slider("Solar kW", 0, 100, 50)
wind = st.slider("Wind kW", 0, 90, 40)
load = st.slider("Load kW", 30, 140, 80)
soc = st.slider("Battery SOC %", 10, 95, 60)
freq = st.slider("Grid Freq Hz", 49.8, 50.2, 50.0)
volt = st.slider("Voltage V", 210, 240, 230)
temp = st.slider("Temperature C", 15, 40, 28)

generation, net, new_soc, grid_flow, twin_status = digital_twin_sim(solar, wind, load, soc)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Generation", f"{generation} kW")
c2.metric("Net Power", f"{net} kW")
c3.metric("Battery After", f"{new_soc:.1f}%")
c4.metric("Grid Flow", f"{grid_flow:.1f} kW")
st.info(twin_status)

# --- LSTM FORECAST ---
st.subheader("🔮 LSTM Forecast - Next 24 Hours")
future_load, future_solar = forecast_next_24h(df)
forecast_df = pd.DataFrame({"Hour": list(range(1, 25)), "Forecast Load kW": future_load, "Forecast Solar kW": future_solar})
st.line_chart(forecast_df.set_index("Hour"))

st.subheader("🔮 Predict Fault - Try it!")
if st.button("Predict Fault"):
    input_df = pd.DataFrame([[solar, wind, load, soc, freq, volt, temp]], columns=FEATURES)
    pred = model.predict(input_df)[0]
    if pred == 1:
        st.error("⚠️ FAULT PREDICTED! - Take Action")
    else:
        st.success("✅ Grid NORMAL - No Fault")

    risk, actions, reasoning, solutions = grid_agent(solar, wind, load, soc, freq, volt, temp, pred)
    st.subheader(f"🤖 AI Agent Decision - Risk: {risk}")
    st.info(reasoning)
    for a in actions:
        st.write(a)

    st.subheader("🛠️ AI Recommended Solution - How to Fix")
    for s in solutions:
        st.markdown(f"**{s['problem']}**")
        st.write(f"**Cause:** {s['cause']}")
        st.success(f"**Solution:** {s['solution']}")
        st.markdown("---")

    st.subheader("🔍 SHAP Explainability - Why Fault Happened?")
    explanations = get_explanation(solar, wind, load, soc, freq, volt, temp, model)
    for feat, imp, val in explanations:
        st.write(f"**{feat}**: {val} - Impact: {imp}%")
        st.progress(min(int(imp), 100))
    st.caption("Higher % = More responsible for fault prediction")

    pdf_bytes = generate_report(solar, wind, load, soc, freq, volt, temp, pred, risk, actions)
    st.download_button("📄 Download PDF Report", data=pdf_bytes, file_name="GridGuard_Report.pdf", mime="application/pdf")