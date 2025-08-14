# scripts/predict_live.py
import json
from pathlib import Path
from datetime import timedelta

import numpy as np
import pandas as pd
import joblib

from feature_engineering import feature_engineering_pipeline

DATA_CSV      = Path("data/hourly_clean_updated.csv")
MODEL_PATH    = Path("models/RandomForest_final_model_v3.joblib")
SCALER_PATH   = Path("models/scaler_v3.joblib")          # optional
FEATCOLS_PATH = Path("models/feature_cols.json")         # optional
OUT_PRED      = Path("data/predictions_72h.csv")

FORECAST_HOURS = 72

def load_feature_cols_or_infer(df_fe: pd.DataFrame) -> list:
    if FEATCOLS_PATH.exists():
        with FEATCOLS_PATH.open("r", encoding="utf-8") as f:
            cols = json.load(f)
        return cols
    # Fallback: all except timestamp & aqi if not provided
    return [c for c in df_fe.columns if c not in ["timestamp", "aqi"]]

def apply_scaler_if_exists(X: pd.DataFrame):
    if SCALER_PATH.exists():
        scaler = joblib.load(SCALER_PATH)
        X_scaled = scaler.transform(X)
        return X_scaled
    return X.values  # no scaling

def forward_fill_future_base_row(hist_row: pd.Series) -> pd.Series:
    """
    For future timestamps, we must provide pollutant/weather features.
    We use the last observed (LOCF).
    """
    carry_cols = ["co","no2","o3","so2","temp_c","humidity","wind_kph","pressure_mb"]
    row = hist_row.copy()
    for c in carry_cols:
        if c not in row.index or pd.isna(row[c]):
            row[c] = row[c] if c in row.index else np.nan
    return row

def main():
    # Sanity checks
    if not DATA_CSV.exists():
        raise FileNotFoundError(f"Clean data not found: {DATA_CSV}")
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    # Load clean hourly history
    hist = pd.read_csv(DATA_CSV, parse_dates=["timestamp"])
    if hist.empty:
        raise ValueError("Clean data is empty.")

    # Build features for history (this also drops early rows w/ NaNs from lags)
    hist_fe = feature_engineering_pipeline(hist.copy())

    # Prepare feature list
    feature_cols = load_feature_cols_or_infer(hist_fe)

    # Train-ready matrix for last known time (we will autoregress from there)
    last_time = hist_fe["timestamp"].max()
    last_row_full = hist_fe[hist_fe["timestamp"] == last_time].iloc[-1]

    # We will keep a rolling small dataframe of recent rows to compute lags/rollings on the fly
    # Start from the *original history* (with true AQI) to compute lags for first forecast step
    work = hist.copy()

    preds = []
    for step in range(1, FORECAST_HOURS + 1):
        new_ts = last_time + timedelta(hours=step)

        # Build a new "base" row by carrying forward last observed pollutants/weather
        base = forward_fill_future_base_row(work.iloc[-1])

        # Set new timestamp & (temporarily) put AQI as last known to compute lags/rollings;
        # then we'll replace with model prediction after we predict this step.
        new_row = {
            "timestamp": new_ts,
            "co": base.get("co", np.nan),
            "no2": base.get("no2", np.nan),
            "o3": base.get("o3", np.nan),
            "so2": base.get("so2", np.nan),
            "temp_c": base.get("temp_c", np.nan),
            "humidity": base.get("humidity", np.nan),
            "wind_kph": base.get("wind_kph", np.nan),
            "pressure_mb": base.get("pressure_mb", np.nan),
            # Put a placeholder AQI = last known AQI for lag/rolling calc; will overwrite with prediction.
            "aqi": work.iloc[-1]["aqi"]
        }
        work = pd.concat([work, pd.DataFrame([new_row])], ignore_index=True)

        # Feature engineering on the most recent window to get features for this one new timestamp
        fe = feature_engineering_pipeline(work.copy())
        this_fe = fe[fe["timestamp"] == new_ts]
        # If FE dropped the row due to missing lags, try recompute using more history (shouldn't happen after enough history)
        if this_fe.empty:
            # Use the tail (ensure min history) and recompute
            fe = feature_engineering_pipeline(work.tail(200).copy())
            this_fe = fe[fe["timestamp"] == new_ts]
            if this_fe.empty:
                raise RuntimeError("Failed to produce features for forecast step — insufficient history.")

        X_this = this_fe[feature_cols]
        X_scaled = apply_scaler_if_exists(X_this)

        # Load model once (outside loop would be faster, but keep clear)
        model = joblib.load(MODEL_PATH)
        y_pred = float(model.predict(X_scaled)[0])

        # Save prediction for this hour
        preds.append({"timestamp": new_ts, "pred_aqi": y_pred})

        # Overwrite the placeholder AQI in 'work' with our prediction, so next-step lags use it
        work.loc[work["timestamp"] == new_ts, "aqi"] = y_pred

    # Write predictions
    pred_df = pd.DataFrame(preds)
    pred_df.to_csv(OUT_PRED, index=False)
    print(f"✅ 72-hour forecast saved → {OUT_PRED}  (rows={len(pred_df)})")

if __name__ == "__main__":
    main()
