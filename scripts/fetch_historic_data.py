import os
import requests
import json
from datetime import datetime, timedelta
from time import sleep

# ✅ Read API Key from environment (set it in PowerShell before running)
API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise ValueError("❌ WEATHER_API_KEY not found. Please set it in your environment.")

# 📍 Location (Karachi)
LOCATION = "Karachi"

# 📅 Date Range (match Open-Meteo range)
START_DATE = datetime(2025, 4, 1)
END_DATE = datetime(2025, 7, 21)

# 📂 Output file
OUTPUT_FILE = "data/historic_weather.json"

all_weather = []

current = START_DATE
while current <= END_DATE:
    date_str = current.strftime("%Y-%m-%d")
    print(f"📅 Fetching hourly weather for {date_str}")

    url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={LOCATION}&dt={date_str}"

    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code != 200:
            print(f"⚠️ Failed for {date_str}: {resp.text}")
            sleep(2)
            current += timedelta(days=1)
            continue

        data = resp.json()

        # ✅ Extract all 24 hours
        hours = data["forecast"]["forecastday"][0]["hour"]
        for record in hours:
            row = {
                "timestamp": record["time"],         # full hourly timestamp
                "temp_c": record["temp_c"],
                "humidity": record["humidity"],
                "wind_kph": record["wind_kph"],
                "pressure_mb": record["pressure_mb"]
            }
            all_weather.append(row)

        print(f"✅ Added {len(hours)} hourly records for {date_str}")

    except Exception as e:
        print(f"❌ Error for {date_str}: {e}")

    # ⏱ Be nice to API (free tier has limits)
    sleep(1)
    current += timedelta(days=1)

# 💾 Save JSON
with open(OUTPUT_FILE, "w") as f:
    json.dump(all_weather, f, indent=2)

print(f"🎉 Saved {len(all_weather)} hourly weather records to {OUTPUT_FILE}")
