import pandas as pd
from datetime import datetime

# 📂 File paths
raw_file = "data/aqi_data.json"          # ✅ CI/CD keeps updating this
clean_file = "data/hourly_clean.csv"     # ✅ We'll generate this cleaned version

print("📥 Loading raw AQI data...")
df = pd.read_json(raw_file)

print(f"✅ Raw file loaded: {len(df)} rows")

# ----------------- 🧹 CLEANING -----------------

# 1️⃣ Fix timestamp format → YYYY-MM-DD HH:MM
print("🕒 Standardizing timestamps...")
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# 2️⃣ Drop rows where timestamp could not be parsed (corrupted rows)
before = len(df)
df = df.dropna(subset=['timestamp'])
print(f"🗑️ Dropped {before - len(df)} bad timestamp rows")

# 3️⃣ Drop rows where all pollutant & weather values are missing
pollutants_weather = ['o3', 'co', 'no2', 'so2', 'temp_c', 'humidity', 'wind_kph', 'pressure_mb']
before = len(df)
df = df.dropna(subset=pollutants_weather, how='all')
print(f"🗑️ Dropped {before - len(df)} empty pollutant rows")

# 4️⃣ Remove duplicates by timestamp (keep latest)
before = len(df)
df = df.drop_duplicates(subset=['timestamp'], keep='last')
print(f"🗑️ Dropped {before - len(df)} duplicate timestamps")

# 5️⃣ Sort chronologically
df = df.sort_values('timestamp')

# ----------------- 💾 SAVE -----------------
df.to_csv(clean_file, index=False)
print(f"🎉 Clean hourly dataset saved to {clean_file}")
print(f"📊 Final rows: {len(df)} (✅ ready for ML, charts & retraining)")
