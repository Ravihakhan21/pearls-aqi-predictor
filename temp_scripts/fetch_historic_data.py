# scripts/fetch_historic_data.py

import requests
import json
import os
from datetime import datetime, timedelta

# Load your API key
API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Karachi"
BASE_URL = "https://api.weatherapi.com/v1/history.json"

# Define date range (15 to 18 July)
start_date = datetime(2025, 7, 15)
end_date = datetime(2025, 7, 18)

# Load existing data if present
file_path = "data/aqi_data.json"
if os.path.exists(file_path):
    with open(file_path, "r") as file:
        existing_data = json.load(file)
else:
    existing_data = []

# Fetch and append new historical data
date = start_date
while date <= end_date:
    formatted_date = date.strftime("%Y-%m-%d")
    url = f"{BASE_URL}?key={API_KEY}&q={CITY}&dt={formatted_date}"
    
    try:
        response = requests.get(url)
        data = response.json()

        # Extract required fields
        forecast = data.get("forecast", {}).get("forecastday", [])[0]
        hour_data = forecast.get("hour", [])
        
        for hour in hour_data:
            entry = {
                "timestamp": hour["time"],
                "aqi": hour["air_quality"]["us-epa-index"],
                "temperature": hour["temp_c"],
                "humidity": hour["humidity"],
                "wind_speed": hour["wind_kph"] / 3.6  # Convert to m/s
            }
            existing_data.append(entry)

        print(f"✅ Fetched {formatted_date}")
    except Exception as e:
        print(f"❌ Failed for {formatted_date}: {e}")

    date += timedelta(days=1)

# Save the updated dataset
with open(file_path, "w") as file:
    json.dump(existing_data, file, indent=2)
