import streamlit as st
import os

st.set_page_config(
    page_title="SPICE Solar Impact Dashboard",
    page_icon="☀️",
    layout="wide"
)

# =========================================================
# IMAGE PATH
# =========================================================
image_path = "solar_image.png"   # keep image in same folder as this file

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
/* -----------------------------
   Global Styling
----------------------------- */
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(24, 83, 62, 0.28) 0%, transparent 30%),
        radial-gradient(circle at top right, rgba(215, 169, 40, 0.14) 0%, transparent 25%),
        linear-gradient(180deg, #05110d 0%, #081914 45%, #0b221a 100%);
    color: #f5f7f6;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    padding-left: 2.4rem;
    padding-right: 2.4rem;
    max-width: 1450px;
}

/* -----------------------------
   Sidebar
----------------------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141926 0%, #1a2130 100%);
    border-right: 1px solid rgba(255,255,255,0.05);
}

section[data-testid="stSidebar"] * {
    color: #f4f4f4 !important;
}

/* -----------------------------
   Hero
----------------------------- */
.hero-box {
    background:
        linear-gradient(135deg, rgba(7, 30, 22, 0.96) 0%, rgba(17, 74, 56, 0.92) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 30px;
    padding: 2.6rem 2.4rem;
    box-shadow: 0 18px 45px rgba(0,0,0,0.28);
    min-height: 360px;
}

.hero-label {
    display: inline-block;
    background: rgba(255,255,255,0.08);
    color: #eef6f1;
    border: 1px solid rgba(255,255,255,0.12);
    padding: 0.45rem 0.95rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 3rem;
    font-weight: 900;
    line-height: 1.08;
    color: #f8fafc;
    margin-bottom: 1rem;
}

.hero-highlight {
    color: #e2b63b;
}

.hero-text {
    color: #dbe8e0;
    font-size: 1.05rem;
    line-height: 1.85;
    margin-bottom: 1rem;
}

.hero-badge-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.7rem;
    margin-top: 1.2rem;
}

.hero-badge, .hero-chip {
    background: rgba(255,255,255,0.09);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.12);
    padding: 0.5rem 0.9rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
}

.image-caption {
    color: #b8c7bf;
    font-size: 0.9rem;
    text-align: center;
    margin-top: 0.5rem;
}

/* -----------------------------
   Section Headings
----------------------------- */
.section-heading {
    font-size: 2.15rem;
    font-weight: 900;
    color: #f8fafc;
    margin-top: 0.4rem;
    margin-bottom: 0.35rem;
}

.section-subtext {
    color: #b8c7bf;
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 1.3rem;
}

