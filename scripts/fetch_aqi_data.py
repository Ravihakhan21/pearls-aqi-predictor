import requests
import json
import os
from datetime import datetime

# ✅ Load API key from GitHub Secret or local env
API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Karachi"
URL = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=yes"

try:
    response = requests.get(URL)
    data = response.json()
except Exception as e:
    print("❌ Failed to fetch data:", e)
    exit()

if "current" not in data or "air_quality" not in data["current"]:
    print("❌ API response missing expected fields")
    exit()

# ✅ Extract allowed features only
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
aq_data = {
    "timestamp": timestamp,
    "o3": data["current"]["air_quality"].get("o3"),
    "co": data["current"]["air_quality"].get("co"),
    "no2": data["current"]["air_quality"].get("no2"),
    "so2": data["current"]["air_quality"].get("so2"),
    "temp_c": data["current"].get("temp_c"),
    "humidity": data["current"].get("humidity"),
    "wind_kph": data["current"].get("wind_kph"),
    "pressure_mb": data["current"].get("pressure_mb")
}

# ✅ Save to data/aqi_data.json
os.makedirs("data", exist_ok=True)
json_file = "data/aqi_data.json"

if os.path.exists(json_file):
    with open(json_file, 'r') as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
else:
    existing_data = []

# ✅ Skip duplicates
if any(item["timestamp"] == aq_data["timestamp"] for item in existing_data):
    print("⏩ Duplicate timestamp, skipping entry.")
else:
    existing_data.append(aq_data)
    with open(json_file, 'w') as f:
        json.dump(existing_data, f, indent=2)
    print(f"✅ AQI data added for {timestamp}")
