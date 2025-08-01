import json
import os

# 🔒 File path for your AQI data
json_file = "data/aqi_data.json"
backup_file = "data/aqi_data_backup.json"

# ✅ Step 1: Make a backup
if os.path.exists(json_file):
    with open(json_file, "r") as f:
        raw_data = f.read()
    with open(backup_file, "w") as f:
        f.write(raw_data)
    print(f"✅ Backup created at {backup_file}")
else:
    print("❌ No aqi_data.json found!")
    exit()

# ✅ Step 2: Remove merge markers
clean_data = []
for line in raw_data.splitlines():
    if not (line.strip().startswith("<<<<<<<") or 
            line.strip().startswith("=======") or 
            line.strip().startswith(">>>>>>>")):
        clean_data.append(line)

# ✅ Step 3: Parse cleaned JSON safely
try:
    parsed_json = json.loads("\n".join(clean_data))
except json.JSONDecodeError as e:
    print("❌ JSON is still broken. Manual fixing may be needed:", e)
    exit()

# ✅ Step 4: Remove duplicate timestamps
seen = set()
final_data = []
for entry in parsed_json:
    ts = entry.get("timestamp")
    if ts and ts not in seen:
        seen.add(ts)
        final_data.append(entry)

# ✅ Step 5: Save the cleaned JSON back
with open(json_file, "w") as f:
    json.dump(final_data, f, indent=2)

print(f"✅ Cleaned JSON saved to {json_file}")
print(f"📂 Original file backed up at {backup_file}")
print(f"📊 Total cleaned entries: {len(final_data)}")
