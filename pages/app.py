import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="SPICE Solar Analytics Dashboard",
    page_icon="☀️",
    layout="wide"
)

# =========================================================
# PATH FIX (IMPORTANT)
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "images"

# =========================================================
# Helper
# =========================================================
def get_base64_image(image_path):
    path = Path(image_path)
    if not path.exists():
        return None
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

banner_base64 = get_base64_image(IMAGE_DIR / "norquest_banner.png")
# =========================================================
# Custom CSS
# =========================================================
st.markdown("""
<style>
/* -------------------------
   Global App Styling
------------------------- */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(32, 92, 70, 0.22) 0%, transparent 28%),
        radial-gradient(circle at top right, rgba(215, 169, 40, 0.10) 0%, transparent 22%),
        linear-gradient(180deg, #06110e 0%, #0a1713 35%, #0c1d18 70%, #10261e 100%);
    color: #f3f4f6;
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2.5rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 1450px;
}

html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

/* -------------------------
   Sidebar polish
------------------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #151823 0%, #1d2130 100%);
    border-right: 1px solid rgba(255,255,255,0.05);
}

section[data-testid="stSidebar"] * {
    color: #f3f4f6 !important;
}

/* -------------------------
   Typography
------------------------- */
.page-tag {
    display: inline-block;
    padding: 0.42rem 0.95rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    color: #eef6f2;
    border: 1px solid rgba(255,255,255,0.12);
    font-size: 0.80rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 1rem;
}

.section-title {
    font-size: 2.1rem;
    font-weight: 900;
    color: #f8fafc;
    margin-top: 0.3rem;
    margin-bottom: 0.4rem;
}

.section-subtext {
    color: #b6c5be;
    font-size: 1rem;
    line-height: 1.75;
    margin-bottom: 1.35rem;
}

.mini-heading {
    color: #d7a928;
    font-size: 0.84rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.5rem;
}

/* -------------------------
   Hero Section
------------------------- */
.hero-wrap {
    position: relative;
    overflow: hidden;
    border-radius: 30px;
    min-height: 390px;
    margin-bottom: 2rem;
    box-shadow: 0 20px 46px rgba(0,0,0,0.36);
    border: 1px solid rgba(255,255,255,0.07);
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background:
        linear-gradient(90deg, rgba(9,36,28,0.96) 0%, rgba(20,83,62,0.88) 42%, rgba(8,18,15,0.72) 100%);
}

.hero-content {
    position: relative;
    z-index: 2;
    padding: 3.2rem 3.3rem;
    max-width: 800px;
}

.hero-title {
    font-size: 3.35rem;
    font-weight: 950;
    line-height: 1.08;
    color: #f8fafc;
    margin-bottom: 1rem;
}

.hero-highlight {
    color: #d7a928;
}

.hero-text {
    color: #e8f2ed;
    font-size: 1.08rem;
    line-height: 1.9;
    max-width: 720px;
    margin-bottom: 1.4rem;
}

.hero-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-top: 1rem;
}

.hero-chip {
    background: rgba(255,255,255,0.10);
    color: #f8fafc;
    border: 1px solid rgba(255,255,255,0.14);
    padding: 0.55rem 0.95rem;
    border-radius: 999px;
    font-size: 0.84rem;
    font-weight: 700;
}

/* -------------------------
   Cards
------------------------- */
.glass-card {
    background: linear-gradient(180deg, rgba(19,35,29,0.96) 0%, rgba(12,24,21,0.96) 100%);
    border: 1px solid rgba(154,205,180,0.11);
    border-radius: 24px;
    padding: 1.4rem 1.35rem;
    box-shadow: 0 14px 30px rgba(0,0,0,0.24);
    min-height: 100%;
    backdrop-filter: blur(6px);
}

.kpi-card {
    background:
        radial-gradient(circle at top right, rgba(215,169,40,0.10) 0%, transparent 26%),
        linear-gradient(135deg, #17382f 0%, #122a22 55%, #0f211b 100%);
    border: 1px solid rgba(154,205,180,0.14);
    border-radius: 24px;
    padding: 1.3rem 1.25rem;
    box-shadow: 0 12px 26px rgba(0,0,0,0.26);
    min-height: 155px;
}

.kpi-label {
    color: #bdd6ca;
    font-size: 0.92rem;
    font-weight: 700;
    margin-bottom: 0.55rem;
}

.kpi-value {
    color: #f8fafc;
    font-size: 2.15rem;
    font-weight: 900;
    line-height: 1.08;
    margin-bottom: 0.35rem;
}

.kpi-delta {
    color: #d7a928;
    font-size: 0.95rem;
    font-weight: 700;
}

.card-title {
    color: #f8fafc;
    font-size: 1.22rem;
    font-weight: 900;
    margin-bottom: 0.7rem;
}

.card-text {
    color: #c8d5cf;
    font-size: 0.98rem;
    line-height: 1.82;
    margin-bottom: 0;
}

.card-highlight {
    color: #d7a928;
    font-weight: 800;
}

.feature-card {
    background:
        linear-gradient(180deg, rgba(18,40,33,0.97) 0%, rgba(11,24,20,0.97) 100%);
    border: 1px solid rgba(215,169,40,0.10);
    border-radius: 22px;
    padding: 1.25rem;
    min-height: 235px;
    box-shadow: 0 10px 22px rgba(0,0,0,0.22);
}

.feature-icon {
    font-size: 1.3rem;
    margin-bottom: 0.6rem;
}

.feature-title {
    color: #f8fafc;
    font-size: 1.08rem;
    font-weight: 850;
    margin-bottom: 0.75rem;
}

.feature-text {
    color: #c8d5cf;
    font-size: 0.95rem;
    line-height: 1.75;
}

/* -------------------------
   Special strips
------------------------- */
.insight-strip {
    background: linear-gradient(90deg, rgba(27,79,62,0.95) 0%, rgba(18,50,41,0.95) 100%);
    border-left: 6px solid #d7a928;
    border-radius: 20px;
    padding: 1.25rem 1.35rem;
    margin-top: 0.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 22px rgba(0,0,0,0.20);
}

.insight-title {
    font-size: 1.08rem;
    font-weight: 850;
    color: #f8fafc;
    margin-bottom: 0.45rem;
}

.insight-text {
    color: #e3eee8;
    font-size: 0.98rem;
    line-height: 1.75;
}

.roadmap-card {
    background: linear-gradient(180deg, rgba(19,35,29,0.96) 0%, rgba(12,24,21,0.96) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 1.15rem;
    min-height: 220px;
    box-shadow: 0 10px 22px rgba(0,0,0,0.22);
}

.roadmap-step {
    display: inline-block;
    background: rgba(215,169,40,0.14);
    color: #f2c44b;
    padding: 0.32rem 0.72rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 800;
    margin-bottom: 0.75rem;
}

.roadmap-title {
    color: #f8fafc;
    font-size: 1.08rem;
    font-weight: 850;
    margin-bottom: 0.65rem;
}

.roadmap-text {
    color: #c8d5cf;
    font-size: 0.95rem;
    line-height: 1.7;
}

/* -------------------------
   Footer
------------------------- */
.footer-note {
    color: #90a69d;
    text-align: center;
    font-size: 0.92rem;
    margin-top: 1.4rem;
    padding-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# Hero
# =========================================================
if banner_base64:
    st.markdown(
        f"""
        <div class="hero-wrap" style="
            background-image: url('data:image/png;base64,{banner_base64}');
            background-size: cover;
            background-position: center;
        ">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="page-tag">SPICE • TEAM DATA ALCHEMISTS • NORQUEST COLLEGE</div>
                <div class="hero-title">
                    Smart Solar Decisions for
                    <span class="hero-highlight">Investment</span>,
                    <span class="hero-highlight">Impact</span>, and
                    <span class="hero-highlight">Growth</span>
                </div>
                <div class="hero-text">
                    A business-focused solar analytics dashboard designed to help stakeholders
                    evaluate solar design choices through energy generation, projected financial
                    return, sustainability impact, and strategic decision support.
                </div>
                <div class="hero-badges">
                    <div class="hero-chip">Energy Analytics</div>
                    <div class="hero-chip">Financial Insight</div>
                    <div class="hero-chip">Environmental Value</div>
                    <div class="hero-chip">Investor Communication</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="page-tag">SPICE • TEAM DATA ALCHEMISTS • NORQUEST COLLEGE</div>
            <div class="hero-title">
                Smart Solar Decisions for
                <span class="hero-highlight">Investment</span>,
                <span class="hero-highlight">Impact</span>, and
                <span class="hero-highlight">Growth</span>
            </div>
            <div class="hero-text">
                A business-focused solar analytics dashboard designed to help stakeholders
                evaluate solar design choices through energy generation, projected financial
                return, sustainability impact, and strategic decision support.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Executive Overview
# =========================================================
st.markdown('<div class="section-title">Executive Overview</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">A premium snapshot of the business value this platform can communicate to SPICE stakeholders, investors, and decision-makers.</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)

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

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# Problem + Value Framing
# =========================================================
left, right = st.columns([1.05, 0.95])

with left:
    st.markdown("""
    <div class="glass-card">
        <div class="mini-heading">Problem Statement</div>
        <div class="card-title">Why This Dashboard Matters</div>
        <p class="card-text">
            SPICE needs a clearer way to explain how solar design choices influence
            <span class="card-highlight">energy production</span>,
            <span class="card-highlight">financial return</span>, and
            <span class="card-highlight">environmental benefit</span>.
            Without a unified dashboard, technical results remain harder to communicate
            to non-technical stakeholders and potential investors.
        </p>
        <br>
        <p class="card-text">
            This platform turns solar inputs and performance outputs into a
            <span class="card-highlight">business-facing decision support experience</span>.
            Instead of only displaying numbers, it helps connect design decisions with
            practical questions around return, feasibility, and sustainability impact.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="glass-card">
        <div class="mini-heading">Strategic Lens</div>
        <div class="card-title">Business Perspective</div>
        <p class="card-text">
            From a business standpoint, the dashboard supports three high-value goals:
        </p>
        <br>
        <p class="card-text">
            1. <span class="card-highlight">Investment clarity</span> — identify whether a configuration appears financially attractive.<br><br>
            2. <span class="card-highlight">Risk awareness</span> — understand how outcomes change under different assumptions and designs.<br><br>
            3. <span class="card-highlight">Sustainability communication</span> — show measurable carbon and environmental value in a stakeholder-friendly way.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Insight Strip
# =========================================================
st.markdown("""
<div class="insight-strip">
    <div class="insight-title">Strategic Positioning</div>
    <div class="insight-text">
        The strongest value of this dashboard is that it does not behave like a simple calculator.
        It behaves like a <b>decision-support platform</b> that helps users compare solar configurations,
        understand trade-offs, and communicate the business case behind renewable energy investment.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# Value Areas
# =========================================================
st.markdown('<div class="section-title">Core Value Areas</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">These areas define how the dashboard supports SPICE in both technical analysis and stakeholder communication.</div>',
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💰</div>
        <div class="feature-title">Financial Feasibility</div>
        <div class="feature-text">
            Evaluate projected revenue, cost efficiency, and payback outlook for different
            solar system configurations. This helps shift the conversation from interest
            to investment readiness.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚙️</div>
        <div class="feature-title">Operational Performance</div>
        <div class="feature-text">
            Show how variables such as system size, tilt, azimuth, and losses can influence
            energy generation. This creates a clearer performance story than static assumptions alone.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🌱</div>
        <div class="feature-title">Environmental Reporting</div>
        <div class="feature-text">
            Translate solar output into carbon reduction and sustainability value. This is
            especially useful for presentations, grant narratives, ESG-style communication,
            and community impact reporting.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# Dashboard Roadmap
# =========================================================
st.markdown('<div class="section-title">Dashboard Experience</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">The dashboard is structured to move from project context into simulation, validation, business impact, and modeling insight.</div>',
    unsafe_allow_html=True
)

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">01 • Context</div>
        <div class="roadmap-title">Home & Data Methodology</div>
        <div class="roadmap-text">
            Introduce the problem, data foundation, and analytical structure behind the dashboard.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">02 • Design</div>
        <div class="roadmap-title">Solar Simulation</div>
        <div class="roadmap-text">
            Compare tilt, azimuth, and system size scenarios to explore how design changes affect output.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">03 • Impact</div>
        <div class="roadmap-title">Financial & Environmental Impact</div>
        <div class="roadmap-text">
            Connect projected solar generation to revenue, payback logic, and carbon reduction outcomes.
        </div>
    </div>
    """, unsafe_allow_html=True)

with r4:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-step">04 • Trust</div>
        <div class="roadmap-title">Validation & Modeling</div>
        <div class="roadmap-text">
            Present real-site validation, forecasting logic, and future explainability layers for transparency.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# Stakeholder + Use Case
# =========================================================
s1, s2 = st.columns([1, 1])

with s1:
    st.markdown("""
    <div class="glass-card">
        <div class="mini-heading">Audience</div>
        <div class="card-title">Primary Stakeholders</div>
        <p class="card-text">
            This dashboard is designed to support:
            <br><br>
            • Community solar investors<br>
            • SPICE project stakeholders<br>
            • Sustainability-focused decision-makers<br>
            • Planning and operations discussions<br>
            • Applied analytics and academic project teams
        </p>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="glass-card">
        <div class="mini-heading">Use Case</div>
        <div class="card-title">Strategic Decision Question</div>
        <p class="card-text">
            The platform is built to help answer one important business question:
            <br><br>
            <span class="card-highlight">
                Which solar configuration delivers the strongest balance of return,
                efficiency, and environmental impact?
            </span>
            <br><br>
            This makes the dashboard useful not only for analysis, but also for
            presentation, justification, and stakeholder communication.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# Team Section
# =========================================================
st.markdown('<div class="section-title">Team Data Alchemists</div>', unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <div class="mini-heading">Project Identity</div>
    <div class="card-title">Applied Solar Analytics for SPICE</div>
    <p class="card-text">
        This dashboard is being developed as part of the SPICE Energy Conservation and
        Data Analytics initiative at NorQuest College. It reflects an applied analytics
        approach to a real renewable energy decision problem by combining simulation logic,
        business interpretation, and stakeholder-facing dashboard design.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# Footer
# =========================================================
st.markdown(
    '<div class="footer-note">SPICE Solar Analytics Dashboard | Premium dark-theme home experience</div>',
    unsafe_allow_html=True
)