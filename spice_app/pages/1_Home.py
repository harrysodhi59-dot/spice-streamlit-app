import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

/* Main spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Hero section */
.hero {
    background: linear-gradient(90deg, #1E6F5C, #0B3C5D);
    padding: 2.8rem;
    border-radius: 24px;
    color: white;
    margin-bottom: 1.6rem;
    box-shadow: 0 16px 36px rgba(0,0,0,0.14);
}

.hero h1 {
    font-size: 3.1rem;
    font-weight: 800;
    margin-bottom: 0.7rem;
    line-height: 1.15;
    color: white !important;
}

.hero p {
    font-size: 1.08rem;
    line-height: 1.75;
    max-width: 920px;
    margin-bottom: 0.6rem;
    color: #F4F8F7 !important;
}

.hero-badge {
    display: inline-block;
    background: #FDB813;
    color: #1A1A1A !important;
    font-weight: 700;
    padding: 0.45rem 0.9rem;
    border-radius: 999px;
    margin-top: 0.8rem;
}

/* Common cards */
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
.card div {
    color: #1F2937 !important;
}

/* KPI cards */
.kpi-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 1.25rem;
    text-align: center;
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.06);
}

.kpi-card div {
    color: #1F2937 !important;
}

.kpi-title {
    color: #0B3C5D !important;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
}

.kpi-value {
    color: #1E6F5C !important;
    font-size: 1.8rem;
    font-weight: 800;
}

/* Titles inside HTML */
.section-title {
    color: #0B3C5D !important;
    font-size: 1.55rem;
    font-weight: 800;
    margin-top: 0.8rem;
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
    background: #F8FAFC;
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

.feature-box p {
    margin-bottom: 0;
    color: #374151 !important;
    line-height: 1.6;
}

/* Highlighted word */
.highlight {
    color: #FDB813 !important;
    font-weight: 800;
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

/* Streamlit markdown headings outside HTML */
h2, h3 {
    color: #F8FAFC !important;
    font-weight: 800 !important;
}

/* Optional: better sidebar look in dark theme */
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
    <div class="sub-label" style="color:#B8E0D2 !important;">SPICE · Solar Power Investment Cooperative of Edmonton</div>
    <h1>Turning Solar Design Choices Into <span class="highlight">Actionable Impact</span></h1>
    <p>
        The SPICE Solar Impact Dashboard is designed to help translate solar system
        configuration into meaningful technical, financial, and environmental insights.
        Instead of stopping at raw energy outputs, the platform supports clearer
        decision-making by connecting solar design to value.
    </p>
    <p>
        This includes energy production estimates, financial performance, emissions
        reduction, real-site validation, and scenario-based comparison for community-focused
        solar planning.
    </p>
    <div class="hero-badge">Built by Data Alchemists</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# PROBLEM + PURPOSE
# -----------------------------
left, right = st.columns([1.2, 1])

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
            into clear and decision-ready insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Platform Goal</div>
        <div class="section-title">Why this matters for SPICE</div>
        <p>
            This platform supports solar planning, project communication,
            and stakeholder confidence by combining simulation, analytics,
            and business interpretation in one place.
        </p>
        <p>
            It is designed to support discussions with building owners,
            investors, and community partners.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# KPI ROW
# -----------------------------
st.markdown("## Dashboard Snapshot")

c1, c2, c3, c4 = st.columns(4)

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
st.markdown("## What this dashboard enables")

col1, col2 = st.columns(2)

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
st.markdown("## Who this supports")

a, b, c = st.columns(3)

with a:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Customers</div>
        <p>
            Helps building owners understand how solar systems may affect
            future energy savings and project feasibility.
        </p>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Investors</div>
        <p>
            Supports financial interpretation by linking production outcomes
            to savings, payback, and long-term value.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Community Stakeholders</div>
        <p>
            Communicates the environmental and social value of community-driven
            solar projects in a clear and accessible way.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# FOOTER NOTE
# -----------------------------
st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Use the sidebar to explore the methodology, simulation,
    financial, environmental, validation, and scenario analysis pages.
</div>
""", unsafe_allow_html=True)
