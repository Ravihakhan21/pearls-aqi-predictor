import requests
import json
import os
from datetime import datetime

# ✅ Load API key from GitHub Secret (match the name exactly)
API_KEY = os.getenv("OWM_API_KEY")  # FIXED: should match your GitHub Secret name
LAT = 24.8607
LON = 67.0011
url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

# ✅ Map AQI category (1–5) to regression values
aqi_mapping = {
    1: 40,
    2: 80,
    3: 120,
    4: 180,
    5: 250
}

# ✅ Fetch data from API
try:
    response = requests.get(url)
    data = response.json()
except Exception as e:
    print("❌ Failed to fetch data from API:", e)
    exit()

# ✅ Handle errors in response
if "list" not in data:
    print("❌ API response error. Full response:")
    print(json.dumps(data, indent=2))
    exit()

# ✅ Extract relevant data
aqi_cat = data["list"][0]["main"]["aqi"]
components = data["list"][0]["components"]
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
aqi_mapped = aqi_mapping.get(aqi_cat)

# ✅ Create record (excluding PM2.5 and PM10)
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

# ✅ Save to JSON file
os.makedirs("data", exist_ok=True)
json_file = "data/aqi_data.json"

# ✅ Load existing and append if timestamp is new
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
