import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Real Site Validation",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Page title
# -----------------------------
st.title("📊 Real Site Validation: Real vs Simulated Performance")
st.markdown(
    "This page compares actual site performance against simulated solar output to evaluate production trends, revenue potential, and validation gaps."
)

# -----------------------------
# Load datasets
# -----------------------------
@st.cache_data
def load_data():
    bissell = pd.read_csv("data/bissell_2025_with_missing_rows.csv")
    visser = pd.read_csv("data/visser_2025_with_missing_rows.csv")
    sim = pd.read_csv("data/St_Augustine_combined_simulated_monthly.csv")
    return bissell, visser, sim

bissell, visser, sim = load_data()

# -----------------------------
# Helpers
# -----------------------------
def clean_columns(df):
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    return df

def process_real(df, site_name):
    df = clean_columns(df.copy())

    if "date" not in df.columns:
        st.error(f"'date' column not found in {site_name}. Found columns: {list(df.columns)}")
        st.stop()

    possible_energy_cols = [
        "daily_kwh",
        "daily_kwh_",
        "daily_kwhs",
        "dailykwh",
        "total_system",
        "energy",
        "kwh"
    ]

    energy_col = None
    for col in possible_energy_cols:
        if col in df.columns:
            energy_col = col
            break

    if energy_col is None:
        st.error(f"Energy column not found in {site_name}. Found columns: {list(df.columns)}")
        st.stop()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df[energy_col] = pd.to_numeric(df[energy_col], errors="coerce").fillna(0)

    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")

    monthly = (
        df.groupby(["month", "month_name"], as_index=False)[energy_col]
        .sum()
        .rename(columns={energy_col: "energy_kwh"})
        .sort_values("month")
    )

    monthly["site"] = site_name
    return monthly

def process_simulated(df):
    df = clean_columns(df.copy())

    if "month" not in df.columns:
        st.error(f"'month' column not found in simulated dataset. Found columns: {list(df.columns)}")
        st.stop()

    possible_energy_cols = [
        "monthly_kwh",
        "month_mainstation",
        "total_system",
        "energy",
        "kwh"
    ]

    energy_col = None
    for col in possible_energy_cols:
        if col in df.columns:
            energy_col = col
            break

    if energy_col is None:
        st.error(f"Monthly energy column not found in simulated dataset. Found columns: {list(df.columns)}")
        st.stop()

    df["month"] = pd.to_numeric(df["month"], errors="coerce")
    df = df.dropna(subset=["month"])
    df["month"] = df["month"].astype(int)

    df[energy_col] = pd.to_numeric(df[energy_col], errors="coerce").fillna(0)

    monthly = (
        df.groupby("month", as_index=False)[energy_col]
        .mean()
        .rename(columns={energy_col: "energy_kwh"})
        .sort_values("month")
    )

    month_map = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    monthly["month_name"] = monthly["month"].map(month_map)
    monthly["site"] = "Simulated"
    return monthly

# -----------------------------
# Process datasets
# -----------------------------
bissell_monthly = process_real(bissell, "Bissell")
visser_monthly = process_real(visser, "Visser")
sim_monthly = process_simulated(sim)

df_all = pd.concat(
    [bissell_monthly, visser_monthly, sim_monthly],
    ignore_index=True
)

# -----------------------------
# Controls
# -----------------------------
st.sidebar.header("Validation Controls")

electricity_rate = st.sidebar.slider(
    "Electricity Rate (CAD/kWh)",
    min_value=0.05,
    max_value=0.30,
    value=0.12,
    step=0.01
)

selected_sites = st.sidebar.multiselect(
    "Select datasets to compare",
    options=df_all["site"].unique().tolist(),
    default=df_all["site"].unique().tolist()
)

show_data_preview = st.sidebar.checkbox("Show data preview", value=False)

df_filtered = df_all[df_all["site"].isin(selected_sites)].copy()

# -----------------------------
# Derived metrics
# -----------------------------
df_filtered["revenue_cad"] = df_filtered["energy_kwh"] * electricity_rate
df_filtered["electricity_saved_kwh"] = df_filtered["energy_kwh"]

summary = (
    df_filtered.groupby("site", as_index=False)
    .agg(
        total_energy_kwh=("energy_kwh", "sum"),
        total_revenue_cad=("revenue_cad", "sum"),
        electricity_saved_kwh=("electricity_saved_kwh", "sum"),
        avg_monthly_kwh=("energy_kwh", "mean")
    )
)

# -----------------------------
# KPI cards
# -----------------------------
st.subheader("Key Performance Summary")

kpi_cols = st.columns(len(summary)) if len(summary) > 0 else []

