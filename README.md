# 🌍 PEARLS AQI Predictor  

An end-to-end **Air Quality Index (AQI) Prediction System** built during my **Data Science Internship at 10Pearls Pakistan**.  

This was my **first ever complete Data Science project** — I started with very little experience beyond my AI course labs, and during this internship I learned to work with **real-world data, APIs, CI/CD pipelines, and deployment**.  

The system predicts AQI for the next **72 hours** and is fully automated via **GitHub Actions**.  

🔗 **Live Dashboard:** [View Here] 
https://pearls-aqi-predictor-afvljwkedamvjej2rtec4c.streamlit.app/

---

##  Project Overview
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

## Key Outcomes

Successfully built a serverless AQI prediction system.

Gained hands-on experience with APIs, CI/CD pipelines, feature engineering, and deployment.

Learned to handle real-world messy data, gaps, and automation failures.

Delivered a working ML pipeline + live dashboard during internship.

## My Journey with 10Pearls

This project marks the beginning of my Data Science journey.

Before this internship, I had never worked with data fetching through APIs, GitHub Actions, CI/CD pipelines, or deployment.

I faced challenges like messy API data, pipeline failures, and broken workflows — but step by step I learned to fix them.

By the end, I gained confidence in handling end-to-end ML projects: from data collection → model training → automation → deployment.

This internship was not just a technical achievement, but also a milestone in my learning journey as an aspiring Data Scientist.    

---

## 📂 Repository Structure
