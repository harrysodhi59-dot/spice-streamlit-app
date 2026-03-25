import streamlit as st

st.set_page_config(
    page_title="SPICE Solar Impact Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.hero {
    background: linear-gradient(90deg, #1E6F5C, #0B3C5D);
    padding: 2.5rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 1.5rem;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.hero p {
    font-size: 1.1rem;
    line-height: 1.7;
    margin-bottom: 0;
}

.info-card {
    background: white;
    border-radius: 18px;
    padding: 1.4rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>SPICE Solar Impact Dashboard</h1>
    <p>
        A university-level solar analytics and decision-support platform for the
        Solar Power Investment Cooperative of Edmonton (SPICE).
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <h3>Welcome</h3>
    <p>
        Use the sidebar to explore the dashboard pages, including methodology,
        solar simulation, financial impact, environmental analysis, weather context,
        validation with real sites, and scenario comparison.
    </p>
</div>
""", unsafe_allow_html=True)

st.success("Open the sidebar to begin with the Home page.")
