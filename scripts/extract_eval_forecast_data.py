import pandas as pd
import json

# ---------- Paths ----------
json_path = "data/aqi_data.json"

# ---------- Load JSON ----------
with open(json_path, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# ---------- Convert timestamp ----------
df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')

# ---------- Keep only clean data from 26 July 2025 onwards ----------
df = df[df['timestamp'] >= "2025-07-26 17:08:15"]

# ---------- Select pollutants + weather ----------
pollutant_cols = ['timestamp', 'co', 'no2', 'o3', 'so2', 
                  'temp_c', 'humidity', 'wind_kph', 'pressure_mb']
df = df[pollutant_cols]

# ---------- Calculate Real AQI (EPA-style formula) ----------
df['aqi'] = (
    df['co'] * 0.02 +
    df['no2'] * 0.6 +
    df['o3'] * 0.3 +
    df['so2'] * 0.5
)

# ---------- Evaluation dataset (1–3 Aug) ----------
eval_df = df[(df['timestamp'] >= "2025-08-01") & (df['timestamp'] < "2025-08-04")]

# Save pollutants only
eval_df[pollutant_cols].to_csv("data/pollutants_1_3_aug.csv", index=False)

# Save real AQI only
eval_df[['timestamp', 'aqi']].to_csv("data/real_aqi_1_3_aug.csv", index=False)

print(f"✅ Saved evaluation pollutants: data/pollutants_1_3_aug.csv ({eval_df.shape[0]} rows)")
print(f"✅ Saved evaluation actual AQI: data/real_aqi_1_3_aug.csv ({eval_df.shape[0]} rows)")

# ---------- Forecast dataset (4–6 Aug) ----------
forecast_df = df[(df['timestamp'] >= "2025-08-04") & (df['timestamp'] < "2025-08-07")]

# Save pollutants only
forecast_df[pollutant_cols].to_csv("data/pollutants_4_6_aug.csv", index=False)

# Save real AQI only
forecast_df[['timestamp', 'aqi']].to_csv("data/real_aqi_4_6_aug.csv", index=False)

print(f"✅ Saved forecast pollutants: data/pollutants_4_6_aug.csv ({forecast_df.shape[0]} rows)")
print(f"✅ Saved forecast actual AQI: data/real_aqi_4_6_aug.csv ({forecast_df.shape[0]} rows)")

# ---------- Summary ----------
print("\n📊 Preview of Real AQI (1–3 Aug):")
print(eval_df[['timestamp', 'aqi']].head())

print("\n📊 Preview of Real AQI (4–6 Aug):")
print(forecast_df[['timestamp', 'aqi']].head())

print("\n🎯 Done! Now you have:")
print("- pollutants_1_3_aug.csv → for model prediction input")
print("- real_aqi_1_3_aug.csv → for actual vs predicted comparison")
print("- pollutants_4_6_aug.csv → for forecasting input")
print("- real_aqi_4_6_aug.csv → for later forecast validation")
