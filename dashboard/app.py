import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="ClimateScope Climate Intelligence",
    layout="wide"
)

st.title("🌍 ClimateScope Climate Intelligence Dashboard")

st.markdown(
"""
Interactive dashboard to explore **global climate trends, weather patterns,
and extreme weather events** using real-world weather data.
"""
)

# ------------------------------------------------
# LOAD DATASET
# ------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("data/cleaned_weather_data.csv")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year

    df = df.dropna()

    return df


df = load_data()

# ------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------

st.sidebar.header("Dashboard Filters")

metric = st.sidebar.selectbox(
    "Select Climate Metric",
    [
        "temperature_celsius",
        "humidity",
        "wind_kph",
        "precipitation_mm"
    ]
)

countries = sorted(df["country"].unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=countries[:4]
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    (df["date"].min(), df["date"].max())
)

filtered_df = df[
    (df["country"].isin(selected_countries)) &
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1]))
]

# ------------------------------------------------
# KPI METRICS
# ------------------------------------------------

st.subheader("🌡 Climate Summary")

k1,k2,k3,k4 = st.columns(4)

k1.metric(
    "Avg Temperature",
    f"{filtered_df['temperature_celsius'].mean():.2f} °C"
)

k2.metric(
    "Avg Humidity",
    f"{filtered_df['humidity'].mean():.2f} %"
)

k3.metric(
    "Avg Wind Speed",
    f"{filtered_df['wind_kph'].mean():.2f} km/h"
)

k4.metric(
    "Avg Rainfall",
    f"{filtered_df['precipitation_mm'].mean():.2f} mm"
)

# ------------------------------------------------
# TABS
# ------------------------------------------------

tab1,tab2,tab3,tab4,tab5 = st.tabs([
    "Overview",
    "Temperature Analysis",
    "Climate Relationships",
    "Extreme Events",
    "Global Insights"
])

# ------------------------------------------------
# OVERVIEW
# ------------------------------------------------

with tab1:

    st.subheader("Climate Trend by Country")

    fig1 = px.line(
        filtered_df,
        x="date",
        y=metric,
        color="country",
        markers=True
    )

    st.plotly_chart(fig1,use_container_width=True)

    st.subheader("Top 10 Hottest Countries")

    hottest = (
        filtered_df.groupby("country")["temperature_celsius"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        hottest,
        x="country",
        y="temperature_celsius",
        color="temperature_celsius"
    )

    st.plotly_chart(fig2,use_container_width=True)

    st.subheader("Top 10 Coldest Countries")

    coldest = (
        filtered_df.groupby("country")["temperature_celsius"]
        .mean()
        .sort_values()
        .head(10)
        .reset_index()
    )

    fig3 = px.bar(
        coldest,
        x="country",
        y="temperature_celsius"
    )

    st.plotly_chart(fig3,use_container_width=True)

# ------------------------------------------------
# TEMPERATURE ANALYSIS
# ------------------------------------------------

with tab2:

    st.subheader("Temperature Distribution")

    fig4 = px.histogram(
        filtered_df,
        x="temperature_celsius",
        nbins=50
    )

    st.plotly_chart(fig4,use_container_width=True)

    st.subheader("Monthly Temperature Trend")

    monthly = (
        filtered_df.groupby("month")["temperature_celsius"]
        .mean()
        .reset_index()
    )

    fig5 = px.line(
        monthly,
        x="month",
        y="temperature_celsius",
        markers=True
    )

    st.plotly_chart(fig5,use_container_width=True)

    st.subheader("Country Temperature Boxplot")

    fig6 = px.box(
        filtered_df,
        x="country",
        y="temperature_celsius"
    )

    st.plotly_chart(fig6,use_container_width=True)

    st.subheader("Rolling Temperature Trend")

    rolling = (
        filtered_df.groupby("date")["temperature_celsius"]
        .mean()
        .rolling(7)
        .mean()
        .reset_index()
    )

    fig7 = px.line(
        rolling,
        x="date",
        y="temperature_celsius"
    )

    st.plotly_chart(fig7,use_container_width=True)

# ------------------------------------------------
# CLIMATE RELATIONSHIPS
# ------------------------------------------------

with tab3:

    st.subheader("Temperature vs Humidity")

    fig8 = px.scatter(
        filtered_df,
        x="temperature_celsius",
        y="humidity",
        color="country"
    )

    st.plotly_chart(fig8,use_container_width=True)

    st.subheader("Humidity vs Rainfall")

    fig9 = px.scatter(
        filtered_df,
        x="humidity",
        y="precipitation_mm",
        color="country"
    )

    st.plotly_chart(fig9,use_container_width=True)

    st.subheader("Climate Correlation Heatmap")

    numeric = filtered_df.select_dtypes(include=np.number)

    corr = numeric.corr()

    fig10 = px.imshow(
        corr,
        text_auto=True
    )

    st.plotly_chart(fig10,use_container_width=True)

# ------------------------------------------------
# EXTREME EVENTS
# ------------------------------------------------

with tab4:

    st.subheader("Extreme Temperature Events")

    threshold = filtered_df["temperature_celsius"].quantile(0.95)

    extreme = filtered_df[
        filtered_df["temperature_celsius"] > threshold
    ]

    st.metric("Extreme Heat Events", len(extreme))

    fig11 = px.scatter(
        extreme,
        x="date",
        y="temperature_celsius",
        color="country"
    )

    st.plotly_chart(fig11,use_container_width=True)

    st.subheader("Flood Risk Detection")

    rain_threshold = filtered_df["precipitation_mm"].quantile(0.95)

    floods = filtered_df[
        filtered_df["precipitation_mm"] > rain_threshold
    ]

    st.metric("Heavy Rainfall Events", len(floods))

    fig12 = px.histogram(
        filtered_df,
        x="precipitation_mm",
        nbins=40
    )

    st.plotly_chart(fig12,use_container_width=True)

# ------------------------------------------------
# GLOBAL INSIGHTS
# ------------------------------------------------

with tab5:

    st.subheader("Global Temperature Map")

    country_temp = (
        filtered_df.groupby("country")["temperature_celsius"]
        .mean()
        .reset_index()
    )

    fig13 = px.choropleth(
        country_temp,
        locations="country",
        locationmode="country names",
        color="temperature_celsius",
        color_continuous_scale="thermal"
    )

    st.plotly_chart(fig13,use_container_width=True)

    if "latitude" in filtered_df.columns:

        st.subheader("Latitude vs Temperature")

        fig14 = px.scatter(
            filtered_df,
            x="latitude",
            y="temperature_celsius",
            color="country"
        )

        st.plotly_chart(fig14,use_container_width=True)

# ------------------------------------------------
# DOWNLOAD DATA
# ------------------------------------------------

st.subheader("Download Filtered Dataset")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "climate_filtered_data.csv",
    "text/csv"
)
