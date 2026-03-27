import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Final Recommendation & Decision Support",
    layout="wide"
)

# -------------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #0b1220;
    color: white;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}
h1, h2, h3, h4 {
    color: white;
}
.metric-card {
    background: linear-gradient(135deg, rgba(163,230,53,0.12), rgba(250,204,21,0.10));
    border: 1px solid rgba(163,230,53,0.20);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.28);
    text-align: center;
    min-height: 135px;
}
.metric-title {
    font-size: 14px;
    color: #d1d5db;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
}
.metric-sub {
    font-size: 13px;
    color: #a3e635;
    margin-top: 8px;
}
.section-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 22px;
    margin-top: 10px;
    margin-bottom: 14px;
}
.highlight-box {
    background: linear-gradient(135deg, rgba(163,230,53,0.10), rgba(250,204,21,0.08));
    border: 1px solid rgba(163,230,53,0.20);
    border-left: 5px solid #a3e635;
    border-radius: 16px;
    padding: 22px;
}
.small-note {
    color: #d1d5db;
    font-size: 14px;
}
.badge-box {
    background: rgba(250,204,21,0.10);
    border: 1px solid rgba(250,204,21,0.20);
    color: #fde68a;
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 14px;
    margin-top: 8px;
}
div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------
def load_data():
    """
    Load dataset from:
    1. session_state["df"]
    2. session_state["uploaded_data"]
    3. uploaded_dataset.csv
    """
    if "df" in st.session_state and st.session_state["df"] is not None:
        return st.session_state["df"]

    if "uploaded_data" in st.session_state and st.session_state["uploaded_data"] is not None:
        return st.session_state["uploaded_data"]

    if "uploaded_file_path" in st.session_state:
        saved_path = st.session_state["uploaded_file_path"]
        if saved_path and os.path.exists(saved_path):
            try:
                return pd.read_csv(saved_path)
            except Exception:
                pass

    if os.path.exists("uploaded_dataset.csv"):
        try:
            return pd.read_csv("uploaded_dataset.csv")
        except Exception:
            pass

    return None


def find_column(df, possible_names):
    df_cols_lower = {col.lower(): col for col in df.columns}

    for name in possible_names:
        if name.lower() in df_cols_lower:
            return df_cols_lower[name.lower()]

    for col in df.columns:
        col_lower = col.lower()
        for name in possible_names:
            if name.lower() in col_lower:
                return col
    return None


def normalize_series(s):
    s = pd.to_numeric(s, errors="coerce").fillna(0)
    if len(s) == 0:
        return s
    if s.max() == s.min():
        return pd.Series([1.0] * len(s), index=s.index)
    return (s - s.min()) / (s.max() - s.min())


def safe_numeric(df, colname, default=0):
    if colname and colname in df.columns:
        return pd.to_numeric(df[colname], errors="coerce").fillna(default)
    return pd.Series([default] * len(df), index=df.index)


def pct_improvement(new, old):
    if old == 0:
        return 0
    return ((new - old) / old) * 100


# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.markdown("""
<div class="section-box">
    <h1 style="margin-bottom: 10px;">Final Recommendation & Decision Support</h1>
    <p class="small-note" style="font-size:18px;">
        Data-driven evaluation of solar design scenarios for SPICE, combining
        energy production, financial return, and environmental benefit into one final recommendation.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
df = load_data()

if df is None:
    st.error("No dataset found. Please upload your CSV file from the Home page first.")
    st.info("Go to the Home page, upload your dataset, then return to this page.")
    st.stop()

# Keep a clean copy
data = df.copy()

