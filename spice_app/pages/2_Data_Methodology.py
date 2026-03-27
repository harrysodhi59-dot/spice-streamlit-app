import os
import streamlit as st

st.set_page_config(
    page_title="Data & Methodology",
    page_icon="🧠",
    layout="wide"
)

# Image path
image_path = os.path.join(os.path.dirname(__file__), "methodology_image.png")

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

/* Main layout */
.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2.4rem;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 100%;
}

/* Background */
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

/* General headings */
h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
    font-weight: 800 !important;
}

.section-heading {
    font-size: 2rem;
    font-weight: 850;
    color: #F8FAFC !important;
    margin-top: 0.4rem;
    margin-bottom: 0.55rem;
}

.section-subtext {
    color: #B6C0CE !important;
    font-size: 1rem;
    line-height: 1.75;
    margin-bottom: 1.3rem;
}

/* Hero */
.hero-box {
    background: linear-gradient(135deg, rgba(30,111,92,0.96) 0%, rgba(11,60,93,0.96) 100%);
    padding: 3rem;
    border-radius: 28px;
    color: white;
    box-shadow: 0 20px 46px rgba(0,0,0,0.34);
    min-height: 430px;
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
    width: 190px;
    height: 190px;
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
    font-size: 3.2rem;
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
    font-size: 1.06rem;
    line-height: 1.88;
    color: #F3F7F6 !important;
    margin-bottom: 0.7rem;
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

/* Image */
[data-testid="stImage"] img {
    border-radius: 26px;
    box-shadow: 0 20px 46px rgba(0,0,0,0.34);
    border: 1px solid rgba(255,255,255,0.08);
    width: 100%;
    object-fit: cover;
}

/* Light cards */
.card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 24px;
    padding: 1.75rem;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    margin-bottom: 1rem;
    border: 1px solid rgba(0,0,0,0.06);
    min-height: 250px;
}

.card p, .card li, .card span, .card div, .card h3, .card h4 {
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
    font-size: 1.6rem;
    font-weight: 850;
    line-height: 1.25;
}

.kpi-note {
    color: #FDB813 !important;
    font-size: 0.88rem;
    font-weight: 700;
    margin-top: 0.45rem;
}

