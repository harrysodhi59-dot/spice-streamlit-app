import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Weather & Seasonality",
    page_icon="🌦️",
    layout="wide"
)

# -----------------------------
# Image path
# -----------------------------
image_path = os.path.join(os.path.dirname(__file__), "spice.png")

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2.4rem;
    padding-left: 2.8rem;
    padding-right: 2.8rem;
    max-width: 100%;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(30,111,92,0.18) 0%, transparent 28%),
        radial-gradient(circle at top right, rgba(253,184,19,0.08) 0%, transparent 18%),
        linear-gradient(180deg, #040816 0%, #07111d 45%, #081423 100%);
    color: #F8FAFC;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141B2D 0%, #182133 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

/* Hero */
.hero-box {
    background: linear-gradient(135deg, rgba(30,111,92,0.96) 0%, rgba(11,60,93,0.96) 100%);
    padding: 2.8rem;
    border-radius: 28px;
    color: white;
    box-shadow: 0 20px 46px rgba(0,0,0,0.34);
    min-height: 360px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
}

.hero-box::after {
    content: "";
    position: absolute;
    top: -30px;
    right: -30px;
    width: 180px;
    height: 180px;
    background: radial-gradient(circle, rgba(253,184,19,0.18) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-label {
    color: #D6EFE6 !important;
    font-size: 0.90rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    margin-bottom: 1rem;
    position: relative;
    z-index: 2;
}

.hero-title {
    font-size: 3rem;
    font-weight: 900;
    line-height: 1.08;
    margin-bottom: 1rem;
    color: #FFFFFF !important;
    position: relative;
    z-index: 2;
}

.hero-highlight {
    color: #FDB813 !important;
}

.hero-text {
    font-size: 1.05rem;
    line-height: 1.85;
    color: #F3F7F6 !important;
    margin-bottom: 0.75rem;
    position: relative;
    z-index: 2;
}

.hero-badge-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.7rem;
    margin-top: 1rem;
    position: relative;
    z-index: 2;
}

.hero-badge {
    display: inline-block;
    background: rgba(253,184,19,0.95);
    color: #111827 !important;
    font-weight: 800;
    padding: 0.58rem 1rem;
    border-radius: 999px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.18);
    font-size: 0.92rem;
}

.hero-chip {
    display: inline-block;
    background: rgba(255,255,255,0.10);
    color: #F8FAFC !important;
    font-weight: 700;
    padding: 0.52rem 0.9rem;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.14);
    font-size: 0.85rem;
}

.image-caption {
    color: #CBD5E1 !important;
    text-align: center;
    font-size: 0.92rem;
    margin-top: 0.75rem;
    line-height: 1.5;
}

[data-testid="stImage"] img {
    border-radius: 26px;
    box-shadow: 0 20px 46px rgba(0,0,0,0.34);
    border: 1px solid rgba(255,255,255,0.08);
    width: 100%;
    object-fit: cover;
}

/* Section text */
.section-heading {
    font-size: 2rem;
    font-weight: 850;
    color: #F8FAFC !important;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
}

.section-subtext {
    color: #B6C0CE !important;
    font-size: 1rem;
    line-height: 1.75;
    margin-bottom: 1.3rem;
}

/* KPI */
.kpi-card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 22px;
    padding: 1.25rem;
    text-align: center;
    box-shadow: 0 12px 26px rgba(0,0,0,0.18);
    border: 1px solid rgba(0,0,0,0.05);
    min-height: 145px;
}

.kpi-title {
    color: #0B3C5D;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.kpi-value {
    color: #1E6F5C;
    font-size: 1.75rem;
    font-weight: 850;
    line-height: 1.2;
}

.kpi-note {
    color: #64748B;
    font-size: 0.86rem;
    margin-top: 0.35rem;
}

/* Cards */
.card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 22px;
    padding: 1.35rem;
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    margin-bottom: 1rem;
    border: 1px solid rgba(0,0,0,0.05);
}

.card,
.card p,
.card span,
.card div,
.card strong,
.card li,
.card h3,
.card h4,
.card ul {
    color: #1F2937 !important;
}

.card-title {
    color: #0B3C5D !important;
    font-size: 1.3rem;
    font-weight: 850;
    margin-bottom: 0.45rem;
}

.card-label {
    color: #1E6F5C !important;
    font-size: 0.88rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.35rem;
}

.small-note {
    color: #334155 !important;
    font-size: 0.95rem;
    line-height: 1.7;
}

