import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Financial Impact",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# Image path
# -----------------------------
image_path = os.path.join(os.path.dirname(__file__), "finance.png")

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

/* Sections */
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

/* KPI cards */
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

/* Metric dark strips */
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
    font-size: 1.85rem;
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
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_rates():
    return pd.read_csv("data/epcor_historical_rates.csv")

@st.cache_data
def load_costs():
    return pd.read_csv("data/spice_actual_project_costs.csv")

try:
    rates_df = load_rates()
    cost_df = load_costs()
except Exception as e:
    st.error(f"Could not load financial datasets: {e}")
    st.stop()

rates_df.columns = [str(c).strip() for c in rates_df.columns]
cost_df.columns = [str(c).strip() for c in cost_df.columns]

if "Project_Name" not in cost_df.columns:
    st.error("Column 'Project_Name' is missing from spice_actual_project_costs.csv")
    st.stop()

# -----------------------------
# Sidebar (reduced)
# -----------------------------
st.sidebar.header("Finance View")
show_data_preview = st.sidebar.checkbox("Show financial data preview", value=False)
compare_top_n = st.sidebar.slider("Projects in cost comparison", 3, min(10, len(cost_df)), min(6, len(cost_df)))

# -----------------------------
# Hero
# -----------------------------
hero_left, hero_right = st.columns([1.35, 1], gap="large")

