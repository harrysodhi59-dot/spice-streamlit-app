from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# Paths
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGE_DIR = BASE_DIR / "images"
MODEL_DIR = BASE_DIR / "models"

# ---------------------------------------------------
# Styling - Dark Mode + Green/Yellow theme
# ---------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(30,111,92,0.18) 0%, transparent 30%),
        radial-gradient(circle at top right, rgba(253,184,19,0.08) 0%, transparent 20%),
        linear-gradient(180deg, #030817 0%, #07111d 45%, #081423 100%);
    color: #F8FAFC;
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 100%;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141B2D 0%, #182133 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

.hero-box {
    background: linear-gradient(135deg, rgba(30,111,92,0.95) 0%, rgba(11,60,93,0.95) 100%);
    padding: 2.5rem;
    border-radius: 26px;
    color: white;
    box-shadow: 0 18px 40px rgba(0,0,0,0.32);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.2rem;
}

.hero-label {
    color: #D6EFE6 !important;
    font-size: 0.9rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 0.8rem;
}

.hero-title {
    font-size: 2.7rem;
    font-weight: 900;
    line-height: 1.08;
    margin-bottom: 0.8rem;
    color: #FFFFFF !important;
}

.hero-highlight {
    color: #FDB813 !important;
}

.hero-text {
    font-size: 1.02rem;
    line-height: 1.8;
    color: #F3F7F6 !important;
}

.section-heading {
    font-size: 1.95rem;
    font-weight: 850;
    color: #F8FAFC !important;
    margin-top: 0.4rem;
    margin-bottom: 0.5rem;
}

.section-subtext {
    color: #B6C0CE !important;
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 1.2rem;
}

.kpi-card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 22px;
    padding: 1.2rem;
    box-shadow: 0 12px 24px rgba(0,0,0,0.18);
    border: 1px solid rgba(0,0,0,0.05);
    min-height: 150px;
}

.kpi-title {
    color: #1E6F5C;
    font-size: 0.88rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
}

.kpi-value {
    color: #0B3C5D;
    font-size: 1.72rem;
    font-weight: 900;
    line-height: 1.2;
}

.kpi-note {
    color: #64748B;
    font-size: 0.88rem;
    margin-top: 0.3rem;
}

.card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 22px;
    padding: 1.35rem;
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    margin-bottom: 1rem;
    border: 1px solid rgba(0,0,0,0.05);
}

.card,
.card p,
.card span,
.card div,
.card strong,
.card li,
.card h3,
.card h4 {
    color: #1F2937 !important;
}

.card-label {
    color: #1E6F5C !important;
    font-size: 0.85rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.35rem;
}

.card-title {
    color: #0B3C5D !important;
    font-size: 1.28rem;
    font-weight: 850;
    margin-bottom: 0.45rem;
}

.small-note {
    color: #334155 !important;
    font-size: 0.95rem;
    line-height: 1.7;
}

.insight-box {
    background: linear-gradient(90deg, rgba(30,111,92,0.20), rgba(11,60,93,0.18));
    border-left: 6px solid #FDB813;
    border-radius: 18px;
    padding: 1.1rem 1.25rem;
    margin-top: 0.8rem;
    margin-bottom: 1.3rem;
    color: #E5F3EE !important;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    font-size: 0.98rem;
    line-height: 1.75;
}

.metric-strip {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1.1rem 1.15rem;
    margin-bottom: 1rem;
}

.metric-label-dark {
    color: #CBD5E1 !important;
    font-size: 0.88rem;
    margin-bottom: 0.35rem;
}

.metric-value-dark {
    color: #F8FAFC !important;
    font-size: 1.75rem;
    font-weight: 850;
}