/* -----------------------------
   Cards
----------------------------- */
.card {
    background: linear-gradient(180deg, rgba(10, 32, 25, 0.96) 0%, rgba(6, 24, 19, 0.96) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 1.4rem 1.35rem;
    box-shadow: 0 12px 28px rgba(0,0,0,0.22);
    min-height: 100%;
}

.sub-label {
    display: inline-block;
    background: rgba(226, 182, 59, 0.14);
    color: #f0c34c;
    padding: 0.36rem 0.82rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 800;
    margin-bottom: 0.9rem;
}

.card-title {
    color: #f8fafc;
    font-size: 1.2rem;
    font-weight: 850;
    margin-bottom: 0.7rem;
}

.card p {
    color: #d1ddd6;
    font-size: 0.98rem;
    line-height: 1.8;
    margin-bottom: 0.8rem;
}

/* -----------------------------
   Dashboard Experience
----------------------------- */
.roadmap-card {
    background: linear-gradient(180deg, rgba(11, 35, 27, 0.96) 0%, rgba(7, 26, 20, 0.96) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 1.4rem 1.3rem;
    min-height: 260px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.22);
}

.roadmap-step {
    display: inline-block;
    background: rgba(226, 182, 59, 0.14);
    color: #f0c34c;
    padding: 0.38rem 0.8rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 800;
    margin-bottom: 1rem;
}

.roadmap-title {
    color: #f8fafc;
    font-size: 1.05rem;
    font-weight: 850;
    margin-bottom: 0.8rem;
}

.roadmap-text {
    color: #cfd9d4;
    font-size: 0.97rem;
    line-height: 1.8;
}

/* -----------------------------
   Insight Strip
----------------------------- */
.insight-strip {
    background: linear-gradient(90deg, rgba(19, 72, 55, 0.95) 0%, rgba(12, 46, 36, 0.95) 100%);
    border-left: 6px solid #e2b63b;
    border-radius: 18px;
    padding: 1.1rem 1.3rem;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
    color: #eef5f1;
    line-height: 1.8;
    box-shadow: 0 10px 22px rgba(0,0,0,0.18);
}

/* -----------------------------
   KPI Cards
----------------------------- */
.kpi-card {
    background: linear-gradient(135deg, rgba(9, 36, 28, 0.97) 0%, rgba(14, 58, 44, 0.94) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 26px;
    padding: 1.35rem 1.2rem;
    min-height: 170px;
    box-shadow: 0 14px 32px rgba(0,0,0,0.24);
}

.kpi-label {
    color: #d8e2dc;
    font-size: 1rem;
    font-weight: 800;
    margin-bottom: 1rem;
}

.kpi-value {
    color: #f8fafc;
    font-size: 2.1rem;
    font-weight: 950;
    margin-bottom: 0.7rem;
    line-height: 1.1;
}

.kpi-delta {
    color: #f0c34c;
    font-size: 0.95rem;
    font-weight: 700;
    line-height: 1.6;
}

/* -----------------------------
   Feature Boxes
----------------------------- */
.feature-box {
    background: linear-gradient(180deg, rgba(11, 31, 24, 0.96) 0%, rgba(8, 23, 18, 0.96) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 22px;
    padding: 1.2rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 10px 24px rgba(0,0,0,0.18);
}

.feature-box h4 {
    color: #f8fafc;
    font-size: 1.05rem;
    font-weight: 850;
    margin-bottom: 0.55rem;
}

.feature-box p {
    color: #cdd8d2;
    font-size: 0.95rem;
    line-height: 1.75;
    margin-bottom: 0;
}

/* -----------------------------
   Footer
----------------------------- */
.footer-note {
    text-align: center;
    color: #91a69d;
    font-size: 0.92rem;
    margin-top: 1.6rem;
    padding-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO SECTION
# =========================================================
left_hero, right_hero = st.columns([1.45, 1], gap="large")

with left_hero:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-label">SPICE · Solar Power Investment Cooperative of Edmonton</div>
        <div class="hero-title">
            Turning Solar Design Choices Into
            <span class="hero-highlight">Actionable Impact</span>
        </div>
        <div class="hero-text">
            The SPICE Solar Impact Dashboard helps translate solar design decisions into
            meaningful technical, financial, and environmental insight. Instead of stopping
            at raw output numbers, it supports stronger planning and clearer stakeholder communication.
        </div>
        <div class="hero-text">
            It brings together solar simulation, business interpretation, environmental value,
            site-based validation, and scenario comparison in one unified decision-support platform.
        </div>
        <div class="hero-badge-wrap">
            <div class="hero-badge">Built by Data Alchemists</div>
            <div class="hero-chip">Energy Analytics</div>
            <div class="hero-chip">Financial Insight</div>
            <div class="hero-chip">Sustainability Value</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right_hero:
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
        st.markdown("""
        <div class="image-caption">
            Real-world solar installation context aligned with SPICE stakeholder communication.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("solar_image.png not found in the same folder as Home.py")

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# DASHBOARD EXPERIENCE
# =========================================================
st.markdown('<div class="section-heading">Dashboard Experience</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">The dashboard is structured to move from project context into simulation, validation, business impact, and modeling insight.</div>',
    unsafe_allow_html=True
)

r1, r2, r3, r4 = st.columns(4, gap="large")

with r1:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">01 · Context</div>
        <div class="roadmap-title">Home & Data Methodology</div>
        <div class="roadmap-text">
            Introduce the problem, data foundation, and analytical structure behind the dashboard.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">02 · Design</div>
        <div class="roadmap-title">Solar Simulation</div>
        <div class="roadmap-text">
            Compare tilt, azimuth, and system size scenarios to explore how design changes affect output.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">03 · Impact</div>
        <div class="roadmap-title">Financial & Environmental Impact</div>
        <div class="roadmap-text">
            Connect projected solar generation to revenue, payback logic, and carbon reduction outcomes.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r4:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">04 · Trust</div>
        <div class="roadmap-title">Validation & Modeling</div>
        <div class="roadmap-text">
            Present real-site validation, forecasting logic, and future explainability layers for transparency.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# STRATEGIC STRIP
# =========================================================
st.markdown("""
<div class="insight-strip">
    <strong>Strategic Lens:</strong>
    This dashboard is not just a technical interface. It is designed as a decision-support
    experience that helps SPICE compare solar configurations, communicate trade-offs,
    and connect solar performance to investment and impact.
</div>
""", unsafe_allow_html=True)

# =========================================================
# KPI ROW
# =========================================================
st.markdown('<div class="section-heading">Dashboard Snapshot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">A quick executive view of the dashboard scope, project identity, and stakeholder-facing value.</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4, gap="large")

with k1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">Estimated Energy Output</div>
        <div class="kpi-value">5.24 MWh</div>
        <div class="kpi-delta">Operational performance insight</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">Projected Revenue</div>
        <div class="kpi-value">$18.5K</div>
        <div class="kpi-delta">Investor-facing financial value</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">CO₂ Reduction</div>
        <div class="kpi-value">2,150 kg</div>
        <div class="kpi-delta">Measured sustainability outcome</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">Payback Outlook</div>
        <div class="kpi-value">6.5 yrs</div>
        <div class="kpi-delta">Investment decision support</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# VALUE BLOCKS
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="section-heading">What this dashboard enables</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">The platform is built to support both analysis and communication across the most important SPICE use cases.</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>Solar Simulation</h4>
        <p>Explore how tilt, azimuth, system size, and design choices affect projected production outcomes.</p>
    </div>

    <div class="feature-box">
        <h4>Financial Analysis</h4>
        <p>Translate production into savings, payback logic, and stakeholder-facing economic value.</p>
    </div>

    <div class="feature-box">
        <h4>Environmental Impact</h4>
        <p>Estimate avoided emissions and sustainability outcomes for community-oriented solar projects.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>Weather & Seasonality Context</h4>
        <p>Show how Edmonton climate conditions influence solar performance and expected production behavior.</p>
    </div>

    <div class="feature-box">
        <h4>Real-Site Validation</h4>
        <p>Compare logic against actual production patterns from sites such as Bissell and Visser.</p>
    </div>

    <div class="feature-box">
        <h4>Scenario Comparison</h4>
        <p>Support better decision-making by comparing multiple design alternatives across simulated cases.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    '<div class="footer-note">SPICE Solar Analytics Dashboard | Premium dark-theme home experience</div>',
    unsafe_allow_html=True
)
