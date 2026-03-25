import streamlit as st
import pandas as pd
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
    return pd.read_excel("data/sample_250000.xlsx")

@st.cache_data
def load_scenario_data():
    return pd.read_csv("data/St_Augustine_combined_simulated_monthly.csv")

try:
    df = load_main_data()
except Exception as e:
    st.error(f"Could not load sample_250000.xlsx: {e}")
    st.stop()

try:
    scenario_df = load_scenario_data()
except Exception as e:
    st.error(f"Could not load St_Augustine_combined_simulated_monthly.csv: {e}")
    st.stop()

# -----------------------------
# Clean columns
# -----------------------------
df.columns = [str(c).strip() for c in df.columns]
scenario_df.columns = [str(c).strip() for c in scenario_df.columns]

# -----------------------------
# Prepare month fields
# -----------------------------
if "datetime" in df.columns:
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df["month_num"] = df["datetime"].dt.month
    df["month_name"] = df["datetime"].dt.strftime("%b")
else:
    st.error("The file sample_250000.xlsx must contain a 'datetime' column.")
    st.write("Columns found:", list(df.columns))
    st.stop()

# -----------------------------
# Detect target column
# -----------------------------
target_col = None
for col in ["power_per_kw", "power", "energy_per_kw", "P"]:
    if col in df.columns:
        target_col = col
        break

if target_col is None:
    st.error("No expected power column found.")
    st.write("Expected one of: power_per_kw, power, energy_per_kw, P")
    st.write("Columns found:", list(df.columns))
    st.stop()

# -----------------------------
# Hero
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="sub-label">Simulation & Design Analysis</div>
    <h1>Solar Simulation</h1>
    <p>
        This page explores how system size, tilt, and azimuth relate to projected
        solar output using the simulation dataset and scenario-based monthly reference data.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Simulation Controls")

system_size = st.sidebar.slider("System Size (kW)", 1, 100, 10)
tilt = st.sidebar.slider("Tilt (degrees)", 0, 60, 30)
azimuth = st.sidebar.slider("Azimuth (degrees)", -180, 180, 0)

# -----------------------------
# Filtering
# -----------------------------
filtered = df.copy()

if "tilt" in filtered.columns:
    filtered = filtered[filtered["tilt"].between(tilt - 5, tilt + 5)]

if "azimuth" in filtered.columns:
    filtered = filtered[filtered["azimuth"].between(azimuth - 15, azimuth + 15)]

if filtered.empty:
    filtered = df.copy()

# -----------------------------
# Monthly summary
# -----------------------------
monthly_summary = (
    filtered.groupby(["month_num", "month_name"])[target_col]
    .mean()
    .reset_index()
    .sort_values("month_num")
)

monthly_summary["estimated_kwh"] = (
    monthly_summary[target_col] / 1000 * system_size * 24 * 30.4
)

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
# Range
# -----------------------------
st.markdown("## Production Range")

c1, c2, c3 = st.columns(3)
c1.metric("Low Scenario", f"{low_energy:,.0f} kWh")
c2.metric("Average Scenario", f"{avg_energy:,.0f} kWh")
c3.metric("High Scenario", f"{high_energy:,.0f} kWh")

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
        labels={"month_name": "Month", "estimated_kwh": "Estimated Energy (kWh)"}
    )
    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Estimated Energy (kWh)",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    st.markdown("""
        <p>
            This chart shows the projected monthly production pattern based on the selected
            system configuration and filtered simulation records.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Scenario Framing</div>
        <div class="section-title">Low / Average / High Annual Output</div>
    """, unsafe_allow_html=True)

    scenario_chart = pd.DataFrame({
        "Scenario": ["Low", "Average", "High"],
        "Annual Energy (kWh)": [low_energy, avg_energy, high_energy]
    })

    fig_range = px.bar(
        scenario_chart,
        x="Scenario",
        y="Annual Energy (kWh)"
    )
    fig_range.update_layout(
        xaxis_title="Scenario",
        yaxis_title="Annual Energy (kWh)",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_range, use_container_width=True)

    st.markdown("""
        <p>
            These scenario bands provide a simple planning range rather than a single fixed estimate.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Scenario reference
# -----------------------------
st.markdown("## Scenario Comparison Reference")

st.markdown("""
<div class="card">
    <div class="sub-label">Scenario Dataset</div>
    <div class="section-title">St. Augustine Monthly Simulation Reference</div>
""", unsafe_allow_html=True)

month_col = None
for col in ["month", "Month", "month_name", "month_num"]:
    if col in scenario_df.columns:
        month_col = col
        break

energy_col = None
for col in ["monthly_kwh", "energy_kwh", "kwh", "Energy", "energy"]:
    if col in scenario_df.columns:
        energy_col = col
        break

if month_col and energy_col:
    fig_sa = px.line(
        scenario_df,
        x=month_col,
        y=energy_col,
        markers=True
    )
    fig_sa.update_layout(
        xaxis_title="Month",
        yaxis_title="Monthly Energy",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_sa, use_container_width=True)
else:
    st.dataframe(scenario_df.head(10), use_container_width=True)
    st.info("The scenario dataset loaded, but automatic charting columns were not found.")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Preview
# -----------------------------
st.markdown("## Filtered Data Preview")
st.dataframe(filtered.head(15), use_container_width=True)

st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Financial Impact page to translate
    projected output into savings, payback, and project value.
</div>
""", unsafe_allow_html=True)
