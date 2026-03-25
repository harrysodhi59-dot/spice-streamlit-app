import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Environmental Impact",
    page_icon="🌍",
    layout="wide"
)

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

st.markdown("""
<div class="hero">
    <div class="sub-label">Sustainability & Policy Value</div>
    <h1>Environmental Impact</h1>
    <p>
        This page translates solar energy production into avoided emissions,
        carbon value, and broader environmental meaning. It helps connect
        project output to sustainability outcomes that matter to SPICE and
        community stakeholders.
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("Environmental Controls")

annual_energy = st.sidebar.number_input(
    "Estimated Annual Energy (kWh)",
    min_value=1000.0,
    max_value=500000.0,
    value=22800.0,
   
