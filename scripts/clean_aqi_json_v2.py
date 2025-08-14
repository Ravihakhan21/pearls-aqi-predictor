# scripts/clean_aqi_json_v2.py
import json
from pathlib import Path
import pandas as pd
import numpy as np

RAW_JSON = Path("data/aqi_data.json")
OUT_CSV  = Path("data/hourly_clean_updated.csv")

START_DATE = pd.Timestamp("2025-07-26 00:00:00")  # keep from here onward

def compute_aqi(df: pd.DataFrame) -> pd.Series:
    """
    Your EPA-style proxy (no PM2.5/PM10):
    AQI = 0.02*CO + 0.6*NO2 + 0.3*O3 + 0.5*SO2
    """
    # Coerce numeric
    for col in ["co","no2","o3","so2"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = np.nan
    return (df["co"] * 0.02) + (df["no2"] * 0.6) + (df["o3"] * 0.3) + (df["so2"] * 0.5)

def main():
    if not RAW_JSON.exists():
        raise FileNotFoundError(f"Raw JSON not found: {RAW_JSON}")

    with RAW_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    if df.empty:
        raise ValueError("JSON contained no rows.")

    # Parse & sort time
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)

    # Keep from 26 July onward
    df = df[df["timestamp"] >= START_DATE].copy()

    # Coerce numeric for all known numeric cols
    numeric_cols = ["o3","co","no2","so2","temp_c","humidity","wind_kph","pressure_mb"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Aggregate to hourly: floor to hour, then for each hour take the LAST non-null row
    df["hour_bucket"] = df["timestamp"].dt.floor("H")
    # Sort within hour so 'last' is truly last
    df = df.sort_values(["hour_bucket", "timestamp"])

    # Define how to take last non-null in a group
    def last_valid(s: pd.Series):
        return s.dropna().iloc[-1] if s.dropna().size > 0 else np.nan

    agg_dict = {c: last_valid for c in numeric_cols}
    hourly = df.groupby("hour_bucket", as_index=False).agg(agg_dict)
    hourly = hourly.rename(columns={"hour_bucket": "timestamp"})

    # Compute AQI with your formula (deterministic "current AQI")
    hourly["aqi"] = compute_aqi(hourly)

    # Final tidy + save
    hourly = hourly.sort_values("timestamp").reset_index(drop=True)
    hourly.to_csv(OUT_CSV, index=False)
    print(f"✅ Clean hourly data saved → {OUT_CSV}  (rows={len(hourly)})")

if __name__ == "__main__":
    main()
