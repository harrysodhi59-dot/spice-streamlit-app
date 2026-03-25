import streamlit as st

st.set_page_config(
    page_title="SPICE Solar Impact Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
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
    padding: 2.7rem;
    border-radius: 22px;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 14px 30px rgba(0,0,0,0.12);
}

.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.hero p {
    font-size: 1.08rem;
    line-height: 1.75;
    margin-bottom: 0;
    max-width: 900px;
}

.info-card {
    background: white;
    border-radius: 18px;
    padding: 1.4rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.kpi-card {
    background: white;
    border-radius: 18px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

.kpi-title {
    color: #0B3C5D;
    font-size: 0.95rem;
    font-weight: 600;
}

.kpi-value {
    color: #1E6F5C;
    font-size: 1.7rem;
    font-weight: 800;
    margin-top: 0.35rem;
}

.section-title {
    color: #0B3C5D;
    font-weight: 800;
    margin-top: 0.6rem;
    margin-bottom: 0.8rem;
}

.team-badge {
    display: inline-block;
    background-color: #FDB813;
    color: #1A1A1A;
    font-weight: 700;
    padding: 0.4rem 0.8rem;
    border-radius: 999px;
    margin-top: 0.8rem;
}

.sidebar-note {
    font-size: 0.95rem;
    color: #444444;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>SPICE Solar Impact Dashboard</h1>
    <p>
        A solar analytics and decision-support platform developed to help the
        Solar Power Investment Cooperative of Edmonton (SPICE) evaluate solar
        design choices, estimate project impact, and communicate technical,
        financial, and environmental value to stakeholders.
    </p>
    <div class="team-badge">Developed by Data Alchemists</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <h3 class="section-title">Welcome</h3>
    <p>
        This dashboard brings together simulation logic, weather context,
        financial analysis, environmental metrics, and real project data
        to support better solar planning and decision-making.
    </p>
    <p>
        Use the sidebar to explore the project pages, including methodology,
        solar simulation, financial impact, environmental analysis,
        weather and seasonality, site validation, and scenario comparison.
    </p>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Client</div>
        <div class="kpi-value">SPICE</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Team</div>
        <div class="kpi-value">Data Alchemists</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Datasets</div>
        <div class="kpi-value">9</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Focus</div>
        <div class="kpi-value">Energy · Finance · Impact</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <h3 class="section-title">Platform Scope</h3>
    <p>
        The dashboard is designed to translate solar system design decisions into
        clear and practical outcomes, including expected energy production,
        financial savings, carbon reduction, and project comparison insights.
    </p>
    <p>
        It supports communication with building owners, investors, and community
        stakeholders by connecting technical analysis to real-world value.
    </p>
</div>
""", unsafe_allow_html=True)

st.success("Open the sidebar to begin with the Home page.")
