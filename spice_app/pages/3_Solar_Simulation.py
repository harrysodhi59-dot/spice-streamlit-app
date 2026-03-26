import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Solar Simulation",
    page_icon="☀️",
    layout="wide"
)

# =========================================================
# Styling
# =========================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}

.hero {
    background: linear-gradient(90deg, #1E6F5C, #0B3C5D);
    padding: 2.4rem;
    border-radius: 22px;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 16px 36px rgba(0,0,0,0.18);
}

.hero h1 {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.6rem;
}

.hero p {
    font-size: 1.04rem;
    line-height: 1.7;
    max-width: 980px;
    margin-bottom: 0;
}

.card {
    background: rgba(255,255,255,0.95);
    border-radius: 20px;
    padding: 1.3rem;
    box-shadow: 0 10px 26px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}

.kpi-card {
    background: rgba(255,255,255,0.97);
    border-radius: 18px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    min-height: 130px;
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
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
}

.sub-label {
    color: #1E6F5C;
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
}

.small-note {
    color: #445;
    font-size: 0.94rem;
    line-height: 1.6;
}

.footer-note {
    background: #EEF5F3;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    color: #234;
    margin-top: 1rem;
}

.insight-box {
    background: linear-gradient(90deg, rgba(30,111,92,0.12), rgba(11,60,93,0.10));
    border-left: 5px solid #1E6F5C;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
    margin-bottom: 1.3rem;
    color: #223;
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

# Limit visible choices to 4 total files for cleaner UX
main_candidates = main_candidates[:4]
reference_candidates = reference_candidates[:4]

# =========================================================
# Hero
# =========================================================
st.markdown("""
<div class="hero">
    <div class="sub-label">Simulation & Design Analysis</div>
    <h1>Solar Simulation</h1>
    <p>
        This page helps SPICE compare solar design choices by showing how changes in
        system size, tilt, and azimuth affect projected energy output. Instead of
        presenting one static estimate, the dashboard supports scenario-based analysis
        for design discussion, investor communication, and project planning.
    </p>
</div>
""", unsafe_allow_html=True)

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

# =========================================================
# KPI row
# =========================================================
st.markdown("## Simulation Summary")

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Dataset</div>
        <div class="kpi-value" style="font-size:1.0rem;">{selected_main_file.name[:18]}</div>
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
# Insight box
# =========================================================
st.markdown(f"""
<div class="insight-box">
    <strong>Design Insight:</strong> With a selected system size of <strong>{system_size} kW</strong>,
    the chosen design at <strong>{tilt}° tilt</strong> and <strong>{azimuth}° azimuth</strong> produces
    <strong>{annual_selected_filtered:,.0f} kWh</strong> over the filtered period. Compared with the
    baseline design, the change is <strong>{pct_difference:+.1f}%</strong>. This helps SPICE explain
    whether a design adjustment creates meaningful value rather than only showing raw technical output.
</div>
""", unsafe_allow_html=True)

# =========================================================
# Production range
# =========================================================
st.markdown("## Production Range")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Low Scenario", f"{low_energy:,.0f} kWh")
c2.metric("Average Scenario", f"{avg_energy:,.0f} kWh")
c3.metric("High Scenario", f"{high_energy:,.0f} kWh")
c4.metric("Lowest Month", worst_month)

# =========================================================
# Monthly comparison
# =========================================================
st.markdown("## Monthly Design Comparison")

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

left, right = st.columns(2)

with left:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Seasonal Output</div>
        <div class="section-title">Selected vs Baseline Monthly Production</div>
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
            This view compares how the selected design performs throughout the year
            against a baseline configuration. It helps show whether the design decision
            improves output consistently or only in certain months.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Quarterly Summary</div>
        <div class="section-title">Quarterly Output Comparison</div>
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
            Quarterly comparison makes it easier to explain broader seasonal trends
            to non-technical users such as stakeholders and investors.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Annual comparison + distribution
# =========================================================
st.markdown("## Design Evaluation")

a1, a2 = st.columns(2)

with a1:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Annual Comparison</div>
        <div class="section-title">Selected vs Baseline Output</div>
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

    st.markdown(f"""
        <p class="small-note">
            The selected configuration changes output by
            <strong>{annual_difference:,.0f} kWh</strong> relative to baseline over the filtered period.
        </p>
    </div>
    """, unsafe_allow_html=True)

with a2:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Distribution</div>
        <div class="section-title">Output Distribution for Selected Design Space</div>
    """, unsafe_allow_html=True)

    if show_distribution and not filtered_selected.empty:
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
            This chart shows the spread of projected output values inside the selected
            design window, which helps indicate whether the design performs consistently.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Heatmap + top combinations
# =========================================================
st.markdown("## Tilt and Azimuth Performance Patterns")

h1, h2 = st.columns(2)

with h1:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Design Surface</div>
        <div class="section-title">Heatmap of Estimated Annual Output</div>
    """, unsafe_allow_html=True)

    surface_df = (
        df.groupby([tilt_col, azimuth_col], as_index=False)[target_col]
        .mean()
    )
    surface_df["annual_kwh_est"] = surface_df[target_col] / 1000 * system_size * 24 * 365

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
            The heatmap helps identify stronger-performing tilt and azimuth zones in the simulation data.
        </p>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Top Designs</div>
        <div class="section-title">Best Performing Tilt / Azimuth Combinations</div>
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
            This chart gives a fast benchmark of which design combinations tend to rank highest.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Reference dataset section
# =========================================================
st.markdown("## Scenario Comparison Reference")

if selected_reference_file is not None:
    reference_df = load_dataset(str(selected_reference_file))
    month_col, energy_col, site_col = guess_reference_columns(reference_df)

    st.markdown("""
    <div class="card">
        <div class="sub-label">Reference Dataset</div>
        <div class="section-title">External / Site-Level Scenario Reference</div>
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
# Raw preview
# =========================================================
st.markdown("## Filtered Data Preview")

preview_cols = [c for c in [datetime_col, tilt_col, azimuth_col, target_col, "month_name", "quarter"] if c in filtered_selected.columns]
st.dataframe(filtered_selected[preview_cols].head(20), use_container_width=True)

# =========================================================
# Footer
# =========================================================
st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Financial Impact page to convert projected
    production into revenue, savings, and business value for SPICE stakeholders.
</div>
""", unsafe_allow_html=True)
