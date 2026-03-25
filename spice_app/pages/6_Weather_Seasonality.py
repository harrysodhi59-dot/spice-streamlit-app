import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Weather & Seasonality",
    page_icon="🌦️",
    layout="wide"
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.hero {
    background: linear-gradient(90deg, #1E6F5C, #0B3C5D);
    padding: 2.5rem;
    border-radius: 22px;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 16px 36px rgba(0,0,0,0.14);
}

.hero h1 {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.6rem;
}

.hero p {
    font-size: 1.05rem;
    line-height: 1.7;
    max-width: 900px;
}

.card {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 10px 26px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}

.kpi-card {
    background: white;
    border-radius: 18px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
}

.kpi-title {
    color: #0B3C5D;
    font-size: 0.95rem;
    font-weight: 700;
}

.kpi-value {
    color: #1E6F5C;
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 0.35rem;
}

.section-title {
    color: #0B3C5D;
    font-size: 1.55rem;
    font-weight: 800;
    margin-top: 0.6rem;
    margin-bottom: 0.8rem;
}

.sub-label {
    color: #1E6F5C;
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
}

.highlight-box {
    background: #F7F9F9;
    border-left: 6px solid #FDB813;
    padding: 1rem 1rem 1rem 1.1rem;
    border-radius: 12px;
    margin-bottom: 0.8rem;
}

.footer-note {
    background: #EEF5F3;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    color: #234;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load weather data
# -----------------------------
@st.cache_data
def load_weather():
    return pd.read_csv("data/edmonton_weather_snow_2018_2025_clean.csv")

try:
    weather_df = load_weather()
except Exception as e:
    st.error(f"Could not load weather dataset: {e}")
    st.stop()

weather_df.columns = [str(c).strip() for c in weather_df.columns]

required_cols = [
    "date",
    "temperature",
    "irradiance",
    "wind_speed",
    "clear_sky_radiation",
    "cloud_cover",
    "snow_depth_cm"
]

missing_cols = [c for c in required_cols if c not in weather_df.columns]

if missing_cols:
    st.error(f"Missing columns in weather dataset: {missing_cols}")
    st.write("Columns found:", list(weather_df.columns))
    st.stop()

# -----------------------------
# Prepare data
# -----------------------------
weather_df["date"] = pd.to_datetime(weather_df["date"], errors="coerce")
weather_df = weather_df.dropna(subset=["date"]).copy()

weather_df["year"] = weather_df["date"].dt.year
weather_df["month_num"] = weather_df["date"].dt.month
weather_df["month_name"] = weather_df["date"].dt.strftime("%b")

month_order = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

# -----------------------------
# Hero
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="sub-label">Climate Context</div>
    <h1>Weather & Seasonality</h1>
    <p>
        This page provides climate and seasonal context for solar performance in Edmonton.
        It helps explain how temperature, irradiance, wind, cloud cover, and snow depth
        shape seasonal solar production patterns and project realism.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Weather Controls")

available_years = sorted(weather_df["year"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", available_years, index=len(available_years)-1)

metric_options = {
    "Temperature (°C)": "temperature",
    "Irradiance": "irradiance",
    "Wind Speed": "wind_speed",
    "Clear Sky Radiation": "clear_sky_radiation",
    "Cloud Cover": "cloud_cover",
    "Snow Depth (cm)": "snow_depth_cm"
}

selected_metric_label = st.sidebar.selectbox("Primary Metric", list(metric_options.keys()))
selected_metric = metric_options[selected_metric_label]

year_df = weather_df[weather_df["year"] == selected_year].copy()

monthly_avg = (
    year_df.groupby(["month_num", "month_name"])[
        ["temperature", "irradiance", "wind_speed", "clear_sky_radiation", "cloud_cover", "snow_depth_cm"]
    ]
    .mean()
    .reset_index()
    .sort_values("month_num")
)

# -----------------------------
# KPI row
# -----------------------------
avg_temp = year_df["temperature"].mean()
avg_irr = year_df["irradiance"].mean()
avg_cloud = year_df["cloud_cover"].mean()
max_snow = year_df["snow_depth_cm"].max()

st.markdown("## Seasonal Snapshot")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Temperature</div>
        <div class="kpi-value">{avg_temp:.1f} °C</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Irradiance</div>
        <div class="kpi-value">{avg_irr:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Cloud Cover</div>
        <div class="kpi-value">{avg_cloud:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Max Snow Depth</div>
        <div class="kpi-value">{max_snow:.1f} cm</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Interpretation cards
# -----------------------------
left, right = st.columns(2)

with left:
    st.markdown(f"""
    <div class="card">
        <div class="sub-label">Seasonal Meaning</div>
        <div class="section-title">Why weather context matters</div>
        <p>
            Solar output is strongly influenced by local environmental conditions.
            In Edmonton, seasonal shifts in daylight, temperature, cloud cover,
            and snow accumulation create meaningful variation in system performance.
        </p>
        <p>
            This weather layer helps explain why annual solar production is not
            evenly distributed across months.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="card">
        <div class="sub-label">Selected Year</div>
        <div class="section-title">Climate profile for {selected_year}</div>
        <p>
            The selected year provides a reference point for interpreting weather-driven
            solar conditions. Monthly averages help reveal broad performance patterns,
            especially winter constraints and summer production advantages.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Charts
# -----------------------------
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Monthly Trend</div>
        <div class="section-title">Primary Weather Metric by Month</div>
    """, unsafe_allow_html=True)

    fig_metric = px.line(
        monthly_avg,
        x="month_name",
        y=selected_metric,
        markers=True
    )
    fig_metric.update_layout(
        xaxis_title="Month",
        yaxis_title=selected_metric_label,
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_metric, use_container_width=True)

    st.markdown("""
        <p>
            This chart highlights how the selected weather metric changes across the year.
            Seasonal variation in these values provides important context for understanding
            changes in solar production.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Solar Context</div>
        <div class="section-title">Irradiance vs Clear Sky Radiation</div>
    """, unsafe_allow_html=True)

    compare_df = monthly_avg[["month_name", "irradiance", "clear_sky_radiation"]].copy()
    compare_long = compare_df.melt(
        id_vars="month_name",
        value_vars=["irradiance", "clear_sky_radiation"],
        var_name="Metric",
        value_name="Value"
    )

    fig_compare = px.line(
        compare_long,
        x="month_name",
        y="Value",
        color="Metric",
        markers=True
    )
    fig_compare.update_layout(
        xaxis_title="Month",
        yaxis_title="Value",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    st.markdown("""
        <p>
            Comparing observed irradiance with clear sky radiation helps show how
            atmospheric conditions such as cloud cover reduce available solar energy
            relative to idealized sky conditions.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Additional seasonal indicators
# -----------------------------
st.markdown("## Seasonal indicators")

a, b, c = st.columns(3)

winter_avg = monthly_avg[monthly_avg["month_name"].isin(["Dec", "Jan", "Feb"])]
summer_avg = monthly_avg[monthly_avg["month_name"].isin(["Jun", "Jul", "Aug"])]

winter_temp = winter_avg["temperature"].mean()
summer_temp = summer_avg["temperature"].mean()
winter_cloud = winter_avg["cloud_cover"].mean()
summer_irr = summer_avg["irradiance"].mean()
winter_snow = winter_avg["snow_depth_cm"].mean()

with a:
    st.markdown(f"""
    <div class="highlight-box">
        <strong>Winter Temperature</strong><br>
        Average winter temperature is approximately <strong>{winter_temp:.1f} °C</strong>.
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown(f"""
    <div class="highlight-box">
        <strong>Winter Snow Depth</strong><br>
        Average winter snow depth is approximately <strong>{winter_snow:.1f} cm</strong>.
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown(f"""
    <div class="highlight-box">
        <strong>Summer Irradiance</strong><br>
        Average summer irradiance is approximately <strong>{summer_irr:.2f}</strong>.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Heatmap-style monthly summary
# -----------------------------
st.markdown("## Monthly climate summary")

heatmap_df = monthly_avg[[
    "month_name", "temperature", "irradiance", "wind_speed",
    "clear_sky_radiation", "cloud_cover", "snow_depth_cm"
]].copy()

heatmap_long = heatmap_df.melt(
    id_vars="month_name",
    var_name="Metric",
    value_name="Value"
)

st.markdown("""
<div class="card">
    <div class="sub-label">Monthly Overview</div>
    <div class="section-title">Weather Pattern Summary</div>
""", unsafe_allow_html=True)

fig_heat = px.imshow(
    heatmap_long.pivot(index="Metric", columns="month_name", values="Value"),
    aspect="auto",
    color_continuous_scale="YlGnBu"
)
fig_heat.update_layout(
    xaxis_title="Month",
    yaxis_title="Metric"
)
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("""
    <p>
        This summary view shows how weather conditions vary across months. Together,
        these variables help explain the seasonal behavior of solar systems in Edmonton.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Data preview
# -----------------------------
st.markdown("## Weather data preview")
st.dataframe(year_df.head(20), use_container_width=True)

st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Real Site Validation page to compare
    modeled ideas with observed production data from SPICE projects.
</div>
""", unsafe_allow_html=True)
