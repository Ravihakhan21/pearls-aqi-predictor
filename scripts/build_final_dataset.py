import pandas as pd
import json

# 📥 Load historic dataset
df_hist = pd.read_csv('data/final_training_dataset.csv')
df_hist['timestamp'] = pd.to_datetime(df_hist['timestamp'], errors='coerce')

# 📥 Load aqi_data.json
with open('data/aqi_data.json', 'r') as f:
    json_data = json.load(f)

# 🔍 Convert JSON to DataFrame
df_json = pd.DataFrame(json_data)
df_json['timestamp'] = pd.to_datetime(df_json['timestamp'], errors='coerce')

# ⏳ Keep only data from 26 July 2025 until 31 July 2025
df_json = df_json[
    (df_json['timestamp'] >= pd.Timestamp("2025-07-26 17:08:15")) &
    (df_json['timestamp'] <= pd.Timestamp("2025-07-31 23:59:59"))
]

# 🧼 Drop rows with missing pollutant values
required_cols = ['co', 'no2', 'o3', 'so2', 'temp_c', 'humidity', 'wind_kph', 'pressure_mb']
df_json = df_json.dropna(subset=required_cols)

# 🧮 Calculate AQI (EPA-style, without PM2.5 and PM10)
df_json['aqi'] = (
    df_json['co'] * 0.02 +
    df_json['no2'] * 0.6 +
    df_json['o3'] * 0.3 +
    df_json['so2'] * 0.5
)

# 🧱 Keep only final dataset columns
final_columns = ['timestamp', 'co', 'no2', 'o3', 'so2', 'temp_c', 'humidity', 'wind_kph', 'pressure_mb', 'aqi']
df_json = df_json[final_columns]

# 📊 Combine old + new
df_final = pd.concat([df_hist, df_json], ignore_index=True)

# 🧹 Sort and reset
df_final = df_final.sort_values(by='timestamp').reset_index(drop=True)

# 🔄 Fill missing values (interpolate + bfill + ffill)
for col in final_columns[1:-1]:  # exclude timestamp and aqi
    df_final[col] = df_final[col].interpolate().bfill().ffill()

# Ensure AQI has no null values
df_final['aqi'] = df_final['aqi'].interpolate().bfill().ffill()

# 💾 Save final training dataset
df_final.to_csv('data/final_training_dataset_v2.csv', index=False)
print("✅ Done! Saved: data/final_training_dataset_v2.csv")