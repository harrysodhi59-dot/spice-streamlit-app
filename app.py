
import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="SPICE Solar Analytics Dashboard",
    page_icon="☀️",
    layout="wide"
)

# -----------------------------
# Load image
# -----------------------------
def get_base64_image(image_path):
    path = Path(image_path)
    if not path.exists():
        return None
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

banner_base64 = get_base64_image("images/norquest_banner.png")

# -----------------------------
# Global Styling
# -----------------------------
st.markdown("""
<style>
body {
    background: #f6f8fb;
}

.block-container {
    padding: 1.2rem 1.5rem;
    max-width: 1400px;
}

.section-card {
    background: white;
    padding: 1.2rem;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}

.small-text {
    color: #5a6a7a;
    font-size: 0.95rem;
    line-height: 1.7;
}

.section-title {
    font-size: 1.6rem;
    font-weight: 800;
    color: #1f3a52;
    margin-top: 1rem;
    margin-bottom: 0.8rem;
}

.snapshot-card {
    background: white;
    padding: 1rem;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

.snapshot-title {
    font-size: 0.7rem;
    color: #6b7280;
    font-weight: 700;
}

.snapshot-value {
    font-size: 1.4rem;
    font-weight: 800;
    color: #0f766e;
}

.feature-left {
    background: #fff7ed;
    border-left: 5px solid #f59e0b;
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 0.7rem;
}

.feature-right {
    background: #eff6ff;
    border-left: 5px solid #3b82f6;
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 0.7rem;
}

.feature-title {
    font-weight: 800;
    color: #1f3a52;
}

.support-card {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    border-top: 4px solid #10b981;
}

.footer {
    background: #eef7f6;
    padding: 0.8rem;
    border-radius: 10px;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO BANNER
# -----------------------------
if banner_base64:
    st.markdown(f"""
    <div style="
        border-radius: 20px;
        overflow: hidden;
        padding: 2.2rem;
        color: white;
        margin-bottom: 1rem;
        background-image:
            linear-gradient(90deg, rgba(24,122,104,0.9), rgba(11,92,122,0.9)),
            url('data:image/png;base64,{banner_base64}');
        background-size: cover;
    ">

        <div style="
            background:#fbbf24;
            color:#111827;
            display:inline-block;
            padding:5px 12px;
            border-radius:20px;
            font-size:12px;
            font-weight:700;
            margin-bottom:12px;
        ">
            Built by Data Alchemists
        </div>

        <h1 style="font-size:2.6rem; font-weight:800; margin-bottom:10px;">
            Turning Solar Design Choices Into
            <span style="color:#fbbf24;">Actionable Impact</span>
        </h1>

        <p style="max-width:700px; font-size:1rem;">
            The SPICE Solar Impact Dashboard helps translate solar system configuration into meaningful
            technical, financial, and environmental insights.
        </p>

        <p style="max-width:700px; font-size:0.95rem;">
            It includes energy production, financial performance, emissions reduction,
            and scenario-based comparisons.
        </p>

    </div>
    """, unsafe_allow_html=True)
else:
    st.error("Image not found: images/norquest_banner.png")

# -----------------------------
# TOP CARDS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="section-card">
    <h3>What problem this dashboard solves</h3>
    <p class="small-text">
    SPICE needs a way to explain how solar design affects energy, cost, and environment.
    This dashboard converts technical data into decision-ready insights.
    </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="section-card">
    <h3>Why this matters for SPICE</h3>
    <p class="small-text">
    Helps investors, building owners, and stakeholders understand solar project value
    using data-driven insights.
    </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# SNAPSHOT
# -----------------------------
st.markdown('<div class="section-title">Dashboard Snapshot</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

c1.markdown('<div class="snapshot-card"><div class="snapshot-title">Client</div><div class="snapshot-value">SPICE</div></div>', unsafe_allow_html=True)
c2.markdown('<div class="snapshot-card"><div class="snapshot-title">Team</div><div class="snapshot-value">Data Alchemists</div></div>', unsafe_allow_html=True)
c3.markdown('<div class="snapshot-card"><div class="snapshot-title">Datasets</div><div class="snapshot-value">9</div></div>', unsafe_allow_html=True)
c4.markdown('<div class="snapshot-card"><div class="snapshot-title">Scope</div><div class="snapshot-value">Energy · Finance · Environment</div></div>', unsafe_allow_html=True)

# -----------------------------
# FEATURES
# -----------------------------
st.markdown('<div class="section-title">What this dashboard enables</div>', unsafe_allow_html=True)

l, r = st.columns(2)

with l:
    st.markdown('<div class="feature-left"><div class="feature-title">Solar Simulation</div>Explore tilt, azimuth, and system size.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-left"><div class="feature-title">Financial Analysis</div>Understand savings and ROI.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-left"><div class="feature-title">Environmental Impact</div>Measure emissions reduction.</div>', unsafe_allow_html=True)

with r:
    st.markdown('<div class="feature-right"><div class="feature-title">Weather Context</div>Understand seasonal impact.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-right"><div class="feature-title">Real Validation</div>Compare with real SPICE data.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-right"><div class="feature-title">Scenario Comparison</div>Compare system options.</div>', unsafe_allow_html=True)

# -----------------------------
# SUPPORT
# -----------------------------
st.markdown('<div class="section-title">Who this supports</div>', unsafe_allow_html=True)

a, b, c = st.columns(3)

a.markdown('<div class="support-card"><b>Customers</b><br>Understand solar savings and feasibility.</div>', unsafe_allow_html=True)
b.markdown('<div class="support-card"><b>Investors</b><br>Analyze ROI and long-term value.</div>', unsafe_allow_html=True)
c.markdown('<div class="support-card"><b>Community</b><br>Understand environmental impact.</div>', unsafe_allow_html=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<div class="footer">
<b>Next step:</b> Use sidebar to explore full dashboard pages.
</div>
""", unsafe_allow_html=True)
