import streamlit as st
import pandas as pd
import numpy as np
import io
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Predictive Modeling", layout="wide")

# =========================
# SHARED SIDEBAR UPLOADER
# =========================
def shared_uploader():
    st.sidebar.markdown("### Dataset Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV",
        type=["csv"],
        key="global_uploader_page8"
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state["df"] = df
        st.session_state["uploaded_data"] = df
        st.session_state["uploaded_file_bytes"] = uploaded_file.getvalue()
        st.session_state["uploaded_file_name"] = uploaded_file.name
        st.sidebar.success("Dataset Loaded ✅")
        return df

    return None

uploaded_df = shared_uploader()

# =========================
# LOAD DATA
# =========================
def load_data():
    if uploaded_df is not None:
        return uploaded_df

    if "df" in st.session_state and st.session_state["df"] is not None:
        return st.session_state["df"]

    if "uploaded_data" in st.session_state and st.session_state["uploaded_data"] is not None:
        return st.session_state["uploaded_data"]

    if "uploaded_file_bytes" in st.session_state:
        try:
            return pd.read_csv(io.BytesIO(st.session_state["uploaded_file_bytes"]))
        except Exception:
            pass

    return None

df = load_data()

# =========================
# STYLING
# =========================
st.markdown("""
<style>
.main-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #16325B;
    margin-bottom: 0.2rem;
}
.sub-text {
    font-size: 1.05rem;
    color: #4F647A;
    margin-bottom: 1.5rem;
}
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #16325B;
    margin-top: 1.4rem;
    margin-bottom: 0.8rem;
}
.metric-card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
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
.info-card {
    background: linear-gradient(135deg, #F8FBFF, #EEF5FF);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #D7E6F5;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    margin-bottom: 12px;
}
.footer-box {
    background: linear-gradient(135deg, #16325B, #2E8BC0);
    color: white;
    padding: 22px;
    border-radius: 18px;
    margin-top: 18px;
}
.small-note {
    color: #6B7280;
    font-size: 0.9rem;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="main-title">Page 8 — Predictive Modeling</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">This page uses a simple machine learning model to estimate solar energy output, revenue, and CO₂ reduction based on system design inputs.</div>',
    unsafe_allow_html=True
)

if df is None:
    st.warning("No dataset is currently available. Upload your CSV using the sidebar uploader.")
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
size_col = find_column(["system_size", "capacity", "kw", "size"])

required_features = [size_col, tilt_col, azimuth_col, loss_col]

# Convert numeric columns
for col in [generation_col, revenue_col, co2_col, tilt_col, azimuth_col, loss_col, size_col]:
    if col is not None:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# MODEL READINESS CHECK
# =========================
st.markdown('<div class="section-title">Model Readiness Check</div>', unsafe_allow_html=True)

missing_requirements = []
if size_col is None:
    missing_requirements.append("system size / capacity")
if tilt_col is None:
    missing_requirements.append("tilt")
if azimuth_col is None:
    missing_requirements.append("azimuth / orientation")
if loss_col is None:
    missing_requirements.append("loss")
if generation_col is None:
    missing_requirements.append("energy output / generation target")

if missing_requirements:
    st.error("This dataset is missing some columns needed for predictive modeling.")
    st.write("Missing:", ", ".join(missing_requirements))
    st.info("Use a dataset that includes system size, tilt, azimuth, loss, and energy output.")
    st.stop()

model_df = df[[size_col, tilt_col, azimuth_col, loss_col, generation_col]].dropna()

if len(model_df) < 10:
    st.warning("There are not enough clean rows to train the model properly. Try a larger dataset.")
    st.stop()

st.success("The dataset has the required columns for a simple prediction model.")

# =========================
# TRAIN MODEL
# =========================
X = model_df[[size_col, tilt_col, azimuth_col, loss_col]]
y = model_df[generation_col]

model = LinearRegression()
model.fit(X, y)

r2_score = model.score(X, y)

# Revenue and CO2 simple rates
revenue_rate = None
co2_rate = None

if revenue_col is not None:
    temp_rev = df[[generation_col, revenue_col]].dropna()
    if len(temp_rev) > 0 and temp_rev[generation_col].sum() != 0:
        revenue_rate = temp_rev[revenue_col].sum() / temp_rev[generation_col].sum()

if co2_col is not None:
    temp_co2 = df[[generation_col, co2_col]].dropna()
    if len(temp_co2) > 0 and temp_co2[generation_col].sum() != 0:
        co2_rate = temp_co2[co2_col].sum() / temp_co2[generation_col].sum()

# =========================
# MODEL SUMMARY
# =========================
st.markdown('<div class="section-title">Model Summary</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(model_df):,}</div>
        <div class="metric-label">Training Rows</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{r2_score:.2f}</div>
        <div class="metric-label">Model R² Score</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    target_name = generation_col if generation_col else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{target_name}</div>
        <div class="metric-label">Prediction Target</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# USER INPUTS
# =========================
st.markdown('<div class="section-title">Scenario Input</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

size_min = float(model_df[size_col].min())
size_max = float(model_df[size_col].max())
size_mean = float(model_df[size_col].mean())

tilt_min = float(model_df[tilt_col].min())
tilt_max = float(model_df[tilt_col].max())
tilt_mean = float(model_df[tilt_col].mean())

azimuth_min = float(model_df[azimuth_col].min())
azimuth_max = float(model_df[azimuth_col].max())
azimuth_mean = float(model_df[azimuth_col].mean())

loss_min = float(model_df[loss_col].min())
loss_max = float(model_df[loss_col].max())
loss_mean = float(model_df[loss_col].mean())

with c1:
    user_size = st.number_input("System Size", min_value=size_min, max_value=size_max, value=size_mean)
    user_tilt = st.number_input("Tilt", min_value=tilt_min, max_value=tilt_max, value=tilt_mean)

with c2:
    user_azimuth = st.number_input("Azimuth / Orientation", min_value=azimuth_min, max_value=azimuth_max, value=azimuth_mean)
    user_loss = st.number_input("System Loss", min_value=loss_min, max_value=loss_max, value=loss_mean)

# =========================
# PREDICTION
# =========================
st.markdown('<div class="section-title">Prediction Results</div>', unsafe_allow_html=True)

input_df = pd.DataFrame({
    size_col: [user_size],
    tilt_col: [user_tilt],
    azimuth_col: [user_azimuth],
    loss_col: [user_loss]
})

predicted_generation = float(model.predict(input_df)[0])

predicted_revenue = predicted_generation * revenue_rate if revenue_rate is not None else None
predicted_co2 = predicted_generation * co2_rate if co2_rate is not None else None

p1, p2, p3 = st.columns(3)

gen_text = f"{predicted_generation:,.2f}"
rev_text = f"${predicted_revenue:,.2f}" if predicted_revenue is not None else "N/A"
co2_text = f"{predicted_co2:,.2f}" if predicted_co2 is not None else "N/A"

with p1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{gen_text}</div>
        <div class="metric-label">Predicted Energy Output</div>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{rev_text}</div>
        <div class="metric-label">Estimated Revenue</div>
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{co2_text}</div>
        <div class="metric-label">Estimated CO₂ Reduction</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# INTERPRETATION
# =========================
st.markdown('<div class="section-title">Business Interpretation</div>', unsafe_allow_html=True)

insights = []

insights.append(
    f"For the selected configuration, the model predicts an energy output of <b>{predicted_generation:,.2f}</b>."
)

if predicted_revenue is not None:
    insights.append(
        f"Based on the dataset pattern, this scenario may generate an estimated revenue of <b>${predicted_revenue:,.2f}</b>."
    )

if predicted_co2 is not None:
    insights.append(
        f"The same configuration may also contribute an estimated <b>{predicted_co2:,.2f}</b> in CO₂ reduction."
    )

if r2_score >= 0.8:
    insights.append(
        "The model fit is strong, which means the selected variables explain the target reasonably well in this dataset."
    )
elif r2_score >= 0.5:
    insights.append(
        "The model fit is moderate, so the prediction is useful for scenario exploration but should not be treated as exact."
    )
else:
    insights.append(
        "The model fit is weak, so this prediction should be used only as an early directional estimate."
    )

for item in insights:
    st.markdown(f'<div class="info-card">{item}</div>', unsafe_allow_html=True)

# =========================
# FINAL TAKEAWAY
# =========================
st.markdown('<div class="section-title">Final Takeaway</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-box">
    <h4 style="margin-top:0;">Data Alchemists — SPICE Project</h4>
    <p style="margin-bottom:0;">
        This page moves the dashboard from descriptive analytics to predictive analytics. It helps users test system design choices
        and understand how those choices may affect future energy output, revenue, and environmental value.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="small-note">Developed by <b>Data Alchemists</b> for the SPICE Energy Conservation & Data Analytics Project.</p>',
    unsafe_allow_html=True
)
