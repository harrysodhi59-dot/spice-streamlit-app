import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Scalability & Business Impact", layout="wide")

# ---------------------------------------------------
# CUSTOM CSS - DARK MODE + GREEN/YELLOW THEME
# ---------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
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

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stMetric"] {
    background-color: #161b22;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 14px;
    border-radius: 16px;
}

.kpi-card {
    background: #161b22;
    border-radius: 18px;
    padding: 18px;
    border-left: 5px solid #facc15;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}

.insight-box {
    background: linear-gradient(135deg, rgba(34,197,94,0.16), rgba(250,204,21,0.12));
    border: 1px solid rgba(250,204,21,0.25);
    border-radius: 18px;
    padding: 20px;
    margin-top: 12px;
    color: white;
}

.section-card {
    background-color: #161b22;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 18px;
    margin-top: 10px;
}

.small-note {
    color: #cbd5e1 !important;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.markdown("<h1 style='color:#facc15;'>Scalability & Business Impact</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='small-note'>Explore how increasing system size improves production, savings, and CO₂ reduction for solar expansion planning.</p>",
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SIDEBAR INPUTS
# ---------------------------------------------------
st.sidebar.markdown("## Scalability Inputs")

selected_size = st.sidebar.slider("Selected System Size (kW)", 10, 200, 50, 10)
performance_ratio = st.sidebar.slider("Performance Ratio (%)", 70, 100, 85, 1)
electricity_rate = st.sidebar.number_input("Electricity Rate ($/kWh)", min_value=0.05, max_value=0.50, value=0.12, step=0.01)
co2_factor = st.sidebar.number_input("CO₂ Emission Factor (kg/kWh)", min_value=0.10, max_value=1.00, value=0.57, step=0.01)

irradiance_option = st.sidebar.selectbox(
    "Solar Irradiance Scenario",
    ["Low", "Medium", "High"],
    index=1
)

# ---------------------------------------------------
# IRRADIANCE MULTIPLIER
# ---------------------------------------------------
irradiance_map = {
    "Low": 0.90,
    "Medium": 1.00,
    "High": 1.10
}
irradiance_multiplier = irradiance_map[irradiance_option]

# ---------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------
sizes = np.arange(10, 201, 10)
base_production_per_kw = 1350  # kWh per kW per year

df_scale = pd.DataFrame({
    "System Size (kW)": sizes
})

df_scale["Annual Production (kWh)"] = (
    df_scale["System Size (kW)"] *
    base_production_per_kw *
    (performance_ratio / 100) *
    irradiance_multiplier
)

df_scale["Annual Savings ($)"] = df_scale["Annual Production (kWh)"] * electricity_rate
df_scale["CO2 Avoided (kg)"] = df_scale["Annual Production (kWh)"] * co2_factor
df_scale["CO2 Avoided (tonnes)"] = df_scale["CO2 Avoided (kg)"] / 1000

selected_row = df_scale[df_scale["System Size (kW)"] == selected_size].iloc[0]

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <h4 style="color:#facc15;">System Size</h4>
        <h2>{selected_row["System Size (kW)"]:.0f} kW</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <h4 style="color:#22c55e;">Annual Production</h4>
        <h2>{selected_row["Annual Production (kWh)"]:,.0f} kWh</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <h4 style="color:#facc15;">Annual Savings</h4>
        <h2>${selected_row["Annual Savings ($)"]:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <h4 style="color:#22c55e;">CO₂ Avoided</h4>
        <h2>{selected_row["CO2 Avoided (tonnes)"]:.2f} t</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------
# CHART 1 - CO2 AVOIDED VS SYSTEM SIZE
# ---------------------------------------------------
fig_co2 = px.line(
    df_scale,
    x="System Size (kW)",
    y="CO2 Avoided (tonnes)",
    markers=True,
    title="CO₂ Avoided vs System Size"
)

fig_co2.update_traces(
    line=dict(width=4, color="#22c55e"),
    marker=dict(size=8, color="#facc15")
)

highlight_df = df_scale[df_scale["System Size (kW)"] == selected_size]

fig_co2.add_trace(go.Scatter(
    x=highlight_df["System Size (kW)"],
    y=highlight_df["CO2 Avoided (tonnes)"],
    mode="markers+text",
    text=[f"{selected_size} kW"],
    textposition="top center",
    marker=dict(size=16, color="white", line=dict(color="#facc15", width=3)),
    name="Selected Size"
))

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

# ---------------------------------------------------
# CHART 2 + CHART 3
# ---------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    colors = ["#22c55e"] * len(df_scale)
    selected_index = df_scale.index[df_scale["System Size (kW)"] == selected_size][0]
    colors[selected_index] = "#facc15"

    fig_prod = px.bar(
        df_scale,
        x="System Size (kW)",
        y="Annual Production (kWh)",
        title="Annual Production vs System Size",
        text_auto=".0f"
    )

    fig_prod.update_traces(marker_color=colors)
    fig_prod.update_layout(
        paper_bgcolor="#0e1117",
        plot_bgcolor="#161b22",
        font=dict(color="white"),
        title_font=dict(size=20, color="#facc15"),
        xaxis=dict(
            title="System Size (kW)",
            showgrid=False
        ),
        yaxis=dict(
            title="Annual Production (kWh)",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)"
        ),
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
        marker=dict(size=8, color="#22c55e")
    )

    fig_save.add_trace(go.Scatter(
        x=highlight_df["System Size (kW)"],
        y=highlight_df["Annual Savings ($)"],
        mode="markers+text",
        text=[f"${highlight_df['Annual Savings ($)'].iloc[0]:,.0f}"],
        textposition="top center",
        marker=dict(size=16, color="white", line=dict(color="#22c55e", width=3)),
        name="Selected Size"
    ))

    fig_save.update_layout(
        paper_bgcolor="#0e1117",
        plot_bgcolor="#161b22",
        font=dict(color="white"),
        title_font=dict(size=20, color="#facc15"),
        xaxis=dict(
            title="System Size (kW)",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)"
        ),
        yaxis=dict(
            title="Annual Savings ($)",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)"
        ),
        height=450
    )

    st.plotly_chart(fig_save, use_container_width=True)

