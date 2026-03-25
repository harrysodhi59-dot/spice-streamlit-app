import streamlit as st
import pandas as pd
import numpy as np
import io

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
    '<div class="sub-text">This page estimates solar energy output, revenue, and CO₂ reduction based on system design inputs using a lightweight predictive approach.</div>',
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
    missing_requirements.append("energy output / generation")

if missing_requirements:
    st.error("This dataset is missing some columns needed for predictive modeling.")
    st.write("Missing:", ", ".join(missing_requirements))
    st.info("Use a dataset that includes system size, tilt, azimuth, loss, and energy output.")
    st.stop()

model_df = df[[size_col, tilt_col, azimuth_col, loss_col, generation_col]].dropna()

if len(model_df) < 5:
    st.warning("There are not enough clean rows to generate predictions. Try a larger dataset.")
    st.stop()

st.success("The dataset has the required columns for lightweight predictive analysis.")

# =========================
# SIMPLE COEFFICIENT ESTIMATION
# =========================
# This is a lightweight approximation approach without sklearn.
size_mean = model_df[size_col].mean()
tilt_mean = model_df[tilt_col].mean()
azimuth_mean = model_df[azimuth_col].mean()
loss_mean = model_df[loss_col].mean()
generation_mean = model_df[generation_col].mean()

def safe_ratio_impact(feature_col, target_col):
    feature_std = feature_col.std()
    target_std = target_col.std()

    if pd.isna(feature_std) or pd.isna(target_std) or feature_std == 0:
        return 0.0

    corr = feature_col.corr(target_col)
    if pd.isna(corr):
        return 0.0

    return corr * (target_std / feature_std)

coef_size = safe_ratio_impact(model_df[size_col], model_df[generation_col])
coef_tilt = safe_ratio_impact(model_df[tilt_col], model_df[generation_col])
coef_azimuth = safe_ratio_impact(model_df[azimuth_col], model_df[generation_col])
coef_loss = safe_ratio_impact(model_df[loss_col], model_df[generation_col])

# Basic pseudo-R2 using average absolute correlation
corrs = []
for c in [size_col, tilt_col, azimuth_col, loss_col]:
    corr_val = model_df[c].corr(model_df[generation_col])
    if not pd.isna(corr_val):
        corrs.append(abs(corr_val))

model_strength = np.mean(corrs) if len(corrs) > 0 else 0.0

# Revenue and CO2 rates
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
        <div class="metric-label">Usable Rows</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{model_strength:.2f}</div>
        <div class="metric-label">Model Strength</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{generation_col}</div>
        <div class="metric-label">Prediction Target</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# SCENARIO INPUT
# =========================
st.markdown('<div class="section-title">Scenario Input</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    user_size = st.number_input(
        "System Size",
        value=float(size_mean)
    )
    user_tilt = st.number_input(
        "Tilt",
        value=float(tilt_mean)
    )

with c2:
    user_azimuth = st.number_input(
        "Azimuth / Orientation",
        value=float(azimuth_mean)
    )
    user_loss = st.number_input(
        "System Loss",
        value=float(loss_mean)
    )

# =========================
# PREDICTION
# =========================
st.markdown('<div class="section-title">Prediction Results</div>', unsafe_allow_html=True)

predicted_generation = (
    generation_mean
    + coef_size * (user_size - size_mean)
    + coef_tilt * (user_tilt - tilt_mean)
    + coef_azimuth * (user_azimuth - azimuth_mean)
    + coef_loss * (user_loss - loss_mean)
)

predicted_generation = max(predicted_generation, 0)

predicted_revenue = predicted_generation * revenue_rate if revenue_rate is not None else None
predicted_co2 = predicted_generation * co2_rate if co2_rate is not None else None

gen_text = f"{predicted_generation:,.2f}"
rev_text = f"${predicted_revenue:,.2f}" if predicted_revenue is not None else "N/A"
co2_text = f"{predicted_co2:,.2f}" if predicted_co2 is not None else "N/A"

p1, p2, p3 = st.columns(3)

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

interpretation = []

interpretation.append(
    f"For the selected configuration, the estimated energy output is <b>{predicted_generation:,.2f}</b>."
)

if predicted_revenue is not None:
    interpretation.append(
        f"Based on the uploaded dataset pattern, this scenario may produce an estimated revenue of <b>${predicted_revenue:,.2f}</b>."
    )

if predicted_co2 is not None:
    interpretation.append(
        f"This same setup may also contribute an estimated <b>{predicted_co2:,.2f}</b> in CO₂ reduction."
    )

if model_strength >= 0.7:
    interpretation.append(
        "The variable relationships in this dataset look relatively strong, so this estimate can support early planning discussions."
    )
elif model_strength >= 0.4:
    interpretation.append(
        "The variable relationships are moderate, so this result is useful for scenario exploration but not as an exact forecast."
    )
else:
    interpretation.append(
        "The variable relationships are weak, so the result should be treated as a rough directional estimate only."
    )

for item in interpretation:
    st.markdown(f'<div class="info-card">{item}</div>', unsafe_allow_html=True)

# =========================
# FEATURE INFLUENCE
# =========================
st.markdown('<div class="section-title">Estimated Feature Influence</div>', unsafe_allow_html=True)

influence_df = pd.DataFrame({
    "Feature": [size_col, tilt_col, azimuth_col, loss_col],
    "Estimated Influence": [coef_size, coef_tilt, coef_azimuth, coef_loss]
})

st.dataframe(influence_df, use_container_width=True, hide_index=True)

# =========================
# FINAL TAKEAWAY
# =========================
st.markdown('<div class="section-title">Final Takeaway</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-box">
    <h4 style="margin-top:0;">Data Alchemists — SPICE Project</h4>
    <p style="margin-bottom:0;">
        This page moves the dashboard from descriptive analytics toward predictive analytics. It gives users a practical way
        to test solar design scenarios and understand how those inputs may influence energy output, revenue, and environmental value.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="small-note">Developed by <b>Data Alchemists</b> for the SPICE Energy Conservation & Data Analytics Project.</p>',
    unsafe_allow_html=True
)
