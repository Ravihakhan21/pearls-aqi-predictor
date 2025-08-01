import requests, json, time

LAT, LON = 24.8607, 67.0011
START_DATE = "2025-04-01"
END_DATE = "2025-07-21"

url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "hourly": "carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide"
}

print("📡 Fetching pollutant data from Open-Meteo...")

for attempt in range(3):  # retry up to 3 times if network fails
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        break
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Attempt {attempt+1} failed: {e}")
        if attempt == 2:
            raise SystemExit("❌ Failed after 3 attempts.")
        time.sleep(5)

data = resp.json()

# ✅ Validate expected structure
if "hourly" not in data:
    raise ValueError(f"❌ Unexpected API response: {data}")

ts = data["hourly"]["time"]
co = data["hourly"]["carbon_monoxide"]
no2 = data["hourly"]["nitrogen_dioxide"]
o3 = data["hourly"]["ozone"]
so2 = data["hourly"]["sulphur_dioxide"]

records = []
for i in range(len(ts)):
    records.append({
        "timestamp": ts[i],
        "co": co[i],
        "no2": no2[i],
        "o3": o3[i],
        "so2": so2[i]
    })

with open("historic_openmeteo_pollutants.json", "w") as f:
    json.dump(records, f, indent=2)

print(f"✅ Saved {len(records)} pollutant-only records from {START_DATE} to {END_DATE}")
