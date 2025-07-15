import requests
import pandas as pd
from datetime import datetime
import os

# ✅ STEP 1: Your AQICN API token
TOKEN = "36ff5b37dedc8de6a3d64ea07c42b99ed300f646"  # Replace with your token

# ✅ STEP 2: API endpoint for Karachi
url = f"https://api.waqi.info/feed/karachi/?token={TOKEN}"

# ✅ STEP 3: Call the API
response = requests.get(url)
data = response.json()

# ✅ STEP 4: If response is valid, extract fields
if data['status'] == 'ok':
    aqi = data['data']['aqi']
    timestamp = data['data']['time']['s']  # Already formatted timestamp from API
    iaqi = data['data']['iaqi']

    temp = iaqi.get('t', {}).get('v')
    humidity = iaqi.get('h', {}).get('v')
    wind = iaqi.get('w', {}).get('v')

    # ✅ STEP 5: Prepare data row
    record = {
        'timestamp': timestamp,
        'aqi': aqi,
        'temperature': temp,
        'humidity': humidity,
        'wind_speed': wind
    }

    df = pd.DataFrame([record])

    # ✅ STEP 6: Set file path (fixed!)
    os.makedirs('data', exist_ok=True)
    file_path = 'data/aqi_data.csv'

    # ✅ STEP 7: Avoid duplicate entries
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        if timestamp in existing_df['timestamp'].values:
            print("⏩ Timestamp already exists, skipping entry.")
            exit()
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

    print("✅ AQI + weather data saved to aqi_data.csv")

else:
    print("❌ API Error:", data.get('data'))
