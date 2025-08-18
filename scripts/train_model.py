# 🚨 NOTE: This script was part of an earlier approach and is NOT used in the final pipeline.
# It is kept here for reference only.

"""
train_model.py
---------------
✅ Reads cleaned training dataset
✅ Adds time-based features (hour, day, month, weekday)
✅ Splits data into train & test
✅ Trains a Random Forest Regressor
✅ Saves the trained model (aqi_model.pkl)
✅ Exports feature importance to CSV (feature_importance.csv)
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# ========================
# 📥 1. LOAD THE DATASET
# ========================
print("📥 Loading dataset...")
df = pd.read_csv("data/final_training_dataset.csv")

print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ========================
# 🛠 2. FEATURE ENGINEERING
# ========================
print("🛠 Adding time-based features...")

# Convert timestamp to datetime (safe conversion)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract useful time components
df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day
df['month'] = df['timestamp'].dt.month
df['dayofweek'] = df['timestamp'].dt.dayofweek

# ========================
# 🗑 3. PREPARE DATA FOR ML
# ========================
# Drop columns not needed for training
X = df.drop(columns=['aqi', 'timestamp'])  # Model doesn’t need raw timestamp
y = df['aqi']

print(f"✅ Features shape: {X.shape}, Target shape: {y.shape}")

# ========================
# 📊 4. TRAIN/TEST SPLIT
# ========================
print("📊 Splitting into train & test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"✅ Training: {X_train.shape}, Testing: {X_test.shape}")

# ========================
# 🤖 5. TRAIN RANDOM FOREST MODEL
# ========================
print("🤖 Training Random Forest model...")
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
print("✅ Model training complete.")

# ========================
# 📈 6. EVALUATE MODEL
# ========================
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"📊 RMSE on test data: {rmse:.2f}")

# ========================
# 💾 7. SAVE MODEL
# ========================
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/aqi_model.pkl")
print("🎉 Model saved to models/aqi_model.pkl")

# ========================
# 📊 8. EXPORT FEATURE IMPORTANCES
# ========================
print("📊 Saving feature importances...")

importances_df = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values(by='importance', ascending=False)

importances_df.to_csv("models/feature_importance.csv", index=False)
print("✅ Feature importances saved to models/feature_importance.csv")

print("\n🚀 Training complete! Model + feature importance ready.")
