import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Financial Impact",
    page_icon="💰",
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

# -----------------------------
# Hero
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="sub-label">Economic Performance</div>
    <h1>Financial Impact</h1>
    <p>
        This page translates solar production into financial value using electricity
        rates and real SPICE project cost benchmarks. It helps show how solar design
        decisions can affect savings, payback, and long-term project performance.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Financial Controls")

project_list = cost_df["Project_Name"].dropna().unique().tolist() if "Project_Name" in cost_df.columns else []
selected_project = st.sidebar.selectbox("Select SPICE Project", project_list)

annual_energy = st.sidebar.number_input(
    "Estimated Annual Energy (kWh)",
    min_value=1000.0,
    max_value=500000.0,
    value=22800.0,
    step=500.0
)

lifetime_years = st.sidebar.slider("Project Lifetime (years)", 5, 30, 25)
annual_escalation = st.sidebar.slider("Annual Savings Growth (%)", 0.0, 5.0, 2.0, 0.1)

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
# Latest electricity rate
# -----------------------------
latest_year = rates_df["Year"].max()
latest_rate_row = rates_df[rates_df["Year"] == latest_year].iloc[0]
rate_cents = latest_rate_row["Total_Delivered_cents_per_kWh"]
rate_dollars = rate_cents / 100

annual_savings = annual_energy * rate_dollars
payback_years = total_cost / annual_savings if annual_savings > 0 else 0
cap_rate = (annual_savings / total_cost * 100) if total_cost > 0 else 0

# lifetime savings with escalation
years = list(range(1, lifetime_years + 1))
yearly_savings = [annual_savings * ((1 + annual_escalation / 100) ** (y - 1)) for y in years]
cumulative_savings = pd.Series(yearly_savings).cumsum()
net_value = cumulative_savings.iloc[-1] - total_cost

# investor return
if spice_investment > 0 and lease_years > 0 and lease_payment > 0:
    total_cash_flow = lease_payment * lease_years
    return_multiple = total_cash_flow / spice_investment
    annual_return = ((return_multiple ** (1 / lease_years)) - 1) * 100
else:
    total_cash_flow = 0
    return_multiple = 0
    annual_return = 0

# -----------------------------
# KPI row
# -----------------------------
st.markdown("## Financial Summary")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Electricity Rate</div>
        <div class="kpi-value">${rate_dollars:.3f}/kWh</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Annual Savings</div>
        <div class="kpi-value">${annual_savings:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Payback Period</div>
        <div class="kpi-value">{payback_years:.1f} yrs</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Cap Rate</div>
        <div class="kpi-value">{cap_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Project overview cards
# -----------------------------
left, right = st.columns(2)

with left:
    st.markdown(f"""
    <div class="card">
        <div class="sub-label">Project Benchmark</div>
        <div class="section-title">{selected_project}</div>
        <p><strong>System Size:</strong> {system_size} kW</p>
        <p><strong>Total Project Cost:</strong> ${total_cost:,.2f}</p>
        <p><strong>Cost per Watt:</strong> ${cost_per_watt:.2f}</p>
        <p><strong>Financing Type:</strong> {financing_type}</p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="card">
        <div class="sub-label">Investment View</div>
        <div class="section-title">SPICE Financing Snapshot</div>
        <p><strong>SPICE Investment:</strong> ${spice_investment:,.2f}</p>
        <p><strong>Annual Lease Payment:</strong> ${lease_payment:,.2f}</p>
        <p><strong>Lease Term:</strong> {lease_years} years</p>
        <p><strong>Estimated Annual Return:</strong> {annual_return:.2f}%</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Charts
# -----------------------------
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Savings Over Time</div>
        <div class="section-title">Projected Cumulative Savings</div>
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
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_savings, use_container_width=True)

    st.markdown("""
        <p>
            This chart shows how energy savings accumulate over the project lifetime.
            It provides a simple view of long-term value creation under the selected assumptions.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Project Comparison</div>
        <div class="section-title">SPICE Project Cost Comparison</div>
    """, unsafe_allow_html=True)

    compare_df = cost_df[["Project_Name", "Total_Cost_CAD"]].copy()
    fig_cost = px.bar(
        compare_df,
        x="Project_Name",
        y="Total_Cost_CAD"
    )
    fig_cost.update_layout(
        xaxis_title="Project",
        yaxis_title="Total Cost (CAD)",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_cost, use_container_width=True)

    st.markdown("""
        <p>
            This comparison places the selected project in the context of other SPICE
            project costs, helping frame scale and financial structure.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Additional metrics
# -----------------------------
st.markdown("## Long-term value indicators")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Lifetime Savings", f"${cumulative_savings.iloc[-1]:,.0f}")

with m2:
    st.metric("Net Value After Cost Recovery", f"${net_value:,.0f}")

with m3:
    st.metric("Investor Return Multiple", f"{return_multiple:.2f}x")

# -----------------------------
# Data preview
# -----------------------------
st.markdown("## Financial data preview")
st.dataframe(cost_df, use_container_width=True)

st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Environmental Impact page to connect
    energy output with emissions reduction and carbon value.
</div>
""", unsafe_allow_html=True)
