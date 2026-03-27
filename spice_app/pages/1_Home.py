import pandas as pd
import os
import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

# Image path (image should be in the same folder as this Home.py file)
image_path = os.path.join(os.path.dirname(__file__), "solar_image.png")

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

/* Main page spacing */
.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2.4rem;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 100%;
}

/* App background */
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

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
    font-weight: 800 !important;
}

.section-heading {
    font-size: 2rem;
    font-weight: 850;
    color: #F8FAFC !important;
    margin-top: 0.4rem;
    margin-bottom: 0.6rem;
}

.section-subtext {
    color: #B6C0CE !important;
    font-size: 1rem;
    line-height: 1.75;
    margin-bottom: 1.3rem;
}

/* HERO */
.hero-box {
    background: linear-gradient(135deg, rgba(30,111,92,0.96) 0%, rgba(11,60,93,0.96) 100%);
    padding: 3rem;
    border-radius: 28px;
    color: white;
    box-shadow: 0 20px 46px rgba(0,0,0,0.34);
    min-height: 460px;
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
    font-size: 3.45rem;
    font-weight: 900;
    line-height: 1.08;
    margin-bottom: 1.1rem;
    color: #FFFFFF !important;
    position: relative;
    z-index: 2;
}

.hero-highlight {
    color: #FDB813 !important;
}

.hero-text {
    font-size: 1.08rem;
    line-height: 1.9;
    color: #F3F7F6 !important;
    margin-bottom: 0.8rem;
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

/* IMAGE */
[data-testid="stImage"] img {
    border-radius: 26px;
    box-shadow: 0 20px 46px rgba(0,0,0,0.34);
    border: 1px solid rgba(255,255,255,0.08);
    width: 100%;
    object-fit: cover;
}

/* LIGHT CARDS */
.card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 24px;
    padding: 1.75rem;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    margin-bottom: 1rem;
    border: 1px solid rgba(0,0,0,0.06);
    min-height: 270px;
}

.card p, .card li, .card span, .card div {
    color: #1F2937 !important;
}

.sub-label {
    color: #1E6F5C !important;
    font-size: 0.88rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.45rem;
}

