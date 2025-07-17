import requests
import json
import os
from datetime import datetime

# ✅ API Details
API_KEY = "b148549bdddc328bcfdd06ab71e9828a"
LAT = 24.8607
LON = 67.0011
url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

# ✅ Mapping AQI category (1–5) to regression value
aqi_mapping = {
    1: 40,
    2: 80,
    3: 120,
    4: 180,
    5: 250
}

# ✅ Fetch data
response = requests.get(url)
data = response.json()

# ✅ Extract and transform
aqi_cat = data["list"][0]["main"]["aqi"]
components = data["list"][0]["components"]
timestamp = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
aqi_mapped = aqi_mapping.get(aqi_cat, None)

# ✅ Save fields (excluding PM2.5 and PM10)
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

# ✅ Create folder if not exist
os.makedirs("data", exist_ok=True)
json_file = "data/aqi_data.json"

# ✅ Load existing data
if os.path.exists(json_file):
    with open(json_file, 'r') as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
else:
    existing_data = []

# ✅ Check for duplicate timestamp (within ±10 minutes window)
timestamps = [item["timestamp"] for item in existing_data]
if timestamp in timestamps:
    print("⏩ Timestamp already exists, skipping entry.")
else:
    existing_data.append(record)
    with open(json_file, 'w') as f:
        json.dump(existing_data, f, indent=2)
    print("✅ AQI data saved to aqi_data.json")
