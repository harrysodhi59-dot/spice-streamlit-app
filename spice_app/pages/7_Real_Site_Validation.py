import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Insights & Recommendations", layout="wide")

# =========================
# PAGE STYLING
# =========================
st.markdown("""
<style>
.main-title {
    font-size: 2.2rem;
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
    font-size: 1.35rem;
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
    font-size: 1.7rem;
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
st.markdown('<div class="main-title">Page 7 — Insights & Recommendations</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">This page summarizes key findings from the uploaded solar dataset and provides practical recommendations for planning, optimization, and decision-making.</div>',
    unsafe_allow_html=True
)

# =========================
# LOAD DATA
# =========================
df = None

if "df" in st.session_state:
    df = st.session_state["df"]
elif "uploaded_data" in st.session_state:
    df = st.session_state["uploaded_data"]

if df is None:
    st.warning("No dataset found in session state. Please upload your dataset on the earlier pages first.")
    st.stop()

# Make a copy
df = df.copy()

# =========================
# COLUMN DETECTION HELPERS
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
date_col = find_column(["date", "time", "month", "year"])

# Convert likely numeric columns
for col in [generation_col, revenue_col, co2_col, tilt_col, azimuth_col, loss_col, size_col]:
    if col is not None:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# QUICK SUMMARY METRICS
# =========================
st.markdown('<div class="section-title">Project Summary</div>', unsafe_allow_html=True)

total_records = len(df)

avg_generation = df[generation_col].mean() if generation_col else np.nan
avg_revenue = df[revenue_col].mean() if revenue_col else np.nan
avg_co2 = df[co2_col].mean() if co2_col else np.nan

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_records:,}</div>
        <div class="metric-label">Total Records</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    value = f"{avg_generation:,.2f}" if not pd.isna(avg_generation) else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">Average Energy Output</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    value = f"${avg_revenue:,.2f}" if not pd.isna(avg_revenue) else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">Average Revenue</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    value = f"{avg_co2:,.2f}" if not pd.isna(avg_co2) else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">Average CO₂ Reduction</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# KEY OBSERVATIONS
# =========================
st.markdown('<div class="section-title">Key Observations</div>', unsafe_allow_html=True)

observations = []

if generation_col:
    max_gen = df[generation_col].max()
    min_gen = df[generation_col].min()
    observations.append(
        f"The dataset shows a wide variation in **{generation_col}**, ranging from **{min_gen:,.2f}** to **{max_gen:,.2f}**. This suggests that system performance is influenced by design and operating conditions."
    )

if revenue_col and generation_col:
    corr = df[[generation_col, revenue_col]].corr().iloc[0, 1]
    if not pd.isna(corr):
        observations.append(
            f"There is a measurable relationship between **energy output** and **revenue**, with a correlation of **{corr:.2f}**. This indicates that stronger production generally supports better financial return."
        )

if co2_col and generation_col:
    corr = df[[generation_col, co2_col]].corr().iloc[0, 1]
    if not pd.isna(corr):
        observations.append(
            f"The relationship between **energy generation** and **CO₂ reduction** is **{corr:.2f}**, showing that higher-performing systems also tend to deliver stronger environmental value."
        )

if loss_col:
    avg_loss = df[loss_col].mean()
    observations.append(
        f"The average system loss in the dataset is **{avg_loss:,.2f}**. Lowering avoidable losses could improve both technical performance and long-term project value."
    )

if tilt_col:
    observations.append(
        f"The **{tilt_col}** values suggest that panel angle should be treated as an important planning variable, since system tilt directly affects solar exposure and total output."
    )

if azimuth_col:
    observations.append(
        f"The **{azimuth_col}** field provides useful insight into orientation effects. This can help compare how different panel directions influence energy generation."
    )

if not observations:
    observations.append(
        "The uploaded dataset was loaded successfully, but the column names do not fully match the expected solar performance fields. You may rename columns or adjust the detection logic for more detailed insights."
    )

for obs in observations[:6]:
    st.markdown(f'<div class="info-card">{obs}</div>', unsafe_allow_html=True)

# =========================
# STRATEGIC RECOMMENDATIONS
# =========================
st.markdown('<div class="section-title">Strategic Recommendations</div>', unsafe_allow_html=True)

recommendations = []

if generation_col and revenue_col:
    recommendations.append("""
    <div class="recommend-box">
        <b>1. Prioritize high-performing system configurations</b><br>
        The team should identify which combinations of system size, tilt, orientation, and losses are associated with stronger energy output and revenue. These configurations can be highlighted in the dashboard for investors and decision-makers.
    </div>
    """)

if loss_col:
    recommendations.append("""
    <div class="recommend-box">
        <b>2. Reduce controllable system losses</b><br>
        Even small reductions in system losses may improve overall project performance. This can strengthen both operational efficiency and projected return on investment.
    </div>
    """)

if tilt_col or azimuth_col:
    recommendations.append("""
    <div class="recommend-box">
        <b>3. Use tilt and orientation as planning levers</b><br>
        Panel tilt and azimuth should be included in scenario analysis because they directly affect solar capture. A comparison view in the app can help users understand which setup provides better expected outcomes.
    </div>
    """)

if co2_col:
    recommendations.append("""
    <div class="recommend-box">
        <b>4. Communicate environmental value alongside financial return</b><br>
        Stakeholders may be more engaged when they can see both profitability and sustainability outcomes together. Showing CO₂ reduction next to revenue can make the dashboard more persuasive.
    </div>
    """)

recommendations.append("""
<div class="recommend-box">
    <b>5. Strengthen the app with predictive analytics</b><br>
    As the project grows, the next step should be adding machine learning models that estimate generation, revenue, and carbon savings based on system design inputs. This would turn the dashboard from descriptive to predictive.
</div>
""")

recommendations.append("""
<div class="recommend-box">
    <b>6. Support decision-making with interactive filtering</b><br>
    Users should be able to compare scenarios by changing key parameters such as system size, tilt, azimuth, and losses. This would make the application more practical for real project planning.
</div>
""")

for rec in recommendations:
    st.markdown(rec, unsafe_allow_html=True)

# =========================
# DATA QUALITY / NEXT STEPS
# =========================
st.markdown('<div class="section-title">Data Quality & Next Steps</div>', unsafe_allow_html=True)

missing_summary = df.isnull().sum()
missing_summary = missing_summary[missing_summary > 0].sort_values(ascending=False)

left, right = st.columns([1.15, 1])

with left:
    st.markdown("""
    <div class="info-card">
    <b>Recommended next steps for the Data Alchemists team:</b><br><br>
    • Improve column consistency and naming conventions across uploaded datasets.<br>
    • Handle missing values before advanced analytics or machine learning modeling.<br>
    • Add visual comparison tools for energy output, revenue, and CO₂ reduction.<br>
    • Introduce predictive models for investor-facing scenario planning.<br>
    • Expand the dashboard so it can clearly support both technical and non-technical stakeholders.
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown('<div class="info-card"><b>Missing Values Snapshot</b></div>', unsafe_allow_html=True)
    if len(missing_summary) > 0:
        missing_df = missing_summary.reset_index()
        missing_df.columns = ["Column", "Missing Values"]
        st.dataframe(missing_df, use_container_width=True, hide_index=True)
    else:
        st.success("No missing values were detected in the uploaded dataset.")

# =========================
# FINAL TAKEAWAY
# =========================
st.markdown('<div class="section-title">Final Takeaway</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-box">
    <h4 style="margin-top:0;">Why this page matters</h4>
    <p style="margin-bottom:0;">
        This page brings together the most important findings from the dataset and translates them into clear action points.
        Instead of only showing charts, it helps users understand what the results mean and what should be done next.
        For the SPICE project, this makes the application more useful, more professional, and more aligned with real decision-making.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="small-note">Developed by <b>Data Alchemists</b> for the SPICE Energy Conservation & Data Analytics Project.</p>',
    unsafe_allow_html=True
)