for i, row in summary.iterrows():
    with kpi_cols[i]:
        st.markdown(f"""
        <div style="
            background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
            padding: 18px;
            border-radius: 18px;
            box-shadow: 0 8px 18px rgba(0,0,0,0.12);
            border: 1px solid rgba(0,0,0,0.05);
            min-height: 170px;
        ">
            <div style="font-size: 0.9rem; color: #1E6F5C; font-weight: 800; text-transform: uppercase;">
                {row["site"]}
            </div>
            <div style="font-size: 1.6rem; color: #0B3C5D; font-weight: 900; margin-top: 8px;">
                {row["total_energy_kwh"]:,.0f} kWh
            </div>
            <div style="margin-top: 6px; color: #475569; font-size: 0.95rem;">
                Total Production
            </div>
            <div style="margin-top: 10px; color: #111827; font-size: 1.1rem; font-weight: 700;">
                ${row["total_revenue_cad"]:,.0f}
            </div>
            <div style="color: #64748B; font-size: 0.9rem;">
                Estimated Revenue
            </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Production trend
# -----------------------------
st.subheader("Monthly Production Comparison")

fig_prod = px.line(
    df_filtered.sort_values("month"),
    x="month_name",
    y="energy_kwh",
    color="site",
    markers=True,
    category_orders={"month_name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}
)
fig_prod.update_layout(
    xaxis_title="Month",
    yaxis_title="Energy Production (kWh)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white",
    font=dict(family="Segoe UI")
)
st.plotly_chart(fig_prod, use_container_width=True)

# -----------------------------
# Revenue comparison
# -----------------------------
st.subheader("Revenue Comparison")

fig_rev = px.bar(
    summary,
    x="site",
    y="total_revenue_cad",
    color="site",
    text="total_revenue_cad"
)
fig_rev.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)
fig_rev.update_layout(
    xaxis_title="Dataset",
    yaxis_title="Revenue (CAD)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white",
    showlegend=False,
    font=dict(family="Segoe UI")
)
st.plotly_chart(fig_rev, use_container_width=True)

# -----------------------------
# Electricity saved comparison
# -----------------------------
st.subheader("Electricity Saved Comparison")

fig_saved = px.bar(
    summary,
    x="site",
    y="electricity_saved_kwh",
    color="site",
    text="electricity_saved_kwh"
)
fig_saved.update_traces(
    texttemplate="%{text:,.0f} kWh",
    textposition="outside"
)
fig_saved.update_layout(
    xaxis_title="Dataset",
    yaxis_title="Electricity Saved (kWh)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white",
    showlegend=False,
    font=dict(family="Segoe UI")
)
st.plotly_chart(fig_saved, use_container_width=True)

# -----------------------------
# Monthly revenue trend
# -----------------------------
st.subheader("Monthly Revenue Trend")

fig_month_rev = px.line(
    df_filtered.sort_values("month"),
    x="month_name",
    y="revenue_cad",
    color="site",
    markers=True,
    category_orders={"month_name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}
)
fig_month_rev.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue (CAD)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white",
    font=dict(family="Segoe UI")
)
st.plotly_chart(fig_month_rev, use_container_width=True)

# -----------------------------
# Validation gap
# -----------------------------
st.subheader("Validation Gap")

sim_total = summary.loc[summary["site"] == "Simulated", "total_energy_kwh"]
real_sites = summary[summary["site"] != "Simulated"]["total_energy_kwh"]

if len(sim_total) > 0 and len(real_sites) > 0:
    sim_value = sim_total.iloc[0]
    real_avg = real_sites.mean()
    gap_kwh = sim_value - real_avg
    gap_pct = (gap_kwh / real_avg * 100) if real_avg != 0 else 0

    g1, g2, g3 = st.columns(3)

    with g1:
        st.metric("Simulated Total", f"{sim_value:,.0f} kWh")

    with g2:
        st.metric("Average Real Total", f"{real_avg:,.0f} kWh")

    with g3:
        st.metric("Validation Gap", f"{gap_kwh:,.0f} kWh", f"{gap_pct:.1f}%")

    if gap_pct > 0:
        insight_text = f"The simulated dataset is overestimating real-site production by approximately {abs(gap_pct):.1f}% compared with the average of the actual sites."
    elif gap_pct < 0:
        insight_text = f"The simulated dataset is underestimating real-site production by approximately {abs(gap_pct):.1f}% compared with the average of the actual sites."
    else:
        insight_text = "The simulated dataset is closely aligned with the average of the actual sites."

    st.info(
        f"{insight_text} This comparison helps evaluate how realistic the modeled solar performance is when compared with real operational data."
    )
else:
    st.warning("Select at least one real dataset and the simulated dataset to calculate validation gap.")

# -----------------------------
# Difference chart
# -----------------------------
st.subheader("Total Production Difference")

fig_diff = px.bar(
    summary,
    x="site",
    y="total_energy_kwh",
    color="site",
    text="total_energy_kwh"
)
fig_diff.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)
fig_diff.update_layout(
    xaxis_title="Dataset",
    yaxis_title="Total Production (kWh)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white",
    showlegend=False,
    font=dict(family="Segoe UI")
)
st.plotly_chart(fig_diff, use_container_width=True)

# -----------------------------
# Optional data preview
# -----------------------------
if show_data_preview:
    st.subheader("Processed Monthly Data Preview")
    st.dataframe(df_filtered.sort_values(["site", "month"]), use_container_width=True)
