import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Solar Simulation",
    page_icon="☀️",
    layout="wide"
)

# =========================================================
# Image path
# =========================================================
image_path = os.path.join(os.path.dirname(__file__), "norquest.png")

# =========================================================
# Styling
# =========================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2.4rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 100%;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(30,111,92,0.18) 0%, transparent 28%),
        radial-gradient(circle at top right, rgba(253,184,19,0.08) 0%, transparent 18%),
        linear-gradient(180deg, #040816 0%, #07111d 45%, #081423 100%);
    color: #F8FAFC;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141B2D 0%, #182133 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

.hero-box {
    background: linear-gradient(135deg, rgba(30,111,92,0.96) 0%, rgba(11,60,93,0.96) 100%);
    padding: 2.8rem;
    border-radius: 28px;
    color: white;
    box-shadow: 0 20px 46px rgba(0,0,0,0.34);
    min-height: 355px;
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
    line-height: 1.88;
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

.kpi-card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 22px;
    padding: 1.25rem;
    text-align: center;
    box-shadow: 0 12px 26px rgba(0,0,0,0.18);
    border: 1px solid rgba(0,0,0,0.05);
    min-height: 140px;
}

.kpi-title {
    color: #0B3C5D;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.kpi-value {
    color: #1E6F5C;
    font-size: 1.8rem;
    font-weight: 850;
    line-height: 1.2;
}

.card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 22px;
    padding: 1.3rem;
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    margin-bottom: 1rem;
    border: 1px solid rgba(0,0,0,0.05);
}

.card-title {
    color: #0B3C5D;
    font-size: 1.3rem;
    font-weight: 850;
    margin-bottom: 0.45rem;
}

.card-label {
    color: #1E6F5C;
    font-size: 0.88rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.35rem;
}

.small-note {
    color: #334155;
    font-size: 0.95rem;
    line-height: 1.7;
}

.insight-box {
    background: linear-gradient(90deg, rgba(30,111,92,0.18), rgba(11,60,93,0.18));
    border-left: 6px solid #FDB813;
    border-radius: 18px;
    padding: 1.1rem 1.25rem;
    margin-top: 0.9rem;
    margin-bottom: 1.3rem;
    color: #E5F3EE !important;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    font-size: 0.98rem;
    line-height: 1.75;
}

.metric-strip {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 1.15rem 1.2rem;
    margin-bottom: 1rem;
}

.metric-label-dark {
    color: #CBD5E1 !important;
    font-size: 0.90rem;
    margin-bottom: 0.35rem;
}

.metric-value-dark {
    color: #F8FAFC !important;
    font-size: 1.95rem;
    font-weight: 850;
}

.footer-note {
    background: linear-gradient(90deg, rgba(30,111,92,0.18), rgba(11,60,93,0.22));
    border-radius: 18px;
    padding: 1rem 1.2rem;
    color: #E5E7EB !important;
    margin-top: 1rem;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
}

