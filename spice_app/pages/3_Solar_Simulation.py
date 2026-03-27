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

/* Text */
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

/* Cards */
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

/* Insight */
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

/* Scenario metrics */
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

/* Mobile */
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

def guess_reference_columns(df):
    month_col = None
    for col in ["month", "Month", "month_name", "month_num"]:
        if col in df.columns:
            month_col = col
            break

    energy_col = None
    for col in ["monthly_kwh", "energy_kwh", "kwh", "Energy", "energy"]:
        if col in df.columns:
            energy_col = col
            break

    site_col = None
    for col in ["site", "Site", "building", "Building", "scenario", "Scenario"]:
        if col in df.columns:
            site_col = col
            break

    return month_col, energy_col, site_col

def format_signed_value(value, suffix=""):
    if value > 0:
        return f"+{value:,.1f}{suffix}"
    if value < 0:
        return f"{value:,.1f}{suffix}"
    return f"{value:,.1f}{suffix}"

def generate_design_insight(system_size, tilt, azimuth, baseline_tilt, baseline_azimuth,
                            output_selected, output_baseline, pct_difference,
                            annual_difference, best_month, worst_month):
    direction = "improves" if annual_difference > 0 else "reduces" if annual_difference < 0 else "maintains"
    strength = abs(pct_difference)

    if strength >= 10:
        impact_phrase = "a strong shift in projected performance"
    elif strength >= 5:
        impact_phrase = "a noticeable improvement in projected output" if annual_difference > 0 else "a noticeable reduction in projected output"
    elif strength >= 1:
        impact_phrase = "a moderate design difference"
    else:
        impact_phrase = "only a small change"

    if annual_difference > 0:
        compare_text = (
            f"This selected setup produces {abs(annual_difference):,.0f} kWh more than the baseline, "
            f"which is {abs(pct_difference):.1f}% higher."
        )
    elif annual_difference < 0:
        compare_text = (
            f"This selected setup produces {abs(annual_difference):,.0f} kWh less than the baseline, "
            f"which is {abs(pct_difference):.1f}% lower."
        )
    else:
        compare_text = "This selected setup performs almost the same as the baseline configuration."

    return (
        f"<strong>Design Insight:</strong> With a selected system size of <strong>{system_size} kW</strong>, "
        f"the current design at <strong>{tilt}° tilt</strong> and <strong>{azimuth}° azimuth</strong> "
        f"generates an estimated <strong>{output_selected:,.0f} kWh</strong> over the filtered period. "
        f"Compared with the baseline setting of <strong>{baseline_tilt}° / {baseline_azimuth}°</strong>, "
        f"the current design <strong>{direction}</strong> projected energy performance and creates "
        f"<strong>{impact_phrase}</strong>. {compare_text} "
        f"The strongest projected month is <strong>{best_month}</strong>, while the weakest month is "
        f"<strong>{worst_month}</strong>. This helps SPICE explain not only what the output is, "
        f"but also how design choices change the business story behind the result."
    )

# =========================================================
# Dataset loading
# =========================================================
available_files = list_available_datasets()

if not available_files:
    st.error("No datasets found in the data folder.")
    st.stop()

main_candidates = []
reference_candidates = []

for file in available_files:
    try:
        test_df = load_dataset(str(file))
        dt_col, tilt_col, azimuth_col, target_col = detect_columns(test_df)
        if dt_col and tilt_col and azimuth_col and target_col:
            main_candidates.append(file)
        else:
            reference_candidates.append(file)
    except Exception:
        pass

if len(main_candidates) == 0:
    st.error("No valid main simulation dataset found. A main dataset must contain datetime, tilt, azimuth, and a power/energy column.")
    st.stop()

main_candidates = main_candidates[:4]
reference_candidates = reference_candidates[:4]

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

baseline_tilt = st.sidebar.slider("Baseline Tilt (comparison)", 0, 60, 20)
baseline_azimuth = st.sidebar.slider("Baseline Azimuth (comparison)", -180, 180, 0)

month_range = st.sidebar.slider("Month Range", 1, 12, (1, 12))
quarter_filter = st.sidebar.multiselect("Quarter Filter", [1, 2, 3, 4], default=[1, 2, 3, 4])

