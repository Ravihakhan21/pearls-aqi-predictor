import streamlit as st
import pandas as pd
import numpy as np

# URLs to CSVs in your GitHub repo
DATA_CLEAN_URL = "https://raw.githubusercontent.com/Ravihakhan21/pearls-aqi-predictor/main/data/hourly_clean_updated.csv"
PRED_CSV_URL   = "https://raw.githubusercontent.com/Ravihakhan21/pearls-aqi-predictor/main/data/predictions_72h.csv"


st.set_page_config(page_title="PEARLS AQI Forecast", layout="wide")
st.title("🌍 PEARLS — Live AQI & 72-hour Forecast")

def compute_aqi_row(row):
    return (row.get('co', 0) * 0.02 +
            row.get('no2', 0) * 0.6 +
            row.get('o3', 0) * 0.3 +
            row.get('so2', 0) * 0.5)

# Sidebar: latest snapshot
st.sidebar.header("Latest observed data")
try:
    df = pd.read_csv(DATA_CLEAN_URL, parse_dates=['timestamp'])
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
except Exception:
    st.sidebar.warning("Could not fetch latest clean data from GitHub.")

# Main: forecast
st.header("Next 72 hours — Forecast")
try:
    pred = pd.read_csv(PRED_CSV_URL, parse_dates=['timestamp'])
    if not pred.empty:
        st.line_chart(pred.set_index('timestamp')['pred_aqi'])
        st.subheader("Forecast table")
        st.dataframe(pred)
        st.download_button("Download predictions_72h.csv",
                           pred.to_csv(index=False).encode('utf-8'),
                           file_name="predictions_72h.csv")
    else:
        st.info("Predictions file exists but is empty.")
except Exception:
    st.info("Could not fetch predictions file from GitHub.")
