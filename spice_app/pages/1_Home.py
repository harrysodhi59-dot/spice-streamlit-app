import streamlit as st
import os

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

# Image path
image_path = os.path.join(os.path.dirname(__file__), "solar_image.png")

# ==============================
# CSS (FULL CLEAN)
# ==============================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

/* Background */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(30,111,92,0.18), transparent 30%),
        linear-gradient(180deg, #040816, #081423);
    color: #F8FAFC;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141B2D, #182133);
}

/* HERO */
.hero-box {
    background: linear-gradient(135deg, #1E6F5C, #0B3C5D);
    padding: 2.8rem;
    border-radius: 28px;
    color: white;
    box-shadow: 0 20px 40px rgba(0,0,0,0.35);
}

.hero-label {
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #D6EFE6;
}

.hero-title {
    font-size: 3rem;
    font-weight: 900;
    line-height: 1.1;
}

.hero-highlight {
    color: #FDB813;
}

.hero-text {
    margin-top: 1rem;
    font-size: 1rem;
    line-height: 1.7;
}

/* BADGES */
.hero-badge-wrap {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 1.2rem;
}

.hero-badge {
    background: #FDB813;
    color: black;
    padding: 8px 14px;
    border-radius: 999px;
    font-weight: 800;
}

.hero-chip {
    background: rgba(255,255,255,0.1);
    padding: 7px 12px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.2);
}

/* CARDS */
.card {
    background: #F8FAFC;
    color: black;
    padding: 1.8rem;
    border-radius: 22px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.sub-label {
    font-size: 0.8rem;
    color: #1E6F5C;
    font-weight: 800;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 900;
    margin: 10px 0;
}

/* KPI */
.kpi-card {
    background: #111827;
    padding: 1.3rem;
    border-radius: 18px;
    text-align: center;
}

.kpi-title {
    color: #94A3B8;
}

.kpi-value {
    font-size: 1.4rem;
    font-weight: 900;
}

.kpi-note {
    color: #FDB813;
    font-size: 0.85rem;
}

/* FEATURE BOX */
.feature-box {
    background: #111827;
    padding: 1rem;
    border-radius: 15px;
    border-left: 4px solid #FDB813;
    margin-bottom: 10px;
}

/* ROADMAP */
.roadmap-card {
    background: #111827;
    padding: 1rem;
    border-radius: 15px;
}

.roadmap-step {
    color: #FDB813;
    font-size: 0.8rem;
}

.footer-note {
    background: rgba(30,111,92,0.2);
    padding: 1rem;
    border-radius: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
left, right = st.columns([1.5, 1])

with left:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-label">SPICE · Solar Power Investment Cooperative of Edmonton</div>

        <div class="hero-title">
            Turning Solar Design Choices Into
            <span class="hero-highlight">Actionable Impact</span>
        </div>

        <div class="hero-text">
            The SPICE dashboard translates solar system configurations into
            financial, environmental, and operational insight.
        </div>

        <div class="hero-text">
            It connects simulation with real decision-making — helping stakeholders
            understand value, not just data.
        </div>

        <div class="hero-badge-wrap">
            <div class="hero-badge">Built by Data Alchemists</div>
            <div class="hero-chip">Energy Analytics</div>
            <div class="hero-chip">Financial Insight</div>
            <div class="hero-chip">Sustainability Value</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning("Add solar_image.png in same folder")

# ==============================
# PROBLEM SECTION
# ==============================
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Client Need</div>
        <div class="section-title">What problem this solves</div>
        SPICE needs a clear way to explain how solar design decisions impact real outcomes.
        This dashboard turns complex solar data into simple, decision-ready insights.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Platform Goal</div>
        <div class="section-title">Why this matters</div>
        It helps stakeholders understand solar value, compare options,
        and make better investment decisions.
    </div>
    """, unsafe_allow_html=True)

# ==============================
# KPI SECTION
# ==============================
st.markdown("### Dashboard Snapshot")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown('<div class="kpi-card"><div class="kpi-title">Client</div><div class="kpi-value">SPICE</div><div class="kpi-note">Community solar</div></div>', unsafe_allow_html=True)

with k2:
    st.markdown('<div class="kpi-card"><div class="kpi-title">Team</div><div class="kpi-value">Data Alchemists</div></div>', unsafe_allow_html=True)

with k3:
    st.markdown('<div class="kpi-card"><div class="kpi-title">Scope</div><div class="kpi-value">Energy + Finance</div></div>', unsafe_allow_html=True)

with k4:
    st.markdown('<div class="kpi-card"><div class="kpi-title">Focus</div><div class="kpi-value">Decision Support</div></div>', unsafe_allow_html=True)

# ==============================
# FEATURES
# ==============================
st.markdown("### What this dashboard does")

f1, f2 = st.columns(2)

with f1:
    st.markdown("""
    <div class="feature-box">
    <b>Solar Simulation</b><br>
    Compare tilt, size, and orientation.
    </div>

    <div class="feature-box">
    <b>Financial Impact</b><br>
    Convert output into revenue insights.
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-box">
    <b>Environmental Impact</b><br>
    CO₂ reduction and sustainability value.
    </div>

    <div class="feature-box">
    <b>Real Site Validation</b><br>
    Compare with real-world data.
    </div>
    """, unsafe_allow_html=True)

# ==============================
# ROADMAP
# ==============================
st.markdown("### Explore the Dashboard")

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown('<div class="roadmap-card"><div class="roadmap-step">01</div>Data Methodology</div>', unsafe_allow_html=True)

with r2:
    st.markdown('<div class="roadmap-card"><div class="roadmap-step">02</div>Simulation</div>', unsafe_allow_html=True)

with r3:
    st.markdown('<div class="roadmap-card"><div class="roadmap-step">03</div>Impact</div>', unsafe_allow_html=True)

with r4:
    st.markdown('<div class="roadmap-card"><div class="roadmap-step">04</div>Modeling</div>', unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.markdown("""
<div class="footer-note">
Use sidebar to explore full dashboard
</div>
""", unsafe_allow_html=True)
