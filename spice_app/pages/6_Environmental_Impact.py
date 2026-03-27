import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Environmental Impact",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# Image path
# -----------------------------
image_path = os.path.join(os.path.dirname(__file__), "environment.png")

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

.card,
.card p,
.card span,
.card div,
.card strong,
.card li,
.card h3,
.card h4 {
    color: #1F2937 !important;
}

.card-title {
    color: #0B3C5D !important;
    font-size: 1.3rem;
    font-weight: 850;
    margin-bottom: 0.45rem;
}

.card-label {
    color: #1E6F5C !important;
    font-size: 0.88rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.35rem;
}

.small-note {
    color: #334155 !important;
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

.insight-box strong {
    color: #8FF0B7 !important;
}

/* Dark strips */
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
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load datasets
# -----------------------------
@st.cache_data
def load_emissions():
    return pd.read_csv("data/alberta_grid_emission_factors.csv")

@st.cache_data
def load_carbon():
    return pd.read_csv("data/federal_carbon_pricing.csv")

try:
    emissions_df = load_emissions()
    carbon_df = load_carbon()
except Exception as e:
    st.error(f"Could not load environmental datasets: {e}")
    st.stop()

emissions_df.columns = [str(c).strip() for c in emissions_df.columns]
carbon_df.columns = [str(c).strip() for c in carbon_df.columns]

required_emissions_cols = ["Year", "Grid_Intensity_kg_CO2e_per_kWh"]
required_carbon_cols = ["Year", "Carbon_Tax_CAD_per_tonne"]

missing_emissions = [c for c in required_emissions_cols if c not in emissions_df.columns]
missing_carbon = [c for c in required_carbon_cols if c not in carbon_df.columns]

if missing_emissions:
    st.error(f"Missing columns in alberta_grid_emission_factors.csv: {missing_emissions}")
    st.write("Columns found:", list(emissions_df.columns))
    st.stop()

if missing_carbon:
    st.error(f"Missing columns in federal_carbon_pricing.csv: {missing_carbon}")
    st.write("Columns found:", list(carbon_df.columns))
    st.stop()

# -----------------------------
# Sidebar (reduced)
# -----------------------------
st.sidebar.header("Environmental View")
show_data_preview = st.sidebar.checkbox("Show environmental data preview", value=False)
show_equivalents = st.sidebar.checkbox("Show real-world equivalents", value=True)

# -----------------------------
# Hero
# -----------------------------
hero_left, hero_right = st.columns([1.35, 1], gap="large")

with hero_left:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-label">Sustainability • Carbon Value • Stakeholder Reporting</div>
        <div class="hero-title">
            Environmental <span class="hero-highlight">Impact</span>
        </div>
        <div class="hero-text">
            This page translates solar generation into avoided emissions, carbon value,
            and broader sustainability meaning for SPICE.
        </div>
        <div class="hero-text">
            It helps connect project performance with environmental outcomes that matter
            for community communication, reporting, and climate-focused decision-making.
        </div>
        <div class="hero-badge-wrap">
            <div class="hero-badge">Carbon Reduction</div>
            <div class="hero-chip">Policy Value</div>
            <div class="hero-chip">Community Impact</div>
            <div class="hero-chip">Sustainability Reporting</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hero_right:
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
        st.markdown("""
        <div class="image-caption">
            Environmental framing helps SPICE connect solar generation to sustainability value and community impact.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("environment.png not found in the same folder as this page")

# -----------------------------
# Main controls on page
# -----------------------------
st.markdown('<div class="section-heading">Environmental Scenario Controls</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">Adjust the energy and policy assumptions below to see how the environmental story changes.</div>',
    unsafe_allow_html=True
)

available_years = sorted(emissions_df["Year"].dropna().unique().tolist())
carbon_years = sorted(carbon_df["Year"].dropna().unique().tolist())

c1, c2, c3, c4 = st.columns(4, gap="large")

annual_energy = c1.number_input(
    "⚡ Estimated Annual Energy (kWh)",
    min_value=1000.0,
    max_value=500000.0,
    value=22800.0,
    step=500.0
)

selected_year = c2.selectbox(
    "🌫️ Select Emissions Year",
    available_years,
    index=len(available_years) - 1
)

default_carbon_index = carbon_years.index(selected_year) if selected_year in carbon_years else len(carbon_years) - 1
selected_carbon_year = c3.selectbox(
    "🏛️ Select Carbon Pricing Year",
    carbon_years,
    index=default_carbon_index
)

planning_horizon = c4.slider(
    "📆 Lifetime Horizon (years)",
    5, 30, 25
)

# -----------------------------
# Calculations
# -----------------------------
emissions_row = emissions_df[emissions_df["Year"] == selected_year].iloc[0]
carbon_row = carbon_df[carbon_df["Year"] == selected_carbon_year].iloc[0]

emission_factor = emissions_row["Grid_Intensity_kg_CO2e_per_kWh"]
carbon_price = carbon_row["Carbon_Tax_CAD_per_tonne"]

co2_kg = annual_energy * emission_factor
co2_tonnes = co2_kg / 1000
carbon_value = co2_tonnes * carbon_price

lifetime_co2 = co2_tonnes * planning_horizon
lifetime_carbon_value = carbon_value * planning_horizon

trees_equivalent = co2_tonnes * 40
cars_removed_equivalent = co2_tonnes / 4.6 if co2_tonnes > 0 else 0
homes_powered_equivalent = annual_energy / 10000

if co2_tonnes >= 20:
    impact_strength = "a strong annual emissions reduction profile"
elif co2_tonnes >= 8:
    impact_strength = "a meaningful annual emissions reduction outcome"
else:
    impact_strength = "a modest but positive annual emissions benefit"

if carbon_value >= 3000:
    value_strength = "a higher environmental policy value"
elif carbon_value >= 1000:
    value_strength = "a moderate environmental policy value"
else:
    value_strength = "an early-stage but still relevant environmental value"

insight_text = f"""
<strong>Environmental Insight:</strong> Based on an estimated annual solar generation of <strong>{annual_energy:,.0f} kWh</strong>
and the selected Alberta grid emissions factor of <strong>{emission_factor:.2f} kg CO₂e/kWh</strong> for <strong>{selected_year}</strong>,
the system avoids approximately <strong>{co2_tonnes:,.2f} tonnes of CO₂e per year</strong>. This creates
<strong>{impact_strength}</strong> and supports stronger sustainability communication for SPICE. Using the selected
carbon pricing value of <strong>${carbon_price:,.0f}/tonne</strong> for <strong>{selected_carbon_year}</strong>,
the avoided emissions correspond to an estimated annual carbon value of <strong>${carbon_value:,.0f}</strong>,
which represents <strong>{value_strength}</strong>. Over a <strong>{planning_horizon}-year</strong> horizon,
the cumulative environmental benefit reaches <strong>{lifetime_co2:,.2f} tonnes of CO₂e avoided</strong>.
"""

# -----------------------------
# KPI row
# -----------------------------
st.markdown('<div class="section-heading">Environmental Summary</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">A stakeholder-facing snapshot of the environmental benefit created under the selected energy and policy assumptions.</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5, gap="large")

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🌫️ Grid Emissions Factor</div>
        <div class="kpi-value">{emission_factor:.2f} kg/kWh</div>
        <div class="kpi-note">Selected emissions year</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">♻️ Avoided Emissions</div>
        <div class="kpi-value">{co2_tonnes:,.2f} t</div>
        <div class="kpi-note">Annual avoided CO₂e</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🏛️ Carbon Price</div>
        <div class="kpi-value">${carbon_price:,.0f}/t</div>
        <div class="kpi-note">Selected policy year</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💚 Carbon Value</div>
        <div class="kpi-value">${carbon_value:,.0f}</div>
        <div class="kpi-note">Annual policy value</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📆 Lifetime Avoided CO₂e</div>
        <div class="kpi-value">{lifetime_co2:,.1f} t</div>
        <div class="kpi-note">{planning_horizon}-year horizon</div>
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
# Interpretation cards
# -----------------------------
left, right = st.columns(2, gap="large")

with left:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">Impact Interpretation</div>
        <div class="card-title">🌱 What the emissions estimate means</div>
        <p>
            Based on the selected annual solar output of <strong>{annual_energy:,.0f} kWh</strong>,
            the system avoids approximately <strong>{co2_tonnes:,.2f} tonnes of CO₂e</strong>
            using the Alberta grid emissions factor for <strong>{selected_year}</strong>.
        </p>
        <p>
            This is a practical sustainability metric that can support project communication,
            climate-focused reporting, and stakeholder engagement across SPICE initiatives.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">Policy Interpretation</div>
        <div class="card-title">📘 What the carbon value means</div>
        <p>
            Using the selected carbon price for <strong>{selected_carbon_year}</strong>,
            the avoided emissions correspond to an estimated annual carbon value of
            <strong>${carbon_value:,.0f}</strong>.
        </p>
        <p>
            This value may not always be direct cash flow, but it expresses the policy
            significance and reporting value of avoided emissions created through solar generation.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Long-term value indicators
# -----------------------------
st.markdown('<div class="section-heading">Long-Term Sustainability Indicators</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3, gap="large")

with m1:
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">🌍 Lifetime Avoided Emissions</div>
        <div class="metric-value-dark">{lifetime_co2:,.2f} t</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">💰 Lifetime Carbon Value</div>
        <div class="metric-value-dark">${lifetime_carbon_value:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">🏠 Homes Powered Reference</div>
        <div class="metric-value-dark">{homes_powered_equivalent:,.1f}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Optional equivalents
# -----------------------------
if show_equivalents:
    st.markdown('<div class="section-heading">Real-World Equivalents</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtext">These reference values help communicate the environmental meaning of solar generation in a more relatable way.</div>',
        unsafe_allow_html=True
    )

    e1, e2, e3 = st.columns(3, gap="large")

    with e1:
        st.markdown(f"""
        <div class="card">
            <div class="card-label">🌳 Trees Equivalent</div>
            <div class="card-title">{trees_equivalent:,.0f} Trees</div>
            <p class="small-note">
                Approximate annual carbon benefit expressed as an equivalent number of trees.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with e2:
        st.markdown(f"""
        <div class="card">
            <div class="card-label">🚗 Cars Removed</div>
            <div class="card-title">{cars_removed_equivalent:,.1f} Cars</div>
            <p class="small-note">
                Roughly comparable to removing this many cars from the road for one year.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with e3:
        st.markdown(f"""
        <div class="card">
            <div class="card-label">🏡 Homes Reference</div>
            <div class="card-title">{homes_powered_equivalent:,.1f} Homes</div>
            <p class="small-note">
                A simple electricity-demand reference to help contextualize annual energy production.
            </p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Charts
# -----------------------------
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""
    <div class="card">
        <div class="card-label">Emissions Context</div>
        <div class="card-title">📉 Alberta Grid Emissions Intensity by Year</div>
    """, unsafe_allow_html=True)

    fig_emissions = px.line(
        emissions_df.sort_values("Year"),
        x="Year",
        y="Grid_Intensity_kg_CO2e_per_kWh",
        markers=True
    )
    fig_emissions.update_layout(
        xaxis_title="Year",
        yaxis_title="Grid Intensity (kg CO₂e per kWh)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        font=dict(family="Segoe UI")
    )
    st.plotly_chart(fig_emissions, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            Lower grid intensity means a cleaner electricity system, which affects how much carbon benefit
            can be attributed to solar generation in each year.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <div class="card-label">Policy Context</div>
        <div class="card-title">📊 Federal Carbon Price by Year</div>
    """, unsafe_allow_html=True)

    fig_carbon = px.bar(
        carbon_df.sort_values("Year"),
        x="Year",
        y="Carbon_Tax_CAD_per_tonne"
    )
    fig_carbon.update_layout(
        xaxis_title="Year",
        yaxis_title="Carbon Price (CAD per tonne)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        font=dict(family="Segoe UI")
    )
    st.plotly_chart(fig_carbon, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            Rising carbon prices strengthen the policy-based value of avoided emissions and help explain
            why clean generation becomes more significant over time.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Clean impact snapshot
# -----------------------------
st.markdown('<div class="section-heading">Impact Snapshot</div>', unsafe_allow_html=True)

snapshot_left, snapshot_right = st.columns(2, gap="large")

emissions_snapshot_df = pd.DataFrame({
    "Metric": ["Avoided Emissions", "Lifetime Avoided Emissions"],
    "Value": [co2_tonnes, lifetime_co2]
})

carbon_snapshot_df = pd.DataFrame({
    "Metric": ["Annual Carbon Value", "Lifetime Carbon Value"],
    "Value": [carbon_value, lifetime_carbon_value]
})

with snapshot_left:
    st.markdown("""
    <div class="card">
        <div class="card-label">Selected Case</div>
        <div class="card-title">🌱 Emissions Benefit Overview</div>
    """, unsafe_allow_html=True)

    fig_emissions_snapshot = px.bar(
        emissions_snapshot_df,
        x="Metric",
        y="Value",
        color="Metric",
        text="Value"
    )

    fig_emissions_snapshot.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_emissions_snapshot.update_layout(
        xaxis_title="Metric",
        yaxis_title="Avoided Emissions (tonnes CO₂e)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        showlegend=False,
        font=dict(family="Segoe UI"),
        margin=dict(t=25, b=20, l=20, r=20)
    )

    st.plotly_chart(fig_emissions_snapshot, use_container_width=True)

    st.markdown(f"""
        <p class="small-note">
            This chart focuses only on the physical environmental benefit in <strong>tonnes of CO₂e</strong>.
            The selected case avoids <strong>{co2_tonnes:,.2f} tonnes</strong> annually and
            <strong>{lifetime_co2:,.2f} tonnes</strong> over the selected project horizon.
        </p>
    </div>
    """, unsafe_allow_html=True)

with snapshot_right:
    st.markdown("""
    <div class="card">
        <div class="card-label">Selected Case</div>
        <div class="card-title">💰 Carbon Value Overview</div>
    """, unsafe_allow_html=True)

    fig_carbon_snapshot = px.bar(
        carbon_snapshot_df,
        x="Metric",
        y="Value",
        color="Metric",
        text="Value"
    )

    fig_carbon_snapshot.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )

    fig_carbon_snapshot.update_layout(
        xaxis_title="Metric",
        yaxis_title="Carbon Value (CAD)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        showlegend=False,
        font=dict(family="Segoe UI"),
        margin=dict(t=25, b=20, l=20, r=20)
    )

    st.plotly_chart(fig_carbon_snapshot, use_container_width=True)

    st.markdown(f"""
        <p class="small-note">
            This chart focuses only on the policy-based environmental value in <strong>CAD</strong>.
            The selected case creates an annual carbon value of <strong>${carbon_value:,.0f}</strong>
            and a lifetime carbon value of <strong>${lifetime_carbon_value:,.0f}</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Optional data preview
# -----------------------------
if show_data_preview:
    st.markdown('<div class="section-heading">Environmental Data Preview</div>', unsafe_allow_html=True)
    preview_choice = st.radio(
        "Choose dataset preview",
        ["Grid Emission Factors", "Carbon Pricing"],
        horizontal=True
    )

    if preview_choice == "Grid Emission Factors":
        st.dataframe(emissions_df, use_container_width=True)
    else:
        st.dataframe(carbon_df, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Weather & Seasonality page to explore
    how Edmonton weather conditions shape solar performance over time.
</div>
""", unsafe_allow_html=True)