/* Insight */
.insight-box {
    background: linear-gradient(90deg, rgba(30,111,92,0.20), rgba(11,60,93,0.18));
    border-left: 6px solid #FDB813;
    border-radius: 18px;
    padding: 1.1rem 1.25rem;
    margin-top: 0.8rem;
    margin-bottom: 1.3rem;
    color: #E5F3EE !important;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    font-size: 0.98rem;
    line-height: 1.75;
}

.insight-box strong {
    color: #8FF0B7 !important;
}

/* Footer */
.footer-note {
    background: linear-gradient(90deg, rgba(30,111,92,0.18), rgba(11,60,93,0.22));
    border-radius: 18px;
    padding: 1rem 1.2rem;
    color: #E5E7EB !important;
    margin-top: 1rem;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
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

# -----------------------------
# Hero
# -----------------------------
hero_left, hero_right = st.columns([1.35, 1], gap="large")

with hero_left:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-label">Climate Context • Seasonal Risk • Production Interpretation</div>
        <div class="hero-title">
            Weather & <span class="hero-highlight">Seasonality</span>
        </div>
        <div class="hero-text">
            This page explains why solar output changes across the year in Edmonton.
            Temperature, irradiance, cloud cover, and snow depth all shape seasonal performance.
        </div>
        <div class="hero-text">
            This context helps SPICE present more realistic expectations to investors,
            stakeholders, and community partners.
        </div>
        <div class="hero-badge-wrap">
            <div class="hero-badge">Climate Context</div>
            <div class="hero-chip">Seasonal Risk</div>
            <div class="hero-chip">Output Interpretation</div>
            <div class="hero-chip">Planning Realism</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hero_right:
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
        st.markdown("""
        <div class="image-caption">
            Seasonal conditions help explain why solar performance is stronger in some months and more constrained in others.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("spice.png not found in the same folder as this page")

# -----------------------------
# Controls on page
# -----------------------------
st.markdown('<div class="section-heading">Weather Scenario Controls</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">Choose the year and focus metric to explore how Edmonton climate conditions shape seasonal solar context.</div>',
    unsafe_allow_html=True
)

available_years = sorted(weather_df["year"].dropna().unique().tolist())

metric_options = {
    "Temperature (°C)": "temperature",
    "Irradiance": "irradiance",
    "Wind Speed": "wind_speed",
    "Clear Sky Radiation": "clear_sky_radiation",
    "Cloud Cover": "cloud_cover",
    "Snow Depth (cm)": "snow_depth_cm"
}

c1, c2 = st.columns(2, gap="large")

selected_year = c1.selectbox("📅 Select Year", available_years, index=len(available_years)-1)
selected_metric_label = c2.selectbox("📊 Primary Metric", list(metric_options.keys()))
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
# KPIs
# -----------------------------
avg_temp = year_df["temperature"].mean()
avg_irr = year_df["irradiance"].mean()
avg_cloud = year_df["cloud_cover"].mean()
max_snow = year_df["snow_depth_cm"].max()

st.markdown('<div class="section-heading">Seasonal Snapshot</div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4, gap="large")

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🌡️ Average Temperature</div>
        <div class="kpi-value">{avg_temp:.1f} °C</div>
        <div class="kpi-note">Selected year average</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">☀️ Average Irradiance</div>
        <div class="kpi-value">{avg_irr:.2f}</div>
        <div class="kpi-note">Solar resource context</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">☁️ Average Cloud Cover</div>
        <div class="kpi-value">{avg_cloud:.1f}</div>
        <div class="kpi-note">Atmospheric condition</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">❄️ Max Snow Depth</div>
        <div class="kpi-value">{max_snow:.1f} cm</div>
        <div class="kpi-note">Winter constraint indicator</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Dynamic insight
# -----------------------------
peak_irr_month = monthly_avg.loc[monthly_avg["irradiance"].idxmax(), "month_name"]
low_irr_month = monthly_avg.loc[monthly_avg["irradiance"].idxmin(), "month_name"]

winter_avg = monthly_avg[monthly_avg["month_name"].isin(["Dec", "Jan", "Feb"])]
summer_avg = monthly_avg[monthly_avg["month_name"].isin(["Jun", "Jul", "Aug"])]

winter_snow = winter_avg["snow_depth_cm"].mean()
summer_irr = summer_avg["irradiance"].mean()
winter_cloud = winter_avg["cloud_cover"].mean()

if summer_irr > winter_avg["irradiance"].mean() * 2:
    season_strength = "a strong seasonal contrast in solar conditions"
else:
    season_strength = "a moderate seasonal shift in solar conditions"

insight_text = f"""
<strong>Seasonality Insight:</strong> In <strong>{selected_year}</strong>, the highest irradiance appears in
<strong>{peak_irr_month}</strong>, while the lowest irradiance occurs in <strong>{low_irr_month}</strong>.
This creates <strong>{season_strength}</strong> for solar production in Edmonton. Winter months also show
an average snow depth of <strong>{winter_snow:.1f} cm</strong> and higher cloud influence, while summer
conditions support stronger generation potential with average irradiance around <strong>{summer_irr:.2f}</strong>.
This helps SPICE explain why monthly solar output is naturally uneven and why long-term planning should rely on annual patterns rather than short-term fluctuations.
"""

st.markdown(f"""
<div class="insight-box">
    {insight_text}
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Charts
# -----------------------------
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""
    <div class="card">
        <div class="card-label">Monthly Trend</div>
        <div class="card-title">Primary Weather Metric by Month</div>
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        font=dict(family="Segoe UI")
    )
    st.plotly_chart(fig_metric, use_container_width=True)

    st.markdown(f"""
        <p class="small-note">
            This chart shows how <strong>{selected_metric_label}</strong> changes across the year,
            providing important context for seasonal changes in solar performance.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <div class="card-label">Solar Context</div>
        <div class="card-title">Irradiance vs Clear Sky Radiation</div>
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        font=dict(family="Segoe UI")
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            Comparing observed irradiance with clear-sky radiation helps show how real atmospheric conditions reduce solar potential relative to ideal conditions.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Business Interpretation FIXED
# -----------------------------
st.markdown('<div class="section-heading">Business Interpretation</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
    <div class="card-label">Planning Meaning</div>
    <div class="card-title">Why seasonality matters for SPICE</div>
    <p>
        Solar generation in Edmonton is not evenly distributed across the year.
        The combination of lower winter irradiance, higher snow depth, and cloud-related reduction
        means that seasonal constraints are a normal part of project performance.
    </p>
    <p>
        For SPICE, this matters because investor and stakeholder discussions should focus on
        <strong>annual performance, long-term averages, and seasonal realism</strong> rather than expecting
        the same production level every month.
    </p>
    <p>
        In practical terms, this weather context strengthens the credibility of the dashboard by
        explaining why summer months support stronger generation while winter months naturally reduce output.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Pie chart added
# -----------------------------
st.markdown('<div class="section-heading">Monthly Climate Overview</div>', unsafe_allow_html=True)

p1, p2 = st.columns(2, gap="large")

with p1:
    st.markdown("""
    <div class="card">
        <div class="card-label">Season Mix</div>
        <div class="card-title">Irradiance Share by Season</div>
    """, unsafe_allow_html=True)

    season_map = {
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Fall", 10: "Fall", 11: "Fall"
    }

    season_df = monthly_avg.copy()
    season_df["Season"] = season_df["month_num"].map(season_map)

    season_irr = season_df.groupby("Season", as_index=False)["irradiance"].sum()

    season_order = ["Winter", "Spring", "Summer", "Fall"]
    season_irr["Season"] = pd.Categorical(season_irr["Season"], categories=season_order, ordered=True)
    season_irr = season_irr.sort_values("Season")

    fig_pie = px.pie(
        season_irr,
        names="Season",
        values="irradiance",
        hole=0.45
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI"),
        legend_title_text="Season"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            This chart shows how the solar resource is distributed across seasons, making it easier to communicate why annual performance depends heavily on summer and spring conditions.
        </p>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown("""
    <div class="card">
        <div class="card-label">Monthly Overview</div>
        <div class="card-title">Weather Pattern Heatmap</div>
    """, unsafe_allow_html=True)

    heatmap_df = monthly_avg[[
        "month_name", "temperature", "irradiance", "wind_speed",
        "clear_sky_radiation", "cloud_cover", "snow_depth_cm"
    ]].copy()

    heatmap_long = heatmap_df.melt(
        id_vars="month_name",
        var_name="Metric",
        value_name="Value"
    )

    fig_heat = px.imshow(
        heatmap_long.pivot(index="Metric", columns="month_name", values="Value"),
        aspect="auto",
        color_continuous_scale="YlGnBu"
    )
    fig_heat.update_layout(
        xaxis_title="Month",
        yaxis_title="Metric",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI")
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            This summary view shows how major climate variables shift through the year and why solar conditions are stronger in some months than others.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Optional preview
# -----------------------------
st.markdown('<div class="section-heading">Weather Data Preview</div>', unsafe_allow_html=True)
st.dataframe(year_df.head(20), use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Real Site Validation page to compare modeled expectations with observed production behavior from real SPICE-related installations.
</div>
""", unsafe_allow_html=True)
