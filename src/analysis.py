# ==========================================================
# ClimateScope Project
# Milestone 2: Core Analysis
# ==========================================================

import pandas as pd
import numpy as np
import os


print("Starting Milestone 2 Analysis...")

# ----------------------------------------------------------
# Step 1: Load Dataset
# ----------------------------------------------------------

file_path = "data/cleaned_weather_data.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    print("Dataset loaded successfully.")
else:
    print("File not found. Please check the path.")
    exit()

print("Dataset shape is:", df.shape)

print("\nFirst 5 rows of dataset:")
print(df.head())

print("\nChecking column names:")
for col in df.columns:
    print("Column:", col)


# ----------------------------------------------------------
# Step 2: Statistical Summary
# ----------------------------------------------------------

print("\nGenerating statistical summary...")

summary = df.describe()

print(summary)

if not os.path.exists("outputs"):
    os.makedirs("outputs")

summary.to_csv("outputs/statistical_summary.csv")

print("Statistical summary saved successfully.")


# ----------------------------------------------------------
# Step 3: Correlation Calculation
# ----------------------------------------------------------

print("\nCalculating correlation between weather parameters...")

columns_for_corr = []
columns_for_corr.append("temperature_celsius")
columns_for_corr.append("humidity")
columns_for_corr.append("precipitation_mm")
columns_for_corr.append("wind_kph")

selected_df = df[columns_for_corr]

correlation_matrix = selected_df.corr()

print("Correlation Matrix:")
print(correlation_matrix)

correlation_matrix.to_csv("outputs/correlation_matrix.csv")

print("Correlation matrix saved.")


# ----------------------------------------------------------
# Step 4: Seasonal Trend Analysis
# ----------------------------------------------------------

print("\nAnalyzing seasonal temperature trends...")

df["date"] = pd.to_datetime(df["date"])

df["month"] = df["date"].dt.month

unique_months = df["month"].unique()

print("Months available in dataset:")
for m in unique_months:
    print("Month:", m)

monthly_avg_list = []

for month_value in range(1, 13):
    month_data = df[df["month"] == month_value]

    if len(month_data) > 0:
        avg_temp = month_data["temperature_celsius"].mean()
        monthly_avg_list.append((month_value, avg_temp))
        print("Average temperature for month", month_value, ":", avg_temp)

print("Seasonal analysis completed.")


# ----------------------------------------------------------
# Step 5: Extreme Weather Detection
# ----------------------------------------------------------

print("\nDetecting extreme weather events...")

temp_threshold = df["temperature_celsius"].quantile(0.95)
rain_threshold = df["precipitation_mm"].quantile(0.95)
wind_threshold = df["wind_kph"].quantile(0.95)

extreme_temp_events = df[df["temperature_celsius"] > temp_threshold]
extreme_rain_events = df[df["precipitation_mm"] > rain_threshold]
extreme_wind_events = df[df["wind_kph"] > wind_threshold]

print("Extreme temperature events count:", len(extreme_temp_events))
print("Extreme rainfall events count:", len(extreme_rain_events))
print("Extreme wind events count:", len(extreme_wind_events))

with open("outputs/extreme_events_summary.txt", "w") as f:
    f.write("Extreme Temperature Events: " + str(len(extreme_temp_events)) + "\n")
    f.write("Extreme Rainfall Events: " + str(len(extreme_rain_events)) + "\n")
    f.write("Extreme Wind Events: " + str(len(extreme_wind_events)) + "\n")

print("Extreme event summary saved.")


# ----------------------------------------------------------
# Step 6: Country Comparison
# ----------------------------------------------------------

print("\nComparing countries based on average temperature...")

countries = df["country"].unique()

country_avg_dict = {}

for country_name in countries:
    country_data = df[df["country"] == country_name]
    avg_temperature = country_data["temperature_celsius"].mean()
    country_avg_dict[country_name] = avg_temperature

sorted_countries = sorted(country_avg_dict.items(), key=lambda x: x[1], reverse=True)

print("\nTop 10 hottest countries:")

counter = 0
for country, value in sorted_countries:
    print(country, ":", value)
    counter += 1
    if counter == 10:
        break

print("\nMilestone 2 completed successfully!")