.section-title {
    color: #0B3C5D !important;
    font-size: 1.7rem;
    font-weight: 850;
    margin-top: 0.25rem;
    margin-bottom: 0.8rem;
    line-height: 1.25;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(180deg, #111827 0%, #172033 100%);
    border-radius: 22px;
    padding: 1.35rem;
    text-align: center;
    box-shadow: 0 12px 26px rgba(0,0,0,0.24);
    border: 1px solid rgba(255,255,255,0.06);
    min-height: 145px;
}

.kpi-title {
    color: #94A3B8 !important;
    font-size: 0.94rem;
    font-weight: 700;
    margin-bottom: 0.45rem;
}

.kpi-value {
    color: #F8FAFC !important;
    font-size: 1.65rem;
    font-weight: 850;
    line-height: 1.25;
}

.kpi-note {
    color: #FDB813 !important;
    font-size: 0.88rem;
    font-weight: 700;
    margin-top: 0.45rem;
}

/* DARK FEATURE BOXES */
.feature-box {
    background: linear-gradient(180deg, #111827 0%, #172033 100%);
    border-left: 6px solid #FDB813;
    padding: 1.15rem 1.15rem 1.15rem 1.2rem;
    border-radius: 18px;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.20);
}

.feature-box h4 {
    color: #F8FAFC !important;
    margin-bottom: 0.45rem;
    font-size: 1.08rem;
    font-weight: 800;
}

.feature-box p {
    margin-bottom: 0;
    color: #CBD5E1 !important;
    line-height: 1.68;
    font-size: 0.97rem;
}

/* STRATEGIC STRIP */
.insight-strip {
    background: linear-gradient(90deg, rgba(30,111,92,0.22), rgba(11,60,93,0.22));
    border-left: 6px solid #FDB813;
    border-radius: 20px;
    padding: 1.05rem 1.2rem;
    margin-top: 0.4rem;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
}

.insight-strip strong {
    color: #FFFFFF !important;
}

.insight-strip span {
    color: #DCE7E2 !important;
    line-height: 1.7;
}

/* ROADMAP */
.roadmap-card {
    background: linear-gradient(180deg, #111827 0%, #172033 100%);
    border-radius: 20px;
    padding: 1.3rem;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.20);
    min-height: 210px;
}

.roadmap-step {
    display: inline-block;
    background: rgba(253,184,19,0.16);
    color: #FDB813 !important;
    font-size: 0.80rem;
    font-weight: 800;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    margin-bottom: 0.7rem;
}

.roadmap-title {
    color: #F8FAFC !important;
    font-size: 1.06rem;
    font-weight: 800;
    margin-bottom: 0.55rem;
}

.roadmap-text {
    color: #CBD5E1 !important;
    font-size: 0.96rem;
    line-height: 1.68;
}

/* Footer note */
.footer-note {
    background: linear-gradient(90deg, rgba(30,111,92,0.18), rgba(11,60,93,0.22));
    border-radius: 18px;
    padding: 1rem 1.2rem;
    color: #E5E7EB !important;
    margin-top: 1rem;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
}

/* Responsive */
@media (max-width: 900px) {
    .hero-title {
        font-size: 2.35rem;
    }
    .hero-box {
        min-height: auto;
        padding: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO SECTION
# -----------------------------
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

# -----------------------------
# PROBLEM + PURPOSE
# -----------------------------
left, right = st.columns([1.15, 1], gap="large")

with left:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Client Need</div>
        <div class="section-title">What problem this dashboard solves</div>
        <p>
            SPICE needs a practical way to explain how solar design decisions affect
            real project outcomes. Stakeholders need more than technical outputs — they need
            a clear view of how configuration choices influence energy generation, economic value,
            and environmental benefit.
        </p>
        <p>
            This dashboard bridges that gap by turning solar system parameters into
            visual, decision-ready insight that supports both project understanding and stakeholder trust.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Platform Goal</div>
        <div class="section-title">Why this matters for SPICE</div>
        <p>
            This platform supports project planning, communication, and confidence-building
            by combining simulation, analytics, and business interpretation in one place.
        </p>
        <p>
            It is designed to strengthen conversations with building owners, investors,
            and community stakeholders who need both technical credibility and business clarity.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# STRATEGIC STRIP
# -----------------------------
st.markdown("""
<div class="insight-strip">
    <strong>Strategic Lens:</strong>
    <span>
        This dashboard is not just a technical interface. It is designed as a decision-support
        experience that helps SPICE compare solar configurations, communicate trade-offs,
        and connect solar performance to investment and impact.
    </span>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# KPI ROW
# -----------------------------
st.markdown('<div class="section-heading">Dashboard Snapshot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">A quick executive view of the dashboard scope, project identity, and stakeholder-facing value.</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4, gap="large")

with c1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Client</div>
        <div class="kpi-value">SPICE</div>
        <div class="kpi-note">Community solar focus</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Team</div>
        <div class="kpi-value">Data Alchemists</div>
        <div class="kpi-note">Applied analytics collaboration</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Dashboard Scope</div>
        <div class="kpi-value">Energy · Finance · Environment</div>
        <div class="kpi-note">Business + technical interpretation</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Decision Focus</div>
        <div class="kpi-value">Simulation + Validation</div>
        <div class="kpi-note">Scenario-based exploration</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# VALUE BLOCKS
# -----------------------------
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

# -----------------------------
# DASHBOARD FLOW
# -----------------------------
st.markdown('<div class="section-heading">Explore the platform</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">The dashboard is structured to move from problem framing into simulation, impact evaluation, site validation, and predictive analysis.</div>',
    unsafe_allow_html=True
)

r1, r2, r3, r4 = st.columns(4, gap="large")

with r1:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">01</div>
        <div class="roadmap-title">Data Methodology</div>
        <div class="roadmap-text">
            Understand the datasets, assumptions, and analytical logic behind the dashboard.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">02</div>
        <div class="roadmap-title">Solar Simulation</div>
        <div class="roadmap-text">
            Compare design variables and evaluate how they influence projected solar performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">03</div>
        <div class="roadmap-title">Impact Pages</div>
        <div class="roadmap-text">
            Connect technical outcomes to financial value and environmental benefit for SPICE stakeholders.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r4:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">04</div>
        <div class="roadmap-title">Validation & Modeling</div>
        <div class="roadmap-text">
            Review real-site comparison and predictive analysis structure for future decision support.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# STAKEHOLDER SECTION
# -----------------------------
st.markdown('<div class="section-heading">Who this supports</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">The dashboard is designed for both technical interpretation and stakeholder-facing communication.</div>',
    unsafe_allow_html=True
)

a, b, c = st.columns(3, gap="large")

with a:
    st.markdown("""
    <div class="card" style="min-height: 220px;">
        <div class="sub-label">Building Owners</div>
        <p>
            Helps property stakeholders understand how solar systems may affect energy savings,
            feasibility, and overall project value.
        </p>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="card" style="min-height: 220px;">
        <div class="sub-label">Investors</div>
        <p>
            Supports financial interpretation by linking output projections to economic value,
            scenario comparison, and return-oriented discussion.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown("""
    <div class="card" style="min-height: 220px;">
        <div class="sub-label">Community Stakeholders</div>
        <p>
            Communicates the environmental and social value of community-driven solar projects
            in a format that is accessible and visually clear.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# FOOTER NOTE
# -----------------------------
st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Use the sidebar to explore methodology, simulation,
    financial impact, environmental impact, validation, and predictive analysis pages.
</div>
""", unsafe_allow_html=True)
