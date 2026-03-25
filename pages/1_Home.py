import streamlit as st

st.title("Home")
st.write("Sidebar page is working.")
import streamlit as st

st.set_page_config(page_title="SPICE Solar Impact Dashboard", layout="wide")

# -----------------------------
# Custom styling
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #F7F9F9;
}

.hero {
    background: linear-gradient(90deg, #1E6F5C, #0B3C5D);
    padding: 42px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    font-size: 19px;
    line-height: 1.6;
}

.section-card {
    background: white;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.kpi-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.08);
}

.kpi-title {
    color: #0B3C5D;
    font-size: 16px;
    font-weight: 600;
}

.kpi-value {
    color: #1E6F5C;
    font-size: 28px;
    font-weight: 800;
    margin-top: 8px;
}

.subheading {
    color: #1E6F5C;
    font-size: 15px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.big-heading {
    color: #0B3C5D;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header / Hero
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="subheading">CMPT 3835 · SPICE Project</div>
    <h1>SPICE Solar Impact Dashboard</h1>
    <p>
        A decision-support platform designed to help the Solar Power Investment Cooperative of Edmonton
        evaluate solar design choices, estimate energy production, analyze financial returns, and communicate
        environmental impact to stakeholders.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Problem + Client Need
# -----------------------------
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown("""
    <div class="section-card">
        <div class="subheading">Client Problem</div>
        <div class="big-heading">What SPICE needs</div>
        <p>
            SPICE needs a clear and interactive way to show how solar system design choices affect
            real-world outcomes. Stakeholders need more than raw technical outputs — they need a tool
            that translates system configuration into understandable value.
        </p>
        <p>
            This dashboard helps connect solar design decisions to:
        </p>
        <ul>
            <li>annual and monthly energy production</li>
            <li>financial savings and investment insights</li>
            <li>environmental and policy impact</li>
            <li>validation against real SPICE project data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="section-card">
        <div class="subheading">Dashboard Purpose</div>
        <div class="big-heading">Why this tool matters</div>
        <p>
            This app is designed as a hybrid solar analytics platform that combines simulation,
            machine learning, business analysis, and storytelling.
        </p>
        <p>
            It supports:
        </p>
        <ul>
            <li>customers exploring solar potential</li>
            <li>investors evaluating project returns</li>
            <li>policy and sustainability discussions</li>
            <li>SPICE communication and decision-making</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# KPI Row
# -----------------------------
st.markdown("### Project Highlights")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Datasets Used</div>
        <div class="kpi-value">9</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Core Focus</div>
        <div class="kpi-value">Energy + Finance</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Client Context</div>
        <div class="kpi-value">SPICE Edmonton</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Approach</div>
        <div class="kpi-value">Simulation + ML</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Navigation / What pages will show
# -----------------------------
st.markdown("### What this dashboard includes")

left, right = st.columns(2)

with left:
    st.markdown("""
    <div class="section-card">
        <div class="subheading">Analytical Pages</div>
        <ul>
            <li>Data and Methodology</li>
            <li>Solar Simulation</li>
            <li>Financial Impact</li>
            <li>Environmental Impact</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="section-card">
        <div class="subheading">Decision-Support Pages</div>
        <ul>
            <li>Weather and Seasonality</li>
            <li>Real Site Validation</li>
            <li>Scenario Explorer</li>
            <li>Model Insights / XAI</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Footer note
# -----------------------------
st.info(
    "This dashboard is being developed as a university-level decision-support tool for the SPICE project in CMPT 3835."
)
