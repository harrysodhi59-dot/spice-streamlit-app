import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Weather & Seasonality", layout="wide")

# -----------------------------
# Image path
# -----------------------------
image_path = os.path.join(os.path.dirname(__file__), "spice.png")

# -----------------------------
# Load weather data
# -----------------------------
@st.cache_data
def load_weather():
    return pd.read_csv("data/edmonton_weather_snow_2018_2025_clean.csv")

weather_df = load_weather()
weather_df["date"] = pd.to_datetime(weather_df["date"])
weather_df["year"] = weather_df["date"].dt.year
weather_df["month"] = weather_df["date"].dt.strftime("%b")
weather_df["month_num"] = weather_df["date"].dt.month

# -----------------------------
# HERO (NEW)
# -----------------------------
left, right = st.columns([1.3,1])

with left:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1E6F5C,#0B3C5D);
                padding:2.5rem;border-radius:25px;color:white;">
        <h1>Weather & <span style='color:#FDB813'>Seasonality</span></h1>
        <p>
        Solar performance is not constant throughout the year. In Edmonton,
        seasonal patterns in sunlight, cloud cover, and snow significantly
        influence energy generation.
        </p>
        <p>
        Understanding this variation helps SPICE explain performance realistically
        to investors and stakeholders.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)

# -----------------------------
# CONTROLS (MOVED FROM SIDEBAR)
# -----------------------------
st.markdown("## Scenario Controls")

years = sorted(weather_df["year"].unique())

c1, c2 = st.columns(2)

selected_year = c1.selectbox("Select Year", years, index=len(years)-1)

metric_options = {
    "Temperature": "temperature",
    "Irradiance": "irradiance",
    "Cloud Cover": "cloud_cover",
    "Snow Depth": "snow_depth_cm"
}

selected_metric_label = c2.selectbox("Primary Metric", list(metric_options.keys()))
selected_metric = metric_options[selected_metric_label]

df = weather_df[weather_df["year"] == selected_year]

monthly = df.groupby(["month","month_num"]).mean().reset_index().sort_values("month_num")

# -----------------------------
# KPIs
# -----------------------------
st.markdown("## Seasonal Snapshot")

k1,k2,k3,k4 = st.columns(4)

k1.metric("Avg Temperature", f"{df['temperature'].mean():.1f} °C")
k2.metric("Avg Irradiance", f"{df['irradiance'].mean():.2f}")
k3.metric("Avg Cloud Cover", f"{df['cloud_cover'].mean():.1f}")
k4.metric("Max Snow", f"{df['snow_depth_cm'].max():.1f} cm")

# -----------------------------
# 🔥 DYNAMIC INSIGHT (IMPORTANT)
# -----------------------------
peak_month = monthly.loc[monthly["irradiance"].idxmax()]["month"]
low_month = monthly.loc[monthly["irradiance"].idxmin()]["month"]

insight = f"""
Solar production in {selected_year} is highly seasonal. Peak generation occurs in **{peak_month}**
due to higher irradiance and longer daylight hours, while the lowest production is observed in
**{low_month}**, driven by reduced sunlight and winter conditions.

This variation highlights why SPICE focuses on **annual performance rather than monthly output**
when evaluating investment decisions.
"""

st.markdown(f"""
<div style="background:#0f2a2a;padding:1rem;border-left:5px solid #FDB813;border-radius:10px;">
{insight}
</div>
""", unsafe_allow_html=True)

# -----------------------------
# CHART 1
# -----------------------------
st.markdown("## Monthly Trend")

fig = px.line(monthly, x="month", y=selected_metric, markers=True)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# CHART 2
# -----------------------------
st.markdown("## Solar Context")

compare = monthly[["month","irradiance","clear_sky_radiation"]].melt(
    id_vars="month", var_name="Type", value_name="Value"
)

fig2 = px.line(compare, x="month", y="Value", color="Type", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# BUSINESS EXPLANATION (UPGRADED)
# -----------------------------
st.markdown("## Business Interpretation")

st.markdown("""
<div style="background:#f8fafc;padding:1.5rem;border-radius:20px;">
<h4>Why seasonality matters for SPICE</h4>

<ul>
<li>Solar output varies significantly across months</li>
<li>Winter reduces production due to snow + low sunlight</li>
<li>Summer drives most of annual energy generation</li>
<li>Investment decisions must consider yearly averages, not monthly fluctuations</li>
</ul>

<p>
This helps SPICE communicate realistic expectations to investors and stakeholders,
avoiding misinterpretation of short-term performance.
</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# HEATMAP
# -----------------------------
st.markdown("## Monthly Climate Overview")

heat = monthly.set_index("month")[[
    "temperature","irradiance","cloud_cover","snow_depth_cm"
]]

fig3 = px.imshow(heat, aspect="auto")
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<div style="margin-top:20px;padding:1rem;background:#0b3c5d;border-radius:10px;">
Next step: Real Site Validation → Compare model insights with actual SPICE installations.
</div>
""", unsafe_allow_html=True)
