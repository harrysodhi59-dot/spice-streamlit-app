import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Scalability & Environmental Impact", layout="wide")

# ---------------------------
# DARK MODE + GREEN/YELLOW CSS
# ---------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3, h4, h5, h6, p, div, span, label {
    color: white !important;
}
[data-testid="stMetric"] {
    background-color: #161b22;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 14px;
}
.insight-box {
    background: linear-gradient(135deg, rgba(34,197,94,0.18), rgba(234,179,8,0.15));
    border: 1px solid rgba(250,204,21,0.25);
    padding: 18px;
    border-radius: 16px;
    color: white;
    margin-top: 10px;
}
.kpi-card {
    background-color: #161b22;
    padding: 18px;
    border-radius: 16px;
    border-left: 5px solid #facc15;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.25);
}
.small-note {
    color: #cbd5e1 !important;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# TITLE
# ---------------------------
st.markdown("<h1 style='color:#facc15;'>Scalability & Environmental Impact</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='small-note'>This page shows how increasing solar system size improves annual energy production, financial savings, and CO₂ avoided.</p>",
    unsafe_allow_html=True
)

# ---------------------------
# SAMPLE / GENERATED DATA
# ---------------------------
# You can replace this later with your actual dataset logic
system_sizes = np.array([10, 20, 30, 40, 50, 75, 100, 125, 150, 175, 200])  # kW

# Assume annual production per kW with slight efficiency variation
production_per_kw = np.array([1320, 1330, 1340, 1345, 1350, 1355, 1360, 1362, 1365, 1368, 1370])

annual_production = system_sizes * production_per_kw  # kWh/year
electricity_rate = 0.12  # $ per kWh
co2_factor = 0.57  # kg CO2 avoided per kWh

annual_savings = annual_production * electricity_rate
co2_avoided_kg = annual_production * co2_factor
co2_avoided_tonnes = co2_avoided_kg / 1000

df_scale = pd.DataFrame({
    "System Size (kW)": system_sizes,
    "Annual Production (kWh)": annual_production,
    "Annual Savings ($)": annual_savings,
    "CO2 Avoided (kg)": co2_avoided_kg,
    "CO2 Avoided (tonnes)": co2_avoided_tonnes
})

# ---------------------------
# SIDEBAR / FILTERS
# ---------------------------
st.sidebar.markdown("## Page 8 Filters")
selected_size = st.sidebar.selectbox(
    "Select System Size (kW)",
    df_scale["System Size (kW)"].tolist(),
    index=4
)

selected_row = df_scale[df_scale["System Size (kW)"] == selected_size].iloc[0]

# ---------------------------
# KPI CARDS
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <h4 style="color:#facc15;">System Size</h4>
        <h2>{selected_row['System Size (kW)']:.0f} kW</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <h4 style="color:#22c55e;">Annual Production</h4>
        <h2>{selected_row['Annual Production (kWh)']:,.0f} kWh</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <h4 style="color:#facc15;">Annual Savings</h4>
        <h2>${selected_row['Annual Savings ($)']:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <h4 style="color:#22c55e;">CO₂ Avoided</h4>
        <h2>{selected_row['CO2 Avoided (tonnes)']:.1f} t</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------
# CHART 1: CO2 vs System Size
# ---------------------------
fig_co2 = px.line(
    df_scale,
    x="System Size (kW)",
    y="CO2 Avoided (tonnes)",
    markers=True,
    title="CO₂ Avoided vs System Size"
)

fig_co2.update_traces(
    line=dict(width=4, color="#22c55e"),
    marker=dict(size=10, color="#facc15")
)

fig_co2.update_layout(
    paper_bgcolor="#0e1117",
    plot_bgcolor="#161b22",
    font=dict(color="white"),
    title_font=dict(size=22, color="#facc15"),
    xaxis=dict(
        title="System Size (kW)",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)"
    ),
    yaxis=dict(
        title="CO₂ Avoided (tonnes/year)",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)"
    ),
    height=500
)

st.plotly_chart(fig_co2, use_container_width=True)

# ---------------------------
# CHART 2 + CHART 3
# ---------------------------
col5, col6 = st.columns(2)

with col5:
    fig_prod = px.bar(
        df_scale,
        x="System Size (kW)",
        y="Annual Production (kWh)",
        title="Annual Production vs System Size",
        text_auto=".0f"
    )
    fig_prod.update_traces(marker_color="#22c55e")
    fig_prod.update_layout(
        paper_bgcolor="#0e1117",
        plot_bgcolor="#161b22",
        font=dict(color="white"),
        title_font=dict(size=20, color="#facc15"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
        height=450
    )
    st.plotly_chart(fig_prod, use_container_width=True)

with col6:
    fig_save = px.line(
        df_scale,
        x="System Size (kW)",
        y="Annual Savings ($)",
        markers=True,
        title="Annual Savings vs System Size"
    )
    fig_save.update_traces(
        line=dict(width=4, color="#facc15"),
        marker=dict(size=9, color="#22c55e")
    )
    fig_save.update_layout(
        paper_bgcolor="#0e1117",
        plot_bgcolor="#161b22",
        font=dict(color="white"),
        title_font=dict(size=20, color="#facc15"),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
        height=450
    )
    st.plotly_chart(fig_save, use_container_width=True)

# ---------------------------
# INSIGHTS SECTION
# ---------------------------
st.markdown("### Key Business Insight")

st.markdown(f"""
<div class="insight-box">
    <b>Selected Scenario: {selected_row['System Size (kW)']:.0f} kW</b><br><br>
    This system is estimated to generate <b>{selected_row['Annual Production (kWh)']:,.0f} kWh/year</b>,
    produce approximately <b>${selected_row['Annual Savings ($)']:,.0f}</b> in annual electricity savings,
    and avoid around <b>{selected_row['CO2 Avoided (tonnes)']:.1f} tonnes of CO₂ per year</b>.<br><br>
    The trend across all scenarios shows that as system size increases, production, savings, and environmental
    benefits also rise. This supports the idea that scaling solar installations can strengthen both financial
    returns and sustainability impact for SPICE.
</div>
""", unsafe_allow_html=True)

# ---------------------------
# OPTIONAL DATA TABLE
# ---------------------------
with st.expander("View Scalability Data Table"):
    st.dataframe(df_scale, use_container_width=True)
