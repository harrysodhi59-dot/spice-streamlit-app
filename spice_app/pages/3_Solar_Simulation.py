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

.small-note {
    color: #555;
    font-size: 0.95rem;
    line-height: 1.6;
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
    scenario_df = load_scenario_data()
except Exception as e:
    st.error(f"Could not load simulation datasets: {e}")
    st.stop()

df.columns = [str(c).strip() for c in df.columns]
scenario_df.columns = [str(c).strip() for c in scenario_df.columns]

# -----------------------------
# Validate required columns
# -----------------------------
required_main = ["datetime", "tilt", "azimuth"]
missing_main = [c for c in required_main if c not in df.columns]
if missing_main:
    st.error(f"Missing required columns in sample_250000.xlsx: {missing_main}")
    st.write("Columns found:", list(df.columns))
    st.stop()

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
# Prepare fields
# -----------------------------
df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
df = df.dropna(subset=["datetime"]).copy()
df["month_num"] = df["datetime"].dt.month
df["month_name"] = df["datetime"].dt.strftime("%b")

# -----------------------------
# Hero
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="sub-label">Simulation & Design Analysis</div>
    <h1>Solar Simulation</h1>
    <p>
        This page explores how system size, tilt, and azimuth influence projected solar
        output. It is designed to support comparison between design choices rather than
        showing a single static estimate.
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

baseline_tilt = st.sidebar.slider("Baseline Tilt (comparison)", 0, 60, 20)
baseline_azimuth = st.sidebar.slider("Baseline Azimuth (comparison)", -180, 180, 0)

# -----------------------------
# Helper
# -----------------------------
def get_design_summary(dataframe, chosen_tilt, chosen_azimuth, size_kw):
    subset = dataframe.copy()

    subset = subset[
        subset["tilt"].between(chosen_tilt - 5, chosen_tilt + 5) &
        subset["azimuth"].between(chosen_azimuth - 15, chosen_azimuth + 15)
    ].copy()

    if subset.empty:
        subset = dataframe.copy()

    monthly = (
        subset.groupby(["month_num", "month_name"])[target_col]
        .mean()
        .reset_index()
        .sort_values("month_num")
    )

    monthly["estimated_kwh"] = monthly[target_col] / 1000 * size_kw * 24 * 30.4
    annual = monthly["estimated_kwh"].sum()

    return subset, monthly, annual

# Selected design
filtered_selected, monthly_selected, annual_selected = get_design_summary(
    df, tilt, azimuth, system_size
)

# Baseline design
filtered_baseline, monthly_baseline, annual_baseline = get_design_summary(
    df, baseline_tilt, baseline_azimuth, system_size
)

low_energy = annual_selected * 0.85
avg_energy = annual_selected
high_energy = annual_selected * 1.15

annual_difference = annual_selected - annual_baseline
pct_difference = (annual_difference / annual_baseline * 100) if annual_baseline != 0 else 0

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
        <div class="kpi-title">Selected Tilt / Azimuth</div>
        <div class="kpi-value">{tilt}° / {azimuth}°</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Annual Output</div>
        <div class="kpi-value">{annual_selected:,.0f} kWh</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Vs Baseline</div>
        <div class="kpi-value">{pct_difference:+.1f}%</div>
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
# Monthly comparison
# -----------------------------
st.markdown("## Monthly design comparison")

compare_monthly = monthly_selected[["month_num", "month_name", "estimated_kwh"]].copy()
compare_monthly = compare_monthly.rename(columns={"estimated_kwh": "Selected Design"})
compare_monthly["Baseline Design"] = monthly_baseline["estimated_kwh"].values

compare_long = compare_monthly.melt(
    id_vars=["month_num", "month_name"],
    value_vars=["Selected Design", "Baseline Design"],
    var_name="Design",
    value_name="Estimated Energy (kWh)"
)

left, right = st.columns(2)

with left:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Seasonal Output</div>
        <div class="section-title">Selected vs Baseline Monthly Production</div>
    """, unsafe_allow_html=True)

    fig_monthly = px.line(
        compare_long,
        x="month_name",
        y="Estimated Energy (kWh)",
        color="Design",
        markers=True
    )
    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Estimated Energy (kWh)",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            This comparison shows how the selected design performs across the year
            relative to a baseline configuration. It helps frame the value of changing
            tilt or azimuth rather than looking at one configuration in isolation.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Annual Comparison</div>
        <div class="section-title">Design Output Comparison</div>
    """, unsafe_allow_html=True)

    annual_compare_df = pd.DataFrame({
        "Design": ["Selected Design", "Baseline Design"],
        "Annual Energy (kWh)": [annual_selected, annual_baseline]
    })

    fig_annual = px.bar(
        annual_compare_df,
        x="Design",
        y="Annual Energy (kWh)",
        color="Design"
    )
    fig_annual.update_layout(
        xaxis_title="Design",
        yaxis_title="Annual Energy (kWh)",
        plot_bgcolor="white",
        showlegend=False
    )
    st.plotly_chart(fig_annual, use_container_width=True)

    st.markdown(f"""
        <p class="small-note">
            The selected configuration changes annual production by
            <strong>{annual_difference:,.0f} kWh</strong> relative to the baseline design.
            This makes the page more useful for design discussion and scenario evaluation.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Design surface summary
# -----------------------------
st.markdown("## Tilt and azimuth performance patterns")

surface_df = (
    df.groupby(["tilt", "azimuth"])[target_col]
    .mean()
    .reset_index()
)

surface_df["annual_kwh_est"] = surface_df[target_col] / 1000 * system_size * 24 * 365

st.markdown("""
<div class="card">
    <div class="sub-label">Design Surface</div>
    <div class="section-title">Estimated Annual Output Across Tilt and Azimuth</div>
""", unsafe_allow_html=True)

fig_surface = px.scatter(
    surface_df,
    x="azimuth",
    y="tilt",
    size="annual_kwh_est",
    color="annual_kwh_est",
    hover_data=["annual_kwh_est"],
)
fig_surface.update_layout(
    xaxis_title="Azimuth (degrees)",
    yaxis_title="Tilt (degrees)",
    plot_bgcolor="white"
)
st.plotly_chart(fig_surface, use_container_width=True)

st.markdown("""
    <p class="small-note">
        This view shows how projected annual output varies across different design
        combinations in the simulation dataset. It helps identify which tilt and azimuth
        regions tend to produce stronger results.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Scenario reference
# -----------------------------
st.markdown("## Scenario comparison reference")

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
st.dataframe(filtered_selected.head(15), use_container_width=True)

st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Financial Impact page to translate
    projected output into savings, payback, and project value.
</div>
""", unsafe_allow_html=True)