@media (max-width: 900px) {
    .hero-title {
        font-size: 2.2rem;
    }
    .hero-box {
        min-height: auto;
        padding: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# Helper functions
# =========================================================
@st.cache_data
def list_available_datasets():
    data_dir = Path("data")
    files = []
    if data_dir.exists():
        for ext in ["*.xlsx", "*.csv"]:
            files.extend(data_dir.glob(ext))
    return sorted(files, key=lambda x: x.name.lower())

@st.cache_data
def load_dataset(path_str):
    path = Path(path_str)
    if path.suffix.lower() == ".xlsx":
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    df.columns = [str(c).strip() for c in df.columns]
    return df

def detect_columns(df):
    datetime_col = None
    for col in ["datetime", "date", "Date", "timestamp", "Timestamp"]:
        if col in df.columns:
            datetime_col = col
            break

    tilt_col = None
    for col in ["tilt", "Tilt", "surface_tilt"]:
        if col in df.columns:
            tilt_col = col
            break

    azimuth_col = None
    for col in ["azimuth", "Azimuth", "surface_azimuth"]:
        if col in df.columns:
            azimuth_col = col
            break

    target_col = None
    for col in ["power_per_kw", "power", "energy_per_kw", "P", "kwh", "energy", "Energy"]:
        if col in df.columns:
            target_col = col
            break

    return datetime_col, tilt_col, azimuth_col, target_col

def prepare_main_df(df, datetime_col):
    temp = df.copy()
    temp[datetime_col] = pd.to_datetime(temp[datetime_col], errors="coerce")
    temp = temp.dropna(subset=[datetime_col]).copy()
    temp["month_num"] = temp[datetime_col].dt.month
    temp["month_name"] = temp[datetime_col].dt.strftime("%b")
    temp["quarter"] = temp[datetime_col].dt.quarter
    return temp

def get_design_summary(dataframe, chosen_tilt, chosen_azimuth, size_kw, target_col, tilt_col, azimuth_col):
    subset = dataframe[
        dataframe[tilt_col].between(chosen_tilt - 5, chosen_tilt + 5) &
        dataframe[azimuth_col].between(chosen_azimuth - 15, chosen_azimuth + 15)
    ].copy()

    if subset.empty:
        subset = dataframe.copy()

    monthly = (
        subset.groupby(["month_num", "month_name"], as_index=False)[target_col]
        .mean()
        .sort_values("month_num")
    )

    monthly["estimated_kwh"] = monthly[target_col] / 1000 * size_kw * 24 * 30.4
    monthly["quarter"] = ((monthly["month_num"] - 1) // 3) + 1
    annual = monthly["estimated_kwh"].sum()
    return subset, monthly, annual

def apply_plot_style(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.96)",
        font=dict(family="Segoe UI"),
        margin=dict(l=30, r=20, t=50, b=30)
    )
    return fig

def generate_design_insight(system_size, tilt, azimuth, annual_output, best_month, worst_month, low_energy, high_energy):
    return (
        f"<strong>Simulation Insight:</strong> With a selected system size of "
        f"<strong>{system_size} kW</strong>, tilt of <strong>{tilt}°</strong>, and azimuth of "
        f"<strong>{azimuth}°</strong>, the projected filtered production is "
        f"<strong>{annual_output:,.0f} kWh</strong>. The strongest projected month is "
        f"<strong>{best_month}</strong>, while the weakest month is <strong>{worst_month}</strong>. "
        f"Based on the same design window, the likely production range spans from "
        f"<strong>{low_energy:,.0f} kWh</strong> to <strong>{high_energy:,.0f} kWh</strong>. "
        f"This helps SPICE explain how system configuration choices affect output in a clear, scenario-based way."
    )

# =========================================================
# Dataset loading
# =========================================================
available_files = list_available_datasets()

if not available_files:
    st.error("No datasets found in the data folder.")
    st.stop()

main_candidates = []

for file in available_files:
    try:
        test_df = load_dataset(str(file))
        dt_col, tilt_col, azimuth_col, target_col = detect_columns(test_df)
        if dt_col and tilt_col and azimuth_col and target_col:
            main_candidates.append(file)
    except Exception:
        pass

if len(main_candidates) == 0:
    st.error("No valid main simulation dataset found. A main dataset must contain datetime, tilt, azimuth, and a power/energy column.")
    st.stop()

main_candidates = main_candidates[:6]

# =========================================================
# Sidebar controls
# =========================================================
st.sidebar.header("Simulation Controls")

selected_main_file = st.sidebar.selectbox(
    "Main Simulation Dataset",
    options=main_candidates,
    format_func=lambda x: x.name
)

df = load_dataset(str(selected_main_file))
datetime_col, tilt_col, azimuth_col, target_col = detect_columns(df)

if not all([datetime_col, tilt_col, azimuth_col, target_col]):
    st.error("Selected main dataset does not have the required structure.")
    st.stop()

df = prepare_main_df(df, datetime_col)

system_size = st.sidebar.slider("System Size (kW)", 1, 100, 10)
tilt = st.sidebar.slider("Tilt (degrees)", 0, 60, 30)
azimuth = st.sidebar.slider("Azimuth (degrees)", -180, 180, 0)

month_range = st.sidebar.slider("Month Range", 1, 12, (1, 12))
quarter_filter = st.sidebar.multiselect("Quarter Filter", [1, 2, 3, 4], default=[1, 2, 3, 4])

chart_type = st.sidebar.selectbox(
    "Monthly Production Chart",
    ["Line", "Bar", "Area"]
)

baseline_tilt = st.sidebar.slider("Baseline Tilt (comparison)", 0, 60, 20)
baseline_azimuth = st.sidebar.slider("Baseline Azimuth (comparison)", -180, 180, 20)

# =========================================================
# Main calculations
# =========================================================
filtered_selected, monthly_selected, annual_selected = get_design_summary(
    df, tilt, azimuth, system_size, target_col, tilt_col, azimuth_col
)

monthly_selected = monthly_selected[
    monthly_selected["month_num"].between(month_range[0], month_range[1]) &
    monthly_selected["quarter"].isin(quarter_filter)
].copy()

annual_selected_filtered = monthly_selected["estimated_kwh"].sum()

_, monthly_baseline, annual_baseline = get_design_summary(
    df, baseline_tilt, baseline_azimuth, system_size, target_col, tilt_col, azimuth_col
)

monthly_baseline = monthly_baseline[
    monthly_baseline["month_num"].between(month_range[0], month_range[1]) &
    monthly_baseline["quarter"].isin(quarter_filter)
].copy()

annual_baseline_filtered = monthly_baseline["estimated_kwh"].sum()
comparison_gap = annual_selected_filtered - annual_baseline_filtered
comparison_pct = (comparison_gap / annual_baseline_filtered * 100) if annual_baseline_filtered != 0 else 0

low_energy = annual_selected_filtered * 0.85
avg_energy = annual_selected_filtered
high_energy = annual_selected_filtered * 1.15

best_month = monthly_selected.loc[monthly_selected["estimated_kwh"].idxmax(), "month_name"] if not monthly_selected.empty else "N/A"
worst_month = monthly_selected.loc[monthly_selected["estimated_kwh"].idxmin(), "month_name"] if not monthly_selected.empty else "N/A"

design_insight_html = generate_design_insight(
    system_size=system_size,
    tilt=tilt,
    azimuth=azimuth,
    annual_output=annual_selected_filtered,
    best_month=best_month,
    worst_month=worst_month,
    low_energy=low_energy,
    high_energy=high_energy
)

# =========================================================
# Hero
# =========================================================
hero_left, hero_right = st.columns([1.4, 1], gap="large")

with hero_left:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-label">Simulation & Design Analysis</div>
        <div class="hero-title">
            Solar <span class="hero-highlight">Simulation</span>
        </div>
        <div class="hero-text">
            This page helps SPICE evaluate how system size, tilt, and azimuth affect projected solar production.
        </div>
        <div class="hero-text">
            The graphs below update dynamically based on the selected design inputs, making the page more useful for planning and stakeholder discussion.
        </div>
        <div class="hero-badge-wrap">
            <div class="hero-badge">Dynamic Output View</div>
            <div class="hero-chip">System Size</div>
            <div class="hero-chip">Tilt</div>
            <div class="hero-chip">Azimuth</div>
            <div class="hero-chip">Production Forecast</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hero_right:
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
        st.markdown("""
        <div class="image-caption">
            Visual context for solar planning and system-level production forecasting.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("norquest.png not found in the same folder as this page")

# =========================================================
# KPI row
# =========================================================
st.markdown('<div class="section-heading">Simulation Summary</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">A quick summary of the currently selected solar configuration and its projected production.</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5, gap="large")

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Dataset</div>
        <div class="kpi-value" style="font-size:1.02rem;">{selected_main_file.name[:18]}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">System Size</div>
        <div class="kpi-value">{system_size} kW</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Tilt</div>
        <div class="kpi-value">{tilt}°</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Azimuth</div>
        <div class="kpi-value">{azimuth}°</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Projected Output</div>
        <div class="kpi-value">{annual_selected_filtered:,.0f} kWh</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Dynamic insight
# =========================================================
st.markdown(f"""
<div class="insight-box">
    {design_insight_html}
</div>
""", unsafe_allow_html=True)

# =========================================================
# Production range
# =========================================================
st.markdown('<div class="section-heading">Production Range</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4, gap="large")

with m1:
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">Low Scenario</div>
        <div class="metric-value-dark">{low_energy:,.0f} kWh</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">Average Scenario</div>
        <div class="metric-value-dark">{avg_energy:,.0f} kWh</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">High Scenario</div>
        <div class="metric-value-dark">{high_energy:,.0f} kWh</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">Peak Month</div>
        <div class="metric-value-dark">{best_month}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Monthly production + quarterly output
# =========================================================
st.markdown('<div class="section-heading">Production Performance</div>', unsafe_allow_html=True)

left, right = st.columns(2, gap="large")

with left:
    st.markdown("""
    <div class="card">
        <div class="card-label">Monthly Output</div>
        <div class="card-title">Monthly Production for Selected System</div>
    """, unsafe_allow_html=True)

    if chart_type == "Line":
        fig_monthly = px.line(
            monthly_selected,
            x="month_name",
            y="estimated_kwh",
            markers=True
        )
    elif chart_type == "Bar":
        fig_monthly = px.bar(
            monthly_selected,
            x="month_name",
            y="estimated_kwh"
        )
    else:
        fig_monthly = px.area(
            monthly_selected,
            x="month_name",
            y="estimated_kwh"
        )

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Estimated Energy (kWh)"
    )
    apply_plot_style(fig_monthly)
    st.plotly_chart(fig_monthly, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            This chart updates directly when the selected system size, tilt, or azimuth changes.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="card-label">Quarterly Output</div>
        <div class="card-title">Quarterly Production Summary</div>
    """, unsafe_allow_html=True)

    q_selected = monthly_selected.groupby("quarter", as_index=False)["estimated_kwh"].sum()
    q_selected["quarter_label"] = "Q" + q_selected["quarter"].astype(str)

    fig_quarter = px.bar(
        q_selected,
        x="quarter_label",
        y="estimated_kwh",
        text="estimated_kwh"
    )
    fig_quarter.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_quarter.update_layout(
        xaxis_title="Quarter",
        yaxis_title="Estimated Energy (kWh)"
    )
    apply_plot_style(fig_quarter)
    st.plotly_chart(fig_quarter, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            This quarterly view helps explain seasonal production patterns in a more business-friendly format.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Annual output + comparison
# =========================================================
st.markdown('<div class="section-heading">System Evaluation</div>', unsafe_allow_html=True)

a1, a2 = st.columns(2, gap="large")

with a1:
    st.markdown("""
    <div class="card">
        <div class="card-label">Annual Output</div>
        <div class="card-title">Projected Energy for Selected System</div>
    """, unsafe_allow_html=True)

    annual_df = pd.DataFrame({
        "Metric": ["Projected Output"],
        "Annual Energy (kWh)": [annual_selected_filtered]
    })

    fig_annual = px.bar(
        annual_df,
        x="Metric",
        y="Annual Energy (kWh)",
        text="Annual Energy (kWh)",
        color="Metric",
        color_discrete_map={"Projected Output": "#1E6F5C"}
    )
    fig_annual.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig_annual.update_layout(
        xaxis_title="",
        yaxis_title="Annual Energy (kWh)",
        showlegend=False
    )
    apply_plot_style(fig_annual)
    st.plotly_chart(fig_annual, use_container_width=True)

    st.markdown(f"""
        <p class="small-note">
            For the current configuration, the filtered annual projection is <strong>{annual_selected_filtered:,.0f} kWh</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

with a2:
    st.markdown("""
    <div class="card">
        <div class="card-label">Design Comparison</div>
        <div class="card-title">Selected vs Baseline Annual Output</div>
    """, unsafe_allow_html=True)

    compare_df = pd.DataFrame({
        "Design": ["Selected Design", "Baseline Design"],
        "Annual Energy (kWh)": [annual_selected_filtered, annual_baseline_filtered]
    })

    fig_compare = px.bar(
        compare_df,
        x="Design",
        y="Annual Energy (kWh)",
        color="Design",
        text="Annual Energy (kWh)",
        color_discrete_map={
            "Selected Design": "#1E6F5C",
            "Baseline Design": "#FDB813"
        }
    )
    fig_compare.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )
    fig_compare.update_layout(
        xaxis_title="",
        yaxis_title="Annual Energy (kWh)",
        showlegend=False
    )
    apply_plot_style(fig_compare)
    st.plotly_chart(fig_compare, use_container_width=True)

    st.markdown(f"""
        <p class="small-note">
            The selected design produces <strong>{annual_selected_filtered:,.0f} kWh</strong>, while the baseline design
            produces <strong>{annual_baseline_filtered:,.0f} kWh</strong>. That is a difference of
            <strong>{comparison_gap:,.0f} kWh</strong> ({comparison_pct:,.1f}%).
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Heatmap + tilt line
# =========================================================
st.markdown('<div class="section-heading">Tilt and Azimuth Performance Patterns</div>', unsafe_allow_html=True)

h1, h2 = st.columns(2, gap="large")

surface_df = (
    df.groupby([tilt_col, azimuth_col], as_index=False)[target_col]
    .mean()
)
surface_df["annual_kwh_est"] = surface_df[target_col] / 1000 * system_size * 24 * 365

with h1:
    st.markdown("""
    <div class="card">
        <div class="card-label">Design Surface</div>
        <div class="card-title">Heatmap of Estimated Annual Output</div>
    """, unsafe_allow_html=True)

    pivot_df = surface_df.pivot(index=tilt_col, columns=azimuth_col, values="annual_kwh_est")

    fig_heatmap = px.imshow(
        pivot_df,
        aspect="auto",
        labels=dict(x="Azimuth (degrees)", y="Tilt (degrees)", color="Annual kWh")
    )
    apply_plot_style(fig_heatmap)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            The heatmap helps show how estimated annual output changes across tilt and azimuth combinations.
        </p>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown("""
    <div class="card">
        <div class="card-label">Tilt Analysis</div>
        <div class="card-title">Tilt vs Annual Energy Output</div>
    """, unsafe_allow_html=True)

    tilt_df = surface_df[
        surface_df[azimuth_col].between(azimuth - 15, azimuth + 15)
    ].copy()

    tilt_summary = (
        tilt_df.groupby(tilt_col, as_index=False)["annual_kwh_est"]
        .mean()
        .sort_values(tilt_col)
    )

    if not tilt_summary.empty:
        fig_tilt = px.line(
            tilt_summary,
            x=tilt_col,
            y="annual_kwh_est",
            markers=True
        )

        fig_tilt.update_layout(
            xaxis_title="Tilt (degrees)",
            yaxis_title="Estimated Annual Energy (kWh)"
        )

        apply_plot_style(fig_tilt)
        st.plotly_chart(fig_tilt, use_container_width=True)

        best_tilt = tilt_summary.loc[
            tilt_summary["annual_kwh_est"].idxmax(), tilt_col
        ]
        best_energy = tilt_summary["annual_kwh_est"].max()

        st.markdown(f"""
            <p class="small-note">
                This graph shows how annual energy output changes with tilt for the selected azimuth range.
                The optimal tilt is approximately <strong>{best_tilt}°</strong>, producing around
                <strong>{best_energy:,.0f} kWh</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No tilt data available for the selected azimuth range.")
        st.markdown("""
            <p class="small-note">
                Adjust the azimuth value to explore how tilt affects annual output under a different design window.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# Data preview
# =========================================================
st.markdown('<div class="section-heading">Filtered Data Preview</div>', unsafe_allow_html=True)

preview_cols = [c for c in [datetime_col, tilt_col, azimuth_col, target_col, "month_name", "quarter"] if c in filtered_selected.columns]
st.dataframe(filtered_selected[preview_cols].head(20), use_container_width=True)

# =========================================================
# Footer
# =========================================================
st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Financial Impact page to convert projected
    solar production into revenue, investment-facing interpretation, and business value for SPICE stakeholders.
</div>
""", unsafe_allow_html=True)
