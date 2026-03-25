import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="SPICE Solar Analytics Dashboard",
    page_icon="☀️",
    layout="wide"
)

# -----------------------------
# Helper
# -----------------------------
def get_base64_image(image_path):
    path = Path(image_path)
    if not path.exists():
        return None
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Use your existing banner image here
banner_base64 = get_base64_image("images/norquest_banner.png")

# -----------------------------
# Custom Theme CSS
# -----------------------------
st.markdown("""
<style>
/* Main app background */
.stApp {
    background: linear-gradient(180deg, #07120f 0%, #0b1714 40%, #0f1f1a 100%);
    color: #f3f4f6;
}

/* Hide default Streamlit header space a bit */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 1400px;
}

/* Global font */
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

/* Section heading */
.section-title {
    font-size: 2rem;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 0.5rem;
    margin-bottom: 0.35rem;
}

.section-subtext {
    color: #b8c4bf;
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 1.5rem;
}

/* Hero badge */
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    color: #f8fafc;
    padding: 0.45rem 0.95rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.4px;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.15);
}

/* Premium card */
.dark-card {
    background: linear-gradient(180deg, rgba(18,33,28,0.96) 0%, rgba(13,24,21,0.96) 100%);
    border: 1px solid rgba(139, 196, 175, 0.14);
    border-radius: 22px;
    padding: 1.35rem 1.35rem;
    box-shadow: 0 10px 28px rgba(0,0,0,0.28);
    min-height: 100%;
}

/* KPI card */
.kpi-card {
    background: linear-gradient(135deg, #17382f 0%, #10271f 100%);
    border: 1px solid rgba(154, 205, 180, 0.15);
    border-radius: 22px;
    padding: 1.25rem 1.2rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}

.kpi-label {
    color: #b9d4c7;
    font-size: 0.92rem;
    font-weight: 600;
    margin-bottom: 0.55rem;
}

.kpi-value {
    color: #f8fafc;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}

.kpi-delta {
    color: #d7a928;
    font-size: 0.95rem;
    font-weight: 700;
}

/* Info text */
.card-title {
    color: #f8fafc;
    font-size: 1.2rem;
    font-weight: 800;
    margin-bottom: 0.7rem;
}

.card-text {
    color: #c5d2cb;
    font-size: 0.98rem;
    line-height: 1.8;
    margin-bottom: 0;
}

.card-highlight {
    color: #d7a928;
    font-weight: 700;
}

/* Mini highlight boxes */
.feature-box {
    background: linear-gradient(180deg, #132a23 0%, #0f1f1a 100%);
    border: 1px solid rgba(215, 169, 40, 0.12);
    border-radius: 20px;
    padding: 1.2rem;
    min-height: 220px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.22);
}

.feature-title {
    color: #f8fafc;
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: 0.8rem;
}

.feature-text {
    color: #c5d2cb;
    font-size: 0.96rem;
    line-height: 1.75;
}

/* Recommendation banner */
.reco-box {
    background: linear-gradient(90deg, rgba(27,79,62,0.95) 0%, rgba(18,50,41,0.95) 100%);
    border-left: 6px solid #d7a928;
    border-radius: 18px;
    padding: 1.25rem 1.35rem;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 18px rgba(0,0,0,0.20);
}

.reco-title {
    font-size: 1.08rem;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 0.5rem;
}

.reco-text {
    color: #dbe7e1;
    font-size: 0.98rem;
    line-height: 1.7;
}

/* Footer line */
.footer-note {
    color: #8fa49b;
    text-align: center;
    font-size: 0.92rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Hero Section
# -----------------------------
if banner_base64:
    st.markdown(
        f"""
        <div style="
            position: relative;
            border-radius: 28px;
            overflow: hidden;
            margin-bottom: 2rem;
            min-height: 360px;
            box-shadow: 0 18px 42px rgba(0,0,0,0.34);
            background-image:
                linear-gradient(90deg, rgba(13,55,42,0.95) 0%, rgba(28,102,76,0.84) 48%, rgba(10,22,18,0.72) 100%),
                url('data:image/png;base64,{banner_base64}');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
        ">
            <div style="padding: 3rem 3.2rem; max-width: 760px;">
                <div class="hero-badge">SPICE • TEAM DATA ALCHEMISTS • NORQUEST COLLEGE</div>
                <h1 style="
                    font-size: 3.25rem;
                    font-weight: 900;
                    line-height: 1.12;
                    margin-bottom: 0.85rem;
                    color: #f8fafc;
                ">
                    Smart Solar Decisions for
                    <span style="color:#d7a928;">Investment</span>,
                    <span style="color:#d7a928;">Impact</span>, and
                    <span style="color:#d7a928;">Growth</span>
                </h1>
                <p style="
                    font-size: 1.08rem;
                    line-height: 1.8;
                    color: #ecf5f1;
                    max-width: 690px;
                    margin-bottom: 0;
                ">
                    A business-focused solar analytics dashboard that helps stakeholders evaluate
                    energy generation, financial return, investment value, and environmental impact
                    across different system configurations.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Banner image not found. Make sure this file exists: images/norquest_banner.png")

# -----------------------------
# KPI Row
# -----------------------------
st.markdown('<div class="section-title">Executive Overview</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">A quick business snapshot of the value this platform can communicate to investors, community stakeholders, and decision-makers.</div>',
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
        <div class="kpi-delta">Sustainability outcome</div>
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

# -----------------------------
# Two-column business value section
# -----------------------------
col1, col2 = st.columns([1.1, 1])

with col1:
    st.markdown("""
    <div class="dark-card">
        <div class="card-title">Why This Dashboard Matters</div>
        <p class="card-text">
            The SPICE Solar Analytics Dashboard is more than a technical project. It is a
            <span class="card-highlight">business decision-support platform</span> that helps users understand how
            different solar configurations affect financial return, operational performance, and
            long-term sustainability value.
        </p>
        <br>
        <p class="card-text">
            Instead of looking only at raw energy numbers, the dashboard connects
            <span class="card-highlight">energy generation</span>,
            <span class="card-highlight">projected revenue</span>,
            <span class="card-highlight">ROI-related indicators</span>, and
            <span class="card-highlight">carbon reduction</span> in one place.
            This makes the platform useful for community investors, planning teams, and stakeholders.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="dark-card">
        <div class="card-title">Business Perspective</div>
        <p class="card-text">
            From a business point of view, this project supports three core goals:
        </p>
        <br>
        <p class="card-text">
            1. <span class="card-highlight">Investment clarity</span> — show whether a solar setup is financially attractive.<br><br>
            2. <span class="card-highlight">Risk awareness</span> — help stakeholders understand uncertainty in outcomes.<br><br>
            3. <span class="card-highlight">Sustainability reporting</span> — communicate measurable environmental value.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Feature / business cards
# -----------------------------
st.markdown('<div class="section-title">Business Value Areas</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">These sections make the homepage feel aligned with SPICE, investor communication, and real-world analytics use cases.</div>',
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-title">Financial Feasibility</div>
        <div class="feature-text">
            Show expected revenue, cost efficiency, and payback outlook for different
            solar system configurations. This helps users move from curiosity to
            investment evaluation.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-title">Operational Performance</div>
        <div class="feature-text">
            Analyze how system size, tilt, orientation, and loss factors influence
            energy generation. This gives users a clearer view of performance behaviour
            instead of relying on static assumptions.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-title">Environmental Reporting</div>
        <div class="feature-text">
            Translate solar production into carbon reduction and sustainability impact.
            This is especially valuable for stakeholder presentations, policy alignment,
            and ESG-style communication.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Stakeholder / recommendation row
# -----------------------------
left, right = st.columns([1, 1])

with left:
    st.markdown("""
    <div class="dark-card">
        <div class="card-title">Primary Stakeholders</div>
        <p class="card-text">
            This dashboard can support:
            <br><br>
            • Community solar investors<br>
            • SPICE project stakeholders<br>
            • Sustainability-focused decision-makers<br>
            • Academic and applied analytics teams<br>
            • Policy and planning discussions
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="dark-card">
        <div class="card-title">Strategic Use Case</div>
        <p class="card-text">
            The strongest use of this dashboard is to help answer one business question:
            <span class="card-highlight">Which solar configuration delivers the best balance of return, efficiency, and impact?</span>
            <br><br>
            That makes the platform useful not just for analysis, but for communication and decision support.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Recommendation strip
# -----------------------------
st.markdown("""
<div class="reco-box">
    <div class="reco-title">Recommended Homepage Direction</div>
    <div class="reco-text">
        Keep this page focused on <b>business value, investor communication, and project purpose</b>.
        Then use the next pages for detailed EDA, financial charts, simulation controls,
        and model-driven insights. This will make the whole dashboard feel structured and professional.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Team section
# -----------------------------
st.markdown('<div class="section-title">Team Data Alchemists</div>', unsafe_allow_html=True)

st.markdown("""
<div class="dark-card">
    <p class="card-text">
        This dashboard is being developed as part of the SPICE Energy Conservation and Data Analytics
        initiative at NorQuest College. It reflects an applied machine learning and analytics approach
        to a real-world renewable energy problem, combining technical analysis with financial and
        stakeholder-facing business insight.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="footer-note">SPICE Solar Analytics Dashboard | Designed for dark theme presentation</div>', unsafe_allow_html=True)
