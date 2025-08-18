# 🌍 PEARLS AQI Predictor  

An end-to-end **Air Quality Index (AQI) Prediction System** built during my **Data Science Internship at 10Pearls Pakistan**.  

This was my **first ever complete Data Science project** — I started with very little experience beyond my AI course labs, and during this internship I learned to work with **real-world data, APIs, CI/CD pipelines, and deployment**.  

The system predicts AQI for the next **72 hours** and is fully automated via **GitHub Actions**.  

🔗 **Live Dashboard:** [View Here] https://pearls-aqi-predictor-afvljwkedamvjej2rtec4c.streamlit.app/


---

## 📌 Project Overview
- **Data Sources**
  - Live hourly pollutants + weather → WeatherAPI  
  - Historic pollutants → OpenMeteo  
  - Historic weather → WeatherAPI  
- **AQI Calculation**
  - Used US EPA standard formula  
  - Final AQI = maximum sub-index of CO, NO₂, O₃, SO₂  
- **Feature Engineering**
  - Time features (hour/day/month, cyclical encoding)  
  - Lag features, rolling averages, change rates  
- **Models Tested**
  - Random Forest, XGBoost, Decision Tree  
  - ✅ Random Forest chosen as best  
- **Automation**
  - GitHub Actions fetches data **hourly**  
  - Predicts next **72 hours** autoregressively  
  - Updates CSV + pushes back to repo  
- **Deployment**
  - Streamlit dashboard for real-time AQI snapshot + forecast  

---

## 🎯 Key Outcomes
- Successfully built a **serverless AQI prediction system**.  
- Gained hands-on experience with **APIs, CI/CD pipelines, feature engineering, and deployment**.  
- Learned to handle **real-world messy data, gaps, and automation failures**.  
- Delivered a **working ML pipeline + live dashboard** during internship.  

---

## 🌟 My Journey with 10Pearls  
This project marks the **beginning of my Data Science journey**.  

- Before this internship, I had never worked with **data fetching through APIs, GitHub Actions, CI/CD pipelines, or deployment**.  
- I faced challenges like messy API data, pipeline failures, and broken workflows — but step by step I learned to fix them.  
- By the end, I gained confidence in handling **end-to-end ML projects**: from data collection → model training → automation → deployment.  

This internship was not just a technical achievement, but also a **milestone in my learning journey** as an aspiring Data Scientist.  

---

## 📂 Repository Structure  

### 🔹 Workflows
- `.github/workflows/fetch_aqi.yml` — ✅ Used (hourly data fetching)  
- `.github/workflows/predict_live.yml` — ✅ Used (72h forecasting)  

### 🔹 Data
- `data/aqi_data.json` — ✅ Used (hourly raw data from API)  
- `data/aqi_data.csv` — 🚨 Earlier approach, not used  
- `data/aqi_data_backup.json` — 🚨 Earlier approach, not used  
- `data/final_training_dataset_v2.csv` — ✅ Used (training dataset v2)  
- `data/final_training_dataset_v3.csv` — ✅ Used (training dataset v3, final)  
- `data/final_training_dataset.csv` — 🚨 Earlier approach, not used  
- `data/historic_openmeteo_pollutants.json` — ✅ Used (historic pollutants)  
- `data/historic_weather.json` — ✅ Used (historic weather)  
- `data/hourly_clean.csv` — ✅ Used (intermediate cleaned data)  
- `data/hourly_clean_updated.csv` — ✅ Used (latest cleaned dataset)  
- `data/hourly_features.csv` — ✅ Used (feature-engineered dataset)  
- `data/pollutants_1_3_aug.csv` — ✅ Used (prediction input for Aug 1–3)  
- `data/pollutants_4_6_aug.csv` — ✅ Used (prediction input for Aug 4–6)  
- `data/predictions_72h.csv` — ✅ Used (72-hour forecast results)  
- `data/real_aqi_1_3_aug.csv` — ✅ Used (ground truth AQI for Aug 1–3)  
- `data/real_aqi_4_6_aug.csv` — ✅ Used (ground truth AQI for Aug 4–6)  

### 🔹 Models
- `models/RandomForest_final_model_v3.joblib` — ✅ Used (final trained model)  
- `models/scaler_v3.joblib` — ✅ Used (final scaler)  
- `models/feature_cols.json` — ✅ Used (feature set)  
- `models/aqi_model.pkl` — 🚨 Earlier approach, not used  
- `models/feature_importance.csv` — 🚨 Earlier approach, not used  

### 🔹 Scripts & Core Files
- `app.py` — ✅ Used (Streamlit dashboard)  
- `requirements.txt` — ✅ Used (dependencies)  
- `scripts/temp_scripts` — 🚨 Earlier approach, not used  
- `enhance_dataset.csv.xlsx` — 🚨 Earlier approach, not used  

### 🔹 Documentation
- `Journey_of_10pearls_AQI_final_report_with_screenshots.docx` — ✅ Used (final report)  
- `PEARLS-AQI-Predictor_Project.ppt (2).pptx` — ✅ Used (final presentation)  
- `README.md` — ✅ Project overview + structure  

---

👩‍💻 Developed by **Raviha Khan** | Internship at 10Pearls Pakistan

