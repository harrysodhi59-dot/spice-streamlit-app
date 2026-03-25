import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="SPICE Solar Analytics Dashboard",
    page_icon="☀️",
    layout="wide"
)

def get_base64_image(image_path):
    path = Path(image_path)
    if not path.exists():
        return None
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

banner_base64 = get_base64_image("images/norquest_banner.png")

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
    background: #f6f8fb;
}

.stApp {
    background: linear-gradient(180deg, #f8fbff 0%, #f4f7fb 100%);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 1.2rem;
    padding-right: 1.2rem;
    max-width: 1500px;
}

h2, h3, h4 {
    color: #12324a;
}

.section-heading {
    font-size: 2rem;
    font-weight: 800;
    color: #19324d;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.section-card {
    background: white;
    padding: 1.25rem;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
    margin-bottom: 1rem;
    border: 1px solid rgba(15, 23, 42, 0.04);
}

.small-text {
    color: #516173;
    font-size: 0.98rem;
    line-height: 1.75;
}

.mini-label {
    color: #1d7a6b;
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.6rem;
}

.snapshot-card {
    background: white;
    border-radius: 18px;
    padding: 1rem 1.2rem;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
    text-align: center;
    border: 1px solid rgba(15, 23, 42, 0.04);
}

.snapshot-title {
    color: #567086;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 0.4rem;
}

.snapshot-value {
    color: #0f766e;
    font-size: 1.55rem;
    font-weight: 800;
}

.feature-box-left {
    background: linear-gradient(135deg, #fff8e7 0%, #ffffff 100%);
    border-left: 5px solid #f59e0b;
    border-radius: 16px;
    padding: 1rem 1rem 0.95rem 1rem;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
    margin-bottom: 0.8rem;
}

.feature-box-right {
    background: linear-gradient(135deg, #eefbff 0%, #ffffff 100%);
    border-left: 5px solid #0ea5e9;
    border-radius: 16px;
    padding: 1rem 1rem 0.95rem 1rem;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
    margin-bottom: 0.8rem;
}

.feature-title {
    color: #16324f;
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 0.35rem;
}

.feature-text {
    color: #5a6a7a;
    font-size: 0.93rem;
    line-height: 1.65;
}

.support-card {
    background: white;
    border-radius: 16px;
    padding: 1rem 1rem 0.95rem 1rem;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
    border-top: 4px solid #14b8a6;
}

.support-title {
    color: #0f766e;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 0.45rem;
}

.support-text {
    color: #5a6a7a;
    font-size: 0.92rem;
    line-height: 1.65;
}

.bottom-note {
    background: linear-gradient(90deg, #eef7f6 0%, #edf6ff 100%);
    border-radius: 14px;
    padding: 0.9rem 1rem;
    color: #29465f;
    font-size: 0.92rem;
    margin-top: 1rem;
    border-left: 4px solid #14b8a6;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Hero Banner
# -----------------------------
if banner_base64:
    st.markdown(
        f"""
        <div style="
            position: relative;
            border-radius: 24px;
            overflow: hidden;
            margin-bottom: 1rem;
            min-height: 300px;
            box-shadow: 0 18px 36px rgba(0,0,0,0.16);
            background-image:
                linear-gradient(90deg, rgba(24,122,104,0.90) 0%, rgba(11,92,122,0.88) 60%, rgba(8,54,92,0.90) 100%),
                url('data:image/png;base64,{banner_base64}');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
        ">
            <div style="padding: 2.4rem 2.6rem; max-width: 880px; color: white;">
                <div style="
                    display: inline-block;
                    background: #fbbf24;
                    color: #1f2937;
                    padding: 0.45rem 0.85rem;
                    border-radius: 999px;
                    font-size: 0.78rem;
                    font-weight: 800;
                    margin-bottom: 1rem;
                    letter-spacing: 0.03em;
                ">
                    Built by Data Alchemists
                </div>

                <h1 style="
                    font-size: 3rem;
                    font-weight: 850;
                    margin-bottom: 0.8rem;
                    line-height: 1.14;
                ">
                    Turning Solar Design Choices Into
                    <span style="color:#fbbf24;">Actionable Impact</span>
                </h1>

                <p style="
                    font-size: 1.02rem;
                    line-height: 1.8;
                    margin-bottom: 0.9rem;
                    max-width: 760px;
                    color: #f5f9ff;
                ">
                    The SPICE Solar Impact Dashboard is designed to help translate solar system
                    configuration into meaningful technical, financial, and environmental insights.
                    Instead of stopping at raw energy outputs, the platform supports clearer
                    decision-making by connecting solar design to value.
                </p>

                <p style="
                    font-size: 0.98rem;
                    line-height: 1.75;
                    margin-bottom: 0;
                    max-width: 760px;
                    color: #eef6fb;
                ">
                    This includes energy production estimates, financial performance, emissions
                    reduction, real-site validation, and scenario-based comparison for
                    community-focused solar planning.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("""
    <div style="
        border-radius: 24px;
        padding: 2.4rem 2.6rem;
        margin-bottom: 1rem;
        min-height: 300px;
        color: white;
        box-shadow: 0 18px 36px rgba(0,0,0,0.16);
        background: linear-gradient(90deg, #187a68 0%, #0b5c7a 60%, #08365c 100%);
    ">
        <div style="
            display: inline-block;
            background: #fbbf24;
            color: #1f2937;
            padding: 0.45rem 0.85rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 800;
            margin-bottom: 1rem;
        ">
            Built by Data Alchemists
        </div>

        <h1 style="font-size: 3rem; font-weight: 850; margin-bottom: 0.8rem; line-height: 1.14;">
            Turning Solar Design Choices Into
            <span style="color:#fbbf24;">Actionable Impact</span>
        </h1>

        <p style="font-size: 1.02rem; line-height: 1.8; max-width: 760px; color: #f5f9ff;">
            The SPICE Solar Impact Dashboard is designed to help translate solar system
            configuration into meaningful technical, financial, and environmental insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Top 2 cards
# -----------------------------
left, right = st.columns([1.25, 1])

with left:
    st.markdown("""
    <div class="section-card">
        <div class="mini-label">Client Need</div>
        <h3 style="margin-top:0; margin-bottom:0.7rem;">What problem this dashboard solves</h3>
        <p class="small-text">
            SPICE needs a practical way to demonstrate how solar design decisions influence
            real project outcomes. Stakeholders need more than technical numbers — they need
            a tool that explains how design choices affect energy production, economic value,
            and environmental benefit.
        </p>
        <p class="small-text" style="margin-bottom:0;">
            This dashboard helps bridge that gap by turning solar system parameters into
            clear and decision-ready insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="section-card">
        <div class="mini-label">Platform Goal</div>
        <h3 style="margin-top:0; margin-bottom:0.7rem;">Why this matters for SPICE</h3>
        <p class="small-text">
            This platform supports solar planning, project communication, and stakeholder
            confidence by combining simulation, analytics, and business interpretation in one place.
        </p>
        <p class="small-text" style="margin-bottom:0;">
            It is designed to support discussions with building owners, investors,
            and community partners.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Snapshot row
# -----------------------------
st.markdown('<div class="section-heading">Dashboard Snapshot</div>', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown("""
    <div class="snapshot-card">
        <div class="snapshot-title">Client</div>
        <div class="snapshot-value">SPICE</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="snapshot-card">
        <div class="snapshot-title">Team</div>
        <div class="snapshot-value">Data Alchemists</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="snapshot-card">
        <div class="snapshot-title">Datasets</div>
        <div class="snapshot-value">9</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class="snapshot-card">
        <div class="snapshot-title">Scope</div>
        <div class="snapshot-value" style="font-size:1.28rem;">Energy · Finance · Environment</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Feature grid
# -----------------------------
st.markdown('<div class="section-heading">What this dashboard enables</div>', unsafe_allow_html=True)

fleft, fright = st.columns(2)

with fleft:
    st.markdown("""
    <div class="feature-box-left">
        <div class="feature-title">Solar Simulation</div>
        <div class="feature-text">
            Explore how tilt, azimuth, system size, and scenario conditions affect production outcomes.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box-left">
        <div class="feature-title">Financial Analysis</div>
        <div class="feature-text">
            Translate energy output into savings, payback, and project value using real pricing and cost context.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box-left">
        <div class="feature-title">Environmental Impact</div>
        <div class="feature-text">
            Estimate avoided emissions, carbon value, and broader sustainability benefits for community projects.
        </div>
    </div>
    """, unsafe_allow_html=True)

with fright:
    st.markdown("""
    <div class="feature-box-right">
        <div class="feature-title">Weather & Seasonality Context</div>
        <div class="feature-text">
            Understand how climate patterns, cloud cover, and snow conditions influence solar performance in Edmonton.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box-right">
        <div class="feature-title">Real-Site Validation</div>
        <div class="feature-text">
            Compare project logic against observed production data from actual SPICE sites such as Bissell and Visser.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box-right">
        <div class="feature-title">Scenario Comparison</div>
        <div class="feature-text">
            Support decision making by comparing design alternatives and system configurations across simulated cases.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Stakeholders
# -----------------------------
st.markdown('<div class="section-heading">Who this supports</div>', unsafe_allow_html=True)

a, b, c = st.columns(3)

with a:
    st.markdown("""
    <div class="support-card">
        <div class="support-title">Customers</div>
        <div class="support-text">
            Helps building owners understand how solar systems may affect future energy savings and project feasibility.
        </div>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="support-card">
        <div class="support-title">Investors</div>
        <div class="support-text">
            Supports financial interpretation by linking production outcomes to savings, payback, and long-term value.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown("""
    <div class="support-card">
        <div class="support-title">Community Stakeholders</div>
        <div class="support-text">
            Communicates the environmental and social value of community-driven solar projects in a clear and accessible way.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Footer note
# -----------------------------
st.markdown("""
<div class="bottom-note">
    <strong>Next step:</strong> Use the sidebar to explore the methodology, simulation,
    financial, environmental, validation, and scenario analysis pages.
</div>
""", unsafe_allow_html=True)