# -------------------------------------------------------
# COLUMN DETECTION
# -------------------------------------------------------
scenario_col = find_column(data, ["scenario", "scenario_name", "design", "design_name", "configuration", "case"])
tilt_col = find_column(data, ["tilt", "tilt_angle"])
azimuth_col = find_column(data, ["azimuth", "orientation"])
size_col = find_column(data, ["system_size", "size_kw", "capacity_kw", "installed_capacity", "kw"])
energy_col = find_column(data, ["energy", "annual_energy", "production", "energy_kwh", "annual_production", "kwh"])
revenue_col = find_column(data, ["revenue", "annual_revenue", "financial_return", "value_cad", "cad_revenue", "profit"])
co2_col = find_column(data, ["co2", "carbon", "co2_reduction", "carbon_reduction", "co2_saved", "emissions_avoided"])
baseline_flag_col = find_column(data, ["baseline", "is_baseline", "base_case"])

# -------------------------------------------------------
# CREATE FALLBACK SCENARIO NAME
# -------------------------------------------------------
if scenario_col is None:
    data["Scenario"] = [f"Scenario {i+1}" for i in range(len(data))]
    scenario_col = "Scenario"

# -------------------------------------------------------
# CREATE REQUIRED NUMERIC METRICS
# -------------------------------------------------------
data["Energy_Value"] = safe_numeric(data, energy_col, 0)
data["Revenue_Value"] = safe_numeric(data, revenue_col, 0)
data["CO2_Value"] = safe_numeric(data, co2_col, 0)

# fallback estimates if revenue or co2 columns missing
if data["Revenue_Value"].sum() == 0 and data["Energy_Value"].sum() > 0:
    data["Revenue_Value"] = data["Energy_Value"] * 0.12

if data["CO2_Value"].sum() == 0 and data["Energy_Value"].sum() > 0:
    data["CO2_Value"] = data["Energy_Value"] * 0.0005

# -------------------------------------------------------
# SIDEBAR SETTINGS
# -------------------------------------------------------
st.sidebar.header("Decision Settings")

energy_weight = st.sidebar.slider("Energy Weight", 0.0, 1.0, 0.40, 0.05)
revenue_weight = st.sidebar.slider("Revenue Weight", 0.0, 1.0, 0.30, 0.05)
co2_weight = st.sidebar.slider("CO₂ Weight", 0.0, 1.0, 0.30, 0.05)

weight_total = energy_weight + revenue_weight + co2_weight
if weight_total == 0:
    energy_weight, revenue_weight, co2_weight = 0.4, 0.3, 0.3
    weight_total = 1.0

energy_weight /= weight_total
revenue_weight /= weight_total
co2_weight /= weight_total

top_n = st.sidebar.selectbox("Top Scenarios to Compare", [3, 5, 7, 10], index=0)

# -------------------------------------------------------
# SCORING ENGINE
# -------------------------------------------------------
data["Energy_Norm"] = normalize_series(data["Energy_Value"])
data["Revenue_Norm"] = normalize_series(data["Revenue_Value"])
data["CO2_Norm"] = normalize_series(data["CO2_Value"])

data["Decision_Score"] = (
    energy_weight * data["Energy_Norm"] +
    revenue_weight * data["Revenue_Norm"] +
    co2_weight * data["CO2_Norm"]
)

data = data.sort_values("Decision_Score", ascending=False).reset_index(drop=True)

if data.empty:
    st.error("The dataset is empty after processing.")
    st.stop()

best_row = data.iloc[0]

# -------------------------------------------------------
# BASELINE IDENTIFICATION
# -------------------------------------------------------
baseline_row = None

if baseline_flag_col is not None:
    temp = data[data[baseline_flag_col].astype(str).str.lower().isin(["true", "1", "yes", "baseline"])]
    if not temp.empty:
        baseline_row = temp.iloc[0]

if baseline_row is None:
    baseline_candidates = data[data[scenario_col].astype(str).str.lower().str.contains("baseline|base", na=False)]
    if not baseline_candidates.empty:
        baseline_row = baseline_candidates.iloc[0]

if baseline_row is None:
    baseline_row = data.iloc[-1]