chart_type = st.sidebar.selectbox(
    "Monthly Comparison Chart",
    ["Line", "Bar", "Area"]
)

show_distribution = st.sidebar.checkbox("Show output distribution", value=True)
show_top_designs = st.sidebar.checkbox("Show top design combinations", value=True)

selected_reference_file = None
if reference_candidates:
    selected_reference_file = st.sidebar.selectbox(
        "Reference Dataset (Optional)",
        options=[None] + reference_candidates,
        format_func=lambda x: "None" if x is None else x.name
    )

# =========================================================
# Main calculations
# =========================================================
filtered_selected, monthly_selected, annual_selected = get_design_summary(
    df, tilt, azimuth, system_size, target_col, tilt_col, azimuth_col
)

filtered_baseline, monthly_baseline, annual_baseline = get_design_summary(
    df, baseline_tilt, baseline_azimuth, system_size, target_col, tilt_col, azimuth_col
)

monthly_selected = monthly_selected[
    monthly_selected["month_num"].between(month_range[0], month_range[1]) &
    monthly_selected["quarter"].isin(quarter_filter)
].copy()

monthly_baseline = monthly_baseline[
    monthly_baseline["month_num"].between(month_range[0], month_range[1]) &
    monthly_baseline["quarter"].isin(quarter_filter)
].copy()

annual_selected_filtered = monthly_selected["estimated_kwh"].sum()
annual_baseline_filtered = monthly_baseline["estimated_kwh"].sum()

low_energy = annual_selected_filtered * 0.85
avg_energy = annual_selected_filtered
high_energy = annual_selected_filtered * 1.15

annual_difference = annual_selected_filtered - annual_baseline_filtered
pct_difference = (annual_difference / annual_baseline_filtered * 100) if annual_baseline_filtered != 0 else 0

best_month = monthly_selected.loc[monthly_selected["estimated_kwh"].idxmax(), "month_name"] if not monthly_selected.empty else "N/A"
worst_month = monthly_selected.loc[monthly_selected["estimated_kwh"].idxmin(), "month_name"] if not monthly_selected.empty else "N/A"

