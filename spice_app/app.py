import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="SPICE Solar Analytics Dashboard",
    page_icon="☀️",
    layout="wide"
)

# -----------------------------
# Helper function to load image
# -----------------------------
def load_image(path):
    if os.path.exists(path):
        return Image.open(path)
    return None

# -----------------------------
# Image paths
# Put these images in your project folder
# -----------------------------
banner_img = load_image("images/solar_banner.jpg")
img1 = load_image("images/panel1.jpg")
img2 = load_image("images/dashboard.jpg")
img3 = load_image("images/environment.jpg")

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .hero-box {
        background: linear-gradient(135deg, #0f172a, #1e3a8a);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
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
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Hero Section
# -----------------------------
col1, col2 = st.columns([1.4, 1])

with col1:
    st.markdown("""
        <div class="hero-box">
            <h1>SPICE Solar Analytics Dashboard</h1>
            <p style="font-size:18px;">
                A data-driven platform developed by <b>Team Data Alchemists</b> to analyze
                solar energy performance, financial return, and environmental impact.
            </p>
            <p style="font-size:16px;">
                This dashboard supports smarter solar investment decisions for Edmonton-based
                energy projects through interactive analytics, predictive modeling, and
                visual storytelling.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if banner_img:
        st.image(banner_img, use_container_width=True)
    else:
        st.info("Add a banner image at: images/solar_banner.jpg")

# -----------------------------
# Project Overview
# -----------------------------
st.markdown("## Project Overview")

col3, col4 = st.columns([1.1, 1])

with col3:
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

with col4:
    if img1:
        st.image(img1, use_container_width=True)
    else:
        st.info("Add image at: images/panel1.jpg")

# -----------------------------
# Key Highlights
# -----------------------------
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

# -----------------------------
# Visual Section
# -----------------------------
st.markdown("## Dashboard Vision")

col5, col6 = st.columns(2)

with col5:
    if img2:
        st.image(img2, caption="Solar dashboard and analytics interface", use_container_width=True)
    else:
        st.info("Add image at: images/dashboard.jpg")

with col6:
    if img3:
        st.image(img3, caption="Environmental and sustainability perspective", use_container_width=True)
    else:
        st.info("Add image at: images/environment.jpg")

# -----------------------------
# Team Section
# -----------------------------
st.markdown("## Team Data Alchemists")

st.markdown("""
<div class="section-card">
    <p class="small-text">
        This project is being developed by <b>Team Data Alchemists</b> as part of the SPICE
        Energy Conservation and Data Analytics initiative. The dashboard reflects an applied
        machine learning and analytics approach to solving real-world renewable energy challenges.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("SPICE Solar Analytics Dashboard | Developed by Team Data Alchemists")
