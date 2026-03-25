import streamlit as st
import pandas as pd
import numpy as np
import os
import streamlit as st
import pandas as pd
import io

def shared_uploader():
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"], key="shared_csv_uploader")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state["df"] = df
        st.session_state["uploaded_data"] = df
        st.session_state["uploaded_file_bytes"] = uploaded_file.getvalue()
        st.session_state["uploaded_file_name"] = uploaded_file.name

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
import streamlit as st
import pandas as pd
import io

def load_data():
    if "df" in st.session_state and st.session_state["df"] is not None:
        return st.session_state["df"]

    if "uploaded_data" in st.session_state and st.session_state["uploaded_data"] is not None:
        return st.session_state["uploaded_data"]

    if "uploaded_file_bytes" in st.session_state:
        try:
            return pd.read_csv(io.BytesIO(st.session_state["uploaded_file_bytes"]))
        except Exception:
            return None

    return None

df = load_data()

if df is None:
    st.warning("No dataset is currently available. Please upload your CSV on the Home page first.")
    st.info("Tip: upload on Home page, then open this page in the same app session.")
    st.write("Current session keys:", list(st.session_state.keys()))
    st.stop()

def load_data():
    if "df" in st.session_state and st.session_state["df"] is not None:
        return st.session_state["df"]

    if "uploaded_data" in st.session_state and st.session_state["uploaded_data"] is not None:
        return st.session_state["uploaded_data"]

    if "uploaded_file_path" in st.session_state:
        file_path = st.session_state["uploaded_file_path"]
        if os.path.exists(file_path):
            return load_csv_file(file_path)

    possible_files = [
        "uploaded_dataset.csv",
        "data.csv",
        "dataset.csv",
        "solar_data.csv"
    ]

    for file in possible_files:
        if os.path.exists(file):
            return load_csv_file(file)

    return None

df = load_data()

if df is None:
    st.warning("No dataset is currently available. Please upload your CSV on the Home page first.")
    st.info("Tip: save uploaded data using st.session_state['df'] = df on the Home page.")
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

for col in [generation_col, revenue_col, co2_col, tilt_col, azimuth_col, loss_col, size_col]:
    if col is not None:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# DATASET OVERVIEW
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
# PERFORMANCE SUMMARY
# =========================
st.markdown('<div class="section-title">Performance Summary</div>', unsafe_allow_html=True)

avg_generation = df[generation_col].mean() if generation_col else np.nan
avg_revenue = df[revenue_col].mean() if revenue_col else np.nan
avg_co2 = df[co2_col].mean() if co2_col else np.nan
avg_loss = df[loss_col].mean() if loss_col else np.nan

gen_value = f"{avg_generation:,.2f}" if not pd.isna(avg_generation) else "N/A"
rev_value = f"${avg_revenue:,.2f}" if not pd.isna(avg_revenue) else "N/A"
co2_value = f"{avg_co2:,.2f}" if not pd.isna(avg_co2) else "N/A"
loss_value = f"{avg_loss:,.2f}" if not pd.isna(avg_loss) else "N/A"

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{gen_value}</div>
        <div class="metric-label">Average Energy Output</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{rev_value}</div>
        <div class="metric-label">Average Revenue</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{co2_value}</div>
        <div class="metric-label">Average CO₂ Reduction</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{loss_value}</div>
        <div class="metric-label">Average System Loss</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# VALIDATION INSIGHTS
# =========================
st.markdown('<div class="section-title">Validation Insights</div>', unsafe_allow_html=True)

insights = []

if generation_col:
    min_gen = df[generation_col].min()
    max_gen = df[generation_col].max()
    insights.append(
        f"The dataset includes <b>{generation_col}</b>, with values ranging from <b>{min_gen:,.2f}</b> to <b>{max_gen:,.2f}</b>. This helps validate solar production performance."
    )

if revenue_col:
    insights.append(
        f"The <b>{revenue_col}</b> column supports financial validation and helps compare system performance with expected economic return."
    )

if co2_col:
    insights.append(
        f"The <b>{co2_col}</b> field is useful for assessing environmental benefit and carbon reduction impact."
    )

if tilt_col or azimuth_col:
    insights.append(
        "Panel tilt and orientation data are available, which helps validate whether system design choices are affecting output."
    )

if loss_col:
    insights.append(
        "System loss information is present, which is useful for operational analysis and future optimization."
    )

if generation_col and revenue_col:
    corr = df[[generation_col, revenue_col]].corr().iloc[0, 1]
    if not pd.isna(corr):
        insights.append(
            f"The correlation between energy output and revenue is <b>{corr:.2f}</b>, which gives a useful signal for business-side validation."
        )

if not insights:
    insights.append(
        "The dataset loaded successfully, but expected solar-related columns were not clearly detected. You may need to rename columns for stronger analysis."
    )

for item in insights:
    st.markdown(f'<div class="info-card">{item}</div>', unsafe_allow_html=True)

# =========================
# MISSING VALUES
# =========================
st.markdown('<div class="section-title">Data Quality Check</div>', unsafe_allow_html=True)

missing_summary = df.isnull().sum()
missing_summary = missing_summary[missing_summary > 0].sort_values(ascending=False)

left, right = st.columns([1.2, 1])

with left:
    st.markdown("""
    <div class="info-card">
    <b>Why this validation matters:</b><br><br>
    This page checks whether the uploaded dataset is clean enough and complete enough to support real analysis.
    It also helps confirm whether the data can be used for performance tracking, financial estimation, and environmental reporting.
    </div>
    """, unsafe_allow_html=True)

with right:
    if len(missing_summary) > 0:
        missing_df = missing_summary.reset_index()
        missing_df.columns = ["Column", "Missing Values"]
        st.dataframe(missing_df, use_container_width=True, hide_index=True)
    else:
        st.success("No missing values were detected in the uploaded dataset.")

# =========================
# RECOMMENDATIONS
# =========================
st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)

st.markdown("""
<div class="recommend-box">
<b>1. Standardize uploaded data structure</b><br>
Keep column names consistent across all uploaded solar datasets so every page in the Streamlit app can read and analyze the file properly.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="recommend-box">
<b>2. Save uploaded dataset in session state</b><br>
On the Home page, store the uploaded dataframe using <code>st.session_state['df'] = df</code> so this page can access it directly.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="recommend-box">
<b>3. Add stronger validation filters</b><br>
Introduce filters for site, season, tilt, azimuth, system size, and losses so users can compare real-world solar scenarios more clearly.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="recommend-box">
<b>4. Connect technical results with business value</b><br>
This page should not only validate the dataset, but also explain why the data matters for decision-making, planning, and investor communication.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="recommend-box">
<b>5. Prepare for predictive modeling</b><br>
Once the dataset structure is stable, this validation page can support the next phase of the project by feeding clean data into machine learning models.
</div>
""", unsafe_allow_html=True)

# =========================
# FINAL TAKEAWAY
# =========================
st.markdown('<div class="section-title">Final Takeaway</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-box">
    <h4 style="margin-top:0;">Data Alchemists — SPICE Project</h4>
    <p style="margin-bottom:0;">
        This page confirms whether the uploaded dataset is usable for analysis and helps translate raw solar records into meaningful project insights.
        With proper file handling and consistent session state management, this becomes a strong final validation page in the application.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="small-note">Developed by <b>Data Alchemists</b> for the SPICE Energy Conservation & Data Analytics Project.</p>',
    unsafe_allow_html=True
)
