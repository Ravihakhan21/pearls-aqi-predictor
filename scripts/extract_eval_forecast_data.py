import pandas as pd
import json

# 🔹 Path to your aqi_data.json (from CI/CD)
json_path = "data/aqi_data.json"

# Load JSON
with open(json_path, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# ✅ Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')

# ✅ Keep only clean data from 26 July 2025 onwards
df = df[df['timestamp'] >= "2025-07-26 17:08:15"]

# ✅ Select only pollutants + weather columns (no AQI, since we are predicting it)
pollutant_cols = ['timestamp', 'co', 'no2', 'o3', 'so2', 'temp_c', 'humidity', 'wind_kph', 'pressure_mb']
df = df[pollutant_cols]

# ✅ Create evaluation dataset (1–3 Aug 2025)
eval_df = df[(df['timestamp'] >= "2025-08-01") & (df['timestamp'] < "2025-08-04")]
eval_df.to_csv("data/pollutants_1_3_aug.csv", index=False)
print(f"✅ Saved evaluation pollutants: data/pollutants_1_3_aug.csv ({eval_df.shape[0]} rows)")

# ✅ Create forecast dataset (4–6 Aug 2025)
forecast_df = df[(df['timestamp'] >= "2025-08-04") & (df['timestamp'] < "2025-08-07")]
forecast_df.to_csv("data/pollutants_4_6_aug.csv", index=False)
print(f"✅ Saved forecast pollutants: data/pollutants_4_6_aug.csv ({forecast_df.shape[0]} rows)")

print("\n🎯 Done! Use 'pollutants_1_3_aug.csv' for evaluation and 'pollutants_4_6_aug.csv' for forecasting.")
