import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Real Site Validation", layout="wide")

# =========================
# PAGE STYLING
# =========================
st.markdown("""
<style>
.main-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #16325B;
    margin-bottom: 0.2rem;
}
.sub-text {
    font-size: 1rem;
    color: #4F647A;
    margin-bottom: 1.5rem;
}
.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #16325B;
    margin-top: 1.2rem;
    margin-bottom: 0.8rem;
}
.info-card {
    background: linear-gradient(135deg, #F8FBFF, #EEF5FF);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #D7E6F5;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
    margin-bottom: 12px;
}
.metric-card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    text-align: center;
}
.metric-value {
    font-size: 1.6rem;
    font-weight: 800;
    color: #16325B;
}
.metric-label {
    font-size: 0.95rem;
    color: #5B6B7A;
}
.recommend-box {
    background: #F9FCFF;
    padding: 16px;
    border-left: 6px solid #2E8BC0;
    border-radius: 12px;
    margin-bottom: 14px;
    border: 1px solid #DCEAF5;
}
.footer-box {
    background: linear-gradient(135deg, #16325B, #2E8BC0);
    color: white;
    padding: 20px;
    border-radius: 18px;
    margin-top: 20px;
}
.small-note {
    color: #6B7280;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="main-title">Page 7 — Real Site Validation</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">This page validates uploaded solar project data and highlights performance, financial, and environmental insights for the SPICE project.</div>',
    unsafe_allow_html=True
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_csv_file(path):
    return pd.read_csv(path)

def load_data():
    # 1. session state
    if "df" in st.session_state and st.session_state["df"] is not None:
        return st.session_state["df"]

    if "uploaded_data" in st.session_state and st.session_state["uploaded_data"] is not None:
        return st.session_state["uploaded_data"]

    # 2. saved csv path from home page
    if "uploaded_file_path" in st.session_state:
        file_path = st.session_state["uploaded_file_path"]
        if os.path.exists(file_path):
            return load_csv_file(file_path)

    # 3. fallback common file names
    possible_files = [
        "data.csv",
        "dataset.csv",
        "solar_data.csv",
        "uploaded_dataset.csv"
    ]

    for file in possible_files:
        if os.path.exists(file):
            return load_csv_file(file)

    return None

df = load_data()

if df is None:
    st.warning("No dataset is currently available. Please upload your CSV on the Home page first.")
    st.info("Tip: after uploading the file on Home page, save it into session state using `st.session_state['df'] = df`.")
    st.stop()

df = df.copy()

# =========================
# HELPER FUNCTION
# =========================
def find_column(possible_names):
    for col in df.columns:
        clean_col = col.strip().lower()
        for name in possible_names:
            if name in clean_col:
                return col
    return None

generation_col = find_column(["generation", "energy", "output", "ac_output", "solar_output", "kwh"])
revenue_col = find_column(["revenue", "income", "profit", "earning"])
co2_col = find_column(["co2", "carbon", "emission"])
tilt_col = find_column(["tilt"])
azimuth_col = find_column(["azimuth", "orientation"])
loss_col = find_column(["loss"])
size_col = find_column(["system_size", "size", "capacity", "kw"])

# Convert numeric columns
for col in [generation_col, revenue_col, co2_col, tilt_col, azimuth_col, loss_col, size_col]:
    if col is not None:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# DATA PREVIEW
# =========================
st.markdown('<div class="section-title">Uploaded Dataset Overview</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{df.shape[0]:,}</div>
        <div class="metric-label">Rows</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{df.shape[1]:,}</div>
        <div class="metric-label">Columns</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{df.isnull().sum().sum():,}</div>
        <div class="metric-label">Total Missing Values</div>
    </div>
    """, unsafe_allow_html=True)

st.dataframe(df.head(10), use_container_width=True)

# =========================
# KEY METRICS
# =========================
st.markdown('<div class="section-title">Performance Summary</div>', unsafe_allow_html=True)

avg_generation = df[generation_col].mean() if generation_col else np.nan
avg_revenue = df[revenue_col].mean() if revenue_col else np.nan
avg_co2 = df[co2_col].mean() if co2_col else np.nan
avg_loss = df[loss_col].mean() if loss_col else np.nan

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_generation:,.2f}" if not pd.isna(avg_generation) else "N/A"}</div>
        <div class="metric-label">Average Energy Output</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    value = f"${avg_revenue:,.2f}" if not pd.isna(avg_revenue) else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">Average Revenue</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    value = f"{avg_co2:,.2f}" if not pd.isna(avg_co2) else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">Average CO₂ Reduction</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    value = f"{avg_loss:,.2f}" if not pd.isna(avg_loss) else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">Average System Loss</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# OBSERVATIONS
# =========================
st.markdown('<div class="section-title">Validation Insights</div>', unsafe_allow_html=True)

insights = []

if generation_col:
    insights.append(f"The dataset includes **{generation_col}**, which helps validate solar production performance across uploaded records.")

if revenue_col:
    insights.append(f"The **{revenue_col}** column supports financial validation and allows comparison between energy generation and expected return.")

if co2_col:
    insights.append(f"The **{co2_col}** field is useful for evaluating environmental benefit and sustainability impact.")

if tilt_col or azimuth_col:
    insights.append("Panel tilt and orientation values are available, which helps validate whether system design factors are influencing performance.")

if loss_col:
    insights.append("System loss information is available, which can support operational analysis and optimization planning.")

if not insights:
    insights.append("The dataset was loaded successfully, but the expected solar-related columns were not clearly detected. You may need to rename the columns for better analysis.")

for item in insights:
    st.markdown(f'<div class="info-card">{item}</div>', unsafe_allow_html=True)

# =========================
# RECOMMENDATIONS
# =========================
st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)

st.markdown("""
<div class="recommend-box">
<b>1. Standardize uploaded data structure</b><br>
Keep column names consistent across all uploaded solar datasets so that every page in the Streamlit app works smoothly.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="recommend-box">
<b>2. Save uploaded dataset in session state</b><br>
The Home page should store the dataframe using <code>st.session_state['df'] = df</code> right after upload so all pages can access it.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="recommend-box">
<b>3. Improve validation with real-world filters</b><br>
Add filters for site, season, system size, tilt, and azimuth so users can compare results more clearly.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="recommend-box">
<b>4. Use this page as a final decision-support layer</b><br>
This page should connect technical findings with business value, showing why the dataset matters for planning and investment decisions.
</div>
""", unsafe_allow_html=True)

# =========================
# FINAL TAKEAWAY
# =========================
st.markdown('<div class="section-title">Final Takeaway</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-box">
    <h4 style="margin-top:0;">Data Alchemists - SPICE Project</h4>
    <p style="margin-bottom:0;">
        This page confirms whether the uploaded dataset is usable for analysis and helps translate raw solar records into meaningful project insights.
        With correct file handling and consistent session state management, this section becomes a strong final validation page in the application.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="small-note">Developed by <b>Data Alchemists</b> for SPICE Energy Conservation & Data Analytics Project.</p>',
    unsafe_allow_html=True
)
