import streamlit as st
import os

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)
image_path = "spice_app/pages/solar_image.png"

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

/* Main page spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 100%;
}

/* App background */
.stApp {
    background: linear-gradient(180deg, #050816 0%, #08111f 100%);
    color: #F8FAFC;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #161B2D;
    border-right: 1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] .css-1d391kg,
section[data-testid="stSidebar"] .css-163ttbj,
section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

/* Streamlit headings */
h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
    font-weight: 800 !important;
}

/* Section heading outside cards */
.section-heading {
    font-size: 1.8rem;
    font-weight: 800;
    color: #F8FAFC !important;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}

/* Hero left box */
.hero-box {
    background: linear-gradient(135deg, #1E6F5C 0%, #0B3C5D 100%);
    padding: 2.7rem;
    border-radius: 26px;
    color: white;
    box-shadow: 0 18px 40px rgba(0,0,0,0.30);
    min-height: 420px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.hero-label {
    color: #B8E0D2 !important;
    font-size: 0.92rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 0.8rem;
}

.hero-title {
    font-size: 3.15rem;
    font-weight: 800;
    line-height: 1.12;
    margin-bottom: 1rem;
    color: #FFFFFF !important;
}

.hero-highlight {
    color: #FDB813 !important;
}

.hero-text {
    font-size: 1.08rem;
    line-height: 1.8;
    color: #F3F7F6 !important;
    margin-bottom: 0.8rem;
}

.hero-badge {
    display: inline-block;
    background: #FDB813;
    color: #111827 !important;
    font-weight: 800;
    padding: 0.55rem 1rem;
    border-radius: 999px;
    margin-top: 0.8rem;
    width: fit-content;
    box-shadow: 0 8px 18px rgba(0,0,0,0.18);
}

/* Hero image card */
.image-card {
    background: linear-gradient(180deg, #111827 0%, #0F172A 100%);
    border-radius: 26px;
    padding: 0.8rem;
    box-shadow: 0 18px 40px rgba(0,0,0,0.30);
    border: 1px solid rgba(255,255,255,0.06);
    min-height: 420px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.image-caption {
    color: #CBD5E1 !important;
    text-align: center;
    font-size: 0.92rem;
    margin-top: 0.65rem;
}

/* Cards */
.card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 22px;
    padding: 1.65rem;
    box-shadow: 0 10px 28px rgba(0,0,0,0.18);
    margin-bottom: 1rem;
    border: 1px solid rgba(0,0,0,0.06);
    min-height: 260px;
}

.card p, 
.card li, 
.card span, 
.card div {
    color: #1F2937 !important;
}

.sub-label {
    color: #1E6F5C !important;
    font-size: 0.9rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.45rem;
}

.section-title {
    color: #0B3C5D !important;
    font-size: 1.65rem;
    font-weight: 800;
    margin-top: 0.25rem;
    margin-bottom: 0.8rem;
    line-height: 1.25;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(180deg, #111827 0%, #172033 100%);
    border-radius: 20px;
    padding: 1.3rem;
    text-align: center;
    box-shadow: 0 12px 26px rgba(0,0,0,0.24);
    border: 1px solid rgba(255,255,255,0.06);
}

.kpi-title {
    color: #94A3B8 !important;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.kpi-value {
    color: #F8FAFC !important;
    font-size: 1.65rem;
    font-weight: 800;
    line-height: 1.25;
}

/* Feature boxes */
.feature-box {
    background: linear-gradient(180deg, #111827 0%, #172033 100%);
    border-left: 6px solid #FDB813;
    padding: 1.1rem 1.1rem 1.1rem 1.15rem;
    border-radius: 16px;
    margin-bottom: 0.95rem;
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
    line-height: 1.65;
    font-size: 0.98rem;
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

/* Image styling */
[data-testid="stImage"] img {
    border-radius: 20px;
    box-shadow: 0 16px 34px rgba(0,0,0,0.30);
    width: 100%;
    object-fit: cover;
}

/* Small responsive improvement */
@media (max-width: 900px) {
    .hero-title {
        font-size: 2.3rem;
    }
    .hero-box {
        min-height: auto;
    }
    .image-card {
        min-height: auto;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO SECTION
# -----------------------------
left_hero, right_hero = st.columns([1.55, 1], gap="large")

with left_hero:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-label">SPICE · Solar Power Investment Cooperative of Edmonton</div>
        <div class="hero-title">
            Turning Solar Design Choices Into
            <span class="hero-highlight">Actionable Impact</span>
        </div>
        <div class="hero-text">
            The SPICE Solar Impact Dashboard is designed to help translate solar system
            configuration into meaningful technical, financial, and environmental insights.
            Instead of stopping at raw energy outputs, the platform supports clearer
            decision-making by connecting solar design to value.
        </div>
        <div class="hero-text">
            This includes energy production estimates, financial performance, emissions
            reduction, real-site validation, and scenario-based comparison for community-focused
            solar planning.
        </div>
        <div class="hero-badge">Built by Data Alchemists</div>
    </div>
    """, unsafe_allow_html=True)

with right_hero:
    st.markdown('<div class="image-card">', unsafe_allow_html=True)

    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.markdown("""
        <div style="
            width:100%;
            padding:3rem 1rem;
            text-align:center;
            color:#CBD5E1;
            font-size:1rem;
        ">
            Image not found.<br>
            Save your file as <strong>solar_image.png</strong> in the same folder as this page.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="image-caption">
            Real-world solar installation context aligned with SPICE stakeholder communication.
        </div>
    </div>
    """, unsafe_allow_html=True)

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
            SPICE needs a practical way to demonstrate how solar design decisions
            influence real project outcomes. Stakeholders need more than technical
            numbers — they need a tool that explains how design choices affect
            energy production, economic value, and environmental benefit.
        </p>
        <p>
            This dashboard helps bridge that gap by turning solar system parameters
            into clear, visual, and decision-ready insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Platform Goal</div>
        <div class="section-title">Why this matters for SPICE</div>
        <p>
            This platform supports solar planning, project communication, and stakeholder
            confidence by combining simulation, analytics, and business interpretation in one place.
        </p>
        <p>
            It is designed to support stronger conversations with building owners, investors,
            and community partners who need both technical credibility and business clarity.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# KPI ROW
# -----------------------------
st.markdown('<div class="section-heading">Dashboard Snapshot</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4, gap="large")

with c1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Client</div>
        <div class="kpi-value">SPICE</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Team</div>
        <div class="kpi-value">Data Alchemists</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Datasets</div>
        <div class="kpi-value">9</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Scope</div>
        <div class="kpi-value">Energy · Finance · Environment</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# VALUE BLOCKS
# -----------------------------
st.markdown('<div class="section-heading">What this dashboard enables</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>Solar Simulation</h4>
        <p>Explore how tilt, azimuth, system size, and scenario conditions affect production outcomes.</p>
    </div>

    <div class="feature-box">
        <h4>Financial Analysis</h4>
        <p>Translate energy output into savings, payback, and project value using real pricing and cost context.</p>
    </div>

    <div class="feature-box">
        <h4>Environmental Impact</h4>
        <p>Estimate avoided emissions, carbon value, and broader sustainability benefits for community projects.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>Weather & Seasonality Context</h4>
        <p>Understand how climate patterns, cloud cover, and snow conditions influence solar performance in Edmonton.</p>
    </div>

    <div class="feature-box">
        <h4>Real-Site Validation</h4>
        <p>Compare project logic against observed production data from actual SPICE sites such as Bissell and Visser.</p>
    </div>

    <div class="feature-box">
        <h4>Scenario Comparison</h4>
        <p>Support decision-making by comparing design alternatives and system configurations across simulated cases.</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# STAKEHOLDER SECTION
# -----------------------------
st.markdown('<div class="section-heading">Who this supports</div>', unsafe_allow_html=True)

a, b, c = st.columns(3, gap="large")

with a:
    st.markdown("""
    <div class="card" style="min-height: 210px;">
        <div class="sub-label">Customers</div>
        <p>
            Helps building owners understand how solar systems may affect future
            energy savings, feasibility, and long-term project value.
        </p>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="card" style="min-height: 210px;">
        <div class="sub-label">Investors</div>
        <p>
            Supports financial interpretation by linking production outcomes to
            savings, payback period, and broader return potential.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown("""
    <div class="card" style="min-height: 210px;">
        <div class="sub-label">Community Stakeholders</div>
        <p>
            Communicates the environmental and social value of community-driven
            solar projects in a clear and accessible format.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# FOOTER NOTE
# -----------------------------
st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Use the sidebar to explore the methodology, simulation,
    financial, environmental, validation, and predictive analysis pages.
</div>
""", unsafe_allow_html=True)
