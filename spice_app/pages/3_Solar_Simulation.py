import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Solar Simulation",
    page_icon="☀️",
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
# Data loading
# -----------------------------
@st.cache_data
def load_main_data():
    df = pd.read_csv("spice_app/data/sample_250000.csv")
    return df

@st.cache_data
def load_scenario_data():
    df = pd.read_csv("spice_app/data/St_Augustine_combined_simulated_monthly.csv")
    return df

df = load_main_data()
scenario_df = load_scenario_data()

# -----------------------------
# Clean main dataset
# -----------------------------
df.columns = [c.strip() for c in df.columns]
scenario_df.columns = [c.strip() for c in scenario_df.columns]

# Try to make monthly view from main dataset
if "datetime" in df.columns:
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df["month_name"] = df["datetime"].dt.strftime("%b")
    df["month_num"] = df["datetime"].dt.month
elif "month" in df.columns:
    df["month_num"] = df["month"]
    month_map = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    df["month_name"] = df["month_num"].map(month_map)
else:
    df["month_num"] = 1
    df["month_name"] = "Jan"

# -----------------------------
# Hero
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="sub-label">Simulation & Design Analysis</div>
    <h1>Solar Simulation</h1>
    <p>
        This page explores how solar design variables relate to projected energy
        production. It provides an interactive view of system behavior using the
        project simulation dataset and scenario-based monthly outputs.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar inputs
# -----------------------------
st.sidebar.header("Simulation Controls")

system_size = st.sidebar.slider("System Size (kW)", 1, 100, 10)
tilt = st.sidebar.slider("Tilt (degrees)", 0, 60, 30)
azimuth = st.sidebar.slider("Azimuth (degrees)", -180, 180, 0)

# -----------------------------
# Main simulation logic
# -----------------------------
# Use approximate filtering around chosen tilt/azimuth
if "tilt" in df.columns and "azimuth" in df.columns:
    filtered = df[
        (df["tilt"].between(tilt - 5, tilt + 5)) &
        (df["azimuth"].between(azimuth - 15, azimuth + 15))
    ].copy()
else:
    filtered = df.copy()

if filtered.empty:
    filtered = df.copy()

# Power column
target_col = None
for col in ["power_per_kw", "P", "power", "energy_per_kw"]:
    if col in filtered.columns:
        target_col = col
        break

if target_col is None:
    st.error("No expected power column was found in sample_250000.csv.")
    st.stop()

# Monthly summary from simulation data
monthly_summary = (
    filtered.groupby(["month_num", "month_name"])[target_col]
    .mean()
    .reset_index()
    .sort_values("month_num")
)

# Approximate annual energy
# mean power_per_kw * system_size * 24 * 30.4 for monthly approximate conversion
monthly_summary["estimated_kwh"] = monthly_summary[target_col] / 1000 * system_size * 24 * 30.4
annual_energy = monthly_summary["estimated_kwh"].sum()

low_energy = annual_energy * 0.85
avg_energy = annual_energy
high_energy = annual_energy * 1.15

# -----------------------------
# KPI row
# -----------------------------
st.markdown("## Simulation Summary")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Selected Size</div>
        <div class="kpi-value">{system_size} kW</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Tilt</div>
        <div class="kpi-value">{tilt}°</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Azimuth</div>
        <div class="kpi-value">{azimuth}°</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Estimated Annual Output</div>
        <div class="kpi-value">{annual_energy:,.0f} kWh</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Energy range
# -----------------------------
st.markdown("## Production range")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Low Scenario", f"{low_energy:,.0f} kWh")

with c2:
    st.metric("Average Scenario", f"{avg_energy:,.0f} kWh")

with c3:
    st.metric("High Scenario", f"{high_energy:,.0f} kWh")

# -----------------------------
# Charts
# -----------------------------
left, right = st.columns(2)

with left:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Seasonal Output</div>
        <div class="section-title">Estimated Monthly Energy Production</div>
    """, unsafe_allow_html=True)

    fig_monthly = px.bar(
        monthly_summary,
        x="month_name",
        y="estimated_kwh",
        labels={"month_name": "Month", "estimated_kwh": "Estimated Energy (kWh)"},
        title=""
    )
    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Estimated Energy (kWh)",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    st.markdown("""
        <p>
            This chart highlights the seasonal pattern of projected energy output.
            Higher summer production is expected because of longer daylight hours
            and stronger solar conditions.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Scenario Profile</div>
        <div class="section-title">Low / Average / High Annual Output</div>
    """, unsafe_allow_html=True)

    scenario_chart = pd.DataFrame({
        "Scenario": ["Low", "Average", "High"],
        "Annual Energy (kWh)": [low_energy, avg_energy, high_energy]
    })

    fig_range = px.bar(
        scenario_chart,
        x="Scenario",
        y="Annual Energy (kWh)",
        labels={"Annual Energy (kWh)": "Annual Energy (kWh)"},
        title=""
    )
    fig_range.update_layout(
        xaxis_title="Scenario",
        yaxis_title="Annual Energy (kWh)",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_range, use_container_width=True)

    st.markdown("""
        <p>
            The scenario range gives a simple view of uncertainty by showing lower,
            average, and higher production cases. This helps frame solar performance
            as a planning range rather than a single fixed value.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# St. Augustine scenario data
# -----------------------------
st.markdown("## Scenario comparison dataset")

if not scenario_df.empty:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Scenario Dataset</div>
        <div class="section-title">St. Augustine Monthly Simulation Reference</div>
    """, unsafe_allow_html=True)

    possible_month_col = None
    for col in ["month", "Month", "month_name"]:
        if col in scenario_df.columns:
            possible_month_col = col
            break

    possible_energy_col = None
    for col in ["energy_kwh", "monthly_kwh", "kwh", "Energy", "energy"]:
        if col in scenario_df.columns:
            possible_energy_col = col
            break

    if possible_month_col and possible_energy_col:
        scenario_plot_df = scenario_df.copy()
        fig_sa = px.line(
            scenario_plot_df,
            x=possible_month_col,
            y=possible_energy_col,
            markers=True,
            title=""
        )
        fig_sa.update_layout(
            xaxis_title="Month",
            yaxis_title="Monthly Energy",
            plot_bgcolor="white"
        )
        st.plotly_chart(fig_sa, use_container_width=True)

        st.markdown("""
            <p>
                This scenario dataset provides an additional monthly reference point
                for system comparison and can support design discussions across
                alternative project conditions.
            </p>
        """, unsafe_allow_html=True)
    else:
        st.dataframe(scenario_df.head(10), use_container_width=True)
        st.markdown("""
            <p>
                The scenario dataset is loaded successfully. A direct chart was not
                created because the expected month or energy column name was not found.
            </p>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Selected data preview
# -----------------------------
st.markdown("## Filtered data preview")

st.dataframe(
    filtered.head(15),
    use_container_width=True
)

st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Financial Impact page to translate
    projected solar output into savings, payback, and project value.
</div>
""", unsafe_allow_html=True)