# -------------------------------------------------------
# IMPROVEMENTS
# -------------------------------------------------------
energy_improve = pct_improvement(best_row["Energy_Value"], baseline_row["Energy_Value"])
revenue_improve = pct_improvement(best_row["Revenue_Value"], baseline_row["Revenue_Value"])
co2_improve = pct_improvement(best_row["CO2_Value"], baseline_row["CO2_Value"])

# -------------------------------------------------------
# KPI CARDS
# -------------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Best Scenario</div>
        <div class="metric-value">{best_row[scenario_col]}</div>
        <div class="metric-sub">Top ranked design</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Annual Energy</div>
        <div class="metric-value">{best_row['Energy_Value']:,.0f}</div>
        <div class="metric-sub">kWh/year</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Annual Revenue</div>
        <div class="metric-value">${best_row['Revenue_Value']:,.0f}</div>
        <div class="metric-sub">Estimated annual value</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">CO₂ Reduction</div>
        <div class="metric-value">{best_row['CO2_Value']:,.2f}</div>
        <div class="metric-sub">tonnes/year</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Decision Score</div>
        <div class="metric-value">{best_row['Decision_Score']:.3f}</div>
        <div class="metric-sub">Weighted optimization</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------------
# DATA STATUS
# -------------------------------------------------------
st.markdown(f"""
<div class="badge-box">
<b>Dataset loaded successfully.</b> Rows: {len(data):,} | Columns: {len(data.columns):,}
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# BASELINE VS RECOMMENDED
# -------------------------------------------------------
st.subheader("Baseline vs Recommended Design")

comparison_df = pd.DataFrame({
    "Metric": ["Energy (kWh)", "Revenue ($)", "CO₂ Reduction (tonnes)"],
    "Baseline": [
        baseline_row["Energy_Value"],
        baseline_row["Revenue_Value"],
        baseline_row["CO2_Value"]
    ],
    "Recommended": [
        best_row["Energy_Value"],
        best_row["Revenue_Value"],
        best_row["CO2_Value"]
    ],
    "Improvement %": [
        energy_improve,
        revenue_improve,
        co2_improve
    ]
})

col_a, col_b = st.columns([1.05, 1.3])

with col_a:
    st.dataframe(
        comparison_df.style.format({
            "Baseline": "{:,.2f}",
            "Recommended": "{:,.2f}",
            "Improvement %": "{:+.2f}%"
        }),
        use_container_width=True
    )

with col_b:
    chart_df = comparison_df.melt(
        id_vars="Metric",
        value_vars=["Baseline", "Recommended"],
        var_name="Design Type",
        value_name="Value"
    )

    fig_compare = px.bar(
        chart_df,
        x="Metric",
        y="Value",
        color="Design Type",
        barmode="group",
        title="Baseline vs Recommended Performance"
    )
    fig_compare.update_layout(
        template="plotly_dark",
        xaxis_title="",
        yaxis_title="Value",
        legend_title=""
    )
    st.plotly_chart(fig_compare, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------
# TOP SCENARIO COMPARISON CHART
# -------------------------------------------------------
st.subheader(f"Top {top_n} Scenario Comparison")

top_df = data.head(top_n).copy()

metric_option = st.selectbox(
    "Choose metric to visualize",
    ["Energy (kWh)", "Revenue ($)", "CO₂ Reduction (tonnes)", "Decision Score"],
    index=0
)

metric_map = {
    "Energy (kWh)": "Energy_Value",
    "Revenue ($)": "Revenue_Value",
    "CO₂ Reduction (tonnes)": "CO2_Value",
    "Decision Score": "Decision_Score"
}

selected_metric_col = metric_map[metric_option]

fig_top = px.bar(
    top_df,
    x=scenario_col,
    y=selected_metric_col,
    color=selected_metric_col,
    title=f"{metric_option} Across Top {top_n} Scenarios",
    text_auto=".2s"
)
fig_top.update_layout(
    template="plotly_dark",
    xaxis_title="Scenario",
    yaxis_title=metric_option,
    coloraxis_showscale=False
)
st.plotly_chart(fig_top, use_container_width=True)

# -------------------------------------------------------
# SCORE CONTRIBUTION DONUT
# -------------------------------------------------------
col_d1, col_d2 = st.columns([1, 1.2])

with col_d1:
    score_weights_df = pd.DataFrame({
        "Metric": ["Energy", "Revenue", "CO₂"],
        "Weight": [energy_weight, revenue_weight, co2_weight]
    })

    fig_donut = px.pie(
        score_weights_df,
        values="Weight",
        names="Metric",
        hole=0.58,
        title="Decision Score Weight Distribution"
    )
    fig_donut.update_layout(template="plotly_dark")
    st.plotly_chart(fig_donut, use_container_width=True)

with col_d2:
    st.markdown("""
    <div class="section-box">
        <h4 style="margin-top:0;">How the scoring works</h4>
        <p class="small-note">
            This page ranks each scenario using a weighted decision score. Instead of focusing
            on only one output, the model combines:
        </p>
        <ul>
            <li><b>Energy production</b> to measure system performance</li>
            <li><b>Revenue</b> to reflect financial value</li>
            <li><b>CO₂ reduction</b> to show environmental impact</li>
        </ul>
        <p class="small-note">
            This gives a more balanced recommendation for SPICE and makes the final page more
            useful for stakeholder-level decision support.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------------
# SCENARIO RANKING TABLE
# -------------------------------------------------------
st.subheader("Scenario Ranking Table")

display_cols = [scenario_col, "Energy_Value", "Revenue_Value", "CO2_Value", "Decision_Score"]
rename_map = {
    scenario_col: "Scenario",
    "Energy_Value": "Energy (kWh)",
    "Revenue_Value": "Revenue ($)",
    "CO2_Value": "CO₂ Reduction (tonnes)",
    "Decision_Score": "Score"
}

if tilt_col:
    display_cols.insert(1, tilt_col)
    rename_map[tilt_col] = "Tilt"

if azimuth_col:
    azimuth_insert_pos = 2 if tilt_col else 1
    display_cols.insert(azimuth_insert_pos, azimuth_col)
    rename_map[azimuth_col] = "Azimuth"

if size_col:
    if tilt_col and azimuth_col:
        size_insert_pos = 3
    elif tilt_col or azimuth_col:
        size_insert_pos = 2
    else:
        size_insert_pos = 1
    display_cols.insert(size_insert_pos, size_col)
    rename_map[size_col] = "System Size"

ranking_df = data[display_cols].copy().rename(columns=rename_map)
ranking_df.index = np.arange(1, len(ranking_df) + 1)

st.dataframe(
    ranking_df.style.format({
        "Energy (kWh)": "{:,.0f}",
        "Revenue ($)": "${:,.0f}",
        "CO₂ Reduction (tonnes)": "{:,.2f}",
        "Score": "{:.3f}"
    }),
    use_container_width=True,
    height=380
)

st.markdown("---")

# -------------------------------------------------------
# RECOMMENDATION PANEL
# -------------------------------------------------------
st.subheader("Recommended Configuration")

tilt_value = best_row[tilt_col] if tilt_col else "N/A"
azimuth_value = best_row[azimuth_col] if azimuth_col else "N/A"
size_value = best_row[size_col] if size_col else "N/A"

st.markdown(f"""
<div class="highlight-box">
    <h3 style="margin-top:0;">Recommended Design: {best_row[scenario_col]}</h3>
    <p>
        Based on the weighted decision model, this scenario provides the strongest balance of
        <b>energy production</b>, <b>financial return</b>, and <b>environmental impact</b>.
    </p>
    <p>
        <b>Tilt:</b> {tilt_value} &nbsp;&nbsp; | &nbsp;&nbsp;
        <b>Azimuth:</b> {azimuth_value} &nbsp;&nbsp; | &nbsp;&nbsp;
        <b>System Size:</b> {size_value}
    </p>
    <p>
        <b>Expected Annual Energy:</b> {best_row['Energy_Value']:,.0f} kWh<br>
        <b>Expected Annual Revenue:</b> ${best_row['Revenue_Value']:,.0f}<br>
        <b>Expected CO₂ Reduction:</b> {best_row['CO2_Value']:,.2f} tonnes/year
    </p>
    <p>
        Compared with the baseline, this design improves energy by <b>{energy_improve:+.2f}%</b>,
        revenue by <b>{revenue_improve:+.2f}%</b>, and carbon benefit by <b>{co2_improve:+.2f}%</b>.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# BUSINESS INSIGHTS
# -------------------------------------------------------
st.subheader("Business Insights")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown("""
    <div class="section-box">
        <h4 style="margin-top:0;">Strategic Interpretation</h4>
        <ul>
            <li>Higher-performing scenarios support clearer investor communication through measurable output and value.</li>
            <li>Strong energy generation strengthens both financial return and environmental storytelling.</li>
            <li>A weighted scoring approach avoids over-relying on a single metric.</li>
            <li>This recommendation is more decision-ready than using charts alone.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with insight_col2:
    st.markdown("""
    <div class="section-box">
        <h4 style="margin-top:0;">Why This Matters for SPICE</h4>
        <ul>
            <li>Supports evidence-based solar planning instead of manual selection.</li>
            <li>Improves the ability to explain benefits to stakeholders using business and sustainability language.</li>
            <li>Creates a scalable framework for future sites and new solar scenarios.</li>
            <li>Connects technical design choices to revenue, carbon reduction, and investor confidence.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------------
# EXECUTIVE SUMMARY
# -------------------------------------------------------
st.subheader("Executive Summary")

summary_text = f"""
The final analysis identifies {best_row[scenario_col]} as the strongest overall solar design scenario
under the current decision framework.

Compared with the baseline scenario {baseline_row[scenario_col]}, the recommended design shows:
- {energy_improve:+.2f}% improvement in annual energy production
- {revenue_improve:+.2f}% improvement in annual revenue
- {co2_improve:+.2f}% improvement in carbon reduction impact

This final recommendation helps SPICE convert raw technical outputs into a clear business-ready decision.
"""

st.markdown(f"""
<div class="section-box">
    <p>
        The final analysis identifies <b>{best_row[scenario_col]}</b> as the strongest overall solar design scenario
        under the current decision framework. This configuration delivers the highest combined performance across
        energy generation, annual financial value, and carbon reduction.
    </p>
    <p>
        Relative to the baseline scenario <b>{baseline_row[scenario_col]}</b>, the recommended design shows:
    </p>
    <ul>
        <li><b>{energy_improve:+.2f}%</b> improvement in annual energy production</li>
        <li><b>{revenue_improve:+.2f}%</b> improvement in annual revenue</li>
        <li><b>{co2_improve:+.2f}%</b> improvement in carbon reduction impact</li>
    </ul>
    <p>
        This page gives SPICE a practical decision-support layer, turning raw model outputs into a clear,
        business-ready recommendation for future solar planning and stakeholder communication.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# DOWNLOAD SUMMARY
# -------------------------------------------------------
st.download_button(
    label="Download Executive Summary",
    data=summary_text,
    file_name="spice_final_recommendation_summary.txt",
    mime="text/plain"
)

# -------------------------------------------------------
# OPTIONAL PROCESSED DATA
# -------------------------------------------------------
with st.expander("Show processed scoring data"):
    preview_cols = [scenario_col, "Energy_Value", "Revenue_Value", "CO2_Value",
                    "Energy_Norm", "Revenue_Norm", "CO2_Norm", "Decision_Score"]
    st.dataframe(data[preview_cols], use_container_width=True)
