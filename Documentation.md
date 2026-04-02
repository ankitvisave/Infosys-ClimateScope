🌍 ClimateScope Travel Planner Dashboard - Documentation

📌 Project Overview

ClimateScope is an interactive data-driven dashboard that analyzes global weather data and provides intelligent travel recommendations. The system helps users make better travel decisions based on climate conditions such as temperature, humidity, wind speed, and rainfall.


🎯 Objectives

- Analyze global climate data effectively
- Provide smart travel recommendations
- Visualize weather trends using interactive charts
- Identify extreme weather conditions
- Suggest best months for travel


🛠 Technologies Used

- Python – Core programming
- Pandas – Data processing and analysis
- Streamlit – Dashboard development
- Plotly – Data visualization
- NumPy – Numerical operations


⚙ Features

🔹 1. Data Processing

- Dataset loading and validation
- Missing value handling
- Date conversion and formatting

🔹 2. Interactive Filters

- Country selection
- Date range filtering

🔹 3. KPI Metrics

- Average temperature
- Humidity
- Wind speed
- Rainfall

🔹 4. Smart Travel Recommendation

- Too hot → Travel not recommended
- Too cold → Travel with caution
- Moderate → Good for travel

🔹 5. Best Month Suggestion

- Identifies ideal months (20°C – 30°C)
- Displays human-readable month names

🔹 6. Data Visualization

- Temperature trend graph
- Multi-country comparison
- Global choropleth map

🔹 7. Extreme Weather Insights

- Heatwave detection
- Flood risk detection


📊 Dataset Information

- Dataset contains weather data with fields:
  - Country
  - Date (last_updated)
  - Temperature (°C)
  - Humidity (%)
  - Wind speed (kph)
  - Rainfall (mm)


▶ How to Run the Project

Step 1: Install dependencies

pip install pandas streamlit plotly numpy

Step 2: Run the application

streamlit run dashboard/app.py


🧠 Working Logic

1. Load dataset
2. Clean and validate data
3. Apply user filters
4. Calculate KPIs
5. Generate insights
6. Display charts and recommendations


🚀 Future Enhancements

- Real-time weather API integration
- AI-based travel recommendation system
- Mobile responsive UI
- User login & personalization
- Advanced analytics dashboard


📌 Conclusion

The ClimateScope Travel Planner Dashboard successfully combines data analysis and visualization to provide meaningful travel insights. It enhances user experience by offering real-time decision-making support based on climate conditions.


👨‍💻 Author
Ankit Visave

Developed as part of Infosys Internship – Milestone 4 Project
