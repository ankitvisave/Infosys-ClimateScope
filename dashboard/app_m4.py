import streamlit as st
import pandas as pd
import plotly.express as px
import os
import calendar

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ClimateScope Travel Planner",
    layout="wide"
)

st.title("🌍 ClimateScope Travel Intelligence Dashboard")

st.markdown("""
Analyze global climate data and get **smart travel recommendations**
based on weather conditions.
""")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    file_path = "data/weather_cleaned.csv"

    if not os.path.exists(file_path):
        st.error("❌ Dataset not found. Please check file path.")
        return pd.DataFrame()

    df = pd.read_csv(file_path)

    required_cols = [
        "country", "last_updated",
        "temperature_celsius", "humidity", "wind_kph"
    ]

    for col in required_cols:
        if col not in df.columns:
            st.error(f"❌ Missing column: {col}")
            return pd.DataFrame()

    # Date processing
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")

    if df["last_updated"].isna().sum() > 0:
        st.warning("⚠ Some invalid dates were removed")

    df = df.dropna(subset=["last_updated"])
    df["month"] = df["last_updated"].dt.month

    return df


df = load_data()

if df.empty:
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔧 Filters")

countries = sorted(df["country"].dropna().unique())

if not countries:
    st.error("❌ No country data available")
    st.stop()

selected_country = st.sidebar.selectbox("🌍 Select Country", countries)

min_date = df["last_updated"].min()
max_date = df["last_updated"].max()

date_range = st.sidebar.date_input(
    "📅 Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Safe date handling
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

# ---------------- FILTER ----------------
filtered_df = df[
    (df["country"] == selected_country) &
    (df["last_updated"] >= pd.to_datetime(start_date)) &
    (df["last_updated"] <= pd.to_datetime(end_date))
]

if filtered_df.empty:
    st.warning("⚠ No data available for selected filters")
    st.stop()

# ---------------- KPI ----------------
st.subheader("📊 Climate Overview")

c1, c2, c3, c4 = st.columns(4)

def safe_mean(series):
    return round(series.mean(), 2) if not series.empty else 0

c1.metric("🌡 Avg Temp", f"{safe_mean(filtered_df['temperature_celsius'])} °C")
c2.metric("💧 Humidity", f"{safe_mean(filtered_df['humidity'])} %")
c3.metric("💨 Wind", f"{safe_mean(filtered_df['wind_kph'])} kph")

if "precip_mm" in filtered_df.columns:
    c4.metric("🌧 Rainfall", f"{safe_mean(filtered_df['precip_mm'])} mm")
else:
    c4.metric("🌧 Rainfall", "N/A")

# ---------------- TRAVEL RECOMMENDATION ----------------
st.subheader("✈️ Smart Travel Recommendation")

avg_temp = safe_mean(filtered_df["temperature_celsius"])

if avg_temp > 35:
    st.error("🔥 Too hot - Travel not recommended")
elif avg_temp < 10:
    st.warning("❄ Too cold - Travel with caution")
else:
    st.success("🌤 Good weather for travel")

if "precip_mm" in filtered_df.columns:
    avg_rain = safe_mean(filtered_df["precip_mm"])

    if avg_rain > 50:
        st.warning("🌧 High rainfall expected")
    else:
        st.success("☀ Low rainfall - Good conditions")

# ---------------- BEST MONTH ----------------
st.subheader("📅 Best Month to Travel")

monthly = df[df["country"] == selected_country] \
    .groupby("month")["temperature_celsius"].mean()

ideal_months = monthly[(monthly > 20) & (monthly < 30)].index.tolist()

if ideal_months:
    month_names = [calendar.month_name[m] for m in ideal_months]
    st.success(f"Best travel months: {', '.join(month_names)}")
else:
    st.info("No ideal months found")

# ---------------- TREND ----------------
st.subheader("📈 Temperature Trend")

trend_df = filtered_df.sort_values("last_updated")

fig = px.line(
    trend_df,
    x="last_updated",
    y="temperature_celsius",
    title=f"Temperature Trend - {selected_country}"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- COMPARISON ----------------
st.subheader("🌍 Country Comparison")

selected_countries = st.multiselect(
    "Select countries",
    countries,
    default=countries[:3] if len(countries) >= 3 else countries
)

compare_df = df[df["country"].isin(selected_countries)]

if not compare_df.empty:
    fig2 = px.line(
        compare_df,
        x="last_updated",
        y="temperature_celsius",
        color="country"
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No comparison data available")

# ---------------- EXTREME EVENTS ----------------
st.subheader("⚠️ Extreme Weather Insights")

heatwaves = filtered_df[filtered_df["temperature_celsius"] > 35].shape[0]
st.metric("🔥 Heatwave Events", heatwaves)

if "precip_mm" in filtered_df.columns:
    flood = filtered_df[filtered_df["precip_mm"] > 50].shape[0]
    st.metric("🌊 Flood Risk Events", flood)

# ---------------- GLOBAL MAP ----------------
st.subheader("🌍 Global Temperature Map")

map_df = df.groupby("country", as_index=False)["temperature_celsius"].mean()

fig_map = px.choropleth(
    map_df,
    locations="country",
    locationmode="country names",
    color="temperature_celsius",
    title="Average Temperature by Country"
)

st.plotly_chart(fig_map, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | ClimateScope Project")
