import pandas as pd
from datetime import datetime

# 📂 File paths
openmeteo_file = "data/historic_openmeteo_pollutants.json"
weather_file = "data/historic_weather.json"
aqi_file = "data/aqi_data.json"
output_file = "data/final_training_dataset.csv"

print("📥 Loading datasets...")

# ✅ Load JSON files into DataFrames
df_openmeteo = pd.read_json(openmeteo_file)
df_weather = pd.read_json(weather_file)
df_aqi = pd.read_json(aqi_file)

print(f"✅ Open-Meteo: {len(df_openmeteo)} rows")
print(f"✅ WeatherAPI: {len(df_weather)} rows")
print(f"✅ AQI Data: {len(df_aqi)} rows")

# ------------------- FIX TIMESTAMPS -------------------
print("\n🕒 Converting timestamps to datetime...")

df_openmeteo['timestamp'] = pd.to_datetime(df_openmeteo['timestamp'], errors='coerce')
df_weather['timestamp'] = pd.to_datetime(df_weather['timestamp'], errors='coerce')
df_aqi['timestamp'] = pd.to_datetime(df_aqi['timestamp'], errors='coerce')

# ------------------- CLEANING -------------------
print("\n🧹 Cleaning data...")

# 1️⃣ Drop junk rows where all pollutants are null
pollutants = ['co', 'no2', 'o3', 'so2']
df_openmeteo.dropna(subset=pollutants, how='all', inplace=True)

# 2️⃣ Deduplicate timestamps in AQI data (keep last occurrence)
df_aqi = df_aqi.drop_duplicates(subset='timestamp', keep='last')

# 3️⃣ Drop unused AQI columns (nh3, no)
for col in ['nh3', 'no']:
    if col in df_aqi.columns:
        df_aqi.drop(columns=col, inplace=True)

# 4️⃣ Filter to April 1 – July 21 (match historic range)
start_date = datetime(2025, 4, 1)
end_date = datetime(2025, 7, 21)

def filter_by_date(df):
    return df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]

df_openmeteo = filter_by_date(df_openmeteo)
df_weather = filter_by_date(df_weather)
df_aqi = filter_by_date(df_aqi)

print(f"✅ After cleaning: Open-Meteo {len(df_openmeteo)}, Weather {len(df_weather)}, AQI {len(df_aqi)}")

# ------------------- MERGING -------------------
print("\n🔗 Merging data...")

# Merge pollutants + weather first
merged = pd.merge(df_openmeteo, df_weather, on="timestamp", how="outer")

# Merge any AQI values (if they exist)
if 'aqi' in df_aqi.columns:
    merged = pd.merge(merged, df_aqi[['timestamp', 'aqi']], on="timestamp", how="left")

# ✅ Sort by timestamp
merged.sort_values(by="timestamp", inplace=True)

# ------------------- AQI CALCULATION -------------------
print("\n📊 Calculating AQI from pollutants...")

def calc_subindex(c, breakpoints):
    """Calculate subindex for one pollutant based on breakpoints"""
    for bp in breakpoints:
        c_low, c_high, i_low, i_high = bp
        if c_low <= c <= c_high:
            return ((i_high - i_low) / (c_high - c_low)) * (c - c_low) + i_low
    return None  # If outside defined range

# Simplified AQI breakpoints for pollutants (values in µg/m³ or ppb approximations)
breakpoints = {
    'co': [
        (0.0, 4400, 0, 50),
        (4500, 9400, 51, 100),
        (9500, 12400, 101, 150),
        (12500, 15400, 151, 200),
    ],
    'no2': [
        (0, 53, 0, 50),
        (54, 100, 51, 100),
        (101, 360, 101, 150),
    ],
    'o3': [
        (0, 54, 0, 50),
        (55, 70, 51, 100),
        (71, 85, 101, 150),
    ],
    'so2': [
        (0, 35, 0, 50),
        (36, 75, 51, 100),
        (76, 185, 101, 150),
    ]
}

def calculate_aqi(row):
    subindexes = []
    for pol in pollutants:
        val = row.get(pol)
        if pd.notna(val):
            idx = calc_subindex(val, breakpoints[pol])
            if idx is not None:
                subindexes.append(idx)
    return max(subindexes) if subindexes else None

# Apply AQI calculation for every row
merged['calculated_aqi'] = merged.apply(calculate_aqi, axis=1)

# If existing AQI is missing, use calculated AQI
if 'aqi' in merged.columns:
    merged['aqi'] = merged['aqi'].fillna(merged['calculated_aqi'])
else:
    merged['aqi'] = merged['calculated_aqi']

# Drop helper column
merged.drop(columns=['calculated_aqi'], inplace=True)

print("✅ AQI calculated and filled.")

# ------------------- SAVE -------------------
merged.to_csv(output_file, index=False)
print(f"\n🎉 Final dataset ready: {output_file}")
print(f"📊 Total rows: {len(merged)}")
print("✅ This dataset is CLEAN, MERGED, and READY for feature engineering.")