/* Dark feature boxes */
.feature-box {
    background: linear-gradient(180deg, #111827 0%, #172033 100%);
    border-left: 6px solid #FDB813;
    padding: 1.15rem 1.15rem 1.15rem 1.2rem;
    border-radius: 18px;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.20);
    min-height: 155px;
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

/* Insight strip */
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

/* Roadmap cards */
.roadmap-card {
    background: linear-gradient(180deg, #111827 0%, #172033 100%);
    border-radius: 20px;
    padding: 1.3rem;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.20);
    min-height: 220px;
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
left_hero, right_hero = st.columns([1.35, 1], gap="large")

with left_hero:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-label">Methodology • Business Logic • Decision Architecture</div>
        <div class="hero-title">
            Turning Data Into
            <span class="hero-highlight">Decision Support</span>
        </div>
        <div class="hero-text">
            This page explains the analytical structure behind the SPICE dashboard. Rather than
            focusing only on raw datasets, the methodology is designed to connect solar design,
            business interpretation, validation logic, and stakeholder-facing communication.
        </div>
        <div class="hero-text">
            The goal is to create a platform that supports practical planning, scenario comparison,
            and value-based discussion around solar investment, performance, and environmental impact.
        </div>
        <div class="hero-badge-wrap">
            <div class="hero-badge">Business-Focused Methodology</div>
            <div class="hero-chip">Decision Support</div>
            <div class="hero-chip">Validation Logic</div>
            <div class="hero-chip">Stakeholder Clarity</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right_hero:
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
        st.markdown("""
        <div class="image-caption">
            Methodology is designed to support real planning, communication, and applied solar decision-making.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("methodology_image.png not found in the same folder as this page")

# -----------------------------
# OVERVIEW
# -----------------------------
left, right = st.columns([1.2, 1], gap="large")

with left:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Methodological Approach</div>
        <div class="section-title">How the platform is structured</div>
        <p>
            The platform is built as a layered decision-support system. It begins with solar simulation
            and performance logic, then adds contextual information such as environmental, operational,
            and financial interpretation to make the results more meaningful for SPICE.
        </p>
        <p>
            This structure helps move the dashboard beyond a basic technical tool by connecting system
            design choices to broader project value, stakeholder confidence, and real planning discussion.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Rubric Alignment</div>
        <div class="section-title">Why this methodology matters</div>
        <p>
            The methodology supports the instructor’s focus on problem understanding, structured analysis,
            business relevance, and interpretability. It explains not only what the platform shows, but
            also why each layer is useful for SPICE as a client-facing decision-support tool.
        </p>
        <p>
            This creates a stronger foundation for simulation, impact analysis, validation, and future modeling.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# INSIGHT STRIP
# -----------------------------
st.markdown("""
<div class="insight-strip">
    <strong>Strategic Lens:</strong>
    <span>
        The methodology is intentionally designed to support client communication, not just analysis.
        Each layer helps translate solar performance into business value, environmental meaning, and
        practical discussion for planning and decision-making.
    </span>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# KPI ROW
# -----------------------------
st.markdown('<div class="section-heading">Methodology Snapshot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">A high-level view of how the platform combines technical logic, business interpretation, and validation-oriented thinking.</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4, gap="large")

with k1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Approach</div>
        <div class="kpi-value">Layered Analytics</div>
        <div class="kpi-note">From simulation to interpretation</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Focus</div>
        <div class="kpi-value">Technical + Business</div>
        <div class="kpi-note">Not only raw output</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Validation Basis</div>
        <div class="kpi-value">Real Site Logic</div>
        <div class="kpi-note">Grounded in operational context</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Team Lens</div>
        <div class="kpi-value">Data Alchemists</div>
        <div class="kpi-note">Applied analytics project</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# CORE PROCESS
# -----------------------------
st.markdown('<div class="section-heading">How the methodology works</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">The platform follows a structured flow that supports comparison, interpretation, and stakeholder-facing discussion.</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""
    <div class="feature-box">
        <h4>1. Simulation Foundation</h4>
        <p>
            The methodology begins with solar system behavior and performance assumptions to estimate
            how design decisions such as tilt, azimuth, and size can influence energy output.
        </p>
    </div>

    <div class="feature-box">
        <h4>2. Context Integration</h4>
        <p>
            Additional context is layered on top of technical results so the dashboard reflects practical
            conditions such as seasonal behavior, project context, and business-facing interpretation.
        </p>
    </div>

    <div class="feature-box">
        <h4>3. Impact Translation</h4>
        <p>
            Technical outputs are translated into decision-ready outcomes such as value discussion,
            sustainability interpretation, and planning relevance.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-box">
        <h4>4. Validation Thinking</h4>
        <p>
            Real-site logic is incorporated to help ground the platform in operational reality and support
            trust in the broader analytical story being communicated to SPICE stakeholders.
        </p>
    </div>

    <div class="feature-box">
        <h4>5. Scenario Comparison</h4>
        <p>
            The methodology supports comparison across multiple design choices so users can evaluate
            trade-offs instead of relying on one static estimate.
        </p>
    </div>

    <div class="feature-box">
        <h4>6. Dashboard Communication</h4>
        <p>
            The final layer presents results visually so the insights are easier to understand, explain,
            and use in both academic and client-facing discussion.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# RUBRIC / BUSINESS VALUE
# -----------------------------
st.markdown('<div class="section-heading">Why this approach fits the project rubric</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">This page is structured to highlight problem understanding, analytical design, and practical business value rather than overwhelming detail.</div>',
    unsafe_allow_html=True
)

r1, r2, r3, r4 = st.columns(4, gap="large")

with r1:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">01</div>
        <div class="roadmap-title">Problem Framing</div>
        <div class="roadmap-text">
            The methodology begins with the client need: helping SPICE explain solar decisions in a more practical and stakeholder-friendly way.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">02</div>
        <div class="roadmap-title">Structured Analysis</div>
        <div class="roadmap-text">
            The platform follows a clear sequence from simulation to interpretation, which makes the analysis easier to justify and present.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">03</div>
        <div class="roadmap-title">Business Relevance</div>
        <div class="roadmap-text">
            Results are framed in terms of value, impact, and communication rather than isolated technical outputs.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r4:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">04</div>
        <div class="roadmap-title">Modeling Readiness</div>
        <div class="roadmap-text">
            The methodology creates a strong base for future modeling, explainability, and client trust as the project evolves.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# DECISION SUPPORT IDEA
# -----------------------------
st.markdown('<div class="section-heading">Core idea behind the methodology</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">The value of the methodology is that it helps turn analysis into discussion, and discussion into better project decisions.</div>',
    unsafe_allow_html=True
)

a, b = st.columns(2, gap="large")

with a:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Beyond raw analysis</div>
        <div class="section-title">Not just about datasets</div>
        <p>
            The purpose of this page is not to list files or technical inputs. It is to show how the
            dashboard is organized to support comparison, interpretation, and practical communication.
        </p>
        <p>
            This makes the methodology more aligned with stakeholder needs and better suited to a business-style presentation.
        </p>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Applied value</div>
        <div class="section-title">From data to action</div>
        <p>
            By combining structure, context, and visual interpretation, the methodology supports a stronger
            decision-support experience for SPICE. It helps connect design logic to value-based conversation.
        </p>
        <p>
            That makes the platform more useful for planning, validation, and stakeholder-facing explanation.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# FOOTER NOTE
# -----------------------------
st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Move to the Solar Simulation page to explore how design choices influence
    projected output and compare different solar scenarios in a more interactive way.
</div>
""", unsafe_allow_html=True)
