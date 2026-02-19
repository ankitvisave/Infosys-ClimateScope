import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("data/GlobalWeatherRepository.csv")

print("Dataset loaded successfully")
print("Shape:", df.shape)

# Inspect dataset
print("\n--- Dataset Info ---")
print(df.info())

print("\n--- Missing Values ---")
print(df.isnull().sum())

# Date conversion
df["date"] = pd.to_datetime(df["date"])

# Handle missing values
df["temperature_celsius"] = df["temperature_celsius"].fillna(df["temperature_celsius"].mean())
df["humidity"] = df["humidity"].fillna(df["humidity"].mean())
df["precipitation_mm"] = df["precipitation_mm"].fillna(0)
df["wind_kph"] = df["wind_kph"].fillna(df["wind_kph"].mean())

print("Missing values handled")

# Feature engineering
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

# Monthly aggregation
monthly_df = (
    df.groupby(["country", "year", "month"])
    .agg({
        "temperature_celsius": "mean",
        "humidity": "mean",
        "precipitation_mm": "sum",
        "wind_kph": "mean"
    })
    .reset_index()
)

print("Monthly aggregation completed")

# Save output
df.to_csv("data/cleaned_weather_data.csv", index=False)
monthly_df.to_csv("data/monthly_weather_data.csv", index=False)

print("Milestone 1 completed successfully")
