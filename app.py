import streamlit as st
import base64
from pathlib import Path

import streamlit as st
st.title("TESTING CURRENT FILE")
st.stop()

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
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.section-card {
    background-color: white;
    padding: 1.2rem;
    border-radius: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}

.feature-card {
    background-color: white;
    padding: 1rem;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
    min-height: 180px;
}

.small-text {
    color: #475569;
    font-size: 16px;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)

if banner_base64:
    st.markdown(
        f"""
        <div style="
            position: relative;
            border-radius: 24px;
            overflow: hidden;
            margin-bottom: 1.5rem;
            min-height: 320px;
            box-shadow: 0 16px 36px rgba(0,0,0,0.18);
            background-image:
                linear-gradient(90deg, rgba(11,60,93,0.88) 0%, rgba(30,111,92,0.78) 55%, rgba(11,60,93,0.52) 100%),
                url('data:image/png;base64,{banner_base64}');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
        ">
            <div style="padding: 2.8rem 3rem; max-width: 760px; color: white;">
                <div style="
                    display: inline-block;
                    background: rgba(255,255,255,0.16);
                    padding: 0.45rem 0.85rem;
                    border-radius: 999px;
                    font-size: 0.85rem;
                    font-weight: 700;
                    margin-bottom: 1rem;
                    letter-spacing: 0.4px;
                ">
                    NORQUEST COLLEGE • TEAM DATA ALCHEMISTS
                </div>
                <h1 style="
                    font-size: 3rem;
                    font-weight: 800;
                    margin-bottom: 0.75rem;
                    line-height: 1.15;
                ">
                    SPICE Solar Analytics Dashboard
                </h1>
                <p style="
                    font-size: 1.08rem;
                    line-height: 1.75;
                    margin-bottom: 0;
                    max-width: 700px;
                ">
                    A data-driven platform developed by Team Data Alchemists to analyze solar energy
                    performance, financial return, and environmental impact.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.error("Banner image not found. Make sure this file exists: images/norquest_banner.png")

st.markdown("## Project Overview")

col1, col2 = st.columns([1.1, 1])

with col1:
    st.markdown("""
        <div class="section-card">
            <h3>About the Project</h3>
            <p class="small-text">
                The SPICE Solar Analytics Dashboard is designed to help users understand how
                different solar system configurations affect energy generation, revenue, and
                carbon reduction. It transforms raw data into meaningful insights that can
                support investors, stakeholders, and decision-makers.
            </p>
            <p class="small-text">
                The project combines exploratory data analysis, system performance metrics,
                financial indicators, and sustainability-focused reporting in one unified platform.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="section-card">
            <h3>Institutional Context</h3>
            <p class="small-text">
                This dashboard is being developed at NorQuest College as part of the SPICE
                Energy Conservation and Data Analytics initiative, with a focus on practical
                machine learning, simulation, and stakeholder communication.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("## Key Highlights")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
        <div class="feature-card">
            <h4>Energy Analytics</h4>
            <p class="small-text">
                Explore solar output, generation trends, and performance behaviour across
                different system settings.
            </p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="feature-card">
            <h4>Financial Insights</h4>
            <p class="small-text">
                Evaluate estimated revenue, cost efficiency, and investment-related indicators
                using interactive visuals.
            </p>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
        <div class="feature-card">
            <h4>Environmental Impact</h4>
            <p class="small-text">
                Understand how solar adoption contributes to carbon reduction and supports
                sustainability goals.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("## Team Data Alchemists")

st.markdown("""
<div class="section-card">
    <p class="small-text">
        This project is being developed by Team Data Alchemists as part of the SPICE
        Energy Conservation and Data Analytics initiative. The dashboard reflects an
        applied machine learning and analytics approach to solving real-world renewable
        energy challenges.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("SPICE Solar Analytics Dashboard | Developed by Team Data Alchemists")
