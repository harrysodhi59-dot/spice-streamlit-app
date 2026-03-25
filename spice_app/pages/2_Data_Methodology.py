import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Data & Methodology",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

/* Main layout */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Hero */
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
    color: white !important;
}

.hero p {
    font-size: 1.05rem;
    line-height: 1.7;
    max-width: 900px;
    color: #F4F8F7 !important;
}

/* Common card */
.card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 10px 26px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
    border: 1px solid rgba(0,0,0,0.06);
}

.card p,
.card li,
.card span,
.card div,
.card h3,
.card h4 {
    color: #1F2937 !important;
}

/* KPI cards */
.kpi-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.06);
}

.kpi-card div,
.kpi-card span,
.kpi-card p {
    color: #1F2937 !important;
}

.kpi-title {
    color: #0B3C5D !important;
    font-size: 0.95rem;
    font-weight: 700;
}

.kpi-value {
    color: #1E6F5C !important;
    font-size: 1.6rem;
    font-weight: 800;
    margin-top: 0.35rem;
}

/* Section headings inside HTML */
.section-title {
    color: #0B3C5D !important;
    font-size: 1.55rem;
    font-weight: 800;
    margin-top: 0.6rem;
    margin-bottom: 0.8rem;
}

.sub-label {
    color: #1E6F5C !important;
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
}

/* Feature boxes */
.feature-box {
    background: #F7F9F9;
    border-left: 6px solid #FDB813;
    padding: 1rem 1rem 1rem 1.1rem;
    border-radius: 12px;
    margin-bottom: 0.8rem;
    border: 1px solid rgba(0,0,0,0.05);
}

.feature-box h4 {
    color: #0B3C5D !important;
    margin-bottom: 0.4rem;
}

.feature-box p,
.feature-box div,
.feature-box span {
    margin-bottom: 0;
    color: #333333 !important;
    line-height: 1.6;
}

/* Footer note */
.footer-note {
    background: #EEF5F3;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    color: #1F2937 !important;
    margin-top: 1rem;
    border: 1px solid rgba(0,0,0,0.05);
}

.footer-note strong {
    color: #0B3C5D !important;
}

/* Streamlit headings */
h2, h3 {
    color: #F8FAFC !important;
    font-weight: 800 !important;
}

/* Dataframe wrapper area */
[data-testid="stDataFrame"] {
    background: transparent;
    border-radius: 14px;
    overflow: hidden;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(255,255,255,0.06);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="sub-label" style="color:#B8E0D2 !important;">Data Architecture</div>
    <h1>Data & Methodology</h1>
    <p>
        This dashboard combines solar simulation data, weather context, financial
        benchmarks, environmental indicators, and real-site production records to
        support practical decision-making for SPICE.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# OVERVIEW
# -----------------------------
left, right = st.columns([1.2, 1])

with left:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Methodological Approach</div>
        <div class="section-title">How the platform is structured</div>
        <p>
            The system is designed as a layered analytics platform. It starts with
            solar production logic, adds contextual data such as weather and pricing,
            and then translates technical outputs into business and environmental
            insights.
        </p>
        <p>
            This makes the platform more useful than a basic solar calculator because
            it connects design decisions to real-world value.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Why this matters</div>
        <div class="section-title">Decision support for SPICE</div>
        <p>
            SPICE needs a way to explain how solar system design choices influence
            energy generation, project savings, emissions reduction, and stakeholder
            confidence. This platform is built to support that communication.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# KPI ROW
# -----------------------------
st.markdown("## Data Snapshot")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Datasets</div>
        <div class="kpi-value">9</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Context Layers</div>
        <div class="kpi-value">Technical + Business</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Validation Inputs</div>
        <div class="kpi-value">Real SPICE Sites</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Team</div>
        <div class="kpi-value">Data Alchemists</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# DATASETS
# -----------------------------
st.markdown("## Datasets used in the platform")

datasets = pd.DataFrame({
    "Dataset": [
        "sample_250000.csv",
        "edmonton_weather_snow_2018_2025_clean.csv",
        "epcor_historical_rates.csv",
        "alberta_grid_emission_factors.csv",
        "federal_carbon_pricing.csv",
        "spice_actual_project_costs.csv",
        "bissell_daily_clean_long.csv",
        "visser_daily_clean_long_v2.csv",
        "St_Augustine_combined_simulated_monthly.csv"
    ],
    "Purpose": [
        "Core solar simulation and modeling dataset",
        "Weather and seasonal context for Edmonton",
        "Electricity pricing for savings analysis",
        "Grid emissions intensity for CO₂ impact",
        "Carbon pricing reference for policy value",
        "Project cost and financing benchmarks",
        "Observed production data for Bissell validation",
        "Observed production data for Visser validation",
        "Scenario-based monthly simulation comparison"
    ],
    "Role in Dashboard": [
        "Simulation and analytics foundation",
        "Weather and seasonality page",
        "Financial impact page",
        "Environmental impact page",
        "Environmental and carbon value page",
        "Financial impact and project comparison",
        "Real-site validation page",
        "Real-site validation page",
        "Scenario explorer page"
    ]
})

st.dataframe(datasets, use_container_width=True, hide_index=True)

# -----------------------------
# PIPELINE
# -----------------------------
st.markdown("## System pipeline")

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="feature-box">
        <h4>1. Simulation Layer</h4>
        <p>Solar generation logic is used to estimate system output based on design variables such as tilt, azimuth, and system size.</p>
    </div>

    <div class="feature-box">
        <h4>2. Data Context Layer</h4>
        <p>Weather, seasonality, pricing, emissions, and project cost data enrich the technical outputs with real-world context.</p>
    </div>

    <div class="feature-box">
        <h4>3. Impact Layer</h4>
        <p>Energy outputs are translated into savings, payback, avoided emissions, and carbon value.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-box">
        <h4>4. Validation Layer</h4>
        <p>Observed production data from real SPICE sites is used to compare and ground the project in operational reality.</p>
    </div>

    <div class="feature-box">
        <h4>5. Scenario Comparison Layer</h4>
        <p>Alternative design cases can be compared to support more informed planning and stakeholder discussions.</p>
    </div>

    <div class="feature-box">
        <h4>6. Dashboard Layer</h4>
        <p>All results are presented in an interactive format designed to support communication, exploration, and decision-making.</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# KEY IDEA
# -----------------------------
st.markdown("## Core idea behind the dashboard")

a, b = st.columns(2)

with a:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Beyond prediction</div>
        <div class="section-title">Not just energy output</div>
        <p>
            The goal is not only to estimate solar energy production. The dashboard
            is built to translate system design decisions into clear business and
            environmental outcomes that matter to SPICE and its stakeholders.
        </p>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Applied value</div>
        <div class="section-title">From data to action</div>
        <p>
            By combining simulation, context data, and interpretation, the platform
            supports a more complete understanding of solar projects and helps turn
            analysis into actionable insight.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Move to the Solar Simulation page to explore how
    design choices influence projected energy production.
</div>
""", unsafe_allow_html=True)