.footer-note {
    background: linear-gradient(90deg, rgba(30,111,92,0.18), rgba(11,60,93,0.22));
    border-radius: 18px;
    padding: 1rem 1.2rem;
    color: #E5E7EB !important;
    margin-top: 1rem;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Load datasets
# ---------------------------------------------------
@st.cache_data
def load_data():
    bissell = pd.read_csv(DATA_DIR / "bissell_complete_dataset_clean.csv")
    visser = pd.read_csv(DATA_DIR / "visser_complete_dataset_clean.csv")
    return bissell, visser

# ---------------------------------------------------
# Helpers
# ---------------------------------------------------
def clean_columns(df):
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    return df

def process_site(df, site_name, energy_col_name):
    df = clean_columns(df.copy())

    if "date" not in df.columns:
        st.error(f"'date' column not found in {site_name}. Found columns: {list(df.columns)}")
        st.stop()

    if energy_col_name not in df.columns:
        st.error(f"'{energy_col_name}' column not found in {site_name}. Found columns: {list(df.columns)}")
        st.stop()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df[energy_col_name] = pd.to_numeric(df[energy_col_name], errors="coerce").fillna(0)

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")

    monthly = (
        df.groupby(["year", "month", "month_name"], as_index=False)[energy_col_name]
        .sum()
        .rename(columns={energy_col_name: "energy_kwh"})
        .sort_values(["year", "month"])
    )

    monthly["site"] = site_name
    return monthly

# ---------------------------------------------------
# Read data
# ---------------------------------------------------
try:
    bissell_raw, visser_raw = load_data()
except Exception as e:
    st.error(f"Could not load validation datasets: {e}")
    st.stop()

bissell = process_site(bissell_raw, "Bissell", "bissell_adjusted_kwh")
visser = process_site(visser_raw, "Visser", "visser_adjusted_kwh")

df_all = pd.concat([bissell, visser], ignore_index=True)

# ---------------------------------------------------
# Sidebar controls
# ---------------------------------------------------
st.sidebar.header("Validation Controls")

available_years = sorted(df_all["year"].dropna().unique().tolist())

selected_years = st.sidebar.multiselect(
    "Select Year(s)",
    options=available_years,
    default=available_years[-3:] if len(available_years) >= 3 else available_years
)

electricity_rate = st.sidebar.slider(
    "Electricity Rate (CAD/kWh)",
    min_value=0.05,
    max_value=0.30,
    value=0.12,
    step=0.01
)

selected_sites = st.sidebar.multiselect(
    "Select Site(s)",
    options=["Bissell", "Visser"],
    default=["Bissell", "Visser"]
)

show_preview = st.sidebar.checkbox("Show processed data preview", value=False)

df_filtered = df_all[
    (df_all["year"].isin(selected_years)) &
    (df_all["site"].isin(selected_sites))
].copy()

if df_filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

df_filtered["revenue_cad"] = df_filtered["energy_kwh"] * electricity_rate
df_filtered["electricity_saved_kwh"] = df_filtered["energy_kwh"]

# ---------------------------------------------------
# Hero
# ---------------------------------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-label">Operational Data • Site Benchmarking • Business Validation</div>
    <div class="hero-title">
        Real Site <span class="hero-highlight">Validation</span>
    </div>
    <div class="hero-text">
        This page compares adjusted solar production across the Bissell and Visser sites
        using multi-year operational data. The goal is to validate performance patterns,
        compare generation strength, and translate production into business-facing value.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Summary data
# ---------------------------------------------------
summary = (
    df_filtered.groupby("site", as_index=False)
    .agg(
        total_energy_kwh=("energy_kwh", "sum"),
        total_revenue_cad=("revenue_cad", "sum"),
        electricity_saved_kwh=("electricity_saved_kwh", "sum"),
        avg_monthly_kwh=("energy_kwh", "mean"),
        best_month_kwh=("energy_kwh", "max")
    )
)

monthly_comparison = (
    df_filtered.groupby(["month", "month_name", "site"], as_index=False)
    .agg(
        energy_kwh=("energy_kwh", "mean"),
        revenue_cad=("revenue_cad", "mean")
    )
)

month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ---------------------------------------------------
# KPI cards
# ---------------------------------------------------
st.markdown('<div class="section-heading">Validation Summary</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">A clean comparison of energy, revenue, and electricity offset across the selected real site datasets.</div>',
    unsafe_allow_html=True
)

kpi_cols = st.columns(len(summary), gap="large")

for i, row in summary.iterrows():
    with kpi_cols[i]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{row["site"]}</div>
            <div class="kpi-value">{row["total_energy_kwh"]:,.0f} kWh</div>
            <div class="kpi-note">Total production</div>
            <div style="margin-top: 10px; color: #1E6F5C; font-weight: 800; font-size: 1.05rem;">
                ${row["total_revenue_cad"]:,.0f}
            </div>
            <div class="kpi-note">Estimated revenue</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# Insight
# ---------------------------------------------------
if len(summary) == 2:
    b_val = summary.loc[summary["site"] == "Bissell", "total_energy_kwh"].iloc[0]
    v_val = summary.loc[summary["site"] == "Visser", "total_energy_kwh"].iloc[0]
    leader = "Bissell" if b_val > v_val else "Visser"
    avg_base = (b_val + v_val) / 2
    gap_pct = abs((b_val - v_val) / avg_base * 100) if avg_base > 0 else 0

    insight_html = f"""
    <div class="insight-box">
        <strong>Validation Insight:</strong> Across the selected years, <strong>{leader}</strong>
        delivers the stronger overall production profile. The difference between the two sites is
        approximately <strong>{gap_pct:.1f}%</strong>, which helps show how site conditions and
        operational variability can influence long-term solar output. Revenue has been retained in the
        summary cards so the comparison still connects clearly to business value.
    </div>
    """
else:
    insight_html = """
    <div class="insight-box">
        <strong>Validation Insight:</strong> This view helps compare selected real-world sites on
        production, electricity offset, and estimated revenue across the chosen time window.
    </div>
    """

st.markdown(insight_html, unsafe_allow_html=True)

# ---------------------------------------------------
# KPI strips
# ---------------------------------------------------
st.markdown('<div class="section-heading">Operational Comparison Metrics</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3, gap="large")

with m1:
    total_energy_all = df_filtered["energy_kwh"].sum()
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">⚡ Total Energy Across Selected Sites</div>
        <div class="metric-value-dark">{total_energy_all:,.0f} kWh</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    total_revenue_all = df_filtered["revenue_cad"].sum()
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">💰 Total Revenue Equivalent</div>
        <div class="metric-value-dark">${total_revenue_all:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    avg_monthly_all = df_filtered["energy_kwh"].mean()
    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-label-dark">📈 Average Monthly Production</div>
        <div class="metric-value-dark">{avg_monthly_all:,.1f} kWh</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# Production trend only
# ---------------------------------------------------
st.markdown("""
<div class="card">
    <div class="card-label">Production Trend</div>
    <div class="card-title">⚡ Average Monthly Production by Site</div>
""", unsafe_allow_html=True)

fig_prod = px.line(
    monthly_comparison.sort_values("month"),
    x="month_name",
    y="energy_kwh",
    color="site",
    markers=True,
    category_orders={"month_name": month_order},
    color_discrete_map={
        "Bissell": "#8ED1FC",
        "Visser": "#156CC4"
    }
)
fig_prod.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Monthly Production (kWh)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white",
    font=dict(family="Segoe UI"),
    legend_title_text=""
)
st.plotly_chart(fig_prod, use_container_width=True)

st.markdown("""
    <p class="small-note">
        This chart compares the average monthly production pattern for each real site over the selected years.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Total production only
# ---------------------------------------------------
st.markdown("""
<div class="card">
    <div class="card-label">Site Comparison</div>
    <div class="card-title">📊 Total Production by Site</div>
""", unsafe_allow_html=True)

fig_total_prod = px.bar(
    summary,
    x="site",
    y="total_energy_kwh",
    color="site",
    text="total_energy_kwh",
    color_discrete_map={
        "Bissell": "#1E6F5C",
        "Visser": "#FDB813"
    }
)
fig_total_prod.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)
fig_total_prod.update_layout(
    xaxis_title="Site",
    yaxis_title="Total Production (kWh)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white",
    showlegend=False,
    font=dict(family="Segoe UI")
)
st.plotly_chart(fig_total_prod, use_container_width=True)

st.markdown("""
    <p class="small-note">
        This view compares total solar generation across the selected sites and years.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Electricity saved + best month
# ---------------------------------------------------
bottom_left, bottom_right = st.columns(2, gap="large")

with bottom_left:
    st.markdown("""
    <div class="card">
        <div class="card-label">Electricity Offset</div>
        <div class="card-title">🔋 Electricity Saved by Site</div>
    """, unsafe_allow_html=True)

    fig_saved = px.bar(
        summary,
        x="site",
        y="electricity_saved_kwh",
        color="site",
        text="electricity_saved_kwh",
        color_discrete_map={
            "Bissell": "#8ED1FC",
            "Visser": "#FDB813"
        }
    )
    fig_saved.update_traces(
        texttemplate="%{text:,.0f} kWh",
        textposition="outside"
    )
    fig_saved.update_layout(
        xaxis_title="Site",
        yaxis_title="Electricity Saved (kWh)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        showlegend=False,
        font=dict(family="Segoe UI")
    )
    st.plotly_chart(fig_saved, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            In this page, electricity saved is represented by the clean electricity generated by each site.
        </p>
    </div>
    """, unsafe_allow_html=True)

with bottom_right:
    st.markdown("""
    <div class="card">
        <div class="card-label">Peak Output</div>
        <div class="card-title">🌤️ Best Monthly Output by Site</div>
    """, unsafe_allow_html=True)

    fig_best = px.bar(
        summary,
        x="site",
        y="best_month_kwh",
        color="site",
        text="best_month_kwh",
        color_discrete_map={
            "Bissell": "#1E6F5C",
            "Visser": "#FDB813"
        }
    )
    fig_best.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )
    fig_best.update_layout(
        xaxis_title="Site",
        yaxis_title="Best Monthly Output (kWh)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        showlegend=False,
        font=dict(family="Segoe UI")
    )
    st.plotly_chart(fig_best, use_container_width=True)

    st.markdown("""
        <p class="small-note">
            This highlights the strongest monthly production value achieved by each site in the selected period.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# Optional preview
# ---------------------------------------------------
if show_preview:
    st.markdown('<div class="section-heading">Processed Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(
        df_filtered.sort_values(["site", "year", "month"]),
        use_container_width=True
    )

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("""
<div class="footer-note">
    <strong>Next step:</strong> Continue to the Predictive Modeling page to connect real site patterns with forecasting and decision support.
</div>
""", unsafe_allow_html=True)