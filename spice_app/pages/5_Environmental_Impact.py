import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Environmental Impact",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# Styling
# -----------------------------
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

.hero {
    background: linear-gradient(90deg, #1E6F5C, #0B3C5D);
    padding: 2.5rem;
    border-radius: 22px;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 16px 36px rgba(0,0,0,0.14);
}

.hero h1 {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.6rem;
}

.hero p {
    font-size: 1.05rem;
    line-height: 1.7;
    max-width: 900px;
}

.card {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 10px 26px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}

.kpi-card {
    background: white;
    border-radius: 18px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
}

.kpi-title {
    color: #0B3C5D;
    font-size: 0.95rem;
    font-weight: 700;
}

.kpi-value {
    color: #1E6F5C;
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 0.35rem;
}

.section-title {
    color: #0B3C5D;
    font-size: 1.55rem;
    font-weight: 800;
    margin-top: 0.6rem;
    margin-bottom: 0.8rem;
}

.sub-label {
    color: #1E6F5C;
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
}

.highlight-box {
    background: #F7F9F9;
    border-left: 6px solid #FDB813;
    padding: 1rem 1rem 1rem 1.1rem;
    border-radius: 12px;
    margin-bottom: 0.8rem;
}

.footer-note {
    background: #EEF5F3;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    color: #234;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load datasets
# -----------------------------
@st.cache_data
def load_emissions():
    return pd.read_csv("data/alberta_grid_emission_factors.csv")

@st.cache_data
def load_carbon():
    return pd.read_csv("data/federal_carbon_pricing.csv")

try:
    emissions_df = load_emissions()
    carbon_df = load_carbon()
except Exception as e:
    st.error(f"Could not load environmental datasets: {e}")
    st.stop()

emissions_df.columns = [str(c).strip() for c in emissions_df.columns]
carbon_df.columns = [str(c).strip() for c in carbon_df.columns]

# -----------------------------
# Required column names
# -----------------------------
required_emissions_cols = ["Year", "Grid_Intensity_kg_CO2e_per_kWh"]
required_carbon_cols = ["Year", "Carbon_Tax_CAD_per_tonne"]

missing_emissions = [c for c in required_emissions_cols if c not in emissions_df.columns]
missing_carbon = [c for c in required_carbon_cols if c not in carbon_df.columns]

if missing_emissions:
    st.error(f"Missing columns in alberta_grid_emission_factors.csv: {missing_emissions}")
    st.write("Columns found:", list(emissions_df.columns))
    st.stop()

if missing_carbon:
    st.error(f"Missing columns in federal_carbon_pricing.csv: {missing_carbon}")
    st.write("Columns found:", list(carbon_df.columns))
    st.stop()

# -----------------------------
# Hero
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="sub-label">Sustainability & Policy Value</div>
    <h1>Environmental Impact</h1>
    <p>
        This page translates solar generation into avoided emissions, carbon value,
        and broader sustainability meaning. It helps connect project performance
        with environmental outcomes that are relevant to SPICE, community stakeholders,
        and climate-focused decision-making.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Environmental Controls")

annual_energy = st.sidebar.number_input(
    "Estimated Annual Energy (kWh)",
    min_value=1000.0,
    max_value=500000.0,
    value=22800.0,
    step=500.0
)

available_years = sorted(emissions_df["Year"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Select Emissions Year", available_years, index=len(available_years)-1)

carbon_years = sorted(carbon_df["Year"].dropna().unique().tolist())
selected_carbon_year = st.sidebar.selectbox("Select Carbon Pricing Year", carbon_years, index=min(len(carbon_years)-1, carbon_years.index(selected_year) if selected_year in carbon_years else len(carbon_years)-1))

# -----------------------------
# Calculations
# -----------------------------
emissions_row = emissions_df[emissions_df["Year"] == selected_year].iloc[0]
carbon_row = carbon_df[carbon_df["Year"] == selected_carbon_year].iloc[0]

emission_factor = emissions_row["Grid_Intensity_kg_CO2e_per_kWh"]      # kg CO2e / kWh
carbon_price = carbon_row["Carbon_Tax_CAD_per_tonne"]                  # CAD / tonne

co2_kg = annual_energy * emission_factor
co2_tonnes = co2_kg / 1000
carbon_value = co2_tonnes * carbon_price

# Simple storytelling equivalents
trees_equivalent = co2_tonnes * 40
cars_removed_equivalent = co2_tonnes / 4.6 if co2_tonnes > 0 else 0
homes_powered_equivalent = annual_energy / 10000

# -----------------------------
# KPI row
# -----------------------------
st.markdown("## Environmental Summary")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Grid Emissions Factor</div>
        <div class="kpi-value">{emission_factor:.2f} kg/kWh</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Avoided Emissions</div>
        <div class="kpi-value">{co2_tonnes:,.2f} t</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Carbon Price</div>
        <div class="kpi-value">${carbon_price:,.0f}/t</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Carbon Value</div>
        <div class="kpi-value">${carbon_value:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Interpretation cards
# -----------------------------
left, right = st.columns(2)

with left:
    st.markdown(f"""
    <div class="card">
        <div class="sub-label">Impact Interpretation</div>
        <div class="section-title">What the emissions estimate means</div>
        <p>
            Based on an annual solar output of <strong>{annual_energy:,.0f} kWh</strong>,
            the system is estimated to avoid approximately
            <strong>{co2_tonnes:,.2f} tonnes of CO₂e</strong> using the selected Alberta
            grid emissions factor for <strong>{selected_year}</strong>.
        </p>
        <p>
            This provides a practical sustainability measure that can support project
            communication, environmental reporting, and stakeholder engagement.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="card">
        <div class="sub-label">Policy Interpretation</div>
        <div class="section-title">What the carbon value means</div>
        <p>
            Using the selected carbon price for <strong>{selected_carbon_year}</strong>,
            the avoided emissions correspond to an estimated carbon value of
            <strong>${carbon_value:,.0f}</strong>.
        </p>
        <p>
            This value does not always translate directly into cash flow, but it does
            express the policy and environmental significance of emissions avoided through
            solar generation.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Equivalents
# -----------------------------
st.markdown("## Real-world equivalents")

e1, e2, e3 = st.columns(3)

with e1:
    st.markdown(f"""
    <div class="highlight-box">
        <strong>Trees Equivalent</strong><br>
        Approximately <strong>{trees_equivalent:,.0f}</strong> trees worth of annual carbon benefit.
    </div>
    """, unsafe_allow_html=True)

with e2:
    st.markdown(f"""
    <div class="highlight-box">
        <strong>Cars Removed Equivalent</strong><br>
        Roughly equal to taking <strong>{cars_removed_equivalent:,.1f}</strong> cars off the road for one year.
    </div>
    """, unsafe_allow_html=True)

with e3:
    st.markdown(f"""
    <div class="highlight-box">
        <strong>Homes Powered Reference</strong><br>
        Equivalent to about <strong>{homes_powered_equivalent:,.1f}</strong> average-home annual electricity demand references.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Charts
# -----------------------------
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Emissions Context</div>
        <div class="section-title">Alberta Grid Emissions Intensity by Year</div>
    """, unsafe_allow_html=True)

    fig_emissions = px.line(
        emissions_df,
        x="Year",
        y="Grid_Intensity_kg_CO2e_per_kWh",
        markers=True
    )
    fig_emissions.update_layout(
        xaxis_title="Year",
        yaxis_title="Grid Intensity (kg CO2e per kWh)",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_emissions, use_container_width=True)

    st.markdown("""
        <p>
            This trend shows how Alberta’s grid emissions intensity changes over time.
            Lower values indicate a cleaner grid, which can affect the carbon reduction
            associated with solar generation.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <div class="sub-label">Policy Context</div>
        <div class="section-title">Federal Carbon Price by Year</div>
    """, unsafe_allow_html=True)

    fig_carbon = px.bar(
        carbon_df,
        x="Year",
        y="Carbon_Tax_CAD_per_tonne"
    )
    fig_carbon.update_layout(
        xaxis_title="Year",
        yaxis_title="Carbon Price (CAD per tonne)",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_carbon, use_container_width=True)

    st.markdown("""
        <p>
            The carbon price provides a policy-based way to estimate the economic value
            of avoided emissions. As the carbon price rises, the environmental value of
            clean generation becomes more significant.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Combined comparison chart
# -----------------------------
st.markdown("## Impact summary")

impact_df = pd.DataFrame({
    "Metric": ["Avoided Emissions (tonnes)", "Carbon Value (CAD)"],
    "Value": [co2_tonnes, carbon_value]
})

st.markdown("""
<div class="card">
    <div class="sub-label">Selected Case</div>
    <div class="section-title">Environmental Benefit Snapshot</div>
""", unsafe_allow_html=True)

fig_summary = px.bar(
    impact_df,
    x="Metric",
    y="Value",
    color="Metric"
)
fig_summary.update_layout(
    xaxis_title="Metric",
    yaxis_title="Value",
    plot_bgcolor="white",
    showlegend=False
)
st.plotly_chart(fig_summary, use_container_width=True)

st.markdown("""
    <p>
        This summary view brings together the physical and policy-based dimensions
        of environmental performance for the selected annual energy output.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Data preview
# -----------------------------
st.markdown("## Environmental data preview")

preview_choice = st.radio(
    "Choose dataset preview",
    ["Grid Emission Factors", "Carbon Pricing"],
    horizontal=True
)

if preview_choice == "Grid Emission Factors":
    st.dataframe(emissions_df, use_container_width=True)
else:
    st.dataframe(carbon_df, use_container_width=True)

st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Weather & Seasonality page to explore
    how Edmonton weather conditions shape solar performance over time.
</div>
""", unsafe_allow_html=True)
