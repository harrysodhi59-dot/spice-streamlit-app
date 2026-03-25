import streamlit as st

st.set_page_config(page_title="Data & Methodology", layout="wide")

st.title("Data & Methodology")

st.markdown("""
## Project Overview

This dashboard is built for the Solar Power Investment Cooperative of Edmonton (SPICE) to
analyze solar energy production, financial returns, and environmental impact.

The system combines simulation, real-world data, and analytical modeling to support
decision-making.
""")

# -------------------------
# DATASETS SECTION
# -------------------------

st.header("Datasets Used")

st.markdown("""
This project integrates multiple datasets to represent real-world solar conditions:

- **PV Simulation Data (sample_250000)**  
  Used to understand relationships between solar inputs and energy output.

- **Weather Data (Edmonton)**  
  Includes temperature, irradiance, cloud cover, and snow depth.

- **Electricity Rates (EPCOR)**  
  Used for financial savings calculations.

- **Carbon Pricing & Emissions**  
  Used to estimate environmental impact and carbon value.

- **SPICE Project Cost Data**  
  Provides real-world financial benchmarks.

- **Real Site Data (Bissell & Visser)**  
  Used for validation against actual solar production.

- **Simulated Monthly Data (St. Augustine)**  
  Used for scenario comparison and system design analysis.
""")

# -------------------------
# PIPELINE
# -------------------------

st.header("System Architecture")

st.markdown("""
The application follows a multi-layer pipeline:

1. **Simulation Layer (PVGIS-style logic)**  
   Models solar production based on tilt, azimuth, and system size.

2. **Data Processing Layer**  
   Integrates weather, seasonal patterns, and system parameters.

3. **Analytical Layer**  
   Converts energy output into financial and environmental metrics.

4. **Visualization Layer (Streamlit Dashboard)**  
   Presents results in an interactive and user-friendly format.
""")

# -------------------------
# KEY IDEA
# -------------------------

st.header("Key Insight")

st.markdown("""
This project is not just about predicting solar energy output.

It focuses on translating solar design decisions into real-world value:

- Energy production (kWh)
- Financial savings (CAD)
- Environmental impact (CO₂ reduction)

This makes the system useful for:
- Customers
- Investors
- Policy stakeholders
- SPICE decision-makers
""")

# -------------------------
# NOTE
# -------------------------

st.info("This page explains how the dashboard is built and why it is relevant for SPICE.")
