import requests
import json
import os
from datetime import datetime

# ✅ Get API key from environment variable
API_KEY = os.getenv("OWM_API_KEY")
LAT = 24.8607
LON = 67.0011
url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

# ✅ AQI category mapping to estimated real values
aqi_mapping = {
    1: 40,
    2: 80,
    3: 120,
    4: 180,
    5: 250
}

# ✅ Fetch and process data
response = requests.get(url)
data = response.json()

aqi_cat = data["list"][0]["main"]["aqi"]
components = data["list"][0]["components"]
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
aqi_mapped = aqi_mapping.get(aqi_cat, None)

record = {
    "timestamp": timestamp,
    "aqi": aqi_mapped,
    "co": components.get("co"),
    "no": components.get("no"),
    "no2": components.get("no2"),
    "o3": components.get("o3"),
    "so2": components.get("so2"),
    "nh3": components.get("nh3")
}

# ✅ Save to JSON
os.makedirs("data", exist_ok=True)
json_file = "data/aqi_data.json"

if os.path.exists(json_file):
    with open(json_file, 'r') as f:
        existing_data = json.load(f)
else:
    existing_data = []

if any(item["timestamp"] == record["timestamp"] for item in existing_data):
    print("⏩ Timestamp already exists, skipping entry.")
else:
    existing_data.append(record)
    with open(json_file, 'w') as f:
        json.dump(existing_data, f, indent=2)
    print("✅ AQI data saved to aqi_data.json")

