import pandas as pd

# 📂 File paths (relative to project root)
V2_PATH = "data/final_training_dataset_v2.csv"
AUG_PATH = "data/pollutants_1_3_aug.csv"
V3_PATH = "data/final_training_dataset_v3.csv"

# 📥 Load existing dataset (up to July 31)
df_v2 = pd.read_csv(V2_PATH)
df_v2['timestamp'] = pd.to_datetime(df_v2['timestamp'], errors='coerce')

# 📥 Load pollutants data for 1–3 Aug
df_aug = pd.read_csv(AUG_PATH)
df_aug['timestamp'] = pd.to_datetime(df_aug['timestamp'], errors='coerce')

# 🧼 Ensure pollutant & weather features are complete
required_cols = ['co', 'no2', 'o3', 'so2', 'temp_c', 'humidity', 'wind_kph', 'pressure_mb']
df_aug = df_aug.dropna(subset=required_cols)

# 🧮 Calculate AQI (EPA-style, excluding PM2.5 & PM10)
df_aug['aqi'] = (
    df_aug['co'] * 0.02 +
    df_aug['no2'] * 0.6 +
    df_aug['o3'] * 0.3 +
    df_aug['so2'] * 0.5
)

# 🧱 Match structure with v2 dataset
final_columns = ['timestamp', 'co', 'no2', 'o3', 'so2', 'temp_c', 'humidity', 'wind_kph', 'pressure_mb', 'aqi']
df_aug = df_aug[final_columns]

# 📊 Combine old + new data
df_v3 = pd.concat([df_v2, df_aug], ignore_index=True)

# 🧹 Sort by timestamp and clean
df_v3 = df_v3.sort_values(by='timestamp').reset_index(drop=True)

# 🔄 Handle missing values (interpolation + fill)
for col in final_columns[1:-1]:  # skip timestamp & aqi
    df_v3[col] = df_v3[col].interpolate().bfill().ffill()
df_v3['aqi'] = df_v3['aqi'].interpolate().bfill().ffill()

# 💾 Save as v3
df_v3.to_csv(V3_PATH, index=False)

print("✅ Created final_training_dataset_v3.csv including Aug 1–3 data")
