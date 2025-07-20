import os
import requests
import json
from datetime import datetime, timedelta
from time import sleep

# 🔑 Load API key from environment variable
API_KEY = os.environ.get("WEATHER_API_KEY")
if not API_KEY:
    raise ValueError("❌ WEATHER_API_KEY not found. Please set it as environment variable.")

# 📍 Set your location (Karachi)
LOCATION = "Karachi"

# 📅 Date Range: 1 Jan to 18 July 2025
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 7, 18)

# 📁 JSON file to append to
output_file = "data/aqi_data.json"

# 📦 Load existing data if file exists
try:
    with open(output_file, "r") as f:
        existing_data = json.load(f)
except FileNotFoundError:
    existing_data = []

# 🚀 Loop through each date
current = start_date
while current <= end_date:
    date_str = current.strftime("%Y-%m-%d")
    print(f"📅 Fetching data for: {date_str}")

    # 🛰 WeatherAPI endpoint for history
    url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={LOCATION}&dt={date_str}&hour=12"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch data for {date_str}: {response.text}")
        sleep(1)  # Wait before next call
        current += timedelta(days=1)
        continue

    data = response.json()

    try:
        hour_data = data["forecast"]["forecastday"][0]["hour"]
        for record in hour_data:
            row = {
                "timestamp": record["time"],
                "o3": record.get("ozone", None),
                "co": record.get("co", None),
                "no2": record.get("no2", None),
                "so2": record.get("so2", None),
                "temp_c": record["temp_c"],
                "humidity": record["humidity"],
                "wind_kph": record["wind_kph"],
                "pressure_mb": record["pressure_mb"]
            }
            existing_data.append(row)

        print(f"✅ Data added for {date_str}")
    except KeyError:
        print(f"⚠️ Missing expected fields for {date_str}")

    # ⏱ Be nice to the API
    sleep(1)
    current += timedelta(days=1)

# 💾 Save back to file
with open(output_file, "w") as f:
    json.dump(existing_data, f, indent=2)

print("🎉 Historic data collection complete!")
