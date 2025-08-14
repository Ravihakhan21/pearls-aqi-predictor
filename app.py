# app.py
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).parent
DATA_CLEAN = ROOT / "data" / "hourly_clean_updated.csv"
PRED_CSV   = ROOT / "data" / "predictions_72h.csv"

st.set_page_config(page_title="PEARLS AQI Forecast", layout="wide")
st.title("🌍 PEARLS — Live AQI & 72-hour Forecast")

def compute_aqi_row(row):
    return (row.get('co', 0) * 0.02 +
            row.get('no2', 0) * 0.6 +
            row.get('o3', 0) * 0.3 +
            row.get('so2', 0) * 0.5)

# Sidebar: latest snapshot
st.sidebar.header("Latest observed data")
if DATA_CLEAN.exists():
    df = pd.read_csv(DATA_CLEAN, parse_dates=['timestamp'])
    if not df.empty:
        latest = df.sort_values('timestamp').iloc[-1]
        latest_aqi = latest['aqi'] if 'aqi' in latest and pd.notna(latest['aqi']) else compute_aqi_row(latest)
        st.sidebar.write("Timestamp:", latest['timestamp'])
        st.sidebar.metric("Current AQI (calc)", float(latest_aqi))
        st.sidebar.caption("Latest pollutants / weather")
        keep = [c for c in ['co','no2','o3','so2','temp_c','humidity','wind_kph','pressure_mb'] if c in df.columns]
        st.sidebar.write(latest[keep])
    else:
        st.sidebar.warning("Clean data exists but is empty.")
else:
    st.sidebar.warning("No cleaned data found. Run the cleaning script first.")

# Main: forecast
st.header("Next 72 hours — Forecast")
if PRED_CSV.exists():
    pred = pd.read_csv(PRED_CSV, parse_dates=['timestamp'])
    if not pred.empty:
        st.line_chart(pred.set_index('timestamp')['pred_aqi'])
        st.subheader("Forecast table")
        st.dataframe(pred)
        st.download_button("Download predictions_72h.csv",
                           pred.to_csv(index=False).encode('utf-8'),
                           file_name="predictions_72h.csv")
    else:
        st.info("Predictions file exists but is empty.")
else:
    st.info("No predictions file yet. Run predict script or wait for CI.")