design_insight_html = generate_design_insight(
    system_size=system_size,
    tilt=tilt,
    azimuth=azimuth,
    baseline_tilt=baseline_tilt,
    baseline_azimuth=baseline_azimuth,
    output_selected=annual_selected_filtered,
    output_baseline=annual_baseline_filtered,
    pct_difference=pct_difference,
    annual_difference=annual_difference,
    best_month=best_month,
    worst_month=worst_month
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
            This page helps SPICE compare solar design choices by showing how changes in
            system size, tilt, and azimuth affect projected energy output.
        </div>
        <div class="hero-text">
            Instead of presenting one static estimate, the dashboard supports scenario-based
            analysis for design discussion, investor communication, and project planning.
        </div>
        <div class="hero-badge-wrap">
            <div class="hero-badge">Design Comparison</div>
            <div class="hero-chip">Scenario Planning</div>
            <div class="hero-chip">Output Forecasting</div>
            <div class="hero-chip">Decision Support</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hero_right:
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
        st.markdown("""
        <div class="image-caption">
            Visual context for solar planning and stakeholder-facing scenario discussion.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("norquest.png not found in the same folder as this page")

# =========================================================
# KPI row
# =========================================================
st.markdown('<div class="section-heading">Simulation Summary</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">A quick comparison of the current solar design against the chosen baseline configuration.</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5, k6 = st.columns(6, gap="large")

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
        <div class="kpi-title">Selected Size</div>
        <div class="kpi-value">{system_size} kW</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Tilt / Azimuth</div>
        <div class="kpi-value">{tilt}° / {azimuth}°</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Filtered Output</div>
        <div class="kpi-value">{annual_selected_filtered:,.0f} kWh</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Vs Baseline</div>
        <div class="kpi-value">{pct_difference:+.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with k6:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Peak Month</div>
        <div class="kpi-value" style="font-size:1.35rem;">{best_month}</div>
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
        <div class="metric-label-dark">Lowest Month</div>
        <div class="metric-value-dark">{worst_month}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Monthly comparison
# =========================================================
st.markdown('<div class="section-heading">Monthly Design Comparison</div>', unsafe_allow_html=True)

compare_monthly = monthly_selected[["month_num", "month_name", "estimated_kwh"]].copy()
compare_monthly = compare_monthly.rename(columns={"estimated_kwh": "Selected Design"})

baseline_map = monthly_baseline.set_index("month_num")["estimated_kwh"].to_dict()
compare_monthly["Baseline Design"] = compare_monthly["month_num"].map(baseline_map).fillna(0)

compare_long = compare_monthly.melt(
    id_vars=["month_num", "month_name"],
    value_vars=["Selected Design", "Baseline Design"],
    var_name="Design",
    value_name="Estimated Energy (kWh)"
).sort_values("month_num")

left, right = st.columns(2, gap="large")

with left:
    st.markdown("""
    <div class="card">
        <div class="card-label">Seasonal Output</div>
        <div class="card-title">Selected vs Baseline Monthly Production</div>
    """, unsafe_allow_html=True)

    if chart_type == "Line":
        fig_monthly = px.line(
            compare_long,
            x="month_name",
            y="Estimated Energy (kWh)",
            color="Design",
            markers=True
        )
    elif chart_type == "Bar":
        fig_monthly = px.bar(
            compare_long,
            x="month_name",
            y="Estimated Energy (kWh)",
            color="Design",
            barmode="group"
        )
    else:
        fig_monthly = px.area(
            compare_long,
            x="month_name",
            y="Estimated Energy (kWh)",
            color="Design"
        )

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Estimated Energy (kWh)"
    )
    apply_plot_style(fig_monthly)
    st.plotly_chart(fig_monthly, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            This chart shows whether the selected design outperforms the baseline consistently
            across the year or only in certain parts of the seasonal cycle.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="card-label">Quarterly Summary</div>
        <div class="card-title">Quarterly Output Comparison</div>
    """, unsafe_allow_html=True)

    q_selected = monthly_selected.groupby("quarter", as_index=False)["estimated_kwh"].sum()
    q_selected["Design"] = "Selected Design"

    q_baseline = monthly_baseline.groupby("quarter", as_index=False)["estimated_kwh"].sum()
    q_baseline["Design"] = "Baseline Design"

    q_compare = pd.concat([q_selected, q_baseline], ignore_index=True)
    q_compare["quarter_label"] = "Q" + q_compare["quarter"].astype(str)

    fig_quarter = px.bar(
        q_compare,
        x="quarter_label",
        y="estimated_kwh",
        color="Design",
        barmode="group"
    )
    fig_quarter.update_layout(
        xaxis_title="Quarter",
        yaxis_title="Estimated Energy (kWh)"
    )
    apply_plot_style(fig_quarter)
    st.plotly_chart(fig_quarter, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            Quarterly comparison gives a broader business-friendly view of seasonal output trends,
            which is helpful for investor discussion and planning.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Annual comparison + distribution
# =========================================================
st.markdown('<div class="section-heading">Design Evaluation</div>', unsafe_allow_html=True)

a1, a2 = st.columns(2, gap="large")

with a1:
    st.markdown("""
    <div class="card">
        <div class="card-label">Annual Comparison</div>
        <div class="card-title">Selected vs Baseline Output</div>
    """, unsafe_allow_html=True)

    annual_compare_df = pd.DataFrame({
        "Design": ["Selected Design", "Baseline Design"],
        "Annual Energy (kWh)": [annual_selected_filtered, annual_baseline_filtered]
    })

    fig_annual = px.bar(
        annual_compare_df,
        x="Design",
        y="Annual Energy (kWh)",
        color="Design",
        text="Annual Energy (kWh)"
    )
    fig_annual.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig_annual.update_layout(
        xaxis_title="Design",
        yaxis_title="Annual Energy (kWh)",
        showlegend=False
    )
    apply_plot_style(fig_annual)
    st.plotly_chart(fig_annual, use_container_width=True)

    direction_word = "increase" if annual_difference > 0 else "decrease" if annual_difference < 0 else "change"
    st.markdown(f"""
        <p class="small-note">
            Relative to the baseline, the selected configuration creates an estimated
            <strong>{abs(annual_difference):,.0f} kWh {direction_word}</strong> over the filtered period.
        </p>
    </div>
    """, unsafe_allow_html=True)

with a2:
    st.markdown("""
    <div class="card">
        <div class="card-label">Distribution</div>
        <div class="card-title">Output Distribution for Selected Design Space</div>
    """, unsafe_allow_html=True)

    if show_distribution and not filtered_selected.empty:
        filtered_selected = filtered_selected.copy()
        filtered_selected["estimated_output_kwh"] = filtered_selected[target_col] / 1000 * system_size * 24

        fig_hist = px.histogram(
            filtered_selected,
            x="estimated_output_kwh",
            nbins=30
        )
        fig_hist.update_layout(
            xaxis_title="Estimated Daily Energy Proxy (kWh)",
            yaxis_title="Count"
        )
        apply_plot_style(fig_hist)
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("Distribution chart hidden from sidebar.")

    st.markdown("""
        <p class="small-note">
            This distribution helps show whether projected output is tightly clustered
            or spread across a wider range inside the selected design window.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Heatmap + top combinations
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
            The heatmap reveals where stronger-performing tilt and azimuth combinations appear
            across the broader simulation space.
        </p>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown("""
    <div class="card">
        <div class="card-label">Top Designs</div>
        <div class="card-title">Best Performing Tilt / Azimuth Combinations</div>
    """, unsafe_allow_html=True)

    if show_top_designs:
        top_designs = surface_df.sort_values("annual_kwh_est", ascending=False).head(10).copy()
        top_designs["design_label"] = (
            "T" + top_designs[tilt_col].astype(str) +
            " / A" + top_designs[azimuth_col].astype(str)
        )

        fig_top = px.bar(
            top_designs,
            x="annual_kwh_est",
            y="design_label",
            orientation="h"
        )
        fig_top.update_layout(
            xaxis_title="Estimated Annual Energy (kWh)",
            yaxis_title="Design Combination"
        )
        apply_plot_style(fig_top)
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("Top design chart hidden from sidebar.")

    st.markdown("""
        <p class="small-note">
            This ranking makes it easier to benchmark how the current design compares with
            some of the strongest combinations in the dataset.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Reference dataset section
# =========================================================
st.markdown('<div class="section-heading">Scenario Comparison Reference</div>', unsafe_allow_html=True)

if selected_reference_file is not None:
    reference_df = load_dataset(str(selected_reference_file))
    month_col, energy_col, site_col = guess_reference_columns(reference_df)

    st.markdown("""
    <div class="card">
        <div class="card-label">Reference Dataset</div>
        <div class="card-title">External / Site-Level Scenario Reference</div>
    """, unsafe_allow_html=True)

    if site_col:
        site_options = sorted(reference_df[site_col].dropna().astype(str).unique().tolist())
        chosen_sites = st.multiselect(
            "Filter Reference Sites / Scenarios",
            options=site_options,
            default=site_options[:min(3, len(site_options))]
        )
        if chosen_sites:
            reference_df = reference_df[reference_df[site_col].astype(str).isin(chosen_sites)].copy()

    if month_col and energy_col:
        ref_chart_type = st.selectbox(
            "Reference Chart Type",
            ["Line", "Bar"],
            key="reference_chart_type"
        )

        if ref_chart_type == "Line":
            fig_ref = px.line(
                reference_df,
                x=month_col,
                y=energy_col,
                color=site_col if site_col else None,
                markers=True
            )
        else:
            fig_ref = px.bar(
                reference_df,
                x=month_col,
                y=energy_col,
                color=site_col if site_col else None,
                barmode="group"
            )

        fig_ref.update_layout(
            xaxis_title="Month",
            yaxis_title="Monthly Energy"
        )
        apply_plot_style(fig_ref)
        st.plotly_chart(fig_ref, use_container_width=True)

        if site_col and month_col:
            summary_table = reference_df.groupby(site_col, as_index=False)[energy_col].sum()
            summary_table = summary_table.sort_values(energy_col, ascending=False)
            st.dataframe(summary_table, use_container_width=True)
    else:
        st.dataframe(reference_df.head(20), use_container_width=True)
        st.info("Reference dataset loaded, but no standard month/energy columns were detected.")

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Select a reference dataset from the sidebar if you want site-level or scenario-level comparison.")

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