with hero_left:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-label">Economic Performance • Investment Logic • Stakeholder Value</div>
        <div class="hero-title">
            Financial <span class="hero-highlight">Impact</span>
        </div>
        <div class="hero-text">
            This page translates projected solar production into financial value using
            electricity rates and real SPICE project cost benchmarks.
        </div>
        <div class="hero-text">
            It helps explain how solar design and project assumptions affect savings,
            payback, investment attractiveness, and long-term business value.
        </div>
        <div class="hero-badge-wrap">
            <div class="hero-badge">Investor-Facing Metrics</div>
            <div class="hero-chip">Savings Analysis</div>
            <div class="hero-chip">Payback Logic</div>
            <div class="hero-chip">Project Benchmarking</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hero_right:
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
        st.markdown("""
        <div class="image-caption">
            Financial interpretation helps connect solar performance with business value and investment discussion.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("finance.png not found in the same folder as this page")

# -----------------------------
# Main controls on page
# -----------------------------
st.markdown('<div class="section-heading">Financial Scenario Controls</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">Adjust the project and planning assumptions below to see how the financial story changes.</div>',
    unsafe_allow_html=True
)

control1, control2, control3, control4 = st.columns(4, gap="large")

project_list = cost_df["Project_Name"].dropna().unique().tolist()
selected_project = control1.selectbox("🏢 Select SPICE Project", project_list)

annual_energy = control2.number_input(
    "⚡ Estimated Annual Energy (kWh)",
    min_value=1000.0,
    max_value=500000.0,
    value=22800.0,
    step=500.0
)

lifetime_years = control3.slider("📆 Project Lifetime (years)", 5, 30, 25)
annual_escalation = control4.slider("📈 Annual Savings Growth (%)", 0.0, 5.0, 2.0, 0.1)

# Optional comparison
compare_projects_default = project_list[:min(4, len(project_list))]
selected_compare_projects = st.multiselect(
    "📊 Compare against other SPICE projects",
    options=project_list,
    default=compare_projects_default
)

# -----------------------------
# Pull selected project values
# -----------------------------
project_row = cost_df[cost_df["Project_Name"] == selected_project].iloc[0]

system_size = project_row["System_Size_kW"] if "System_Size_kW" in project_row else 0
total_cost = project_row["Total_Cost_CAD"] if "Total_Cost_CAD" in project_row else 0
cost_per_watt = project_row["Cost_per_Watt_CAD"] if "Cost_per_Watt_CAD" in project_row else 0
lease_payment = project_row["Lease_Annual_Payment"] if "Lease_Annual_Payment" in project_row else 0
lease_years = project_row["Lease_Term_Years"] if "Lease_Term_Years" in project_row else 0
financing_type = project_row["Financing_Type"] if "Financing_Type" in project_row else "N/A"
spice_investment = project_row["SPICE_Investment_CAD"] if "SPICE_Investment_CAD" in project_row else 0

# -----------------------------
# Rate selection logic
# -----------------------------
latest_year = rates_df["Year"].max()
latest_rate_row = rates_df[rates_df["Year"] == latest_year].iloc[0]
rate_cents = latest_rate_row["Total_Delivered_cents_per_kWh"]
rate_dollars = rate_cents / 100

annual_savings = annual_energy * rate_dollars
payback_years = total_cost / annual_savings if annual_savings > 0 else 0
cap_rate = (annual_savings / total_cost * 100) if total_cost > 0 else 0

years = list(range(1, lifetime_years + 1))
yearly_savings = [annual_savings * ((1 + annual_escalation / 100) ** (y - 1)) for y in years]
cumulative_savings = pd.Series(yearly_savings).cumsum()
net_value = cumulative_savings.iloc[-1] - total_cost

# Investor return
if spice_investment > 0 and lease_years > 0 and lease_payment > 0:
    total_cash_flow = lease_payment * lease_years
    return_multiple = total_cash_flow / spice_investment
    annual_return = ((return_multiple ** (1 / lease_years)) - 1) * 100
else:
    total_cash_flow = 0
    return_multiple = 0
    annual_return = 0

# Financial insight
if annual_savings > total_cost / 10:
    strength_text = "a relatively strong annual savings position"
elif annual_savings > total_cost / 20:
    strength_text = "a moderate annual savings profile"
else:
    strength_text = "a slower financial recovery profile"

if payback_years <= 8:
    payback_text = "a comparatively attractive payback period"
elif payback_years <= 15:
    payback_text = "a moderate payback outlook"
else:
    payback_text = "a longer-term payback horizon"

insight_text = f"""
<strong>Financial Insight:</strong> Based on an estimated annual production of <strong>{annual_energy:,.0f} kWh</strong>
and a delivered electricity rate of <strong>${rate_dollars:.3f}/kWh</strong>, the selected project
(<strong>{selected_project}</strong>) generates estimated annual savings of <strong>${annual_savings:,.0f}</strong>.
This creates <strong>{strength_text}</strong> and suggests <strong>{payback_text}</strong> at approximately
<strong>{payback_years:.1f} years</strong>. Over a <strong>{lifetime_years}-year</strong> horizon with
<strong>{annual_escalation:.1f}%</strong> annual savings growth, cumulative savings reach
<strong>${cumulative_savings.iloc[-1]:,.0f}</strong>, producing an estimated net value of
<strong>${net_value:,.0f}</strong> after project cost recovery.
"""

# -----------------------------
# KPI row
# -----------------------------
st.markdown('<div class="section-heading">Financial Summary</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">A business-facing snapshot of the current project’s financial performance under the selected assumptions.</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5, gap="large")

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">⚡ Electricity Rate</div>
        <div class="kpi-value">${rate_dollars:.3f}/kWh</div>
        <div class="kpi-note">Latest delivered rate</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💵 Annual Savings</div>
        <div class="kpi-value">${annual_savings:,.0f}</div>
        <div class="kpi-note">Energy value per year</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">⏳ Payback Period</div>
        <div class="kpi-value">{payback_years:.1f} yrs</div>
        <div class="kpi-note">Cost recovery timing</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📊 Cap Rate</div>
        <div class="kpi-value">{cap_rate:.1f}%</div>
        <div class="kpi-note">Annual savings / cost</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🏦 Return Multiple</div>
        <div class="kpi-value">{return_multiple:.2f}x</div>
        <div class="kpi-note">SPICE investment view</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Dynamic insight
# -----------------------------
st.markdown(f"""
<div class="insight-box">
    {insight_text}
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Project overview cards
# -----------------------------
left, right = st.columns(2, gap="large")

with left:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">Project Benchmark</div>
        <div class="card-title">🏢 {selected_project}</div>
        <p><strong>System Size:</strong> {system_size} kW</p>
        <p><strong>Total Project Cost:</strong> ${total_cost:,.2f}</p>
        <p><strong>Cost per Watt:</strong> ${cost_per_watt:.2f}</p>
        <p><strong>Financing Type:</strong> {financing_type}</p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">Investment View</div>
        <div class="card-title">📌 SPICE Financing Snapshot</div>
        <p><strong>SPICE Investment:</strong> ${spice_investment:,.2f}</p>
        <p><strong>Annual Lease Payment:</strong> ${lease_payment:,.2f}</p>
        <p><strong>Lease Term:</strong> {lease_years} years</p>
        <p><strong>Estimated Annual Return:</strong> {annual_return:.2f}%</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Long-term indicators
# -----------------------------
st.markdown('<div class="section-heading">Long-Term Value Indicators</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3, gap="large")

with m1:
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">💼 Lifetime Savings</div>
        <div class="metric-value-dark">${cumulative_savings.iloc[-1]:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">📈 Net Value After Cost Recovery</div>
        <div class="metric-value-dark">${net_value:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">🏁 Estimated Annual Return</div>
        <div class="metric-value-dark">{annual_return:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Charts
# -----------------------------
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""
    <div class="card">
        <div class="card-label">Savings Over Time</div>
        <div class="card-title">📈 Projected Cumulative Savings</div>
    """, unsafe_allow_html=True)

    savings_df = pd.DataFrame({
        "Year": years,
        "Annual Savings": yearly_savings,
        "Cumulative Savings": cumulative_savings
    })

    fig_savings = px.line(
        savings_df,
        x="Year",
        y="Cumulative Savings",
        markers=True
    )
    fig_savings.update_layout(
        xaxis_title="Year",
        yaxis_title="Cumulative Savings (CAD)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        font=dict(family="Segoe UI")
    )
    st.plotly_chart(fig_savings, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            This chart shows how the selected project’s savings accumulate over time
            based on the current energy and escalation assumptions.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <div class="card-label">Scenario Comparison</div>
        <div class="card-title">🏗️ SPICE Project Cost Comparison</div>
    """, unsafe_allow_html=True)

    compare_df = cost_df.copy()
    if selected_compare_projects:
        compare_df = compare_df[compare_df["Project_Name"].isin(selected_compare_projects)].copy()

    compare_df = compare_df.sort_values("Total_Cost_CAD", ascending=False).head(compare_top_n)

    fig_cost = px.bar(
        compare_df,
        x="Project_Name",
        y="Total_Cost_CAD",
        text="Total_Cost_CAD"
    )
    fig_cost.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_cost.update_layout(
        xaxis_title="Project",
        yaxis_title="Total Cost (CAD)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        font=dict(family="Segoe UI")
    )
    st.plotly_chart(fig_cost, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            This comparison places the selected project in the context of other SPICE
            projects, helping explain scale, investment level, and cost positioning.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Rate trend + payback comparison
# -----------------------------
d1, d2 = st.columns(2, gap="large")

with d1:
    st.markdown("""
    <div class="card">
        <div class="card-label">Rate Context</div>
        <div class="card-title">⚡ Historical Electricity Rate Trend</div>
    """, unsafe_allow_html=True)

    if "Year" in rates_df.columns and "Total_Delivered_cents_per_kWh" in rates_df.columns:
        fig_rates = px.line(
            rates_df.sort_values("Year"),
            x="Year",
            y="Total_Delivered_cents_per_kWh",
            markers=True
        )
        fig_rates.update_layout(
            xaxis_title="Year",
            yaxis_title="Delivered Rate (cents/kWh)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="white",
            font=dict(family="Segoe UI")
        )
        st.plotly_chart(fig_rates, use_container_width=True)
    else:
        st.info("Rate trend columns not found.")

    st.markdown("""
        <p class="small-note">
            Historical rate movement provides context for why long-term solar savings
            can become more meaningful over time.
        </p>
    </div>
    """, unsafe_allow_html=True)

with d2:
    st.markdown("""
    <div class="card">
        <div class="card-label">Benchmarking</div>
        <div class="card-title">⏱️ Estimated Payback by Project</div>
    """, unsafe_allow_html=True)

    benchmark_df = cost_df.copy()
    if "Total_Cost_CAD" in benchmark_df.columns:
        benchmark_df["Estimated_Payback_Years"] = benchmark_df["Total_Cost_CAD"] / annual_savings
        benchmark_df = benchmark_df.replace([float("inf")], pd.NA).dropna(subset=["Estimated_Payback_Years"])
        benchmark_df = benchmark_df.sort_values("Estimated_Payback_Years").head(compare_top_n)

        fig_payback = px.bar(
            benchmark_df,
            x="Project_Name",
            y="Estimated_Payback_Years",
            text="Estimated_Payback_Years"
        )
        fig_payback.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_payback.update_layout(
            xaxis_title="Project",
            yaxis_title="Estimated Payback (years)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="white",
            font=dict(family="Segoe UI")
        )
        st.plotly_chart(fig_payback, use_container_width=True)
    else:
        st.info("Project cost column not available for payback comparison.")

    st.markdown("""
        <p class="small-note">
            This chart compares how quickly project costs may be recovered under the same
            annual savings assumption, making relative financial positioning easier to explain.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Optional data preview
# -----------------------------
if show_data_preview:
    st.markdown('<div class="section-heading">Financial Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(cost_df, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Environmental Impact page to connect
    projected solar output with emissions reduction, carbon value, and sustainability-focused stakeholder reporting.
</div>
""", unsafe_allow_html=True)