# ---------------------------------------------------
# EXTRA SCENARIO COMPARISON
# ---------------------------------------------------
st.markdown("### Scenario Comparison")

scenario_col1, scenario_col2, scenario_col3 = st.columns(3)

small_size = 50
medium_size = 100
large_size = 150

small_row = df_scale[df_scale["System Size (kW)"] == small_size].iloc[0]
medium_row = df_scale[df_scale["System Size (kW)"] == medium_size].iloc[0]
large_row = df_scale[df_scale["System Size (kW)"] == large_size].iloc[0]

with scenario_col1:
    st.markdown(f"""
    <div class="section-card">
        <h4 style="color:#facc15;">Small Scale - {small_size} kW</h4>
        <p><b>Production:</b> {small_row["Annual Production (kWh)"]:,.0f} kWh</p>
        <p><b>Savings:</b> ${small_row["Annual Savings ($)"]:,.0f}</p>
        <p><b>CO₂ Avoided:</b> {small_row["CO2 Avoided (tonnes)"]:.2f} t</p>
    </div>
    """, unsafe_allow_html=True)

with scenario_col2:
    st.markdown(f"""
    <div class="section-card">
        <h4 style="color:#22c55e;">Medium Scale - {medium_size} kW</h4>
        <p><b>Production:</b> {medium_row["Annual Production (kWh)"]:,.0f} kWh</p>
        <p><b>Savings:</b> ${medium_row["Annual Savings ($)"]:,.0f}</p>
        <p><b>CO₂ Avoided:</b> {medium_row["CO2 Avoided (tonnes)"]:.2f} t</p>
    </div>
    """, unsafe_allow_html=True)

with scenario_col3:
    st.markdown(f"""
    <div class="section-card">
        <h4 style="color:#facc15;">Large Scale - {large_size} kW</h4>
        <p><b>Production:</b> {large_row["Annual Production (kWh)"]:,.0f} kWh</p>
        <p><b>Savings:</b> ${large_row["Annual Savings ($)"]:,.0f}</p>
        <p><b>CO₂ Avoided:</b> {large_row["CO2 Avoided (tonnes)"]:.2f} t</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# INSIGHT SECTION
# ---------------------------------------------------
st.markdown("### Key Insight")

st.markdown(f"""
<div class="insight-box">
    <b>Selected Scenario: {selected_row["System Size (kW)"]:.0f} kW</b><br><br>
    Under the current assumptions of <b>{performance_ratio}% performance ratio</b>,
    <b>${electricity_rate:.2f}/kWh electricity rate</b>, and
    <b>{co2_factor:.2f} kg/kWh emission factor</b>, this system can generate
    <b>{selected_row["Annual Production (kWh)"]:,.0f} kWh/year</b>,
    save approximately <b>${selected_row["Annual Savings ($)"]:,.0f}</b> annually,
    and avoid around <b>{selected_row["CO2 Avoided (tonnes)"]:.2f} tonnes of CO₂ per year</b>.<br><br>
    The trend shows that when system size increases, production, savings, and environmental
    benefits also increase. This supports solar expansion as a scalable strategy for SPICE,
    helping stakeholders understand both the financial and sustainability value of growth.
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------
with st.expander("View Scalability Data Table"):
    st.dataframe(df_scale.style.format({
        "Annual Production (kWh)": "{:,.0f}",
        "Annual Savings ($)": "${:,.0f}",
        "CO2 Avoided (kg)": "{:,.0f}",
        "CO2 Avoided (tonnes)": "{:.2f}"
    }), use_container_width=True)
