🧪 Test Cases - ClimateScope Travel Planner Dashboard


✅ Test Case 1: Application Launch

- Input: Run "streamlit run dashboard/app.py"
- Expected Result: Dashboard loads successfully without errors


✅ Test Case 2: Dataset Availability

- Input: Dataset file present in "data/weather_cleaned.csv"
- Expected Result: Data loads correctly


❌ Test Case 3: Missing Dataset

- Input: Remove dataset file
- Expected Result: Error message displayed: "Dataset not found"


✅ Test Case 4: Required Columns Check

- Input: Dataset with all required columns
- Expected Result: Application runs normally


❌ Test Case 5: Missing Columns

- Input: Dataset missing required columns
- Expected Result: Error message indicating missing column


✅ Test Case 6: Country Selection Filter

- Input: Select a country from dropdown
- Expected Result: Dashboard updates data based on selected country


✅ Test Case 7: Date Range Filter

- Input: Select valid date range
- Expected Result: Filtered data displayed correctly


❌ Test Case 8: Invalid Date Range

- Input: Incorrect or empty date input
- Expected Result: Safe handling without crash


✅ Test Case 9: KPI Calculation

- Input: Valid filtered dataset
- Expected Result: Correct values for temperature, humidity, wind


✅ Test Case 10: Travel Recommendation

- Input: Temperature > 35°C

- Expected Result: "Too hot - Travel not recommended"

- Input: Temperature < 10°C

- Expected Result: "Too cold - Travel with caution"

- Input: Temperature between 10°C–35°C

- Expected Result: "Good weather for travel"


✅ Test Case 11: Rainfall Check

- Input: Rainfall > 50 mm
- Expected Result: Warning message shown


✅ Test Case 12: Best Month Suggestion

- Input: Country selected
- Expected Result: Ideal months (20°C–30°C) displayed


✅ Test Case 13: Temperature Trend Graph

- Input: Valid dataset
- Expected Result: Line chart renders correctly


✅ Test Case 14: Country Comparison

- Input: Select multiple countries
- Expected Result: Multi-line comparison chart displayed


❌ Test Case 15: No Data After Filter

- Input: Apply filters with no matching data
- Expected Result: Warning message displayed


✅ Test Case 16: Extreme Weather Detection

- Input: High temperature (>35°C)
- Expected Result: Heatwave count displayed


✅ Test Case 17: Flood Detection

- Input: Rainfall > 50 mm
- Expected Result: Flood risk count displayed


✅ Test Case 18: Global Map Visualization

- Input: Valid dataset
- Expected Result: Choropleth map renders correctly


📌 Conclusion

All core functionalities including filtering, visualization, and recommendation system are tested and working as expected.
