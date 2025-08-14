# scripts/feature_engineering.py
import pandas as pd
import numpy as np

def make_time_features(df):
    df['hour'] = df['timestamp'].dt.hour
    df['dayofweek'] = df['timestamp'].dt.dayofweek
    df['month'] = df['timestamp'].dt.month
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    return df

def make_lags(df, col='aqi', lags=[1, 3, 6]):
    for lag in lags:
        if col in df.columns:
            df[f"{col}_lag_{lag}"] = df[col].shift(lag)
        else:
            df[f"{col}_lag_{lag}"] = np.nan
    return df

def make_rolling(df, col='aqi', windows=[3, 12]):
    for w in windows:
        if col in df.columns:
            df[f"{col}_roll_{w}"] = df[col].rolling(window=w, min_periods=1).mean()
        else:
            df[f"{col}_roll_{w}"] = np.nan
    return df

def feature_engineering_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies the complete feature engineering process.
    Handles both training (AQI exists) and forecasting (AQI missing).
    """
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])

    has_aqi = 'aqi' in df.columns

    df = make_time_features(df)
    df = make_lags(df, 'aqi')
    df = make_rolling(df, 'aqi')

    if has_aqi:
        df['aqi_change_rate'] = df['aqi'].diff().fillna(0)
        initial_rows = len(df)
        df = df.dropna().reset_index(drop=True)
        if len(df) < initial_rows:
            print(f"Dropped {initial_rows - len(df)} rows due to NaN after FE.")
    else:
        df['aqi_change_rate'] = np.nan

    return df
if __name__ == "__main__":
    import os

    # 1️⃣ Load the cleaned data
    input_path = os.path.join("data", "hourly_clean_updated.csv")
    df = pd.read_csv(input_path)

    # 2️⃣ Run feature engineering
    df_fe = feature_engineering_pipeline(df)

    # 3️⃣ Save the features file
    output_path = os.path.join("data", "hourly_features.csv")
    df_fe.to_csv(output_path, index=False)

    # 4️⃣ Print success message
    print(f"✅ Features saved → {output_path} (rows={len(df_fe)})")
